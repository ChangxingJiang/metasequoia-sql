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
        """
        参数模式

        Returns
        -------
        EnumProcedureParamMode
            参数模式（IN、OUT、INOUT）
        """
        return self._param_mode

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
        # pylint: disable=R0913,R0917
        self._definer = definer
        self._if_not_exists = if_not_exists
        self._procedure_name = procedure_name
        self._param_list = param_list
        self._option_list = option_list
        self._body = body

    @property
    def definer(self) -> Optional["UserName"]:
        """
        存储过程定义者

        Returns
        -------
        Optional["UserName"]
            存储过程定义者用户名
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
    def procedure_name(self) -> Optional["Identifier"]:
        """
        存储过程名称标识符

        Returns
        -------
        Optional["Identifier"]
            存储过程名称标识符
        """
        return self._procedure_name

    @property
    def param_list(self) -> List["ProcedureParam"]:
        """
        存储过程参数列表

        Returns
        -------
        List["ProcedureParam"]
            存储过程参数列表
        """
        return self._param_list

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
    def body(self) -> Optional["ProcessCommand"]:
        """
        存储过程执行体

        Returns
        -------
        Optional["ProcessCommand"]
            存储过程执行体
        """
        return self._body
