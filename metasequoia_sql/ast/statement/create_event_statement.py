"""
CREATE EVENT 语句（create event statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.phrase.schedule_time import ScheduleTime
    from metasequoia_sql.ast.basic.fixed_enum import EnumEventCompletionType, EnumEventStatusType
    from metasequoia_sql.ast.phrase.process_command import ProcessCommand

__all__ = [
    "CreateEventStatement",
]


class CreateEventStatement(Statement):
    """CREATE EVENT 语句"""

    __slots__ = (
        "_definer",
        "_if_not_exists",
        "_event_name",
        "_schedule_time",
        "_completion_type",
        "_event_status",
        "_event_comment",
        "_event_body",
    )

    def __init__(self,
                 definer: Optional["UserName"],
                 if_not_exists: bool,
                 event_name: "Identifier",
                 schedule_time: "ScheduleTime",
                 completion_type: Optional["EnumEventCompletionType"],
                 event_status: Optional["EnumEventStatusType"],
                 event_comment: Optional[str],
                 event_body: "ProcessCommand"):
        """
        初始化 CREATE EVENT 语句

        Parameters
        ----------
        definer : Optional[UserName]
            定义者子句，指定事件的创建者
        if_not_exists : bool
            是否使用 IF NOT EXISTS 选项
        event_name : Identifier
            事件名称标识符
        schedule_time : ScheduleTime
            事件调度时间
        completion_type : Optional[EnumEventCompletionType]
            事件完成类型，如果为 None 则使用默认值
        event_status : Optional[EnumEventStatusType]
            事件状态，如果为 None 则使用默认值
        event_comment : Optional[str]
            事件注释，如果为 None 则表示无注释
        event_body : ProcessCommand
            事件执行体
        """
        self._definer = definer
        self._if_not_exists = if_not_exists
        self._event_name = event_name
        self._schedule_time = schedule_time
        self._completion_type = completion_type
        self._event_status = event_status
        self._event_comment = event_comment
        self._event_body = event_body

    @property
    def definer(self) -> Optional["UserName"]:
        return self._definer

    @property
    def if_not_exists(self) -> bool:
        return self._if_not_exists

    @property
    def event_name(self) -> "Identifier":
        return self._event_name

    @property
    def schedule_time(self) -> "ScheduleTime":
        return self._schedule_time

    @property
    def completion_type(self) -> Optional["EnumEventCompletionType"]:
        return self._completion_type

    @property
    def event_status(self) -> Optional["EnumEventStatusType"]:
        return self._event_status

    @property
    def event_comment(self) -> Optional[str]:
        return self._event_comment

    @property
    def event_body(self) -> "ProcessCommand":
        return self._event_body
