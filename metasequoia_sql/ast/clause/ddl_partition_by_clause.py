"""
DDL 中的 PARTITION BY 子句（ddl partition by clause）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import IntLiteral

__all__ = [
    "PartitionTypeDefinition",
    "PartitionTypeDefinitionExpressionBase",
    "PartitionTypeDefinitionColumnsBase",
    "PartitionTypeDefinitionKey",
    "PartitionTypeDefinitionHash",
    "PartitionTypeDefinitionRange",
    "PartitionTypeDefinitionRangeColumns",
    "PartitionTypeDefinitionList",
    "PartitionTypeDefinitionListColumns",
    "SubPartitionTypeDefinition",
    "SubPartitionTypeDefinitionByHash",
    "SubPartitionTypeDefinitionByKey",
    "PartitionOption",
    "PartitionOptionStrBase",
    "PartitionOptionIntBase",
    "PartitionOptionTablespace",
    "PartitionOptionStorageEngine",
    "PartitionOptionNodeGroup",
    "PartitionOptionMaxRows",
    "PartitionOptionMinRows",
    "PartitionOptionDataDirectory",
    "PartitionOptionIndexDirectory",
    "PartitionOptionComment",
    "SubPartitionDefinition",
    "PartitionValue",
    "PartitionValueMaxValue",
    "PartitionValueExpression",
    "PartitionValues",
    "PartitionValuesLessThanMaxValue",
    "PartitionValuesLessThanList",
    "PartitionValuesInValueList",
    "PartitionValuesInValueMatrix",
    "PartitionDefinition",
    "DdlPartitionByClause",
]


class PartitionTypeDefinition(Node):
    """DDL 分区类型定义"""


class PartitionTypeDefinitionExpressionBase(PartitionTypeDefinition):
    """表达式类型 DDL 分区类型定义的基类"""

    __slots__ = (
        "_expression"
    )

    def __init__(self, expression: Expression):
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression


class PartitionTypeDefinitionColumnsBase(PartitionTypeDefinition):
    """字段列表类型 DDL 分区类型定义的基类"""

    __slots__ = (
        "_column_list"
    )

    def __init__(self, column_list: List[str]):
        self._column_list = column_list

    @property
    def column_list(self) -> List[str]:
        return self._column_list


class PartitionTypeDefinitionKey(PartitionTypeDefinitionColumnsBase):
    """DDL 分区类型定义（KEY）"""

    __slots__ = (
        "_key_algorithm"
    )

    def __init__(self, key_algorithm: Optional["IntLiteral"], column_list: List[str]):
        super().__init__(column_list)
        self._key_algorithm = key_algorithm

    @property
    def key_algorithm(self) -> Optional["IntLiteral"]:
        return self._key_algorithm


class PartitionTypeDefinitionHash(PartitionTypeDefinitionExpressionBase):
    """DDL 分区类型定义（HASH）"""


class PartitionTypeDefinitionRange(PartitionTypeDefinitionExpressionBase):
    """DDL 分区类型定义（RANGE）"""


class PartitionTypeDefinitionRangeColumns(PartitionTypeDefinitionColumnsBase):
    """DDL 分区类型定义（RANGE COLUMNS）"""


class PartitionTypeDefinitionList(PartitionTypeDefinitionExpressionBase):
    """DDL 分区类型定义（LIST）"""


class PartitionTypeDefinitionListColumns(PartitionTypeDefinitionColumnsBase):
    """DDL 分区类型定义（LIST COLUMNS）"""


class SubPartitionTypeDefinition(PartitionTypeDefinition):
    """子分区类型的定义"""

    __slots__ = (
        "_partition_num",
    )

    def __init__(self, partition_num: Optional[int]):
        self._partition_num = partition_num

    @property
    def partition_num(self) -> Optional[int]:
        return self._partition_num


class SubPartitionTypeDefinitionByHash(SubPartitionTypeDefinition):
    """通过 HASH 方式分区的子分区类型的定义"""

    __slots__ = (
        "_expression",
    )

    def __init__(self, expression: Expression, partition_num: Optional[int]):
        super().__init__(partition_num)
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression


class SubPartitionTypeDefinitionByKey(SubPartitionTypeDefinition):
    """通过 KEY 方式分区的子分区类型的定义"""

    __slots__ = (
        "_key_algorithm",
        "_column_list",
    )

    def __init__(self, key_algorithm: Optional["IntLiteral"], column_list: List[str], partition_num: Optional[int]):
        super().__init__(partition_num)
        self._key_algorithm = key_algorithm
        self._column_list = column_list

    @property
    def key_algorithm(self) -> Optional["IntLiteral"]:
        return self._key_algorithm

    @property
    def column_list(self) -> List[str]:
        return self._column_list


class PartitionOption(Node):
    """分区配置选项"""


class PartitionOptionStrBase(Node):
    """字符串类型的分区配置选项的基类"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class PartitionOptionIntBase(Node):
    """整型类型的分区配置选项的基类"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value


class PartitionOptionTablespace(PartitionOptionStrBase):
    """DDL 分区配置选项（TABLESPACE）"""


class PartitionOptionStorageEngine(PartitionOptionStrBase):
    """DDL 分区配置选项（STORAGE ENGINE 或 ENGINE）"""


class PartitionOptionNodeGroup(PartitionOptionIntBase):
    """DDL 分区配置选项（NODEGROUP）"""


class PartitionOptionMaxRows(PartitionOptionIntBase):
    """DDL 分区配置选项（MAX_ROWS）"""


class PartitionOptionMinRows(PartitionOptionIntBase):
    """DDL 分区配置选项（MIN_ROWS）"""


class PartitionOptionDataDirectory(PartitionOptionStrBase):
    """DDL 分区配置选项（DATA DIRECTORY）"""


class PartitionOptionIndexDirectory(PartitionOptionStrBase):
    """DDL 分区配置选项（INDEX DIRECTORY）"""


class PartitionOptionComment(PartitionOptionStrBase):
    """DDL 分区配置选项（COMMENT）"""


class SubPartitionDefinition(Node):
    """子分区定义子句"""

    __slots__ = (
        "_name",
        "_options"
    )

    def __init__(self, name: str, options: List[PartitionOption]):
        self._name = name
        self._options = options

    @property
    def name(self) -> str:
        return self._name

    @property
    def options(self) -> List[PartitionOption]:
        return self._options


class PartitionValue(Node):
    """分区值"""


class PartitionValueMaxValue(PartitionValue):
    """分区值（MAX_VALUE 关键字表示）"""


class PartitionValueExpression(PartitionValue):
    """分区值（通过表达式表示）"""

    __slots__ = (
        "_expression"
    )

    def __init__(self, expression: Expression):
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression


class PartitionValues(Node):
    """`VALUES` 关键字引导的分区值列表的基类"""


class PartitionValuesLessThanMaxValue(PartitionValues):
    """`VALUES` 关键字引导的分区值列表：VALUES LESS THAN MAX_VALUE"""


class PartitionValuesLessThanList(PartitionValues):
    """`VALUES` 关键字引导的分区值列表：VALUES LESS THAN ( ... ) """

    __slots__ = (
        "_value_list"
    )

    def __init__(self, value_list: List[PartitionValue]):
        self._value_list = value_list

    @property
    def value_list(self) -> List[PartitionValue]:
        return self._value_list


class PartitionValuesInValueList(PartitionValues):
    """`VALUES` 关键字引导的分区值列表：VALUES IN (...) """

    __slots__ = (
        "_value_list"
    )

    def __init__(self, value_list: List[PartitionValue]):
        self._value_list = value_list

    @property
    def value_list(self) -> List[PartitionValue]:
        return self._value_list


class PartitionValuesInValueMatrix(PartitionValues):
    """关键字引导的分区值列表：VALUES IN ((...), (...), ...) """

    __slots__ = (
        "_value_matrix"
    )

    def __init__(self, value_matrix: List[List[PartitionValue]]):
        self._value_matrix = value_matrix

    @property
    def value_matrix(self) -> List[List[PartitionValue]]:
        return self._value_matrix


class PartitionDefinition(Node):
    """分区定义子句"""

    __slots__ = (
        "_partition_name",
        "_partition_values",
        "_partition_options",
        "_sub_partition_list"
    )

    def __init__(self,
                 partition_name: str,
                 partition_values: PartitionValues,
                 partition_options: List[PartitionOption],
                 sub_partition_list: List[SubPartitionDefinition]):
        self._partition_name = partition_name
        self._partition_values = partition_values
        self._partition_options = partition_options
        self._sub_partition_list = sub_partition_list

    @property
    def partition_name(self) -> str:
        return self._partition_name

    @property
    def partition_values(self) -> PartitionValues:
        return self._partition_values

    @property
    def partition_options(self) -> List[PartitionOption]:
        return self._partition_options

    @property
    def sub_partition_list(self) -> List[SubPartitionDefinition]:
        return self._sub_partition_list


class DdlPartitionByClause(Node):
    """DDL 中的 PARTITION BY 子句"""

    __slots__ = (
        "_partition_type",
        "_num_partitions",
        "_subpartition_type",
        "_partition_list"
    )

    def __init__(self,
                 partition_type: PartitionTypeDefinition,
                 num_partitions: Optional[int],
                 subpartition_type: SubPartitionTypeDefinition,
                 partition_list: List[PartitionDefinition]
                 ):
        self._partition_type = partition_type
        self._num_partitions = num_partitions
        self._subpartition_type = subpartition_type
        self._partition_list = partition_list

    @property
    def partition_type(self) -> PartitionTypeDefinition:
        return self._partition_type

    @property
    def num_partitions(self) -> Optional[int]:
        return self._num_partitions

    @property
    def subpartition_type(self) -> SubPartitionTypeDefinition:
        return self._subpartition_type

    @property
    def partition_list(self) -> List[PartitionDefinition]:
        return self._partition_list
