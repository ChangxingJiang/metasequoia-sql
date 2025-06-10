"""
CREATE TABLE 语句（create table statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_table_option import TableOption
    from metasequoia_sql.ast.clause.ddl_partition_by_clause import DdlPartitionByClause
    from metasequoia_sql.ast.phrase.on_duplicate import OnDuplicate
    from metasequoia_sql.ast.statement.select_statement import QueryExpression
    from metasequoia_sql.ast.basic.ident import TableIdent
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
                 opt_create_table_option_list: List["TableOption"],
                 opt_partition_clause: Optional["DdlPartitionByClause"],
                 on_duplicate: "OnDuplicate",
                 opt_query_expression: Optional["QueryExpression"]):
        self._opt_create_table_option_list = opt_create_table_option_list
        self._opt_partition_clause = opt_partition_clause
        self._on_duplicate = on_duplicate
        self._opt_query_expression = opt_query_expression

    @property
    def opt_create_table_option_list(self) -> List["TableOption"]:
        return self._opt_create_table_option_list

    @property
    def opt_partition_clause(self) -> Optional["DdlPartitionByClause"]:
        return self._opt_partition_clause

    @property
    def on_duplicate(self) -> "OnDuplicate":
        return self._on_duplicate

    @property
    def opt_query_expression(self) -> Optional["QueryExpression"]:
        return self._opt_query_expression

    def set_create_table_option_list(self, create_table_option_list: List["TableOption"]) -> "TempCreateTableOption":
        self._opt_create_table_option_list = create_table_option_list
        return self

    def set_partition_clause(self, partition_clause: "DdlPartitionByClause") -> "TempCreateTableOption":
        self._opt_partition_clause = partition_clause
        return self


class CreateTableStatement(Statement):
    """CREATE TABLE 语句的抽象类"""

    __slots__ = (
        "_temporary",
        "_if_not_exists",
        "_table_ident"
    )

    def __init__(self, temporary: bool, if_not_exists: bool, table_ident: "TableIdent"):
        self._temporary = temporary
        self._if_not_exists = if_not_exists
        self._table_ident = table_ident

    @property
    def temporary(self) -> bool:
        return self._temporary

    @property
    def if_not_exists(self) -> bool:
        return self._if_not_exists

    @property
    def table_ident(self) -> "TableIdent":
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
                 table_ident: "TableIdent",
                 table_element_list: List["TableElement"],
                 opt_create_table_option_list: List["TableOption"],
                 opt_partition_clause: Optional["DdlPartitionByClause"],
                 on_duplicate: "OnDuplicate",
                 opt_query_expression: Optional["QueryExpression"], ):
        super().__init__(temporary, if_not_exists, table_ident)
        self._table_element_list = table_element_list
        self._opt_create_table_option_list = opt_create_table_option_list
        self._opt_partition_clause = opt_partition_clause
        self._on_duplicate = on_duplicate
        self._opt_query_expression = opt_query_expression

    @property
    def table_element_list(self) -> List["TableElement"]:
        return self._table_element_list

    @property
    def opt_create_table_option_list(self) -> List["TableOption"]:
        return self._opt_create_table_option_list

    @property
    def opt_partition_clause(self) -> Optional["DdlPartitionByClause"]:
        return self._opt_partition_clause

    @property
    def on_duplicate(self) -> "OnDuplicate":
        return self._on_duplicate

    @property
    def opt_query_expression(self) -> Optional["QueryExpression"]:
        return self._opt_query_expression


class CreateTableStatementAsLike(CreateTableStatement):
    """通过 LIKE 子句构造的 CREATE TABLE 语句"""

    __slots__ = (
        "_like_table_ident"
    )

    def __init__(self,
                 temporary: bool,
                 if_not_exists: bool,
                 table_ident: "TableIdent",
                 like_table_ident: "TableIdent"):
        super().__init__(temporary, if_not_exists, table_ident)
        self._like_table_ident = like_table_ident

    @property
    def like_table_ident(self) -> "TableIdent":
        return self._like_table_ident
