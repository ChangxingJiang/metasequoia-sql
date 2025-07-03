"""
GET DIAGNOSTICS 语句（get diagnostics statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import (
        EnumDiagnosticsAreaType,
        EnumStatementInformationType,
        EnumConditionInformationType,
    )

__all__ = [
    "StatementInformationItem",
    "StatementInformation",
    "ConditionInformationItem",
    "ConditionInformation",
    "DiagnosticsInformation",
    "GetDiagnosticsStatement",
]


class StatementInformationItem(Node):
    """语句信息项"""

    __slots__ = ["_item_name", "_target_variable"]

    def __init__(self, item_name: "EnumStatementInformationType", target_variable: Expression):
        self._item_name = item_name
        self._target_variable = target_variable

    @property
    def item_name(self) -> "EnumStatementInformationType":
        """
        语句信息项名称

        Returns
        -------
        EnumStatementInformationType
            语句信息项名称
        """
        return self._item_name

    @property
    def target_variable(self) -> Expression:
        """
        目标变量

        Returns
        -------
        Expression
            目标变量
        """
        return self._target_variable


class StatementInformation(Node):
    """语句信息"""

    __slots__ = ["_statement_information_item_list"]

    def __init__(self, statement_information_item_list: List[StatementInformationItem]):
        self._statement_information_item_list = statement_information_item_list

    @property
    def statement_information_item_list(self) -> List[StatementInformationItem]:
        """
        语句信息项列表

        Returns
        -------
        List[StatementInformationItem]
            语句信息项列表
        """
        return self._statement_information_item_list


class ConditionInformationItem(Node):
    """条件信息项"""

    __slots__ = ["_item_name", "_target_variable"]

    def __init__(self, item_name: "EnumConditionInformationType", target_variable: Expression):
        self._item_name = item_name
        self._target_variable = target_variable

    @property
    def item_name(self) -> "EnumConditionInformationType":
        """
        条件信息项名称

        Returns
        -------
        EnumConditionInformationType
            条件信息项名称
        """
        return self._item_name

    @property
    def target_variable(self) -> Expression:
        """
        目标变量

        Returns
        -------
        Expression
            目标变量
        """
        return self._target_variable


class ConditionInformation(Node):
    """条件信息"""

    __slots__ = ["_condition_number", "_condition_information_item_list"]

    def __init__(self, condition_number: Expression, condition_information_item_list: List[ConditionInformationItem]):
        self._condition_number = condition_number
        self._condition_information_item_list = condition_information_item_list

    @property
    def condition_number(self) -> Expression:
        """
        条件编号

        Returns
        -------
        Expression
            条件编号
        """
        return self._condition_number

    @property
    def condition_information_item_list(self) -> List[ConditionInformationItem]:
        """
        条件信息项列表

        Returns
        -------
        List[ConditionInformationItem]
            条件信息项列表
        """
        return self._condition_information_item_list


class DiagnosticsInformation(Node):
    """诊断信息"""

    __slots__ = ["_statement_information", "_condition_information"]

    def __init__(self,
                 statement_information: Optional[StatementInformation] = None,
                 condition_information: Optional[ConditionInformation] = None):
        self._statement_information = statement_information
        self._condition_information = condition_information

    @property
    def statement_information(self) -> Optional[StatementInformation]:
        """
        语句信息

        Returns
        -------
        Optional[StatementInformation]
            语句信息
        """
        return self._statement_information

    @property
    def condition_information(self) -> Optional[ConditionInformation]:
        """
        条件信息

        Returns
        -------
        Optional[ConditionInformation]
            条件信息
        """
        return self._condition_information


class GetDiagnosticsStatement(Statement):
    """GET DIAGNOSTICS 语句"""

    __slots__ = ["_which_area", "_diagnostics_information"]

    def __init__(self,
                 which_area: "EnumDiagnosticsAreaType",
                 diagnostics_information: DiagnosticsInformation):
        self._which_area = which_area
        self._diagnostics_information = diagnostics_information

    @property
    def which_area(self) -> "EnumDiagnosticsAreaType":
        """
        诊断区域类型

        Returns
        -------
        EnumDiagnosticsAreaType
            诊断区域类型
        """
        return self._which_area

    @property
    def diagnostics_information(self) -> DiagnosticsInformation:
        """
        诊断信息

        Returns
        -------
        DiagnosticsInformation
            诊断信息
        """
        return self._diagnostics_information
