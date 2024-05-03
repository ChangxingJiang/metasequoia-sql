"""
抽象语法树（AST）的 DML 类节点
"""

import abc
import dataclasses
from typing import Optional, Tuple

from metasequoia_sql.core.node.abc_node import ASTBase
from metasequoia_sql.core.node.basic_node import ASTInsertType
from metasequoia_sql.core.node.dql_node import (ASTStatement, ASTTableNameExpression, ASTColumnNameExpression,
                                                ASTValueExpression, ASTSelectStatement, ASTGeneralExpression)
from metasequoia_sql.core.node.sql_type import SQLType

__all__ = [
    "ASTEqualExpression",  # 等式表达式
    "ASTPartitionExpression",  # 分区表达式
    "ASTInsertStatement",  # INSERT 语句
    "ASTInsertValuesStatement",  # INSERT ... VALUES ... 语句
    "ASTInsertSelectStatement",  # INSERT ... SELECT ... 语句
]


# ---------------------------------------- 等式表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTEqualExpression(ASTBase):
    """等式表达式"""

    before_value: ASTGeneralExpression = dataclasses.field(kw_only=True)
    after_value: ASTGeneralExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.before_value.source(data_source)} = {self.after_value.source(data_source)}"


# ---------------------------------------- 分区表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTPartitionExpression(ASTBase):
    """分区表达式：PARTITION (<partition_expression>)"""

    partition_list: Tuple[ASTEqualExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        partition_list_str = ", ".join(partition.source(data_source) for partition in self.partition_list)
        return f"PARTITION ({partition_list_str})"


# ---------------------------------------- INSERT 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertStatement(ASTStatement, abc.ABC):
    """INSERT 表达式

    两个子类包含 VALUES 和 SELECT 两种方式

    INSERT {INTO|OVERWRITE} [TABLE] <table_name_expression> [PARTITION (<partition_expression>)]
    [(<colum_name_expression [,<column_name_expression> ...]>)]
    {VALUES <value_expression> [,<value_expression> ...] | <select_statement>}
    """

    insert_type: ASTInsertType = dataclasses.field(kw_only=True)
    table_name: ASTTableNameExpression = dataclasses.field(kw_only=True)
    partition: Optional[ASTPartitionExpression] = dataclasses.field(kw_only=True)
    columns: Optional[Tuple[ASTColumnNameExpression, ...]] = dataclasses.field(kw_only=True)

    def _insert_str(self, data_source: SQLType) -> str:
        insert_type_str = self.insert_type.source(data_source)
        table_keyword_str = "TABLE " if data_source == SQLType.HIVE else ""
        partition_str = self.partition.source(data_source) + " " if self.partition is not None else ""
        if self.columns is not None:
            columns_str = "(" + ", ".join(column.source(data_source) for column in self.columns) + ") "
        else:
            columns_str = ""
        return (f"{insert_type_str} {table_keyword_str}{self.table_name.source(data_source)} "
                f"{partition_str}{columns_str}")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertValuesStatement(ASTInsertStatement):
    """INSERT ... VALUES ... 语句"""

    values: Tuple[ASTValueExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        values_str = ", ".join(value.source(data_source) for value in self.values)
        return f"{self._insert_str(data_source)}VALUES {values_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertSelectStatement(ASTInsertStatement):
    """INSERT ... SELECT ... 语句"""

    select_statement: ASTSelectStatement = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._insert_str(data_source)} {self.select_statement.source(data_source)}"
