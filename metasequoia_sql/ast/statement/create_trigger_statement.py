"""
CREATE TRIGGER 语句（create trigger statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumTriggerActionTimeType, EnumTriggerEventType, \
        EnumTriggerActionOrderType
    from metasequoia_sql.ast.phrase.process_command import ProcessCommand
    from metasequoia_sql.ast.basic.literal import UserName

__all__ = [
    "TriggerFollowsPrecedesClause",
    "CreateTriggerStatement"
]


class TriggerFollowsPrecedesClause(Node):
    """
    触发器 FOLLOWS/PRECEDES 子句
    
    Parameters
    ----------
    ordering_clause : Optional[EnumTriggerActionOrderType]
        触发器顺序类型，None 表示没有指定顺序
    anchor_trigger_name : Optional[str]
        锚点触发器名称，当指定了顺序时的参考触发器名称
    """

    __slots__ = ("_ordering_clause", "_anchor_trigger_name")

    def __init__(self,
                 ordering_clause: Optional["EnumTriggerActionOrderType"],
                 anchor_trigger_name: Optional[str]):
        self._ordering_clause = ordering_clause
        self._anchor_trigger_name = anchor_trigger_name

    @property
    def ordering_clause(self) -> Optional["EnumTriggerActionOrderType"]:
        """
        触发器顺序类型

        Returns
        -------
        Optional["EnumTriggerActionOrderType"]
            触发器顺序类型
        """
        return self._ordering_clause

    @property
    def anchor_trigger_name(self) -> Optional[str]:
        """
        锚点触发器名称

        Returns
        -------
        Optional[str]
            锚点触发器名称
        """
        return self._anchor_trigger_name


class CreateTriggerStatement(Statement):
    # pylint: disable=R0902
    """
    CREATE TRIGGER 语句
    
    Parameters
    ----------
    definer : Optional[UserName]
        定义者用户名，可选
    if_not_exists : bool
        是否包含 IF NOT EXISTS 子句
    trigger_name : Identifier
        触发器名称
    action_time : EnumTriggerActionTimeType
        触发器动作时间（BEFORE/AFTER）
    trigger_event : EnumTriggerEventType
        触发器事件类型（INSERT/UPDATE/DELETE）
    table_ident : Identifier
        表标识符
    follows_precedes_clause : TriggerFollowsPrecedesClause
        FOLLOWS/PRECEDES 子句
    trigger_body : ProcessCommand
        触发器体（存储过程语句）
    """

    __slots__ = ("_definer", "_if_not_exists", "_trigger_name", "_action_time",
                 "_trigger_event", "_table_ident", "_follows_precedes_clause", "_trigger_body")

    def __init__(self,
                 definer: Optional["UserName"],
                 if_not_exists: bool,
                 trigger_name: "Identifier",
                 action_time: "EnumTriggerActionTimeType",
                 trigger_event: "EnumTriggerEventType",
                 table_ident: "Identifier",
                 follows_precedes_clause: TriggerFollowsPrecedesClause,
                 trigger_body: "ProcessCommand"):
        # pylint: disable=R0913
        self._definer = definer
        self._if_not_exists = if_not_exists
        self._trigger_name = trigger_name
        self._action_time = action_time
        self._trigger_event = trigger_event
        self._table_ident = table_ident
        self._follows_precedes_clause = follows_precedes_clause
        self._trigger_body = trigger_body

    @property
    def definer(self) -> Optional["UserName"]:
        """
        触发器定义者

        Returns
        -------
        Optional["UserName"]
            触发器定义者用户名
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
    def trigger_name(self) -> "Identifier":
        """
        触发器名称标识符

        Returns
        -------
        Identifier
            触发器名称标识符
        """
        return self._trigger_name

    @property
    def action_time(self) -> "EnumTriggerActionTimeType":
        """
        触发器动作时间

        Returns
        -------
        EnumTriggerActionTimeType
            触发器动作时间（BEFORE/AFTER）
        """
        return self._action_time

    @property
    def trigger_event(self) -> "EnumTriggerEventType":
        """
        触发器事件类型

        Returns
        -------
        EnumTriggerEventType
            触发器事件类型（INSERT/UPDATE/DELETE）
        """
        return self._trigger_event

    @property
    def table_ident(self) -> "Identifier":
        """
        表标识符

        Returns
        -------
        Identifier
            表标识符
        """
        return self._table_ident

    @property
    def follows_precedes_clause(self) -> TriggerFollowsPrecedesClause:
        """
        FOLLOWS/PRECEDES 子句

        Returns
        -------
        TriggerFollowsPrecedesClause
            FOLLOWS/PRECEDES 子句
        """
        return self._follows_precedes_clause

    @property
    def trigger_body(self) -> "ProcessCommand":
        """
        触发器执行体

        Returns
        -------
        ProcessCommand
            触发器执行体
        """
        return self._trigger_body
