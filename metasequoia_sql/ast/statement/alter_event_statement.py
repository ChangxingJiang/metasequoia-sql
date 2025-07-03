"""
ALTER EVENT 语句（alter event statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.schedule_time import ScheduleTime
    from metasequoia_sql.ast.basic.fixed_enum import EnumEventCompletionType, EnumEventStatusType
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.phrase.process_command import ProcessCommand

__all__ = [
    "AlterEventStatement",
]


class AlterEventStatement(Statement):
    # pylint: disable=R0902
    """ALTER EVENT 语句"""

    __slots__ = (
        "_definer",
        "_event_name",
        "_schedule_time",
        "_completion_type",
        "_event_rename",
        "_event_status",
        "_event_comment",
        "_process_command",
    )

    def __init__(self,
                 definer: Optional["UserName"],
                 event_name: "Identifier",
                 schedule_time: Optional["ScheduleTime"],
                 completion_type: Optional["EnumEventCompletionType"],
                 event_rename: Optional["Identifier"],
                 event_status: Optional["EnumEventStatusType"],
                 event_comment: Optional[str],
                 process_command: Optional["ProcessCommand"]):
        # pylint: disable=R0913,R0917
        """
        初始化 ALTER EVENT 语句

        Parameters
        ----------
        definer : Optional[UserName]
            定义者子句
        event_name : Identifier
            事件名称
        schedule_time : Optional[ScheduleTime]
            调度时间，如果为 None 则表示不修改调度时间
        completion_type : Optional[EnumEventCompletionType]
            完成类型，如果为 None 则表示不修改完成类型
        event_rename : Optional[Identifier]
            事件重命名，如果为 None 则表示不重命名
        event_status : Optional[EnumEventStatusType]
            事件状态，如果为 None 则表示不修改状态
        event_comment : Optional[str]
            事件注释，如果为 None 则表示不修改注释
        process_command : Optional[ProcessCommand]
            事件执行的 SQL 语句，如果为 None 则表示不修改
        """
        self._definer = definer
        self._event_name = event_name
        self._schedule_time = schedule_time
        self._completion_type = completion_type
        self._event_rename = event_rename
        self._event_status = event_status
        self._event_comment = event_comment
        self._process_command = process_command

    @property
    def definer(self) -> Optional["UserName"]:
        """
        定义者子句

        Returns
        -------
        Optional[UserName]
            定义者子句，如果为 None 则表示使用当前用户
        """
        return self._definer

    @property
    def event_name(self) -> "Identifier":
        """
        事件名称

        Returns
        -------
        Identifier
            事件名称
        """
        return self._event_name

    @property
    def schedule_time(self) -> Optional["ScheduleTime"]:
        """
        调度时间

        Returns
        -------
        Optional[ScheduleTime]
            调度时间，如果为 None 则表示不修改调度时间
        """
        return self._schedule_time

    @property
    def completion_type(self) -> Optional["EnumEventCompletionType"]:
        """
        完成类型

        Returns
        -------
        Optional[EnumEventCompletionType]
            完成类型，如果为 None 则表示不修改完成类型
        """
        return self._completion_type

    @property
    def event_rename(self) -> Optional["Identifier"]:
        """
        事件重命名

        Returns
        -------
        Optional[Identifier]
            事件重命名，如果为 None 则表示不重命名
        """
        return self._event_rename

    @property
    def event_status(self) -> Optional["EnumEventStatusType"]:
        """
        事件状态

        Returns
        -------
        Optional[EnumEventStatusType]
            事件状态，如果为 None 则表示不修改状态
        """
        return self._event_status

    @property
    def event_comment(self) -> Optional[str]:
        """
        事件注释

        Returns
        -------
        Optional[str]
            事件注释，如果为 None 则表示不修改注释
        """
        return self._event_comment

    @property
    def process_command(self) -> Optional["ProcessCommand"]:
        """
        事件执行的 SQL 语句

        Returns
        -------
        Optional[ProcessCommand]
            事件执行的 SQL 语句，如果为 None 则表示不修改
        """
        return self._process_command
