# pylint: disable=C0302

"""
修改命令（alter command）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumCheckType, EnumRepairType, EnumDropRestrict
    from metasequoia_sql.ast.clause.ddl_partition_by_clause import PartitionDefinition, DdlPartitionByClause
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOptionWithValidation
    from metasequoia_sql.ast.phrase.ddl_table_element import FieldDefinition, TableElement
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.clause.order_by_clause import OrderExpression
    from metasequoia_sql.ast.base import Expression

__all__ = [
    # 抽象基类
    "AlterCommand",

    # 修改命令具体类型
    "AlterDiscardTablespace",
    "AlterImportTablespace",
    "AlterAddPartition",
    "AlterAddPartitionByDefinitionList",
    "AlterAddPartitionByPartitionNum",
    "AlterDropPartition",
    "AlterRebuildPartition",
    "AlterOptimizePartition",
    "AlterAnalyzePartition",
    "AlterCheckPartition",
    "AlterRepairPartition",
    "AlterCoalescePartition",
    "AlterTruncatePartition",
    "AlterReorganizePartition",
    "AlterReorganizePartitionInto",
    "AlterExchangePartition",
    "AlterDiscardPartitionTablespace",
    "AlterImportPartitionTablespace",
    "AlterSecondaryLoad",
    "AlterSecondaryUnload",
    "AlterAddColumn",
    "AlterAddColumns",
    "AlterAddConstraint",
    "AlterChangeColumn",
    "AlterModifyColumn",
    "AlterDropColumn",
    "AlterDropForeignKey",
    "AlterDropPrimaryKey",
    "AlterDropKey",
    "AlterDropCheckConstraint",
    "AlterDropConstraint",
    "AlterDisableKeys",
    "AlterEnableKeys",
    "AlterSetDefaultValue",
    "AlterSetDefaultExpression",
    "AlterDropDefault",
    "AlterSetColumnVisibility",
    "AlterSetIndexVisibility",
    "AlterEnforceCheckConstraint",
    "AlterEnforceConstraint",
    "AlterRenameTable",
    "AlterRenameKey",
    "AlterRenameColumn",
    "AlterConvertToCharset",
    "AlterConvertToDefaultCharset",
    "AlterForce",
    "AlterOrderBy",
    "AlterPartitionBy",
    "AlterRemovePartitioning",

    # 修改位置元素
    "AlterPlace",
    "AlterPlaceAfter",
    "AlterPlaceFirst",
    "AlterPlaceDefault",
]


class AlterCommand(Node):
    """ALTER TABLE 中的 ALTER 命令"""


class AlterDiscardTablespace(AlterCommand):
    """ALTER TABLE 命令：DISCARD TABLESPACE"""


class AlterImportTablespace(AlterCommand):
    """ALTER TABLE 命令：IMPORT TABLESPACE"""


class AlterAddPartition(AlterCommand):
    """ALTER TABLE 命令：ADD PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
    )

    def __init__(self, no_write_to_binlog: bool):
        """
        初始化 ADD PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        """
        self._no_write_to_binlog = no_write_to_binlog

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog


class AlterAddPartitionByDefinitionList(AlterCommand):
    """ALTER TABLE 命令：ADD PARTITION ( partition_definition_list )"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: List["PartitionDefinition"]):
        """
        初始化 ADD PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        partition_list : List[PartitionDefinition]
            分区定义列表
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> List["PartitionDefinition"]:
        """
        获取分区定义列表。

        Returns
        -------
        List[PartitionDefinition]
            分区定义列表
        """
        return self._partition_list


class AlterAddPartitionByPartitionNum(AlterCommand):
    """ALTER TABLE 命令：ADD PARTITION PARTITIONS num_partition"""

    __slots__ = (
        "_no_write_to_binlog",
        "_num_partition"
    )

    def __init__(self, no_write_to_binlog: bool, num_partition: int):
        """
        初始化 ADD PARTITION PARTITIONS 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        num_partition : int
            分区数量
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._num_partition = num_partition

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def num_partition(self) -> int:
        """
        获取分区数量。

        Returns
        -------
        int
            分区数量
        """
        return self._num_partition


class AlterDropPartition(AlterCommand):
    """ALTER TABLE 命令：DROP PARTITION"""

    __slots__ = (
        "_partition_list",
    )

    def __init__(self, partition_list: List[str]):
        """
        初始化 DROP PARTITION 命令。

        Parameters
        ----------
        partition_list : List[str]
            要删除的分区列表
        """
        self._partition_list = partition_list

    @property
    def partition_list(self) -> List[str]:
        """
        获取要删除的分区列表。

        Returns
        -------
        List[str]
            要删除的分区列表
        """
        return self._partition_list


class AlterRebuildPartition(AlterCommand):
    """ALTER TABLE 命令：REBUILD PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]]):
        """
        初始化 REBUILD PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        partition_list : Optional[List[str]]
            分区列表
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取分区列表。

        Returns
        -------
        Optional[List[str]]
            分区列表
        """
        return self._partition_list


class AlterOptimizePartition(AlterCommand):
    """ALTER TABLE 命令：OPTIMIZE PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]]):
        """
        初始化 ANALYZE PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        partition_list : Optional[List[str]]
            分区列表
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取分区列表。

        Returns
        -------
        Optional[List[str]]
            分区列表
        """
        return self._partition_list


class AlterAnalyzePartition(AlterCommand):
    """ALTER TABLE 命令：ANALYZE PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]]):
        """
        初始化 OPTIMIZE PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        partition_list : Optional[List[str]]
            分区列表
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取分区列表。

        Returns
        -------
        Optional[List[str]]
            分区列表
        """
        return self._partition_list


class AlterCheckPartition(AlterCommand):
    """ALTER TABLE 命令：CHECK PARTITION"""

    __slots__ = (
        "_partition_list",
        "_check_type",
    )

    def __init__(self, partition_list: Optional[List[str]], check_type: "EnumCheckType"):
        """
        初始化 CHECK PARTITION 命令。

        Parameters
        ----------
        partition_list : Optional[List[str]]
            分区列表
        check_type : EnumCheckType
            检查类型
        """
        self._partition_list = partition_list
        self._check_type = check_type

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取分区列表。

        Returns
        -------
        Optional[List[str]]
            分区列表
        """
        return self._partition_list

    @property
    def check_type(self) -> "EnumCheckType":
        """
        获取检查类型。

        Returns
        -------
        EnumCheckType
            检查类型
        """
        return self._check_type


class AlterRepairPartition(AlterCommand):
    """ALTER TABLE 命令：REPAIR PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list",
        "_repair_type",
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]], repair_type: "EnumRepairType"):
        """
        初始化 REPAIR PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        partition_list : Optional[List[str]]
            分区列表
        repair_type : EnumRepairType
            修复类型
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list
        self._repair_type = repair_type

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取分区列表。

        Returns
        -------
        Optional[List[str]]
            分区列表
        """
        return self._partition_list

    @property
    def repair_type(self) -> "EnumRepairType":
        """
        获取修复类型。

        Returns
        -------
        EnumRepairType
            修复类型
        """
        return self._repair_type


class AlterCoalescePartition(AlterCommand):
    """ALTER TABLE 命令：COALESCE PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_num_partition"
    )

    def __init__(self, no_write_to_binlog: bool, num_partition: int):
        """
        初始化 COALESCE PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        num_partition : int
            分区数量
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._num_partition = num_partition

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def num_partition(self) -> int:
        """
        获取分区数量。

        Returns
        -------
        int
            分区数量
        """
        return self._num_partition


class AlterTruncatePartition(AlterCommand):
    """ALTER TABLE 命令：TRUNCATE PARTITION"""

    __slots__ = (
        "_partition_list",
    )

    def __init__(self, partition_list: Optional[List[str]]):
        """
        初始化 TRUNCATE PARTITION 命令。

        Parameters
        ----------
        partition_list : Optional[List[str]]
            要截断的分区列表
        """
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取要截断的分区列表。

        Returns
        -------
        Optional[List[str]]
            要截断的分区列表
        """
        return self._partition_list


class AlterReorganizePartition(AlterCommand):
    """ALTER TABLE 命令：REORGANIZE PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
    )

    def __init__(self, no_write_to_binlog: bool):
        """
        初始化 REORGANIZE PARTITION 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        """
        self._no_write_to_binlog = no_write_to_binlog

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog


class AlterReorganizePartitionInto(AlterCommand):
    """ALTER TABLE 命令：REORGANIZE PARTITION partition_list INTO ( partition_definition_list )"""

    __slots__ = (
        "_no_write_to_binlog",
        "_source_partition_list",
        "_target_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, source_partition_list: List[str],
                 target_partition_list: List["PartitionDefinition"]):
        """
        初始化 REORGANIZE PARTITION INTO 命令。

        Parameters
        ----------
        no_write_to_binlog : bool
            是否不写入二进制日志
        source_partition_list : List[str]
            源分区列表
        target_partition_list : List[PartitionDefinition]
            目标分区定义列表
        """
        self._no_write_to_binlog = no_write_to_binlog
        self._source_partition_list = source_partition_list
        self._target_partition_list = target_partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        """
        获取是否不写入二进制日志的标识。

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def source_partition_list(self) -> List[str]:
        """
        获取源分区列表。

        Returns
        -------
        List[str]
            源分区列表
        """
        return self._source_partition_list

    @property
    def target_partition_list(self) -> List["PartitionDefinition"]:
        """
        获取目标分区定义列表。

        Returns
        -------
        List[PartitionDefinition]
            目标分区定义列表
        """
        return self._target_partition_list


class AlterExchangePartition(AlterCommand):
    """ALTER TABLE 命令：EXCHANGE PARTITION"""

    __slots__ = (
        "_partition_name",
        "_table",
        "_with_validation"
    )

    def __init__(self, partition_name: str, table: "Identifier", with_validation: "AlterOptionWithValidation"):
        """
        初始化 EXCHANGE PARTITION 命令。

        Parameters
        ----------
        partition_name : str
            分区名称
        table : Identifier
            要交换的表
        with_validation : AlterOptionWithValidation
            验证选项
        """
        self._partition_name = partition_name
        self._table = table
        self._with_validation = with_validation

    @property
    def partition_name(self) -> str:
        """
        获取分区名称。

        Returns
        -------
        str
            分区名称
        """
        return self._partition_name

    @property
    def table(self) -> "Identifier":
        """
        获取要交换的表。

        Returns
        -------
        Identifier
            要交换的表
        """
        return self._table

    @property
    def with_validation(self) -> "AlterOptionWithValidation":
        """
        获取验证选项。

        Returns
        -------
        AlterOptionWithValidation
            验证选项
        """
        return self._with_validation


class AlterDiscardPartitionTablespace(AlterCommand):
    """ALTER TABLE 命令：DISCARD PARTITION partition_list TABLESPACE"""

    __slots__ = (
        "_partition_list",
    )

    def __init__(self, partition_list: Optional[List[str]]):
        """
        初始化 DISCARD PARTITION TABLESPACE 命令。

        Parameters
        ----------
        partition_list : Optional[List[str]]
            要丢弃表空间的分区列表
        """
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取要丢弃表空间的分区列表。

        Returns
        -------
        Optional[List[str]]
            要丢弃表空间的分区列表
        """
        return self._partition_list


class AlterImportPartitionTablespace(AlterCommand):
    """ALTER TABLE 命令：IMPORT PARTITION partition_list TABLESPACE"""

    __slots__ = (
        "_partition_list",
    )

    def __init__(self, partition_list: Optional[List[str]]):
        """
        初始化 IMPORT PARTITION TABLESPACE 命令。

        Parameters
        ----------
        partition_list : Optional[List[str]]
            要导入表空间的分区列表
        """
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        获取要导入表空间的分区列表。

        Returns
        -------
        Optional[List[str]]
            要导入表空间的分区列表
        """
        return self._partition_list


class AlterSecondaryLoad(AlterCommand):
    """ALTER TABLE 命令：SECONDARY_LOAD"""


class AlterSecondaryUnload(AlterCommand):
    """ALTER TABLE 命令：SECONDARY_UNLOAD"""


class AlterPlace(Node):
    """字段位置子句基类"""


class AlterPlaceDefault(AlterPlace):
    """默认位置（不指定位置）"""


class AlterPlaceAfter(AlterPlace):
    """在指定字段之后"""

    __slots__ = ("_column_name",)

    def __init__(self, column_name: str):
        """
        初始化 AFTER 位置子句。

        Parameters
        ----------
        column_name : str
            字段名称
        """
        self._column_name = column_name

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name


class AlterPlaceFirst(AlterPlace):
    """在第一个位置"""


class AlterAddColumn(AlterCommand):
    """ALTER TABLE 命令：ADD COLUMN column_name field_definition"""

    __slots__ = ["_column_name", "_field_definition", "_place"]

    def __init__(self, column_name: str, field_definition: "FieldDefinition", place: AlterPlace):
        """
        初始化 ADD COLUMN 命令。

        Parameters
        ----------
        column_name : str
            字段名称
        field_definition : FieldDefinition
            字段定义
        place : AlterPlace
            位置信息
        """
        self._column_name = column_name
        self._field_definition = field_definition
        self._place = place

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name

    @property
    def field_definition(self) -> "FieldDefinition":
        """
        获取字段定义。

        Returns
        -------
        FieldDefinition
            字段定义
        """
        return self._field_definition

    @property
    def place(self) -> AlterPlace:
        """
        获取位置信息。

        Returns
        -------
        AlterPlace
            位置信息
        """
        return self._place


class AlterAddColumns(AlterCommand):
    """ALTER TABLE 命令：ADD ( table_element_list )"""

    __slots__ = ["_table_element_list"]

    def __init__(self, table_element_list: List["TableElement"]):
        """
        初始化 ADD COLUMNS 命令。

        Parameters
        ----------
        table_element_list : List[TableElement]
            表元素列表
        """
        self._table_element_list = table_element_list

    @property
    def table_element_list(self) -> List["TableElement"]:
        """
        获取表元素列表。

        Returns
        -------
        List[TableElement]
            表元素列表
        """
        return self._table_element_list


class AlterAddConstraint(AlterCommand):
    """ALTER TABLE 命令：ADD constraint_definition"""

    __slots__ = ["_constraint_definition"]

    def __init__(self, constraint_definition: "TableElement"):
        """
        初始化 ADD CONSTRAINT 命令。

        Parameters
        ----------
        constraint_definition : TableElement
            约束定义
        """
        self._constraint_definition = constraint_definition

    @property
    def constraint_definition(self) -> "TableElement":
        """
        获取约束定义。

        Returns
        -------
        TableElement
            约束定义
        """
        return self._constraint_definition


class AlterChangeColumn(AlterCommand):
    """ALTER TABLE 命令：CHANGE COLUMN old_name new_name field_definition"""

    __slots__ = ["_old_column_name", "_new_column_name", "_field_definition", "_place"]

    def __init__(self, old_column_name: str, new_column_name: str, field_definition: "FieldDefinition",
                 place: AlterPlace):
        # pylint: disable=R0913
        """
        初始化 CHANGE COLUMN 命令。

        Parameters
        ----------
        old_column_name : str
            旧字段名称
        new_column_name : str
            新字段名称
        field_definition : FieldDefinition
            字段定义
        place : AlterPlace
            位置信息
        """
        self._old_column_name = old_column_name
        self._new_column_name = new_column_name
        self._field_definition = field_definition
        self._place = place

    @property
    def old_column_name(self) -> str:
        """
        获取旧字段名称。

        Returns
        -------
        str
            旧字段名称
        """
        return self._old_column_name

    @property
    def new_column_name(self) -> str:
        """
        获取新字段名称。

        Returns
        -------
        str
            新字段名称
        """
        return self._new_column_name

    @property
    def field_definition(self) -> "FieldDefinition":
        """
        获取字段定义。

        Returns
        -------
        FieldDefinition
            字段定义
        """
        return self._field_definition

    @property
    def place(self) -> AlterPlace:
        """
        获取位置信息。

        Returns
        -------
        AlterPlace
            位置信息
        """
        return self._place


class AlterModifyColumn(AlterCommand):
    """ALTER TABLE 命令：MODIFY COLUMN column_name field_definition"""

    __slots__ = ["_column_name", "_field_definition", "_place"]

    def __init__(self, column_name: str, field_definition: "FieldDefinition", place: AlterPlace):
        """
        初始化 MODIFY COLUMN 命令。

        Parameters
        ----------
        column_name : str
            字段名称
        field_definition : FieldDefinition
            字段定义
        place : AlterPlace
            位置信息
        """
        self._column_name = column_name
        self._field_definition = field_definition
        self._place = place

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name

    @property
    def field_definition(self) -> "FieldDefinition":
        """
        获取字段定义。

        Returns
        -------
        FieldDefinition
            字段定义
        """
        return self._field_definition

    @property
    def place(self) -> AlterPlace:
        """
        获取位置信息。

        Returns
        -------
        AlterPlace
            位置信息
        """
        return self._place


class AlterDropColumn(AlterCommand):
    """ALTER TABLE 命令：DROP COLUMN column_name"""

    __slots__ = ["_column_name", "_drop_restrict"]

    def __init__(self, column_name: str, drop_restrict: "EnumDropRestrict"):
        """
        初始化 DROP COLUMN 命令。

        Parameters
        ----------
        column_name : str
            字段名称
        drop_restrict : EnumDropRestrict
            删除限制类型
        """
        self._column_name = column_name
        self._drop_restrict = drop_restrict

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name

    @property
    def drop_restrict(self) -> "EnumDropRestrict":
        """
        获取删除限制类型。

        Returns
        -------
        EnumDropRestrict
            删除限制类型
        """
        return self._drop_restrict


class AlterDropForeignKey(AlterCommand):
    """ALTER TABLE 命令：DROP FOREIGN KEY key_name"""

    __slots__ = ["_key_name"]

    def __init__(self, key_name: str):
        """
        初始化 DROP FOREIGN KEY 命令。

        Parameters
        ----------
        key_name : str
            外键名称
        """
        self._key_name = key_name

    @property
    def key_name(self) -> str:
        """
        获取外键名称。

        Returns
        -------
        str
            外键名称
        """
        return self._key_name


class AlterDropPrimaryKey(AlterCommand):
    """ALTER TABLE 命令：DROP PRIMARY KEY"""


class AlterDropKey(AlterCommand):
    """ALTER TABLE 命令：DROP KEY/INDEX key_name"""

    __slots__ = ["_key_name"]

    def __init__(self, key_name: str):
        """
        初始化 DROP KEY/INDEX 命令。

        Parameters
        ----------
        key_name : str
            索引名称
        """
        self._key_name = key_name

    @property
    def key_name(self) -> str:
        """
        获取索引名称。

        Returns
        -------
        str
            索引名称
        """
        return self._key_name


class AlterDropCheckConstraint(AlterCommand):
    """ALTER TABLE 命令：DROP CHECK constraint_name"""

    __slots__ = ["_constraint_name"]

    def __init__(self, constraint_name: str):
        """
        初始化 DROP CHECK CONSTRAINT 命令。

        Parameters
        ----------
        constraint_name : str
            约束名称
        """
        self._constraint_name = constraint_name

    @property
    def constraint_name(self) -> str:
        """
        获取约束名称。

        Returns
        -------
        str
            约束名称
        """
        return self._constraint_name


class AlterDropConstraint(AlterCommand):
    """ALTER TABLE 命令：DROP CONSTRAINT constraint_name"""

    __slots__ = ["_constraint_name"]

    def __init__(self, constraint_name: str):
        """
        初始化 DROP CONSTRAINT 命令。

        Parameters
        ----------
        constraint_name : str
            约束名称
        """
        self._constraint_name = constraint_name

    @property
    def constraint_name(self) -> str:
        """
        获取约束名称。

        Returns
        -------
        str
            约束名称
        """
        return self._constraint_name


class AlterDisableKeys(AlterCommand):
    """ALTER TABLE 命令：DISABLE KEYS"""


class AlterEnableKeys(AlterCommand):
    """ALTER TABLE 命令：ENABLE KEYS"""


class AlterSetDefaultValue(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name SET DEFAULT value"""

    __slots__ = ["_column_name", "_default_value"]

    def __init__(self, column_name: str, default_value: "Expression"):
        """
        初始化 SET DEFAULT VALUE 命令。

        Parameters
        ----------
        column_name : str
            字段名称
        default_value : Expression
            默认值
        """
        self._column_name = column_name
        self._default_value = default_value

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name

    @property
    def default_value(self) -> "Expression":
        """
        获取默认值。

        Returns
        -------
        Expression
            默认值
        """
        return self._default_value


class AlterSetDefaultExpression(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name SET DEFAULT ( expression )"""

    __slots__ = ["_column_name", "_default_expression"]

    def __init__(self, column_name: str, default_expression: "Expression"):
        """
        初始化 SET DEFAULT EXPRESSION 命令。

        Parameters
        ----------
        column_name : str
            字段名称
        default_expression : Expression
            默认表达式
        """
        self._column_name = column_name
        self._default_expression = default_expression

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name

    @property
    def default_expression(self) -> "Expression":
        """
        获取默认表达式。

        Returns
        -------
        Expression
            默认表达式
        """
        return self._default_expression


class AlterDropDefault(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name DROP DEFAULT"""

    __slots__ = ["_column_name"]

    def __init__(self, column_name: str):
        """
        初始化 DROP DEFAULT 命令。

        Parameters
        ----------
        column_name : str
            字段名称
        """
        self._column_name = column_name

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name


class AlterSetColumnVisibility(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name SET visibility"""

    __slots__ = ["_column_name", "_visibility"]

    def __init__(self, column_name: str, visibility: bool):
        """
        初始化 SET COLUMN VISIBILITY 命令。

        Parameters
        ----------
        column_name : str
            字段名称
        visibility : bool
            可见性
        """
        self._column_name = column_name
        self._visibility = visibility

    @property
    def column_name(self) -> str:
        """
        获取字段名称。

        Returns
        -------
        str
            字段名称
        """
        return self._column_name

    @property
    def visibility(self) -> bool:
        """
        获取可见性。

        Returns
        -------
        bool
            可见性
        """
        return self._visibility


class AlterSetIndexVisibility(AlterCommand):
    """ALTER TABLE 命令：ALTER INDEX index_name visibility"""

    __slots__ = ["_index_name", "_visibility"]

    def __init__(self, index_name: str, visibility: bool):
        """
        初始化 SET INDEX VISIBILITY 命令。

        Parameters
        ----------
        index_name : str
            索引名称
        visibility : bool
            可见性
        """
        self._index_name = index_name
        self._visibility = visibility

    @property
    def index_name(self) -> str:
        """
        获取索引名称。

        Returns
        -------
        str
            索引名称
        """
        return self._index_name

    @property
    def visibility(self) -> bool:
        """
        获取可见性。

        Returns
        -------
        bool
            可见性
        """
        return self._visibility


class AlterEnforceCheckConstraint(AlterCommand):
    """ALTER TABLE 命令：ALTER CHECK constraint_name enforcement"""

    __slots__ = ["_constraint_name", "_enforcement"]

    def __init__(self, constraint_name: str, enforcement: bool):
        """
        初始化 ENFORCE CHECK CONSTRAINT 命令。

        Parameters
        ----------
        constraint_name : str
            约束名称
        enforcement : bool
            强制执行标识
        """
        self._constraint_name = constraint_name
        self._enforcement = enforcement

    @property
    def constraint_name(self) -> str:
        """
        获取约束名称。

        Returns
        -------
        str
            约束名称
        """
        return self._constraint_name

    @property
    def enforcement(self) -> bool:
        """
        获取强制执行标识。

        Returns
        -------
        bool
            强制执行标识
        """
        return self._enforcement


class AlterEnforceConstraint(AlterCommand):
    """ALTER TABLE 命令：ALTER CONSTRAINT constraint_name enforcement"""

    __slots__ = ["_constraint_name", "_enforcement"]

    def __init__(self, constraint_name: str, enforcement: bool):
        """
        初始化 ENFORCE CONSTRAINT 命令。

        Parameters
        ----------
        constraint_name : str
            约束名称
        enforcement : bool
            强制执行标识
        """
        self._constraint_name = constraint_name
        self._enforcement = enforcement

    @property
    def constraint_name(self) -> str:
        """
        获取约束名称。

        Returns
        -------
        str
            约束名称
        """
        return self._constraint_name

    @property
    def enforcement(self) -> bool:
        """
        获取强制执行标识。

        Returns
        -------
        bool
            强制执行标识
        """
        return self._enforcement


class AlterRenameTable(AlterCommand):
    """ALTER TABLE 命令：RENAME TO table_name"""

    __slots__ = ["_new_table_name"]

    def __init__(self, new_table_name: "Identifier"):
        """
        初始化 RENAME TABLE 命令。

        Parameters
        ----------
        new_table_name : Identifier
            新表名
        """
        self._new_table_name = new_table_name

    @property
    def new_table_name(self) -> "Identifier":
        """
        获取新表名。

        Returns
        -------
        Identifier
            新表名
        """
        return self._new_table_name


class AlterRenameKey(AlterCommand):
    """ALTER TABLE 命令：RENAME KEY/INDEX old_name TO new_name"""

    __slots__ = ["_old_key_name", "_new_key_name"]

    def __init__(self, old_key_name: str, new_key_name: str):
        """
        初始化 RENAME KEY 命令。

        Parameters
        ----------
        old_key_name : str
            旧索引名称
        new_key_name : str
            新索引名称
        """
        self._old_key_name = old_key_name
        self._new_key_name = new_key_name

    @property
    def old_key_name(self) -> str:
        """
        获取旧索引名称。

        Returns
        -------
        str
            旧索引名称
        """
        return self._old_key_name

    @property
    def new_key_name(self) -> str:
        """
        获取新索引名称。

        Returns
        -------
        str
            新索引名称
        """
        return self._new_key_name


class AlterRenameColumn(AlterCommand):
    """ALTER TABLE 命令：RENAME COLUMN old_name TO new_name"""

    __slots__ = ["_old_column_name", "_new_column_name"]

    def __init__(self, old_column_name: str, new_column_name: str):
        """
        初始化 RENAME COLUMN 命令。

        Parameters
        ----------
        old_column_name : str
            旧字段名称
        new_column_name : str
            新字段名称
        """
        self._old_column_name = old_column_name
        self._new_column_name = new_column_name

    @property
    def old_column_name(self) -> str:
        """
        获取旧字段名称。

        Returns
        -------
        str
            旧字段名称
        """
        return self._old_column_name

    @property
    def new_column_name(self) -> str:
        """
        获取新字段名称。

        Returns
        -------
        str
            新字段名称
        """
        return self._new_column_name


class AlterConvertToCharset(AlterCommand):
    """ALTER TABLE 命令：CONVERT TO CHARACTER SET charset_name"""

    __slots__ = ["_charset", "_collation"]

    def __init__(self, charset: "Charset", collation: Optional["Charset"]):
        """
        初始化 CONVERT TO CHARSET 命令。

        Parameters
        ----------
        charset : Charset
            字符集
        collation : Optional[Charset]
            排序规则
        """
        self._charset = charset
        self._collation = collation

    @property
    def charset(self) -> "Charset":
        """
        获取字符集。

        Returns
        -------
        Charset
            字符集
        """
        return self._charset

    @property
    def collation(self) -> Optional["Charset"]:
        """
        获取排序规则。

        Returns
        -------
        Optional[Charset]
            排序规则
        """
        return self._collation


class AlterConvertToDefaultCharset(AlterCommand):
    """ALTER TABLE 命令：CONVERT TO CHARACTER SET DEFAULT"""

    __slots__ = ["_collation"]

    def __init__(self, collation: Optional["Charset"]):
        """
        初始化 CONVERT TO DEFAULT CHARSET 命令。

        Parameters
        ----------
        collation : Optional[Charset]
            排序规则
        """
        self._collation = collation

    @property
    def collation(self) -> Optional["Charset"]:
        """
        获取排序规则。

        Returns
        -------
        Optional[Charset]
            排序规则
        """
        return self._collation


class AlterForce(AlterCommand):
    """ALTER TABLE 命令：FORCE"""


class AlterOrderBy(AlterCommand):
    """ALTER TABLE 命令：ORDER BY order_list"""

    __slots__ = (
        "_order_list",
    )

    def __init__(self, order_list: List["OrderExpression"]):
        """
        初始化 ORDER BY 命令。

        Parameters
        ----------
        order_list : List[OrderExpression]
            排序表达式列表
        """
        self._order_list = order_list

    @property
    def order_list(self) -> List["OrderExpression"]:
        """
        获取排序表达式列表。

        Returns
        -------
        List[OrderExpression]
            排序表达式列表
        """
        return self._order_list


class AlterPartitionBy(AlterCommand):
    """ALTER TABLE 命令：PARTITION BY partition_definition"""

    __slots__ = (
        "_partition_clause",
    )

    def __init__(self, partition_clause: "DdlPartitionByClause"):
        """
        初始化 PARTITION BY 命令。

        Parameters
        ----------
        partition_clause : DdlPartitionByClause
            分区子句
        """
        self._partition_clause = partition_clause

    @property
    def partition_clause(self) -> "DdlPartitionByClause":
        """
        获取分区子句。

        Returns
        -------
        DdlPartitionByClause
            分区子句
        """
        return self._partition_clause


class AlterRemovePartitioning(AlterCommand):
    """ALTER TABLE 命令：REMOVE PARTITIONING"""
