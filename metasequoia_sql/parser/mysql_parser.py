"""
MySQL 解析器

Hive 保留字：https://cwiki.apache.org/confluence/display/Hive/LanguageManual+DDL
"""

from metasequoia_sql.objects.mysql import *
from metasequoia_sql.parser.common import *


class MySQLCreateTableParser:
    """
    当前已知不支持的场景：虚拟列 GENERATED ALWAYS AS（RDS427.prism1.oned_topic_kafka）
    """

    def __init__(self, scanner: TokenScanner):
        # 过滤 statement 中的空白字符
        self.scanner = scanner

        # 解析字段、索引括号前的部分
        scanner.match("CREATE", "TABLE")
        if_not_exists = scanner.search_and_move("IF", "NOT", "EXISTS")
        table_name = scanner.pop_as_source().strip("`")  # TODO 待改为 TableNameExpression，并支持 schema_name

        # 解析字段和索引
        columns: List[DDLColumnExpression] = []
        primary_key: Optional[DDLPrimaryIndexExpression] = None
        unique_key: List[DDLUniqueIndexExpression] = []
        key: List[DDLNormalIndexExpression] = []
        fulltext_key: List[DDLFulltextIndexExpression] = []
        foreign_key: List[DDLForeignKeyExpression] = []
        for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            if is_ddl_primary_index_expression(group_scanner):
                primary_key = parse_ddl_primary_index_expression(group_scanner)
            elif is_ddl_unique_index_expression(group_scanner):
                unique_key.append(parse_ddl_unique_index_expression(group_scanner))
            elif is_ddl_normal_index_expression(group_scanner):
                key.append(parse_ddl_normal_index_expression(group_scanner))
            elif is_ddl_fulltext_expression(group_scanner):
                fulltext_key.append(parse_ddl_fulltext_expression(group_scanner))
            elif is_ddl_foreign_key_expression(group_scanner):
                foreign_key.append(parse_dll_foreign_key_expression(group_scanner))
            else:
                columns.append(parse_ddl_column_expression(group_scanner))

        # 解析表属性
        comment: Optional[str] = None
        engine: Optional[str] = None
        auto_increment: Optional[int] = None
        default_charset: Optional[str] = None
        collate: Optional[str] = None
        row_format: Optional[str] = None
        states_persistent: Optional[str] = None
        while not scanner.is_finish:
            if scanner.search_and_move("ENGINE"):
                scanner.search_and_move("=")
                engine = scanner.pop_as_source()
            elif scanner.search_and_move("AUTO_INCREMENT"):
                scanner.match("=")
                auto_increment = int(scanner.pop_as_source())
            elif scanner.search_and_move("DEFAULT", "CHARSET"):
                scanner.match("=")
                default_charset = scanner.pop_as_source()
            elif scanner.search_and_move("ROW_FORMAT"):
                scanner.match("=")
                row_format = scanner.pop_as_source()
            elif scanner.search_and_move("COLLATE"):
                scanner.match("=")
                collate = scanner.pop_as_source()
            elif scanner.search_and_move("COMMENT"):
                scanner.match("=")
                comment = scanner.pop_as_source()
            elif scanner.search_and_move("STATS_PERSISTENT"):
                scanner.match("=")
                states_persistent = scanner.pop_as_source()
            else:
                raise SqlParseError(f"未知的 DDL 表属性: {scanner}")
        scanner.search_and_move(";")

        self.builder = DDLCreateTableStatementMySQL(
            table_name=table_name,
            comment=comment,
            if_not_exists=if_not_exists,
            columns=columns,
            primary_key=primary_key,
            unique_key=unique_key,
            key=key,
            fulltext_key=fulltext_key,
            foreign_key=foreign_key,
            engine=engine,
            auto_increment=auto_increment,
            default_charset=default_charset,
            collate=collate,
            row_format=row_format,
            states_persistent=states_persistent
        )


def parse_mysql_create_table_statement(sql: str) -> DDLCreateTableStatementMySQL:
    # 将 sql 解析为多个表达式，并检查是否有且只有 1 个表达式
    scanner = build_token_scanner(sql)
    return MySQLCreateTableParser(scanner).builder
