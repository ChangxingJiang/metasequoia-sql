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
        "_expression",
    )

    def __init__(self, expression: Expression):
        """初始化表达式类型 DDL 分区类型定义
        
        Parameters
        ----------
        expression : Expression
            分区表达式
        """
        self._expression = expression

    @property
    def expression(self) -> Expression:
        """获取分区表达式
        
        Returns
        -------
        Expression
            分区表达式
        """
        return self._expression


class PartitionTypeDefinitionColumnsBase(PartitionTypeDefinition):
    """字段列表类型 DDL 分区类型定义的基类"""

    __slots__ = (
        "_column_list",
    )

    def __init__(self, column_list: List[str]):
        """初始化字段列表类型 DDL 分区类型定义
        
        Parameters
        ----------
        column_list : List[str]
            分区字段列表
        """
        self._column_list = column_list

    @property
    def column_list(self) -> List[str]:
        """获取分区字段列表
        
        Returns
        -------
        List[str]
            分区字段列表
        """
        return self._column_list


class PartitionTypeDefinitionKey(PartitionTypeDefinitionColumnsBase):
    """DDL 分区类型定义（KEY）"""

    __slots__ = (
        "_key_algorithm",
    )

    def __init__(self, key_algorithm: Optional["IntLiteral"], column_list: List[str]):
        """初始化 KEY 分区类型定义
        
        Parameters
        ----------
        key_algorithm : Optional[IntLiteral]
            KEY 算法参数
        column_list : List[str]
            分区字段列表
        """
        super().__init__(column_list)
        self._key_algorithm = key_algorithm

    @property
    def key_algorithm(self) -> Optional["IntLiteral"]:
        """获取 KEY 算法参数
        
        Returns
        -------
        Optional[IntLiteral]
            KEY 算法参数
        """
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
        """初始化子分区类型定义
        
        Parameters
        ----------
        partition_num : Optional[int]
            分区数量
        """
        self._partition_num = partition_num

    @property
    def partition_num(self) -> Optional[int]:
        """获取分区数量
        
        Returns
        -------
        Optional[int]
            分区数量
        """
        return self._partition_num


class SubPartitionTypeDefinitionByHash(SubPartitionTypeDefinition):
    """通过 HASH 方式分区的子分区类型的定义"""

    __slots__ = (
        "_expression",
    )

    def __init__(self, expression: Expression, partition_num: Optional[int]):
        """初始化 HASH 子分区类型定义
        
        Parameters
        ----------
        expression : Expression
            HASH 表达式
        partition_num : Optional[int]
            分区数量
        """
        super().__init__(partition_num)
        self._expression = expression

    @property
    def expression(self) -> Expression:
        """获取 HASH 表达式
        
        Returns
        -------
        Expression
            HASH 表达式
        """
        return self._expression


class SubPartitionTypeDefinitionByKey(SubPartitionTypeDefinition):
    """通过 KEY 方式分区的子分区类型的定义"""

    __slots__ = (
        "_key_algorithm",
        "_column_list",
    )

    def __init__(self, key_algorithm: Optional["IntLiteral"], column_list: List[str], partition_num: Optional[int]):
        """初始化 KEY 子分区类型定义
        
        Parameters
        ----------
        key_algorithm : Optional[IntLiteral]
            KEY 算法参数
        column_list : List[str]
            分区字段列表
        partition_num : Optional[int]
            分区数量
        """
        super().__init__(partition_num)
        self._key_algorithm = key_algorithm
        self._column_list = column_list

    @property
    def key_algorithm(self) -> Optional["IntLiteral"]:
        """获取 KEY 算法参数
        
        Returns
        -------
        Optional[IntLiteral]
            KEY 算法参数
        """
        return self._key_algorithm

    @property
    def column_list(self) -> List[str]:
        """获取分区字段列表
        
        Returns
        -------
        List[str]
            分区字段列表
        """
        return self._column_list


class PartitionOption(Node):
    """分区配置选项"""


class PartitionOptionStrBase(Node):
    """字符串类型的分区配置选项的基类"""

    __slots__ = (
        "_value",
    )

    def __init__(self, value: str):
        """初始化字符串类型的分区配置选项
        
        Parameters
        ----------
        value : str
            配置选项值
        """
        self._value = value

    @property
    def value(self) -> str:
        """获取配置选项值
        
        Returns
        -------
        str
            配置选项值
        """
        return self._value


class PartitionOptionIntBase(Node):
    """整型类型的分区配置选项的基类"""

    __slots__ = (
        "_value",
    )

    def __init__(self, value: int):
        """初始化整型类型的分区配置选项
        
        Parameters
        ----------
        value : int
            配置选项值
        """
        self._value = value

    @property
    def value(self) -> int:
        """获取配置选项值
        
        Returns
        -------
        int
            配置选项值
        """
        return self._value


class PartitionOptionTablespace(PartitionOptionStrBase):
    """分区表空间配置选项"""


class PartitionOptionStorageEngine(PartitionOptionStrBase):
    """分区存储引擎配置选项"""


class PartitionOptionNodeGroup(PartitionOptionIntBase):
    """分区节点组配置选项"""


class PartitionOptionMaxRows(PartitionOptionIntBase):
    """分区最大行数配置选项"""


class PartitionOptionMinRows(PartitionOptionIntBase):
    """分区最小行数配置选项"""


class PartitionOptionDataDirectory(PartitionOptionStrBase):
    """分区数据目录配置选项"""


class PartitionOptionIndexDirectory(PartitionOptionStrBase):
    """分区索引目录配置选项"""


class PartitionOptionComment(PartitionOptionStrBase):
    """分区注释配置选项"""


class SubPartitionDefinition(Node):
    """子分区定义子句"""

    __slots__ = (
        "_name",
        "_options",
    )

    def __init__(self, name: str, options: List[PartitionOption]):
        """初始化子分区定义
        
        Parameters
        ----------
        name : str
            子分区名称
        options : List[PartitionOption]
            子分区选项列表
        """
        self._name = name
        self._options = options

    @property
    def name(self) -> str:
        """获取子分区名称
        
        Returns
        -------
        str
            子分区名称
        """
        return self._name

    @property
    def options(self) -> List[PartitionOption]:
        """获取子分区选项列表
        
        Returns
        -------
        List[PartitionOption]
            子分区选项列表
        """
        return self._options


class PartitionValue(Node):
    """分区值"""


class PartitionValueMaxValue(PartitionValue):
    """分区值（MAXVALUE）"""


class PartitionValueExpression(PartitionValue):
    """分区值（通过表达式表示）"""

    __slots__ = (
        "_expression",
    )

    def __init__(self, expression: Expression):
        """初始化表达式分区值
        
        Parameters
        ----------
        expression : Expression
            分区值表达式
        """
        self._expression = expression

    @property
    def expression(self) -> Expression:
        """获取分区值表达式
        
        Returns
        -------
        Expression
            分区值表达式
        """
        return self._expression


class PartitionValues(Node):
    """分区值集合"""


class PartitionValuesLessThanMaxValue(PartitionValues):
    """分区值集合（VALUES LESS THAN MAXVALUE）"""


class PartitionValuesLessThanList(PartitionValues):
    """`VALUES` 关键字引导的分区值列表：VALUES LESS THAN ( ... ) """

    __slots__ = (
        "_value_list",
    )

    def __init__(self, value_list: List[PartitionValue]):
        """初始化 VALUES LESS THAN 分区值列表
        
        Parameters
        ----------
        value_list : List[PartitionValue]
            分区值列表
        """
        self._value_list = value_list

    @property
    def value_list(self) -> List[PartitionValue]:
        """获取分区值列表
        
        Returns
        -------
        List[PartitionValue]
            分区值列表
        """
        return self._value_list


class PartitionValuesInValueList(PartitionValues):
    """`VALUES` 关键字引导的分区值列表：VALUES IN (...) """

    __slots__ = (
        "_value_list",
    )

    def __init__(self, value_list: List[PartitionValue]):
        """初始化 VALUES IN 分区值列表
        
        Parameters
        ----------
        value_list : List[PartitionValue]
            分区值列表
        """
        self._value_list = value_list

    @property
    def value_list(self) -> List[PartitionValue]:
        """获取分区值列表
        
        Returns
        -------
        List[PartitionValue]
            分区值列表
        """
        return self._value_list


class PartitionValuesInValueMatrix(PartitionValues):
    """关键字引导的分区值列表：VALUES IN ((...), (...), ...) """

    __slots__ = (
        "_value_matrix",
    )

    def __init__(self, value_matrix: List[List[PartitionValue]]):
        """初始化 VALUES IN 分区值矩阵
        
        Parameters
        ----------
        value_matrix : List[List[PartitionValue]]
            分区值矩阵
        """
        self._value_matrix = value_matrix

    @property
    def value_matrix(self) -> List[List[PartitionValue]]:
        """获取分区值矩阵
        
        Returns
        -------
        List[List[PartitionValue]]
            分区值矩阵
        """
        return self._value_matrix


class PartitionDefinition(Node):
    """分区定义子句"""

    __slots__ = (
        "_partition_name",
        "_partition_values",
        "_partition_options",
        "_sub_partition_list",
    )

    def __init__(self,
                 partition_name: str,
                 partition_values: PartitionValues,
                 partition_options: List[PartitionOption],
                 sub_partition_list: List[SubPartitionDefinition]):
        """初始化分区定义
        
        Parameters
        ----------
        partition_name : str
            分区名称
        partition_values : PartitionValues
            分区值集合
        partition_options : List[PartitionOption]
            分区选项列表
        sub_partition_list : List[SubPartitionDefinition]
            子分区定义列表
        """
        self._partition_name = partition_name
        self._partition_values = partition_values
        self._partition_options = partition_options
        self._sub_partition_list = sub_partition_list

    @property
    def partition_name(self) -> str:
        """获取分区名称
        
        Returns
        -------
        str
            分区名称
        """
        return self._partition_name

    @property
    def partition_values(self) -> PartitionValues:
        """获取分区值集合
        
        Returns
        -------
        PartitionValues
            分区值集合
        """
        return self._partition_values

    @property
    def partition_options(self) -> List[PartitionOption]:
        """获取分区选项列表
        
        Returns
        -------
        List[PartitionOption]
            分区选项列表
        """
        return self._partition_options

    @property
    def sub_partition_list(self) -> List[SubPartitionDefinition]:
        """获取子分区定义列表
        
        Returns
        -------
        List[SubPartitionDefinition]
            子分区定义列表
        """
        return self._sub_partition_list


class DdlPartitionByClause(Node):
    """DDL 中的 PARTITION BY 子句"""

    __slots__ = (
        "_partition_type",
        "_num_partitions",
        "_subpartition_type",
        "_partition_list",
    )

    def __init__(self,
                 partition_type: PartitionTypeDefinition,
                 num_partitions: Optional[int],
                 subpartition_type: Optional[SubPartitionTypeDefinition],
                 partition_list: List[PartitionDefinition]
                 ):
        """初始化 DDL 中的 PARTITION BY 子句
        
        Parameters
        ----------
        partition_type : PartitionTypeDefinition
            分区类型定义
        num_partitions : Optional[int]
            分区数量
        subpartition_type : SubPartitionTypeDefinition
            子分区类型定义
        partition_list : List[PartitionDefinition]
            分区定义列表
        """
        self._partition_type = partition_type
        self._num_partitions = num_partitions
        self._subpartition_type = subpartition_type
        self._partition_list = partition_list

    @property
    def partition_type(self) -> PartitionTypeDefinition:
        """获取分区类型定义
        
        Returns
        -------
        PartitionTypeDefinition
            分区类型定义
        """
        return self._partition_type

    @property
    def num_partitions(self) -> Optional[int]:
        """获取分区数量
        
        Returns
        -------
        Optional[int]
            分区数量
        """
        return self._num_partitions

    @property
    def subpartition_type(self) -> Optional[SubPartitionTypeDefinition]:
        """获取子分区类型定义
        
        Returns
        -------
        SubPartitionTypeDefinition
            子分区类型定义
        """
        return self._subpartition_type

    @property
    def partition_list(self) -> List[PartitionDefinition]:
        """获取分区定义列表
        
        Returns
        -------
        List[PartitionDefinition]
            分区定义列表
        """
        return self._partition_list
