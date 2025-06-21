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

__all__ = [
    "FunctionParam",
    "CreateFunctionStatement",
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
        return self._param_name

    @property
    def param_type(self) -> "FieldType":
        return self._param_type

    @property
    def param_collate(self) -> Optional["Charset"]:
        return self._param_collate


class CreateFunctionStatement(Statement):
    """CREATE FUNCTION 语句"""

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
        return self._definer

    @property
    def if_not_exists(self) -> bool:
        return self._if_not_exists

    @property
    def function_name(self) -> "Identifier":
        return self._function_name

    @property
    def param_list(self) -> List["FunctionParam"]:
        return self._param_list

    @property
    def return_type(self) -> "FieldType":
        return self._return_type

    @property
    def return_collate(self) -> Optional["Charset"]:
        return self._return_collate

    @property
    def option_list(self) -> List["FunctionOption"]:
        return self._option_list

    @property
    def body(self) -> "ProcessCommand":
        return self._body
