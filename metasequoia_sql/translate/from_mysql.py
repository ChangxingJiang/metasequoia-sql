"""
类型转换：将 MySQL 特性的 SQL 语句转化为全特性 SQL 语句
"""

from metasequoia_sql.statements.mysql import *
from metasequoia_sql.translate.full_statement import *


def ddl_column_type_from_mysql(column_type: DDLColumnTypeMySQL) -> DDLColumnTypeFull:
    return DDLColumnTypeFull(
        name=column_type.name,
        params=column_type.params
    )


def ddl_column_from_mysql(column: DDLColumnMySQL) -> DDLColumnFull:
    return DDLColumnFull(
        column_name=column.column_name,
        column_type=ddl_column_type_from_mysql(column.column_type),
        is_unsigned=column.is_unsigned,
        is_zerofill=column.is_zerofill,
        character_set=column.character_set,
        collate=column.collate,
        is_allow_null=column.is_allow_null,
        is_not_null=column.is_not_null,
        is_auto_increment=column.is_auto_increment,
        default=column.default,
        on_update=column.on_update,
        comment=column.comment
    )


def ddl_primary_key_from_mysql(primary_key: DDLPrimaryKeyMySQL) -> DDLPrimaryKeyFull:
    return DDLPrimaryKeyFull(
        column=primary_key.column
    )


def ddl_unique_key_from_mysql(unique_key: DDLUniqueKeyMySQL) -> DDLUniqueKeyFull:
    return DDLUniqueKeyFull(
        name=unique_key.name,
        columns=unique_key.columns
    )


def ddl_key_from_mysql(unique_key: DDLKeyMySQL) -> DDLKeyFull:
    return DDLKeyFull(
        name=unique_key.name,
        columns=unique_key.columns
    )


def ddl_foreign_key_from_mysql(foreign_key: DDLForeignKeyMySQL) -> DDLForeignKeyFull:
    return DDLForeignKeyFull(
        constraint_name=foreign_key.constraint_name,
        slave_columns=foreign_key.slave_columns,
        master_table_name=foreign_key.master_table_name,
        master_columns=foreign_key.master_columns
    )


def ddl_fulltext_key_from_mysql(fulltext_key: DDLFulltextKeyMysql) -> DDLFulltextKeyFull:
    return DDLFulltextKeyFull(
        name=fulltext_key.name,
        columns=fulltext_key.columns
    )


def ddl_create_table_statement_from_mysql(
        create_table_statement: DDLCreateTableStatementMySQL
) -> DDLCreateTableStatementFull:
    return DDLCreateTableStatementFull(
        schema_name=create_table_statement.schema_name,
        table_name=create_table_statement.table_name,
        comment=create_table_statement.comment,
        if_not_exists=create_table_statement.if_not_exists,
        columns=[ddl_column_from_mysql(column) for column in create_table_statement.columns],
        primary_key=create_table_statement.primary_key,
        unique_key=[ddl_unique_key_from_mysql(unique_key) for unique_key in create_table_statement.unique_key],
        key=[ddl_key_from_mysql(key) for key in create_table_statement.key],
        fulltext_key=[ddl_fulltext_key_from_mysql(key) for key in create_table_statement.fulltext_key],
        foreign_key=[ddl_foreign_key_from_mysql(foreign_key) for foreign_key in create_table_statement.foreign_key],
        engine=create_table_statement.engine,
        auto_increment=create_table_statement.auto_increment,
        default_charset=create_table_statement.default_charset,
        collate=create_table_statement.collate,
        row_format=create_table_statement.row_format,
        states_persistent=create_table_statement.states_persistent
    )
