"""
类型转换：将全属性 SQL 语句转化为 Hive 特性 SQL 语句
"""

from metasequoia_sql.objects.hive import *


def ddl_column_to_hive(column: DDLColumnExpression) -> DDLColumnExpression:
    return DDLColumnExpression(
        column_name=column.column_name,
        column_type=column.column_type,
        comment=column.comment
    )


def ddl_create_table_statement_to_hive(
        create_table_statement: DDLCreateTableStatement
) -> DDLCreateTableStatementHive:
    return DDLCreateTableStatementHive(
        schema_name=create_table_statement.schema_name,
        table_name=create_table_statement.table_name,
        comment=create_table_statement.comment,
        if_not_exists=create_table_statement.if_not_exists,
        columns=[ddl_column_to_hive(column) for column in create_table_statement.columns],
        partition_by=[ddl_column_to_hive(column) for column in create_table_statement.partition_by]
    )
