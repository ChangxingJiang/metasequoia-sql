"""
SET RESOURCE GROUP 语句（set resource group statement）
"""

from typing import List, Optional

from metasequoia_sql.ast.base import Statement

__all__ = [
    "SetResourceGroupStatement",
]


class SetResourceGroupStatement(Statement):
    """SET RESOURCE GROUP 语句

    语法：
    SET RESOURCE GROUP resource_group_name
    SET RESOURCE GROUP resource_group_name FOR thread_id_list
    """

    __slots__ = ["_resource_group_name", "_thread_id_list"]

    def __init__(self, resource_group_name: str, thread_id_list: Optional[List[int]]):
        self._resource_group_name = resource_group_name
        self._thread_id_list = thread_id_list

    @property
    def resource_group_name(self) -> str:
        return self._resource_group_name

    @property
    def thread_id_list(self) -> List[int]:
        return self._thread_id_list
