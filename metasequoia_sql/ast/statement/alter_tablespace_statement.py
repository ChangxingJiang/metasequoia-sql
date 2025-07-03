"""
ALTER TABLESPACE 语句（alter tablespace statement）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "EnumAlterTablespaceActionType",
    "AlterTablespaceStatement",
]


class EnumAlterTablespaceActionType(IntEnum):
    """ALTER TABLESPACE 语句的操作类型"""

    ADD = 1
    DROP = 2
    RENAME = 3
    ALTER = 4


class AlterTablespaceStatement(Statement):
    """ALTER TABLESPACE 语句"""

    __slots__ = ["_tablespace_name", "_action_type", "_datafile", "_target_name", "_option_list"]

    def __init__(self,
                 tablespace_name: str,
                 action_type: EnumAlterTablespaceActionType,
                 datafile: Optional[str] = None,
                 target_name: Optional[str] = None,
                 option_list: Optional[List["DdlOption"]] = None):
        # pylint: disable=R0913,R0917
        self._tablespace_name = tablespace_name
        self._action_type = action_type  # ADD, DROP, RENAME, ALTER
        self._datafile = datafile
        self._target_name = target_name  # for RENAME operation
        self._option_list = option_list if option_list is not None else []

    @property
    def tablespace_name(self) -> str:
        """
        表空间名称

        Returns
        -------
        str
            表空间名称
        """
        return self._tablespace_name

    @property
    def action_type(self) -> EnumAlterTablespaceActionType:
        """
        操作类型

        Returns
        -------
        EnumAlterTablespaceActionType
            操作类型（ADD、DROP、RENAME、ALTER）
        """
        return self._action_type

    @property
    def datafile(self) -> Optional[str]:
        """
        数据文件路径

        Returns
        -------
        Optional[str]
            数据文件路径
        """
        return self._datafile

    @property
    def target_name(self) -> Optional[str]:
        """
        目标名称

        Returns
        -------
        Optional[str]
            目标名称（用于重命名操作）
        """
        return self._target_name

    @property
    def option_list(self) -> List["DdlOption"]:
        """
        DDL 选项列表

        Returns
        -------
        List["DdlOption"]
            DDL 选项列表
        """
        return self._option_list
