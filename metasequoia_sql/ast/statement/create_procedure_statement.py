"""
CREATE PROCEDURE 语句（create procedure statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.basic.fixed_enum import EnumProcedureParamMode
    from metasequoia_sql.ast.phrase.field_type import FieldType
    from metasequoia_sql.ast.phrase.function_option import FunctionOption
    from metasequoia_sql.ast.phrase.process_command import ProcessCommand
    from metasequoia_sql.ast.basic.charset_name import Charset

__all__ = [
    "ProcedureParam",
    "CreateProcedureStatement",
]


class ProcedureParam(Node):
    """存储过程参数"""

    __slots__ = (
        "_param_mode",
        "_param_name",
        "_param_type",
        "_param_collate",
    )

    def __init__(
            self,
            param_mode: "EnumProcedureParamMode",
            param_name: str,
            param_type: "FieldType",
            param_collate: Optional["Charset"] = None,
    ):
        self._param_mode = param_mode
        self._param_name = param_name
        self._param_type = param_type
        self._param_collate = param_collate

    @property
    def param_mode(self) -> "EnumProcedureParamMode":
        return self._param_mode

    @property
    def param_name(self) -> str:
        return self._param_name

    @property
    def param_type(self) -> "FieldType":
        return self._param_type

    @property
    def param_collate(self) -> Optional["Charset"]:
        return self._param_collate


class CreateProcedureStatement(Statement):
    """CREATE PROCEDURE 语句"""

    __slots__ = (
        "_definer",
        "_if_not_exists",
        "_procedure_name",
        "_param_list",
        "_option_list",
        "_body",
    )

    def __init__(
            self,
            definer: Optional["UserName"],
            if_not_exists: bool,
            procedure_name: "Identifier",
            param_list: List["ProcedureParam"],
            option_list: List["FunctionOption"],
            body: "ProcessCommand",
    ):
        self._definer = definer
        self._if_not_exists = if_not_exists
        self._procedure_name = procedure_name
        self._param_list = param_list
        self._option_list = option_list
        self._body = body

    @property
    def definer(self) -> Optional["UserName"]:
        return self._definer

    @property
    def if_not_exists(self) -> bool:
        return self._if_not_exists

    @property
    def procedure_name(self) -> Optional["Identifier"]:
        return self._procedure_name

    @property
    def param_list(self) -> List["ProcedureParam"]:
        return self._param_list

    @property
    def option_list(self) -> List["FunctionOption"]:
        return self._option_list

    @property
    def body(self) -> Optional["ProcessCommand"]:
        return self._body
