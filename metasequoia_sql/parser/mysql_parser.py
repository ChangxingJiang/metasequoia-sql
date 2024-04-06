"""
MySQL 解析器

Hive 保留字：https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL
"""

import enum
from typing import List

from metasequoia_sql import ast
from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.objects.data_source import DataSource
from metasequoia_sql.objects.mysql import *
from metasequoia_sql.parser.sentence_parser import parse_sentence, parse_sql_column_type


class MySQLCreateTableParser:
    """
    当前已知不支持的场景：虚拟列 GENERATED ALWAYS AS（RDS427.prism1.oned_topic_kafka）
    """

    def __init__(self, root: ast.AST):
        # 过滤 statement 中的空白字符
        self.tokens: List[ast.AST] = [token for token in root.children if token.is_space is False]
        self.n_token = len(self.tokens)

        # 初始化自动机状态类
        self.idx = 0  # 当前自动机位置下标
        self.stage = MySQLCreateTableParser.ParseStage.START  # 当前自动机状态

        # 初始化匹配结果
        self.builder = DDLCreateTableStatementMySQL()

        # 执行解析逻辑
        self._parse()

    def _parse(self) -> None:
        """使用自动机解析 CREATE TABLE 建表语句（如果 SQL 表达式无法解析则返回 False）"""
        while self.idx < self.n_token:
            if self.stage == MySQLCreateTableParser.ParseStage.START:  # 刚开始匹配（未匹配任何部分）
                self._parse_create_table()  # 解析 CREATE TABLE 关键字
            elif self.stage == MySQLCreateTableParser.ParseStage.AFTER_CREATE_TABLE:  # 已匹配 CREATE TABLE
                if self._parse_if_not_exists():
                    continue
                else:  # 匹配表名
                    self._parse_table_name()
            elif self.stage == MySQLCreateTableParser.ParseStage.AFTER_IF_NOT_EXISTS:  # 已匹配 IF NOT EXISTS
                self._parse_table_name()
            elif self.stage == MySQLCreateTableParser.ParseStage.AFTER_TABLE_NAME:  # 已匹配表名
                self._parse_columns_and_key()
            elif self.stage == MySQLCreateTableParser.ParseStage.AFTER_COLUMNS_AND_KEY_LIST:  # 已匹配字段和索引
                self._parse_table_config()
            else:  # CreateTableParser.ParseStage.FINISH
                break

    def _parse_create_table(self) -> bool:
        """解析 CREATE TABLE 关键字（如果匹配成功返回 True，否则返回 False）"""
        if not (self.tokens[self.idx].source == "CREATE" and
                self.idx + 1 < self.n_token and self.tokens[self.idx + 1].source == "TABLE"):
            raise SqlParseError("cannot find 'CREATE TABLE' at the first of statement")
        self.idx += 2
        self.stage = MySQLCreateTableParser.ParseStage.AFTER_CREATE_TABLE
        return True

    def _parse_if_not_exists(self) -> bool:
        """解析 IF NOT EXISTS 字句（如果匹配成功返回 True，否则返回 False）"""
        if not (self.tokens[self.idx].source == "IF" and
                self.idx + 1 < self.n_token and self.tokens[self.idx + 1].source == "NOT" and
                self.idx + 2 < self.n_token and self.tokens[self.idx + 2].source == "EXISTS"):
            return False
        self.builder.set_if_not_exists(True)
        self.idx += 3
        self.stage = MySQLCreateTableParser.ParseStage.AFTER_IF_NOT_EXISTS
        return True

    def _parse_table_name(self) -> bool:
        """解析表名（如果匹配成功返回 True，否则返回 False）"""
        table_name = self.tokens[self.idx].source
        table_name = table_name.strip("`")
        self.builder.set_table_name(table_name)
        self.idx += 1
        self.stage = MySQLCreateTableParser.ParseStage.AFTER_TABLE_NAME
        return True

    def _parse_columns_and_key(self) -> bool:
        """解析字段和索引（如果匹配成功返回 True，否则返回 False）"""
        outer_token = self.tokens[self.idx]
        if not isinstance(outer_token, ast.ASTParenthesis):
            raise SqlParseError("cannot find parenthesis after table name")

        # 过滤插入语中的空白字符
        inner_tokens: List[ast.AST] = [token for token in outer_token.children if
                                       token.is_space is False and token.is_multiline_comment is False]

        # 根据逗号拆分插入语中的内容
        column_group_tokens: List[List[ast.AST]] = [[]]
        for token in inner_tokens:
            if token.is_comma:
                column_group_tokens.append([])
            else:
                column_group_tokens[-1].append(token)

        for column_group in column_group_tokens:
            if column_group[0].equals("PRIMARY"):
                if self.builder.primary_key is not None:
                    raise SqlParseError("duplicate primary key")
                if (len(column_group) >= 2 and column_group[1].equals("KEY")
                        and isinstance(column_group[2], ast.ASTParenthesis)):
                    self.builder.set_primary_key(DDLPrimaryKeyMySQL(column_group[2].children[0].source))
                else:
                    raise SqlParseError("unknown primary key format")
            elif column_group[0].equals("UNIQUE"):
                if (len(column_group) >= 3 and column_group[1].equals("KEY")
                        and isinstance(column_group[3], ast.ASTParenthesis)):
                    self.builder.add_unique_key(DDLUniqueKeyMySQL(
                        column_group[2].source,
                        [node.source for node in column_group[3].children if not node.is_comma]))
                else:
                    raise SqlParseError("unknown uniquekey format")
            elif column_group[0].equals("KEY"):
                if len(column_group) >= 2 and isinstance(column_group[2], ast.ASTParenthesis):
                    self.builder.add_key(DDLKeyMySQL(
                        column_group[1].source,
                        [node.source for node in column_group[2].children if not node.is_comma]))
                else:
                    raise SqlParseError("unknown key format")
            elif column_group[0].equals("FULLTEXT"):
                if (len(column_group) >= 3 and column_group[1].equals("KEY")
                        and isinstance(column_group[3], ast.ASTParenthesis)):
                    self.builder.add_fulltext_key(DDLFulltextKeyMysql(
                        column_group[2].source,
                        [node.source for node in column_group[3].children if not node.is_comma]))
                else:
                    raise SqlParseError("unknown uniquekey format")
            elif column_group[0].equals("CONSTRAINT"):
                if (len(column_group) >= 8 and
                        isinstance(column_group[4], ast.ASTParenthesis) and
                        isinstance(column_group[7], ast.ASTParenthesis)):
                    self.builder.add_foreign_key(DDLForeignKeyMySQL(
                        column_group[1].source,
                        [node.source for node in column_group[4].children if not node.is_comma],
                        column_group[6].source,
                        [node.source for node in column_group[7].children if not node.is_comma]
                    ))
            else:
                scanner = TokenScanner(column_group)
                column_name = scanner.pop_as_source()
                column_type = parse_sql_column_type(scanner, DataSource.MYSQL)
                column = DDLColumnMySQL(column_name, column_type)
                while not scanner.is_finish:
                    if scanner.get().equals("NOT"):
                        scanner.match("NOT", "NULL")
                        column.is_not_null = True
                    elif scanner.get().equals("NULL"):
                        scanner.match("NULL")
                        column.set_is_allow_null(True)
                    elif scanner.get().equals("CHARACTER"):
                        scanner.match("CHARACTER", "SET")
                        column.set_character_set(scanner.pop_as_source())
                    elif scanner.get().equals("COLLATE"):
                        scanner.match("COLLATE")
                        column.set_collate(scanner.pop_as_source())
                    elif scanner.get().equals("DEFAULT"):
                        scanner.match("DEFAULT")
                        column.default = parse_sentence(scanner, DataSource.MYSQL)
                    elif scanner.get().equals("COMMENT"):
                        scanner.match("COMMENT")
                        column.set_comment(scanner.pop_as_source())
                    elif scanner.get().equals("ON"):  # ON UPDATE
                        scanner.match("ON", "UPDATE")
                        column.on_update = parse_sentence(scanner, DataSource.MYSQL)
                    elif scanner.get().equals("AUTO_INCREMENT"):
                        scanner.match("AUTO_INCREMENT")
                        column.is_auto_increment = True
                    elif scanner.get().equals("UNSIGNED"):
                        scanner.match("UNSIGNED")
                        column.is_unsigned = True
                    elif scanner.get().equals("ZEROFILL"):
                        scanner.match("ZEROFILL")
                        column.is_zerofill = True
                    else:
                        raise SqlParseError(f"Cannot parse ddl column: {column_group}")
                self.builder.append_column(column)

        self.idx += 1
        self.stage = MySQLCreateTableParser.ParseStage.AFTER_COLUMNS_AND_KEY_LIST
        return True

    def _parse_table_config(self):
        tokens = self.tokens[self.idx:]
        if len(tokens) >= 1 and isinstance(tokens[-1], ast.ASTSemicolon):
            tokens.pop()
        i = 0
        while i < len(tokens):
            if tokens[i].is_multiline_comment:
                i += 1
            elif tokens[i].equals("ENGINE"):
                if i + 2 < len(tokens) and tokens[i + 1].equals("="):
                    self.builder.set_engine(tokens[i + 2].source)
                else:
                    raise SqlParseError(f"unknown engine: {tokens}")
                i += 3
            elif tokens[i].equals("AUTO_INCREMENT"):
                if i + 2 < len(tokens) and tokens[i + 1].equals("="):
                    self.builder.set_table_auto_increment(int(tokens[i + 2].source))
                else:
                    raise SqlParseError("unknown AUTO_INCREMENT")
                i += 3
            elif tokens[i].equals("DEFAULT"):
                if i + 3 < len(tokens) and tokens[i + 1].equals("CHARSET") and tokens[i + 2].equals("="):
                    self.builder.set_default_charset(tokens[i + 3].source)
                else:
                    raise SqlParseError("unknown DEFAULT")
                i += 4
            elif tokens[i].equals("ROW_FORMAT"):
                if i + 2 < len(tokens) and tokens[i + 1].equals("="):
                    self.builder.set_row_format(tokens[i + 2].source)
                else:
                    raise SqlParseError("unknown ROW_FORMAT")
                i += 3
            elif tokens[i].equals("COLLATE"):
                if i + 2 < len(tokens) and tokens[i + 1].equals("="):
                    self.builder.set_row_format(tokens[i + 2].source)
                else:
                    raise SqlParseError("unknown COLLATE")
                i += 3
            elif tokens[i].equals("COMMENT"):
                if i + 2 < len(tokens) and tokens[i + 1].equals("="):
                    self.builder.set_comment(tokens[i + 2].source)
                else:
                    raise SqlParseError("unknown COMMENT")
                i += 3
            elif tokens[i].equals("STATS_PERSISTENT"):
                if i + 2 < len(tokens) and tokens[i + 1].equals("="):
                    self.builder.states_persistent = tokens[i + 2].source
                else:
                    raise SqlParseError("unknown STATS_PERSISTENT")
                i += 3
            else:
                raise SqlParseError(f"unknown table config: {tokens[i:]}")
        self.idx = len(self.tokens)
        self.stage = MySQLCreateTableParser.ParseStage.FINISH
        return True

    class ParseStage(enum.Enum):
        START = 0  # 刚开始匹配（未匹配任何部分）
        AFTER_CREATE_TABLE = 100  # 已匹配 CREATE TABLE
        AFTER_IF_NOT_EXISTS = 200  # 已匹配 IF NOT EXISTS
        AFTER_TABLE_NAME = 300  # 已匹配表名
        AFTER_COLUMNS_AND_KEY_LIST = 400  # 已匹配字段和索引信息
        FINISH = 1000  # 已匹配完成


def parse_mysql_create_table_statement(sql: str) -> DDLCreateTableStatementMySQL:
    # 将 sql 解析为多个表达式，并检查是否有且只有 1 个表达式
    root: ast.AST = ast.parse_as_statements(sql)[0]
    return MySQLCreateTableParser(root).builder
