"""
SIGNAL/RESIGNAL 语句（signal or resignal statement）
"""

from typing import List, Optional, TYPE_CHECKING, Union

from metasequoia_sql.ast.base import Expression, Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumSignalConditionType
    from metasequoia_sql.ast.phrase.sql_state import SqlState

__all__ = [
    "SignalInformation",
    "SignalStatement",
    "ResignalStatement"
]


class SignalInformation(Node):
    """
    SIGNAL/RESIGNAL 语句中的信息项的抽象语法树节点。

    语法规则：
        signal_condition_information_item_name = signal_allowed_expr
    """

    __slots__ = (
        "_item_name",
        "_item_value"
    )

    def __init__(self, item_name: "EnumSignalConditionType", item_value: Expression) -> None:
        """
        初始化信号信息项节点。

        Parameters
        ----------
        item_name : EnumSignalConditionType
            信息项名称
        item_value : Expression
            信息项值
        """
        self._item_name = item_name
        self._item_value = item_value

    @property
    def item_name(self) -> "EnumSignalConditionType":
        """
        获取信息项名称。

        Returns
        -------
        EnumSignalConditionType
            信息项名称
        """
        return self._item_name

    @property
    def item_value(self) -> Expression:
        """
        获取信息项值。

        Returns
        -------
        Expression
            信息项值
        """
        return self._item_value


class SignalStatement(Statement):
    """
    SIGNAL 语句的抽象语法树节点。

    语法规则：
        SIGNAL signal_value [SET signal_information_item_list]
    """

    __slots__ = (
        "_signal_value",
        "_information_items"
    )

    def __init__(self,
                 signal_value: Union[str, "SqlState"],
                 information_items: List[SignalInformation]) -> None:
        """
        初始化 SIGNAL 语句节点。

        Parameters
        ----------
        signal_value : Union[str, SqlState]
            信号值，可以是条件名称或SQL状态
        information_items : Optional[List[SignalInformationItem]], optional
            信息项列表，默认为 None
        """
        self._signal_value = signal_value
        self._information_items = information_items

    @property
    def signal_value(self) -> Union[str, "SqlState"]:
        """
        获取信号值。

        Returns
        -------
        Union[str, SqlState]
            信号值
        """
        return self._signal_value

    @property
    def information_items(self) -> List[SignalInformation]:
        """
        获取信息项列表。

        Returns
        -------
        List[SignalInformation]
            信息项列表
        """
        return self._information_items


class ResignalStatement(Statement):
    """
    RESIGNAL 语句的抽象语法树节点。

    语法规则：
        RESIGNAL [signal_value] [SET signal_information_item_list]
    """

    __slots__ = (
        "_signal_value",
        "_information_items"
    )

    def __init__(self,
                 signal_value: Optional[Union[str, "SqlState"]],
                 information_items: List[SignalInformation]) -> None:
        """
        初始化 RESIGNAL 语句节点。

        Parameters
        ----------
        signal_value : Optional[Union[str, SqlState]], optional
            信号值，可以是条件名称或SQL状态，默认为 None
        information_items : Optional[List[SignalInformationItem]], optional
            信息项列表，默认为 None
        """
        self._signal_value = signal_value
        self._information_items = information_items

    @property
    def signal_value(self) -> Optional[Union[str, "SqlState"]]:
        """
        获取信号值。

        Returns
        -------
        Optional[Union[str, SqlState]]
            信号值
        """
        return self._signal_value

    @property
    def information_items(self) -> List[SignalInformation]:
        """
        获取信息项列表。

        Returns
        -------
        List[SignalInformation]
            信息项列表
        """
        return self._information_items
