"""
类型转换：将 MySQL 特性的 SQL 语句转化为全特性 SQL 语句
"""

from metasequoia_sql.objects.mysql import *
from metasequoia_sql.translate.full_statement import *


def ddl_create_table_statement_from_mysql(
        create_table_statement: DDLCreateTableStatementMySQL
) -> DDLCreateTableStatementFull:
    return DDLCreateTableStatementFull(
        schema_name=create_table_statement.schema_name,
        table_name=create_table_statement.table_name,
        comment=create_table_statement.comment,
        if_not_exists=create_table_statement.if_not_exists,
        columns=create_table_statement.columns,
        primary_key=create_table_statement.primary_key,
        unique_key=create_table_statement.unique_key,
        key=create_table_statement.key,
        fulltext_key=create_table_statement.fulltext_key,
        foreign_key=create_table_statement.foreign_key,
        engine=create_table_statement.engine,
        auto_increment=create_table_statement.auto_increment,
        default_charset=create_table_statement.default_charset,
        collate=create_table_statement.collate,
        row_format=create_table_statement.row_format,
        states_persistent=create_table_statement.states_persistent
    )
