"""
ALTER TABLE 语句（alter table statement）
"""

from typing import List

from metasequoia_sql.ast.base import Node


class AlterTableCommand(Node):
    """ALTER TABLE 中的 ALTER 命令"""


class AlterTableDiscardTablespace(AlterTableCommand):
    """ALTER TABLE 命令：DISCARD TABLESPACE"""


class AlterTableImportTablespace(AlterTableCommand):
    """ALTER TABLE 命令：IMPORT TABLESPACE"""


class AlterTableAddPartition(AlterTableCommand):
    """ALTER TABLE 命令：ADD PARTITION"""

    __slots__ = (
        "_no_write_to_binlog"
    )

    def __init__(self, no_write_to_binlog: bool):
        self._no_write_to_binlog = no_write_to_binlog

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog


class AlterTableAddPartitionByDefinitionList(AlterTableCommand):
    """ALTER TABLE 命令：ADD PARTITION ( partition_definition_list )"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_definition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_definition_list: list):
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_definition_list = partition_definition_list

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def partition_definition_list(self) -> list:
        return self._partition_definition_list


class AlterTableAddPartitionByPartitionNum(AlterTableCommand):
    """ALTER TABLE 命令：ADD PARTITION PARTITIONS num_partition"""

    __slots__ = (
        "_no_write_to_binlog",
        "_num_partition"
    )

    def __init__(self, no_write_to_binlog: bool, num_partition: int):
        self._no_write_to_binlog = no_write_to_binlog
        self._num_partition = num_partition

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def num_partition(self) -> int:
        return self._num_partition


class AlterTableDropPartition(AlterTableCommand):
    """ALTER TABLE 命令：DROP PARTITION"""

    __slots__ = (
        "_partition_list"
    )

    def __init__(self, partition_list: List[str]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> List[str]:
        return self._partition_list
