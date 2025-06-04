"""
INSERT 语句和 REPLACE 语句（insert or replace statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.statement.select_statement import QueryExpression
    from metasequoia_sql.ast.phrase.dml_option import DmlOption
    from metasequoia_sql.ast.statement.update_statement import UpdateElement
    from metasequoia_sql.ast.basic.ident import TableIdent

__all__ = [
    "RowValue",
    "TempInsertColumnAndValue",
    "TempInsertColumnAndQuery",
    "TempInsertAlias",
    "InsertOrReplaceStatement",
]


class RowValue(Node):
    """INSERT 和 REPLACE 语句中的行数据"""

    __slots__ = (
        "_value_list"
    )

    def __init__(self, value_list: List[Expression]):
        self._value_list = value_list

    @property
    def value_list(self) -> List[Expression]:
        return self._value_list


class TempInsertColumnAndValue(Node):
    """【临时对象】INSERT 和 REPLACE 语句中字段名称列表和值列表的元组"""

    __slots__ = (
        "_column_list",
        "_value_list"
    )

    def __init__(self, column_list: List[Expression], value_list: List[RowValue]):
        self._column_list = column_list
        self._value_list = value_list

    @property
    def column_list(self) -> List[Expression]:
        return self._column_list

    @property
    def value_list(self) -> List[RowValue]:
        return self._value_list


class TempInsertColumnAndQuery(Node):
    """【临时对象】INSERT 和 REPLACE 语句中字段名称列表和查询表达式的元组"""

    __slots__ = (
        "_column_list",
        "_query_expression"
    )

    def __init__(self, column_list: List[Expression], query_expression: "QueryExpression"):
        self._column_list = column_list
        self._query_expression = query_expression

    @property
    def column_list(self) -> List[Expression]:
        return self._column_list

    @property
    def query_expression(self) -> "QueryExpression":
        return self._query_expression


class TempInsertAlias(Node):
    """【临时对象】INSERT 语句中的表别名和字段别名的元组"""

    __slots__ = (
        "_table_alias",
        "_column_alias_list"
    )

    def __init__(self, table_alias: Optional[str], column_alias_list: Optional[List[str]]):
        self._table_alias = table_alias
        self._column_alias_list = column_alias_list

    @property
    def table_alias(self) -> Optional[str]:
        return self._table_alias

    @property
    def column_alias_list(self) -> Optional[List[str]]:
        return self._column_alias_list


class InsertOrReplaceStatement(Node):
    """INSERT 语句和 REPLACE 语句

    标注格式：https://dev.mysql.com/doc/refman/8.4/en/insert.html
    """

    __slots__ = (
        "_is_replace",
        "_dml_option",
        "_table_name",
        "_use_partition",
        "_column_list",
        "_value_list",
        "_set_update_list",
        "_table_alias",
        "_column_alias_list",
        "_query_expression",
        "_on_duplicate_key_update_list"
    )

    def __init__(self,
                 is_replace: bool,
                 dml_option: "DmlOption",
                 table_name: "TableIdent",
                 use_partition: Optional[List[Expression]],
                 column_list: List[Expression],
                 value_list: List[RowValue],
                 set_update_list: List["UpdateElement"],
                 table_alias: Optional[str],
                 column_alias_list: Optional[List[str]],
                 query_expression: Optional["QueryExpression"],
                 on_duplicate_key_update_list: List["UpdateElement"]
                 ):
        self._is_replace = is_replace
        self._dml_option = dml_option
        self._table_name = table_name
        self._use_partition = use_partition
        self._column_list = column_list
        self._value_list = value_list
        self._set_update_list = set_update_list
        self._table_alias = table_alias
        self._column_alias_list = column_alias_list
        self._query_expression = query_expression
        self._on_duplicate_key_update_list = on_duplicate_key_update_list

    @staticmethod
    def create_insert_by_values(dml_option: "DmlOption",
                                table_name: "TableIdent",
                                use_partition: Optional[List[Expression]],
                                column_list: List[Expression],
                                value_list: List[RowValue],
                                table_alias: Optional[str],
                                column_alias_list: Optional[List[str]],
                                on_duplicate_key_update_list: List["UpdateElement"]
                                ) -> "InsertOrReplaceStatement":
        """构造第 1 种格式的 INSERT 语句"""
        return InsertOrReplaceStatement(
            is_replace=False,
            dml_option=dml_option,
            table_name=table_name,
            use_partition=use_partition,
            column_list=column_list,
            value_list=value_list,
            set_update_list=[],
            table_alias=table_alias,
            column_alias_list=column_alias_list,
            query_expression=None,
            on_duplicate_key_update_list=on_duplicate_key_update_list
        )

    @staticmethod
    def create_insert_by_set(dml_option: "DmlOption",
                             table_name: "TableIdent",
                             use_partition: Optional[List[Expression]],
                             set_update_list: List["UpdateElement"],
                             table_alias: Optional[str],
                             column_alias_list: Optional[List[str]],
                             on_duplicate_key_update_list: List["UpdateElement"]
                             ) -> "InsertOrReplaceStatement":
        """构造第 2 种格式的 INSERT 语句"""
        return InsertOrReplaceStatement(
            is_replace=False,
            dml_option=dml_option,
            table_name=table_name,
            use_partition=use_partition,
            column_list=[],
            value_list=[],
            set_update_list=set_update_list,
            table_alias=table_alias,
            column_alias_list=column_alias_list,
            query_expression=None,
            on_duplicate_key_update_list=on_duplicate_key_update_list
        )

    @staticmethod
    def create_insert_by_query(dml_option: "DmlOption",
                               table_name: "TableIdent",
                               use_partition: Optional[List[Expression]],
                               column_list: List[Expression],
                               query_expression: "QueryExpression",
                               on_duplicate_key_update_list: List["UpdateElement"]):
        """构造第 3 种格式的 INSERT 语句"""
        return InsertOrReplaceStatement(
            is_replace=False,
            dml_option=dml_option,
            table_name=table_name,
            use_partition=use_partition,
            column_list=column_list,
            value_list=[],
            set_update_list=[],
            table_alias=None,
            column_alias_list=None,
            query_expression=query_expression,
            on_duplicate_key_update_list=on_duplicate_key_update_list
        )

    @staticmethod
    def create_replace_by_values(dml_option: "DmlOption",
                                 table_name: "TableIdent",
                                 use_partition: Optional[List[Expression]],
                                 column_list: List[Expression],
                                 value_list: List[RowValue]):
        """构造第 1 种格式的 REPLACE 语句"""
        return InsertOrReplaceStatement(
            is_replace=True,
            dml_option=dml_option,
            table_name=table_name,
            use_partition=use_partition,
            column_list=column_list,
            value_list=value_list,
            set_update_list=[],
            table_alias=None,
            column_alias_list=None,
            query_expression=None,
            on_duplicate_key_update_list=[]
        )

    @staticmethod
    def create_replace_by_set(dml_option: "DmlOption",
                              table_name: "TableIdent",
                              use_partition: Optional[List[Expression]],
                              set_update_list: List["UpdateElement"]):
        """构造第 2 种格式的 REPLACE 语句"""
        return InsertOrReplaceStatement(
            is_replace=True,
            dml_option=dml_option,
            table_name=table_name,
            use_partition=use_partition,
            column_list=[],
            value_list=[],
            set_update_list=set_update_list,
            table_alias=None,
            column_alias_list=None,
            query_expression=None,
            on_duplicate_key_update_list=[]
        )

    @staticmethod
    def create_replace_by_query(dml_option: "DmlOption",
                                table_name: "TableIdent",
                                use_partition: Optional[List[Expression]],
                                column_list: List[Expression],
                                query_expression: "QueryExpression"):
        """构造第 3 种格式的 REPLACE 语句"""
        return InsertOrReplaceStatement(
            is_replace=True,
            dml_option=dml_option,
            table_name=table_name,
            use_partition=use_partition,
            column_list=column_list,
            value_list=[],
            set_update_list=[],
            table_alias=None,
            column_alias_list=None,
            query_expression=query_expression,
            on_duplicate_key_update_list=[]
        )

    @property
    def is_replace(self) -> bool:
        return self._is_replace

    @property
    def dml_option(self) -> "DmlOption":
        return self._dml_option

    @property
    def table_name(self) -> "TableIdent":
        return self._table_name

    @property
    def use_partition(self) -> Optional[List[Expression]]:
        return self._use_partition

    @property
    def column_list(self) -> List[Expression]:
        return self._column_list

    @property
    def value_list(self) -> List[RowValue]:
        return self._value_list

    @property
    def set_update_list(self) -> List["UpdateElement"]:
        return self._set_update_list

    @property
    def table_alias(self) -> Optional[str]:
        return self._table_alias

    @property
    def column_alias_list(self) -> Optional[List[str]]:
        return self._column_alias_list

    @property
    def query_expression(self) -> Optional["QueryExpression"]:
        return self._query_expression

    @property
    def on_duplicate_key_update_list(self) -> List["UpdateElement"]:
        return self._on_duplicate_key_update_list
