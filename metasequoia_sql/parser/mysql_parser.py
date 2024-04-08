"""
MySQL 解析器

Hive 保留字：https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL
"""

import enum

from metasequoia_sql.common.token_scanner import build_token_scanner, TokenScanner
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.objects.mysql import *
from metasequoia_sql.parser.common import parse_general_expression, parse_sql_column_type


class MySQLCreateTableParser:
    """
    当前已知不支持的场景：虚拟列 GENERATED ALWAYS AS（RDS427.prism1.oned_topic_kafka）
    """

    def __init__(self, scanner: TokenScanner):
        # 过滤 statement 中的空白字符
        self.scanner = scanner

        # 初始化自动机状态类
        self.stage = MySQLCreateTableParser.ParseStage.START  # 当前自动机状态

        # 初始化匹配结果
        self.builder = DDLCreateTableStatementMySQL()

        # 执行解析逻辑
        self._parse()

    def _parse(self) -> None:
        """使用自动机解析 CREATE TABLE 建表语句（如果 SQL 表达式无法解析则返回 False）"""
        while not self.scanner.is_finish:
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
        self.scanner.match("CREATE", "TABLE")
        self.stage = MySQLCreateTableParser.ParseStage.AFTER_CREATE_TABLE
        return True

    def _parse_if_not_exists(self) -> bool:
        """解析 IF NOT EXISTS 字句（如果匹配成功返回 True，否则返回 False）"""
        if not self.scanner.search_and_move("IF", "NOT", "EXISTS"):
            return False
        self.builder.set_if_not_exists(True)
        self.stage = MySQLCreateTableParser.ParseStage.AFTER_IF_NOT_EXISTS
        return True

    def _parse_table_name(self) -> bool:
        """解析表名（如果匹配成功返回 True，否则返回 False）"""
        table_name = self.scanner.pop_as_source()
        table_name = table_name.strip("`")
        self.builder.set_table_name(table_name)
        self.stage = MySQLCreateTableParser.ParseStage.AFTER_TABLE_NAME
        return True

    def _parse_columns_and_key(self) -> bool:
        """解析字段和索引（如果匹配成功返回 True，否则返回 False）"""
        if not self.scanner.now.is_parenthesis:
            raise SqlParseError("cannot find parenthesis after table name")

        group_scanner_list = self.scanner.pop_as_children_scanner_list_split_by(",")

        for group_scanner in group_scanner_list:
            if group_scanner.search_and_move("PRIMARY"):
                if self.builder.primary_key is not None:
                    raise SqlParseError("duplicate primary key")
                if group_scanner.search_and_move("KEY") and group_scanner.now.is_parenthesis:
                    self.builder.set_primary_key(
                        DDLPrimaryKeyMySQL(group_scanner.pop_as_children_scanner().pop_as_source()))
                else:
                    raise SqlParseError("unknown primary key format")
            elif group_scanner.search_and_move("UNIQUE"):
                if group_scanner.search_and_move("KEY") and group_scanner.next1.is_parenthesis:
                    name = group_scanner.pop_as_source()
                    columns = [column_scanner.pop_as_source()
                               for column_scanner in group_scanner.pop_as_children_scanner_list_split_by(",")]
                    self.builder.add_unique_key(DDLUniqueKeyMySQL(name=name, columns=columns))
                else:
                    raise SqlParseError("unknown uniquekey format")
            elif group_scanner.search_and_move("KEY"):
                if group_scanner.next1.is_parenthesis:
                    name = group_scanner.pop_as_source()
                    columns = [column_scanner.pop_as_source()
                               for column_scanner in group_scanner.pop_as_children_scanner_list_split_by(",")]
                    self.builder.add_key(DDLKeyMySQL(name=name, columns=columns))
                else:
                    raise SqlParseError("unknown key format")
            elif group_scanner.search_and_move("FULLTEXT"):
                group_scanner.match("KEY")
                if group_scanner.next1.is_parenthesis:
                    name = group_scanner.pop_as_source()
                    columns = [column_scanner.pop_as_source()
                               for column_scanner in group_scanner.pop_as_children_scanner_list_split_by(",")]
                    self.builder.add_fulltext_key(DDLFulltextKeyMysql(name=name, columns=columns))
                else:
                    raise SqlParseError("unknown uniquekey format")
            elif group_scanner.search_and_move("CONSTRAINT"):
                constraint_name = group_scanner.pop_as_source()
                group_scanner.pop()
                group_scanner.pop()
                slave_columns = [column_scanner.pop_as_source()
                                 for column_scanner in group_scanner.pop_as_children_scanner_list_split_by(",")]
                group_scanner.pop()
                master_table_name = group_scanner.pop_as_source()
                master_columns = [column_scanner.pop_as_source()
                                  for column_scanner in group_scanner.pop_as_children_scanner_list_split_by(",")]
                self.builder.add_foreign_key(DDLForeignKeyMySQL(
                    constraint_name=constraint_name,
                    slave_columns=slave_columns,
                    master_table_name=master_table_name,
                    master_columns=master_columns
                ))
            else:
                column_name = group_scanner.pop_as_source()
                column_type = parse_sql_column_type(group_scanner)
                column = DDLColumnMySQL(column_name, column_type)
                while not group_scanner.is_finish:
                    if group_scanner.search_and_move("NOT", "NULL"):
                        column.is_not_null = True
                    elif group_scanner.search_and_move("NULL"):
                        column.set_is_allow_null(True)
                    elif group_scanner.search_and_move("CHARACTER", "SET"):
                        column.set_character_set(group_scanner.pop_as_source())
                    elif group_scanner.search_and_move("COLLATE"):
                        column.set_collate(group_scanner.pop_as_source())
                    elif group_scanner.search_and_move("DEFAULT"):
                        column.default = parse_general_expression(group_scanner)
                    elif group_scanner.search_and_move("COMMENT"):
                        column.set_comment(group_scanner.pop_as_source())
                    elif group_scanner.search_and_move("ON", "UPDATE"):  # ON UPDATE
                        column.on_update = parse_general_expression(group_scanner)
                    elif group_scanner.search_and_move("AUTO_INCREMENT"):
                        column.is_auto_increment = True
                    elif group_scanner.search_and_move("UNSIGNED"):
                        column.is_unsigned = True
                    elif group_scanner.search_and_move("ZEROFILL"):
                        column.is_zerofill = True
                    else:
                        raise SqlParseError(f"Cannot parse ddl column: {group_scanner}")
                self.builder.append_column(column)

        self.stage = MySQLCreateTableParser.ParseStage.AFTER_COLUMNS_AND_KEY_LIST
        return True

    def _parse_table_config(self):
        while not self.scanner.is_finish:
            if self.scanner.search_and_move("ENGINE"):
                self.scanner.match("=")
                self.builder.set_engine(self.scanner.pop_as_source())
            elif self.scanner.search_and_move("AUTO_INCREMENT"):
                self.scanner.match("=")
                self.builder.set_table_auto_increment(int(self.scanner.pop_as_source()))
            elif self.scanner.search_and_move("DEFAULT", "CHARSET"):
                self.scanner.match("=")
                self.builder.set_default_charset(self.scanner.pop_as_source())
            elif self.scanner.search_and_move("ROW_FORMAT"):
                self.scanner.match("=")
                self.builder.set_row_format(self.scanner.pop_as_source())
            elif self.scanner.search_and_move("COLLATE"):
                self.scanner.match("=")
                self.builder.set_row_format(self.scanner.pop_as_source())
            elif self.scanner.search_and_move("COMMENT"):
                self.scanner.match("=")
                self.builder.set_comment(self.scanner.pop_as_source())
            elif self.scanner.search_and_move("STATS_PERSISTENT"):
                self.scanner.match("=")
                self.builder.states_persistent = self.scanner.pop_as_source()
            else:
                raise SqlParseError(f"unknown table config: {self.scanner}")
        self.scanner.search_and_move(";")
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
    scanner = build_token_scanner(sql)
    return MySQLCreateTableParser(scanner).builder
