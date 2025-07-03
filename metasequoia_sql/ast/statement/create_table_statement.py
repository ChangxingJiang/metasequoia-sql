"""
CREATE TABLE 语句（create table statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption
    from metasequoia_sql.ast.clause.ddl_partition_by_clause import DdlPartitionByClause
    from metasequoia_sql.ast.phrase.on_duplicate import OnDuplicate
    from metasequoia_sql.ast.statement.select_statement import QueryExpression
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.ddl_table_element import TableElement

__all__ = [
    "TempCreateTableOption",
    "CreateTableStatement",
    "CreateTableStatementAsDefinition",
    "CreateTableStatementAsLike",
]


class TempCreateTableOption(Node):
    """【临时】CREATE TABLE 的选项"""

    __slots__ = (
        "_opt_create_table_option_list",
        "_opt_partition_clause",
        "_on_duplicate",
        "_opt_query_expression"
    )

    def __init__(self,
                 opt_create_table_option_list: List["DdlOption"],
                 opt_partition_clause: Optional["DdlPartitionByClause"],
                 on_duplicate: "OnDuplicate",
                 opt_query_expression: Optional["QueryExpression"]):
        self._opt_create_table_option_list = opt_create_table_option_list
        self._opt_partition_clause = opt_partition_clause
        self._on_duplicate = on_duplicate
        self._opt_query_expression = opt_query_expression

    @property
    def opt_create_table_option_list(self) -> List["DdlOption"]:
        """
        可选的创建表选项列表

        Returns
        -------
        List["DdlOption"]
            可选的创建表选项列表
        """
        return self._opt_create_table_option_list

    @property
    def opt_partition_clause(self) -> Optional["DdlPartitionByClause"]:
        """
        可选的分区子句

        Returns
        -------
        Optional["DdlPartitionByClause"]
            可选的分区子句
        """
        return self._opt_partition_clause

    @property
    def on_duplicate(self) -> "OnDuplicate":
        """
        重复键处理选项

        Returns
        -------
        OnDuplicate
            重复键处理选项
        """
        return self._on_duplicate

    @property
    def opt_query_expression(self) -> Optional["QueryExpression"]:
        """
        可选的查询表达式

        Returns
        -------
        Optional["QueryExpression"]
            可选的查询表达式
        """
        return self._opt_query_expression

    def set_create_table_option_list(self, create_table_option_list: List["DdlOption"]) -> "TempCreateTableOption":
        """
        设置创建表选项列表

        Parameters
        ----------
        create_table_option_list : List["DdlOption"]
            创建表选项列表

        Returns
        -------
        TempCreateTableOption
            当前实例
        """
        self._opt_create_table_option_list = create_table_option_list
        return self

    def set_partition_clause(self, partition_clause: "DdlPartitionByClause") -> "TempCreateTableOption":
        """
        设置分区子句

        Parameters
        ----------
        partition_clause : "DdlPartitionByClause"
            分区子句

        Returns
        -------
        TempCreateTableOption
            当前实例
        """
        self._opt_partition_clause = partition_clause
        return self


class CreateTableStatement(Statement):
    """CREATE TABLE 语句的抽象类"""

    __slots__ = (
        "_temporary",
        "_if_not_exists",
        "_table_ident"
    )

    def __init__(self, temporary: bool, if_not_exists: bool, table_ident: "Identifier"):
        self._temporary = temporary
        self._if_not_exists = if_not_exists
        self._table_ident = table_ident

    @property
    def temporary(self) -> bool:
        """
        是否为临时表

        Returns
        -------
        bool
            是否为临时表
        """
        return self._temporary

    @property
    def if_not_exists(self) -> bool:
        """
        是否使用 IF NOT EXISTS 选项

        Returns
        -------
        bool
            是否使用 IF NOT EXISTS 选项
        """
        return self._if_not_exists

    @property
    def table_ident(self) -> "Identifier":
        """
        表标识符

        Returns
        -------
        Identifier
            表标识符
        """
        return self._table_ident


class CreateTableStatementAsDefinition(CreateTableStatement):
    """通过定义字段和索引构造的 CREATE TABLE 语句"""

    __slots__ = (
        "_table_element_list",
        "_opt_create_table_option_list",
        "_opt_partition_clause",
        "_on_duplicate",
        "_opt_query_expression"
    )

    def __init__(self,
                 temporary: bool,
                 if_not_exists: bool,
                 table_ident: "Identifier",
                 table_element_list: List["TableElement"],
                 opt_create_table_option_list: List["DdlOption"],
                 opt_partition_clause: Optional["DdlPartitionByClause"],
                 on_duplicate: "OnDuplicate",
                 opt_query_expression: Optional["QueryExpression"]):
        # pylint: disable=R0913,R0917
        super().__init__(temporary, if_not_exists, table_ident)
        self._table_element_list = table_element_list
        self._opt_create_table_option_list = opt_create_table_option_list
        self._opt_partition_clause = opt_partition_clause
        self._on_duplicate = on_duplicate
        self._opt_query_expression = opt_query_expression

    @property
    def table_element_list(self) -> List["TableElement"]:
        """
        表元素列表

        Returns
        -------
        List["TableElement"]
            表元素列表
        """
        return self._table_element_list

    @property
    def opt_create_table_option_list(self) -> List["DdlOption"]:
        """
        可选的创建表选项列表

        Returns
        -------
        List["DdlOption"]
            可选的创建表选项列表
        """
        return self._opt_create_table_option_list

    @property
    def opt_partition_clause(self) -> Optional["DdlPartitionByClause"]:
        """
        可选的分区子句

        Returns
        -------
        Optional["DdlPartitionByClause"]
            可选的分区子句
        """
        return self._opt_partition_clause

    @property
    def on_duplicate(self) -> "OnDuplicate":
        """
        重复键处理选项

        Returns
        -------
        OnDuplicate
            重复键处理选项
        """
        return self._on_duplicate

    @property
    def opt_query_expression(self) -> Optional["QueryExpression"]:
        """
        可选的查询表达式

        Returns
        -------
        Optional["QueryExpression"]
            可选的查询表达式
        """
        return self._opt_query_expression


class CreateTableStatementAsLike(CreateTableStatement):
    """通过 LIKE 子句构造的 CREATE TABLE 语句"""

    __slots__ = (
        "_like_table_ident",
    )

    def __init__(self,
                 temporary: bool,
                 if_not_exists: bool,
                 table_ident: "Identifier",
                 like_table_ident: "Identifier"):
        super().__init__(temporary, if_not_exists, table_ident)
        self._like_table_ident = like_table_ident

    @property
    def like_table_ident(self) -> "Identifier":
        """
        LIKE 表标识符

        Returns
        -------
        Identifier
            LIKE 表标识符
        """
        return self._like_table_ident
