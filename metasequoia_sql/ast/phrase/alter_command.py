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
        "_no_write_to_binlog"
    )

    def __init__(self, no_write_to_binlog: bool):
        self._no_write_to_binlog = no_write_to_binlog

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog


class AlterAddPartitionByDefinitionList(AlterCommand):
    """ALTER TABLE 命令：ADD PARTITION ( partition_definition_list )"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: List["PartitionDefinition"]):
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> List["PartitionDefinition"]:
        return self._partition_list


class AlterAddPartitionByPartitionNum(AlterCommand):
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


class AlterDropPartition(AlterCommand):
    """ALTER TABLE 命令：DROP PARTITION"""

    __slots__ = (
        "_partition_list"
    )

    def __init__(self, partition_list: List[str]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> List[str]:
        return self._partition_list


class AlterRebuildPartition(AlterCommand):
    """ALTER TABLE 命令：REBUILD PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]]):
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list


class AlterOptimizePartition(AlterCommand):
    """ALTER TABLE 命令：OPTIMIZE PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]]):
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list


class AlterAnalyzePartition(AlterCommand):
    """ALTER TABLE 命令：ANALYZE PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list"
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]]):
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list


class AlterCheckPartition(AlterCommand):
    """ALTER TABLE 命令：CHECK PARTITION"""

    __slots__ = (
        "_partition_list",
        "_check_type",
    )

    def __init__(self, partition_list: Optional[List[str]], check_type: "EnumCheckType"):
        self._partition_list = partition_list
        self._check_type = check_type

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list

    @property
    def check_type(self) -> "EnumCheckType":
        return self._check_type


class AlterRepairPartition(AlterCommand):
    """ALTER TABLE 命令：REPAIR PARTITION"""

    __slots__ = (
        "_no_write_to_binlog",
        "_partition_list",
        "_repair_type",
    )

    def __init__(self, no_write_to_binlog: bool, partition_list: Optional[List[str]], repair_type: "EnumRepairType"):
        self._no_write_to_binlog = no_write_to_binlog
        self._partition_list = partition_list
        self._repair_type = repair_type

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list

    @property
    def repair_type(self) -> "EnumRepairType":
        return self._repair_type


class AlterCoalescePartition(AlterCommand):
    """ALTER TABLE 命令：COALESCE PARTITION"""

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


class AlterTruncatePartition(AlterCommand):
    """ALTER TABLE 命令：TRUNCATE PARTITION"""

    __slots__ = (
        "_partition_list"
    )

    def __init__(self, partition_list: Optional[List[str]]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list


class AlterReorganizePartition(AlterCommand):
    """ALTER TABLE 命令：REORGANIZE PARTITION"""

    __slots__ = (
        "_no_write_to_binlog"
    )

    def __init__(self, no_write_to_binlog: bool):
        self._no_write_to_binlog = no_write_to_binlog

    @property
    def no_write_to_binlog(self) -> bool:
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
        self._no_write_to_binlog = no_write_to_binlog
        self._source_partition_list = source_partition_list
        self._target_partition_list = target_partition_list

    @property
    def no_write_to_binlog(self) -> bool:
        return self._no_write_to_binlog

    @property
    def source_partition_list(self) -> List[str]:
        return self._source_partition_list

    @property
    def target_partition_list(self) -> List["PartitionDefinition"]:
        return self._target_partition_list


class AlterExchangePartition(AlterCommand):
    """ALTER TABLE 命令：EXCHANGE PARTITION"""

    __slots__ = (
        "_partition_name",
        "_table",
        "_with_validation"
    )

    def __init__(self, partition_name: str, table: "Identifier", with_validation: "AlterOptionWithValidation"):
        self._partition_name = partition_name
        self._table = table
        self._with_validation = with_validation

    @property
    def partition_name(self) -> str:
        return self._partition_name

    @property
    def table(self) -> "Identifier":
        return self._table

    @property
    def with_validation(self) -> "AlterOptionWithValidation":
        return self._with_validation


class AlterDiscardPartitionTablespace(AlterCommand):
    """ALTER TABLE 命令：DISCARD PARTITION partition_list TABLESPACE"""

    __slots__ = (
        "_partition_list"
    )

    def __init__(self, partition_list: Optional[List[str]]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list


class AlterImportPartitionTablespace(AlterCommand):
    """ALTER TABLE 命令：IMPORT PARTITION partition_list TABLESPACE"""

    __slots__ = (
        "_partition_list"
    )

    def __init__(self, partition_list: Optional[List[str]]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
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

    __slots__ = ["_column_name"]

    def __init__(self, column_name: str):
        self._column_name = column_name

    @property
    def column_name(self) -> str:
        return self._column_name


class AlterPlaceFirst(AlterPlace):
    """在第一个位置"""


class AlterAddColumn(AlterCommand):
    """ALTER TABLE 命令：ADD COLUMN column_name field_definition"""

    __slots__ = ["_column_name", "_field_definition", "_place"]

    def __init__(self, column_name: str, field_definition: "FieldDefinition", place: AlterPlace):
        self._column_name = column_name
        self._field_definition = field_definition
        self._place = place

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def field_definition(self) -> "FieldDefinition":
        return self._field_definition

    @property
    def place(self) -> AlterPlace:
        return self._place


class AlterAddColumns(AlterCommand):
    """ALTER TABLE 命令：ADD ( table_element_list )"""

    __slots__ = ["_table_element_list"]

    def __init__(self, table_element_list: List["TableElement"]):
        self._table_element_list = table_element_list

    @property
    def table_element_list(self) -> List["TableElement"]:
        return self._table_element_list


class AlterAddConstraint(AlterCommand):
    """ALTER TABLE 命令：ADD constraint_definition"""

    __slots__ = ["_constraint_definition"]

    def __init__(self, constraint_definition: "TableElement"):
        self._constraint_definition = constraint_definition

    @property
    def constraint_definition(self) -> "TableElement":
        return self._constraint_definition


class AlterChangeColumn(AlterCommand):
    """ALTER TABLE 命令：CHANGE COLUMN old_name new_name field_definition"""

    __slots__ = ["_old_column_name", "_new_column_name", "_field_definition", "_place"]

    def __init__(self, old_column_name: str, new_column_name: str, field_definition: "FieldDefinition",
                 place: AlterPlace):
        self._old_column_name = old_column_name
        self._new_column_name = new_column_name
        self._field_definition = field_definition
        self._place = place

    @property
    def old_column_name(self) -> str:
        return self._old_column_name

    @property
    def new_column_name(self) -> str:
        return self._new_column_name

    @property
    def field_definition(self) -> "FieldDefinition":
        return self._field_definition

    @property
    def place(self) -> AlterPlace:
        return self._place


class AlterModifyColumn(AlterCommand):
    """ALTER TABLE 命令：MODIFY COLUMN column_name field_definition"""

    __slots__ = ["_column_name", "_field_definition", "_place"]

    def __init__(self, column_name: str, field_definition: "FieldDefinition", place: AlterPlace):
        self._column_name = column_name
        self._field_definition = field_definition
        self._place = place

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def field_definition(self) -> "FieldDefinition":
        return self._field_definition

    @property
    def place(self) -> AlterPlace:
        return self._place


class AlterDropColumn(AlterCommand):
    """ALTER TABLE 命令：DROP COLUMN column_name"""

    __slots__ = ["_column_name", "_drop_restrict"]

    def __init__(self, column_name: str, drop_restrict: "EnumDropRestrict"):
        self._column_name = column_name
        self._drop_restrict = drop_restrict

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def drop_restrict(self) -> "EnumDropRestrict":
        return self._drop_restrict


class AlterDropForeignKey(AlterCommand):
    """ALTER TABLE 命令：DROP FOREIGN KEY key_name"""

    __slots__ = ["_key_name"]

    def __init__(self, key_name: str):
        self._key_name = key_name

    @property
    def key_name(self) -> str:
        return self._key_name


class AlterDropPrimaryKey(AlterCommand):
    """ALTER TABLE 命令：DROP PRIMARY KEY"""


class AlterDropKey(AlterCommand):
    """ALTER TABLE 命令：DROP KEY/INDEX key_name"""

    __slots__ = ["_key_name"]

    def __init__(self, key_name: str):
        self._key_name = key_name

    @property
    def key_name(self) -> str:
        return self._key_name


class AlterDropCheckConstraint(AlterCommand):
    """ALTER TABLE 命令：DROP CHECK constraint_name"""

    __slots__ = ["_constraint_name"]

    def __init__(self, constraint_name: str):
        self._constraint_name = constraint_name

    @property
    def constraint_name(self) -> str:
        return self._constraint_name


class AlterDropConstraint(AlterCommand):
    """ALTER TABLE 命令：DROP CONSTRAINT constraint_name"""

    __slots__ = ["_constraint_name"]

    def __init__(self, constraint_name: str):
        self._constraint_name = constraint_name

    @property
    def constraint_name(self) -> str:
        return self._constraint_name


class AlterDisableKeys(AlterCommand):
    """ALTER TABLE 命令：DISABLE KEYS"""


class AlterEnableKeys(AlterCommand):
    """ALTER TABLE 命令：ENABLE KEYS"""


class AlterSetDefaultValue(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name SET DEFAULT value"""

    __slots__ = ["_column_name", "_default_value"]

    def __init__(self, column_name: str, default_value: Expression):
        self._column_name = column_name
        self._default_value = default_value

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def default_value(self) -> Expression:
        return self._default_value


class AlterSetDefaultExpression(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name SET DEFAULT ( expression )"""

    __slots__ = ["_column_name", "_default_expression"]

    def __init__(self, column_name: str, default_expression: Expression):
        self._column_name = column_name
        self._default_expression = default_expression

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def default_expression(self) -> Expression:
        return self._default_expression


class AlterDropDefault(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name DROP DEFAULT"""

    __slots__ = ["_column_name"]

    def __init__(self, column_name: str):
        self._column_name = column_name

    @property
    def column_name(self) -> str:
        return self._column_name


class AlterSetColumnVisibility(AlterCommand):
    """ALTER TABLE 命令：ALTER COLUMN column_name SET visibility"""

    __slots__ = ["_column_name", "_visibility"]

    def __init__(self, column_name: str, visibility: bool):
        self._column_name = column_name
        self._visibility = visibility

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def visibility(self) -> bool:
        return self._visibility


class AlterSetIndexVisibility(AlterCommand):
    """ALTER TABLE 命令：ALTER INDEX index_name visibility"""

    __slots__ = ["_index_name", "_visibility"]

    def __init__(self, index_name: str, visibility: bool):
        self._index_name = index_name
        self._visibility = visibility

    @property
    def index_name(self) -> str:
        return self._index_name

    @property
    def visibility(self) -> bool:
        return self._visibility


class AlterEnforceCheckConstraint(AlterCommand):
    """ALTER TABLE 命令：ALTER CHECK constraint_name enforcement"""

    __slots__ = ["_constraint_name", "_enforcement"]

    def __init__(self, constraint_name: str, enforcement: bool):
        self._constraint_name = constraint_name
        self._enforcement = enforcement

    @property
    def constraint_name(self) -> str:
        return self._constraint_name

    @property
    def enforcement(self) -> bool:
        return self._enforcement


class AlterEnforceConstraint(AlterCommand):
    """ALTER TABLE 命令：ALTER CONSTRAINT constraint_name enforcement"""

    __slots__ = ["_constraint_name", "_enforcement"]

    def __init__(self, constraint_name: str, enforcement: bool):
        self._constraint_name = constraint_name
        self._enforcement = enforcement

    @property
    def constraint_name(self) -> str:
        return self._constraint_name

    @property
    def enforcement(self) -> bool:
        return self._enforcement


class AlterRenameTable(AlterCommand):
    """ALTER TABLE 命令：RENAME TO table_name"""

    __slots__ = ["_new_table_name"]

    def __init__(self, new_table_name: "Identifier"):
        self._new_table_name = new_table_name

    @property
    def new_table_name(self) -> "Identifier":
        return self._new_table_name


class AlterRenameKey(AlterCommand):
    """ALTER TABLE 命令：RENAME KEY/INDEX old_name TO new_name"""

    __slots__ = ["_old_key_name", "_new_key_name"]

    def __init__(self, old_key_name: str, new_key_name: str):
        self._old_key_name = old_key_name
        self._new_key_name = new_key_name

    @property
    def old_key_name(self) -> str:
        return self._old_key_name

    @property
    def new_key_name(self) -> str:
        return self._new_key_name


class AlterRenameColumn(AlterCommand):
    """ALTER TABLE 命令：RENAME COLUMN old_name TO new_name"""

    __slots__ = ["_old_column_name", "_new_column_name"]

    def __init__(self, old_column_name: str, new_column_name: str):
        self._old_column_name = old_column_name
        self._new_column_name = new_column_name

    @property
    def old_column_name(self) -> str:
        return self._old_column_name

    @property
    def new_column_name(self) -> str:
        return self._new_column_name


class AlterConvertToCharset(AlterCommand):
    """ALTER TABLE 命令：CONVERT TO CHARACTER SET charset_name"""

    __slots__ = ["_charset", "_collation"]

    def __init__(self, charset: "Charset", collation: Optional["Charset"]):
        self._charset = charset
        self._collation = collation

    @property
    def charset(self) -> "Charset":
        return self._charset

    @property
    def collation(self) -> Optional["Charset"]:
        return self._collation


class AlterConvertToDefaultCharset(AlterCommand):
    """ALTER TABLE 命令：CONVERT TO CHARACTER SET DEFAULT"""

    __slots__ = ["_collation"]

    def __init__(self, collation: Optional["Charset"]):
        self._collation = collation

    @property
    def collation(self) -> Optional["Charset"]:
        return self._collation


class AlterForce(AlterCommand):
    """ALTER TABLE 命令：FORCE"""


class AlterOrderBy(AlterCommand):
    """ALTER TABLE 命令：ORDER BY order_list"""

    __slots__ = ["_order_list"]

    def __init__(self, order_list: List["OrderExpression"]):
        self._order_list = order_list

    @property
    def order_list(self) -> List["OrderExpression"]:
        return self._order_list


class AlterPartitionBy(AlterCommand):
    """ALTER TABLE 命令：PARTITION BY partition_definition"""

    __slots__ = (
        "_partition_clause"
    )

    def __init__(self, partition_clause: "DdlPartitionByClause"):
        self._partition_clause = partition_clause

    @property
    def partition_clause(self) -> "DdlPartitionByClause":
        return self._partition_clause


class AlterRemovePartitioning(AlterCommand):
    """ALTER TABLE 命令：REMOVE PARTITIONING"""
