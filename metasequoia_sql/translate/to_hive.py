"""
类型转换：将全属性 SQL 语句转化为 Hive 特性 SQL 语句
"""

from metasequoia_sql.objects.hive import *
from metasequoia_sql.translate.full_statement import *


def ddl_column_type_to_hive(column_type: DDLColumnTypeFull) -> DDLColumnTypeHive:
    return DDLColumnTypeHive(
        name=column_type.name,
        params=column_type.params
    )


def ddl_column_to_hive(column: DDLColumnFull) -> DDLColumnHive:
    return DDLColumnHive(
        column_name=column.column_name,
        column_type=ddl_column_type_to_hive(column.column_type),
        comment=column.comment
    )


def ddl_create_table_statement_to_hive(
        create_table_statement: DDLCreateTableStatementFull
) -> DDLCreateTableStatementHive:
    return DDLCreateTableStatementHive(
        schema_name=create_table_statement.schema_name,
        table_name=create_table_statement.table_name,
        comment=create_table_statement.comment,
        if_not_exists=create_table_statement.if_not_exists,
        columns=[ddl_column_to_hive(column) for column in create_table_statement.columns],
        partition_by=[ddl_column_to_hive(column) for column in create_table_statement.partition_by]
    )
