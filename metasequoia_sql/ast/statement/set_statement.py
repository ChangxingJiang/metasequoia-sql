# pylint: disable=R0801

"""
SET 语句（set statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Statement
from metasequoia_sql.ast.basic.fixed_enum import EnumSetOptionType, EnumSetVariableType

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.basic.variable import UserVariable

__all__ = [
    "SetOptionValue",
    "SetVariableValue",
    "SetUserVariableValue",
    "SetSystemVariableValue",
    "SetCharsetValue",
    "SetNamesInvalidValue",
    "SetNamesValue",
    "SetNamesDefaultValue",
    "SetStatement",
]


class SetOptionValue(Node):
    """SET语句中的选项值基类"""

    __slots__ = ["_option_type"]

    def __init__(self, option_type: "EnumSetOptionType"):
        self._option_type = option_type

    @property
    def option_type(self) -> "EnumSetOptionType":
        """
        选项类型

        Returns
        -------
        EnumSetOptionType
            选项类型
        """
        return self._option_type

    def set_option_type(self, option_type: "EnumSetOptionType") -> "SetOptionValue":
        """
        设置选项类型

        Parameters
        ----------
        option_type : EnumSetOptionType
            选项类型

        Returns
        -------
        SetOptionValue
            设置选项值
        """
        self._option_type = option_type
        return self


class SetVariableValue(SetOptionValue):
    """设置变量值 (lvalue_variable equal set_expr_or_default)
    
    Parameters
    ----------
    variable : Identifier
        变量标识符
    value : Expression
        设置的值
    """

    __slots__ = ["_variable", "_value"]

    def __init__(self, variable: "Identifier", value: Expression, option_type: "EnumSetOptionType"):
        super().__init__(option_type)
        self._variable = variable
        self._value = value

    @property
    def variable(self) -> "Identifier":
        """
        变量标识符

        Returns
        -------
        Identifier
            变量标识符
        """
        return self._variable

    @property
    def value(self) -> Expression:
        """
        设置的值

        Returns
        -------
        Expression
            设置的值
        """
        return self._value


class SetUserVariableValue(SetOptionValue):
    """设置用户变量值 (@ ident_or_text equal expr)
    
    Parameters
    ----------
    variable : UserVariable
        用户变量名
    value : Expression
        设置的值
    """

    __slots__ = ["_variable", "_value"]

    def __init__(self, variable: "UserVariable", value: Expression, option_type: "EnumSetOptionType"):
        super().__init__(option_type)
        self._variable = variable
        self._value = value

    @property
    def variable(self) -> "UserVariable":
        """
        用户变量

        Returns
        -------
        UserVariable
            用户变量
        """
        return self._variable

    @property
    def value(self) -> Expression:
        """
        设置的值

        Returns
        -------
        Expression
            设置的值
        """
        return self._value


class SetSystemVariableValue(SetOptionValue):
    """设置系统变量值 (@ @ opt_set_var_ident_type lvalue_variable equal set_expr_or_default)
    
    Parameters
    ----------
    variable_type : EnumSetVariableType
        变量类型
    variable : Identifier
        变量标识符
    value : Expression
        设置的值
    """

    __slots__ = ["_variable_type", "_variable", "_value"]

    def __init__(self, variable_type: "EnumSetVariableType", variable: "Identifier", value: Expression,
                 option_type: "EnumSetOptionType"):
        super().__init__(option_type)
        self._variable_type = variable_type
        self._variable = variable
        self._value = value

    @property
    def variable_type(self) -> "EnumSetVariableType":
        """
        变量类型

        Returns
        -------
        EnumSetVariableType
            变量类型
        """
        return self._variable_type

    @property
    def variable(self) -> "Identifier":
        """
        变量标识符

        Returns
        -------
        Identifier
            变量标识符
        """
        return self._variable

    @property
    def value(self) -> Expression:
        """
        设置的值

        Returns
        -------
        Expression
            设置的值
        """
        return self._value


class SetCharsetValue(SetOptionValue):
    """设置字符集 (character_set old_or_new_charset_name_or_default)
    
    Parameters
    ----------
    charset : Charset, optional
        字符集，None表示DEFAULT
    """

    __slots__ = ["_charset"]

    def __init__(self, charset: Optional["Charset"], option_type: "EnumSetOptionType"):
        super().__init__(option_type)
        self._charset = charset

    @property
    def charset(self) -> Optional["Charset"]:
        """
        字符集

        Returns
        -------
        Optional[Charset]
            字符集，None 表示 DEFAULT
        """
        return self._charset


class SetNamesInvalidValue(SetOptionValue):
    """无效的NAMES语法 (NAMES equal expr) - 总是产生错误"""

    __slots__ = ["_value"]

    def __init__(self, value: Expression, option_type: "EnumSetOptionType"):
        super().__init__(option_type)
        self._value = value

    @property
    def value(self) -> Expression:
        """
        值

        Returns
        -------
        Expression
            值
        """
        return self._value


class SetNamesValue(SetOptionValue):
    """设置NAMES (NAMES charset_name opt_collate)
    
    Parameters
    ----------
    charset : Charset
        字符集
    collation : Charset, optional
        排序规则
    """

    __slots__ = ["_charset", "_collation"]

    def __init__(self, charset: "Charset", collation: Optional["Charset"], option_type: "EnumSetOptionType"):
        super().__init__(option_type)
        self._charset = charset
        self._collation = collation

    @property
    def charset(self) -> "Charset":
        """
        字符集

        Returns
        -------
        Charset
            字符集
        """
        return self._charset

    @property
    def collation(self) -> Optional["Charset"]:
        """
        排序规则

        Returns
        -------
        Optional[Charset]
            排序规则
        """
        return self._collation


class SetNamesDefaultValue(SetOptionValue):
    """设置NAMES为默认值 (NAMES DEFAULT)"""


class SetStatement(Statement):
    """SET语句

    Parameters
    ----------
    option_values : list[SetOptionValue]
        选项值列表
    """

    __slots__ = ["_option_values"]

    def __init__(self, option_values: List[SetOptionValue]):
        self._option_values = option_values

    @property
    def option_values(self) -> List[SetOptionValue]:
        """
        选项值列表

        Returns
        -------
        List[SetOptionValue]
            选项值列表
        """
        return self._option_values
