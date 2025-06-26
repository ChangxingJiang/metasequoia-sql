"""
表达式相关抽象语法树节点
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.statement.select_statement import QueryExpression

__all__ = [
    "UdfExpression",
    "Row",
    "OdbcDate",
    "WhenItem",
    "Case",
    "TableWild",
    "ExpressionWithAlias",
    "Wild",
    "DefaultValue",
    "SingleRowSubSelect",
    "ExistsSubSelect",
]


class UdfExpression(Expression):
    """UDF 表达式"""

    __slots__ = ["_expression", "_alias"]

    def __init__(self, expression: Expression, alias: Optional[str]):
        """初始化 UDF 表达式
        
        Parameters
        ----------
        expression : Expression
            表达式
        alias : Optional[str]
            别名
        """
        self._expression = expression
        self._alias = alias

    @property
    def expression(self) -> Expression:
        """获取表达式
        
        Returns
        -------
        Expression
            表达式
        """
        return self._expression

    @property
    def alias(self) -> Optional[str]:
        """获取别名
        
        Returns
        -------
        Optional[str]
            别名
        """
        return self._alias


class Row(Expression):
    """行表达式"""

    __slots__ = ["_value_list"]

    def __init__(self, value_list: List[Expression]):
        """初始化行表达式
        
        Parameters
        ----------
        value_list : List[Expression]
            值列表
        """
        self._value_list = value_list

    @property
    def value_list(self) -> List[Expression]:
        """获取值列表
        
        Returns
        -------
        List[Expression]
            值列表
        """
        return self._value_list


class OdbcDate(Expression):
    """ODBC 日期格式

    { odbc_type odbc_value }
    """

    __slots__ = ["_odbc_type", "_odbc_value"]

    def __init__(self, odbc_type: str, odbc_value: Expression):
        """初始化 ODBC 日期格式
        
        Parameters
        ----------
        odbc_type : str
            ODBC 类型
        odbc_value : Expression
            ODBC 值表达式
        """
        self._odbc_type = odbc_type
        self._odbc_value = odbc_value

    @property
    def odbc_type(self) -> str:
        """获取 ODBC 类型
        
        Returns
        -------
        str
            ODBC 类型
        """
        return self._odbc_type

    @property
    def odbc_value(self) -> Expression:
        """获取 ODBC 值表达式
        
        Returns
        -------
        Expression
            ODBC 值表达式
        """
        return self._odbc_value


class WhenItem(Node):
    """CASE 结构中 WHEN 条件"""

    __slots__ = ["_condition", "_expression"]

    def __init__(self, condition: Expression, expression: Expression):
        """初始化 WHEN 条件项
        
        Parameters
        ----------
        condition : Expression
            条件表达式
        expression : Expression
            结果表达式
        """
        self._condition = condition
        self._expression = expression

    @property
    def condition(self) -> Expression:
        """获取条件表达式
        
        Returns
        -------
        Expression
            条件表达式
        """
        return self._condition

    @property
    def expression(self) -> Expression:
        """获取结果表达式
        
        Returns
        -------
        Expression
            结果表达式
        """
        return self._expression


class Case(Expression):
    """CASE 结构"""

    __slots__ = ["_case_expression", "_when_list", "_else_expression"]

    def __init__(self, case_expression: Expression, when_list: List[WhenItem], else_expression: Expression):
        """初始化 CASE 表达式
        
        Parameters
        ----------
        case_expression : Expression
            CASE 表达式
        when_list : List[WhenItem]
            WHEN 条件列表
        else_expression : Expression
            ELSE 表达式
        """
        self._case_expression = case_expression
        self._when_list = when_list
        self._else_expression = else_expression

    @property
    def case_expression(self) -> Expression:
        """获取 CASE 表达式
        
        Returns
        -------
        Expression
            CASE 表达式
        """
        return self._case_expression

    @property
    def when_list(self) -> List[WhenItem]:
        """获取 WHEN 条件列表
        
        Returns
        -------
        List[WhenItem]
            WHEN 条件列表
        """
        return self._when_list

    @property
    def else_expression(self) -> Expression:
        """获取 ELSE 表达式
        
        Returns
        -------
        Expression
            ELSE 表达式
        """
        return self._else_expression


class TableWild(Expression):
    """表中所有字段的通配符

    table_name.*
    schema_name.table_name.*
    """

    __slots__ = ["_schema_name", "_table_name"]

    def __init__(self, schema_name: Optional[str], table_name: str):
        """初始化表通配符
        
        Parameters
        ----------
        schema_name : Optional[str]
            模式名
        table_name : str
            表名
        """
        self._schema_name = schema_name
        self._table_name = table_name

    @property
    def schema_name(self) -> Optional[str]:
        """获取模式名
        
        Returns
        -------
        Optional[str]
            模式名
        """
        return self._schema_name

    @property
    def table_name(self) -> Optional[str]:
        """获取表名
        
        Returns
        -------
        Optional[str]
            表名
        """
        return self._table_name


class ExpressionWithAlias(Expression):
    """包含别名的表达式"""

    __slots__ = ["_expression", "_alias"]

    def __init__(self, expression: Expression, alias: Optional[str]):
        """初始化包含别名的表达式
        
        Parameters
        ----------
        expression : Expression
            表达式
        alias : Optional[str]
            别名
        """
        self._expression = expression
        self._alias = alias

    @property
    def expression(self) -> Expression:
        """获取表达式
        
        Returns
        -------
        Expression
            表达式
        """
        return self._expression

    @property
    def alias(self) -> Optional[str]:
        """获取别名
        
        Returns
        -------
        Optional[str]
            别名
        """
        return self._alias


class Wild(Expression):
    """通配符"""


class DefaultValue(Expression):
    """DEFAULT 关键字表示的默认值"""


class SingleRowSubSelect(Expression):
    """单行子查询表达式"""

    __slots__ = ["_query_expression"]

    def __init__(self, query_expression: "QueryExpression"):
        """初始化单行子查询表达式
        
        Parameters
        ----------
        query_expression : QueryExpression
            查询表达式
        """
        self._query_expression = query_expression

    @property
    def query_expression(self) -> "QueryExpression":
        """获取查询表达式
        
        Returns
        -------
        QueryExpression
            查询表达式
        """
        return self._query_expression


class ExistsSubSelect(Expression):
    """存在子查询表达式"""

    __slots__ = ["_query_expression"]

    def __init__(self, query_expression: "QueryExpression"):
        """初始化存在子查询表达式
        
        Parameters
        ----------
        query_expression : QueryExpression
            查询表达式
        """
        self._query_expression = query_expression

    @property
    def query_expression(self) -> "QueryExpression":
        """获取查询表达式
        
        Returns
        -------
        QueryExpression
            查询表达式
        """
        return self._query_expression
