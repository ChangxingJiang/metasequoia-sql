"""
CREATE FUNCTION 语句（create function statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.phrase.field_type import FieldType
    from metasequoia_sql.ast.phrase.function_option import FunctionOption
    from metasequoia_sql.ast.phrase.process_command import ProcessCommand
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.basic.fixed_enum import EnumUdfReturnType

__all__ = [
    "FunctionParam",
    "CreateFunctionStatement",
    "CreateFunctionStandardStatement",
    "CreateFunctionUdfStatement",
    "CreateFunctionAggregateUdfStatement",
]


class FunctionParam(Node):
    """存储函数参数"""

    __slots__ = (
        "_param_name",
        "_param_type",
        "_param_collate",
    )

    def __init__(
            self,
            param_name: str,
            param_type: "FieldType",
            param_collate: Optional["Charset"],
    ):
        self._param_name = param_name
        self._param_type = param_type
        self._param_collate = param_collate

    @property
    def param_name(self) -> str:
        """
        参数名称

        Returns
        -------
        str
            参数名称
        """
        return self._param_name

    @property
    def param_type(self) -> "FieldType":
        """
        参数类型

        Returns
        -------
        FieldType
            参数类型
        """
        return self._param_type

    @property
    def param_collate(self) -> Optional["Charset"]:
        """
        参数排序规则

        Returns
        -------
        Optional["Charset"]
            参数排序规则
        """
        return self._param_collate


class CreateFunctionStatement(Statement):
    """CREATE FUNCTION 语句的基类"""


class CreateFunctionStandardStatement(CreateFunctionStatement):
    # pylint: disable=R0902
    """标准 CREATE FUNCTION 语句"""

    __slots__ = (
        "_definer",
        "_if_not_exists",
        "_function_name",
        "_param_list",
        "_return_type",
        "_return_collate",
        "_option_list",
        "_body",
    )

    def __init__(
            self,
            definer: Optional["UserName"],
            if_not_exists: bool,
            function_name: "Identifier",
            param_list: List["FunctionParam"],
            return_type: "FieldType",
            return_collate: Optional["Charset"],
            option_list: List["FunctionOption"],
            body: "ProcessCommand",
    ):
        # pylint: disable=R0913
        self._definer = definer
        self._if_not_exists = if_not_exists
        self._function_name = function_name
        self._param_list = param_list
        self._return_type = return_type
        self._return_collate = return_collate
        self._option_list = option_list
        self._body = body

    @property
    def definer(self) -> Optional["UserName"]:
        """
        函数定义者

        Returns
        -------
        Optional["UserName"]
            函数定义者用户名
        """
        return self._definer

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
    def function_name(self) -> "Identifier":
        """
        函数名称标识符

        Returns
        -------
        Identifier
            函数名称标识符
        """
        return self._function_name

    @property
    def param_list(self) -> List["FunctionParam"]:
        """
        函数参数列表

        Returns
        -------
        List["FunctionParam"]
            函数参数列表
        """
        return self._param_list

    @property
    def return_type(self) -> "FieldType":
        """
        函数返回类型

        Returns
        -------
        FieldType
            函数返回类型
        """
        return self._return_type

    @property
    def return_collate(self) -> Optional["Charset"]:
        """
        返回值排序规则

        Returns
        -------
        Optional["Charset"]
            返回值排序规则
        """
        return self._return_collate

    @property
    def option_list(self) -> List["FunctionOption"]:
        """
        函数选项列表

        Returns
        -------
        List["FunctionOption"]
            函数选项列表
        """
        return self._option_list

    @property
    def body(self) -> "ProcessCommand":
        """
        函数执行体

        Returns
        -------
        ProcessCommand
            函数执行体
        """
        return self._body


class CreateFunctionUdfStatement(CreateFunctionStatement):
    """CREATE UDF FUNCTION 语句"""

    __slots__ = (
        "_if_not_exists",
        "_function_name",
        "_return_type",
        "_library_name",
    )

    def __init__(
            self,
            if_not_exists: bool,
            function_name: str,
            return_type: "EnumUdfReturnType",
            library_name: str,
    ):
        self._if_not_exists = if_not_exists
        self._function_name = function_name
        self._return_type = return_type
        self._library_name = library_name

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
    def function_name(self) -> str:
        """
        函数名称

        Returns
        -------
        str
            函数名称
        """
        return self._function_name

    @property
    def return_type(self) -> "EnumUdfReturnType":
        """
        UDF 函数返回类型

        Returns
        -------
        EnumUdfReturnType
            UDF 函数返回类型
        """
        return self._return_type

    @property
    def library_name(self) -> str:
        """
        库名称

        Returns
        -------
        str
            库名称
        """
        return self._library_name


class CreateFunctionAggregateUdfStatement(CreateFunctionStatement):
    """CREATE AGGREGATE UDF FUNCTION 语句"""

    __slots__ = (
        "_if_not_exists",
        "_function_name",
        "_return_type",
        "_library_name",
    )

    def __init__(
            self,
            if_not_exists: bool,
            function_name: str,
            return_type: "EnumUdfReturnType",
            library_name: str,
    ):
        self._if_not_exists = if_not_exists
        self._function_name = function_name
        self._return_type = return_type
        self._library_name = library_name

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
    def function_name(self) -> str:
        """
        函数名称

        Returns
        -------
        str
            函数名称
        """
        return self._function_name

    @property
    def return_type(self) -> "EnumUdfReturnType":
        """
        聚合 UDF 函数返回类型

        Returns
        -------
        EnumUdfReturnType
            聚合 UDF 函数返回类型
        """
        return self._return_type

    @property
    def library_name(self) -> str:
        """
        库名称

        Returns
        -------
        str
            库名称
        """
        return self._library_name
