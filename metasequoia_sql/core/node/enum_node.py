"""
枚举类抽象语法树节点
"""

import dataclasses
import enum

from metasequoia_sql.core.node.abc_node import ASTBase
from metasequoia_sql.core.node.sql_type import SQLType
from metasequoia_sql.errors import UnSupportDataSourceError

__all__ = [
    # 插入类型
    "EnumInsertType", "ASTInsertType",

    # 关联类型
    "EnumJoinType", "ASTJoinType",

    # 排序类型
    "EnumOrderType", "ASTOrderType",

    # 组合类型
    "EnumUnionType", "ASTUnionType",

    # 比较运算符
    "EnumCompareOperator", "ASTCompareOperator",

    # 计算运算符
    "EnumComputeOperator", "ASTComputeOperator",

    # 逻辑运算符
    "EnumLogicalOperator", "ASTLogicalOperator"

]


# ---------------------------------------- 插入类型 ----------------------------------------


class EnumInsertType(enum.Enum):
    """插入类型的枚举类"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertType(ASTBase):
    """插入类型"""

    insert_type: EnumInsertType = dataclasses.field(kw_only=True)  # 插入类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.insert_type.value)


# ---------------------------------------- 关联类型 ----------------------------------------


class EnumJoinType(enum.Enum):
    """关联类型的枚举类"""
    JOIN = ["JOIN"]  # 内连接
    INNER_JOIN = ["INNER", "JOIN"]  # 内连接
    LEFT_JOIN = ["LEFT", "JOIN"]  # 左外连接
    LEFT_OUTER_JOIN = ["LEFT", "OUTER", "JOIN"]  # 左外连接
    RIGHT_JOIN = ["RIGHT", "JOIN"]  # 右外连接
    RIGHT_OUTER_JOIN = ["RIGHT", "OUTER", "JOIN"]  # 右外连接
    FULL_JOIN = ["FULL", "JOIN"]  # 全外连接
    FULL_OUTER_JOIN = ["FULL", "OUTER", "JOIN"]  # 全外连接
    CROSS_JOIN = ["CROSS", "JOIN"]  # 交叉连接


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinType(ASTBase):
    """关联类型"""

    join_type: EnumJoinType = dataclasses.field(kw_only=True)  # 关联类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.join_type.value)


# ---------------------------------------- 排序类型 ----------------------------------------


class EnumOrderType(enum.Enum):
    """排序类型的枚举类"""
    ASC = "ASC"  # 升序
    DESC = "DESC"  # 降序


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTOrderType(ASTBase):
    """排序类型"""

    order_type: EnumOrderType = dataclasses.field(kw_only=True)  # 排序类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.order_type.value


# ---------------------------------------- 组合类型 ----------------------------------------


class EnumUnionType(enum.Enum):
    """组合类型的枚举类"""
    UNION_ALL = ["UNION", "ALL"]
    UNION = ["UNION"]
    EXCEPT = ["EXCEPT"]
    INTERSECT = ["INTERSECT"]
    MINUS = ["MINUS"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUnionType(ASTBase):
    """组合类型"""

    union_type: EnumUnionType = dataclasses.field(kw_only=True)  # 组合类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.union_type.value)


# ---------------------------------------- 比较运算符 ----------------------------------------

class EnumCompareOperator(enum.Enum):
    """比较运算符的枚举类"""
    EQ = "="
    EQUAL_TO = "="
    NEQ = "!="
    NOT_EQUAL_TO = "!="
    LT = "<"
    LESS_THAN = "<"
    LTE = "<="
    LESS_THAN_OR_EQUAL = "<="
    GT = ">"
    GREATER_THAN = ">"
    GTE = ">="
    GREATER_THAN_OR_EQUAL = ">="


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCompareOperator(ASTBase):
    """比较运算符"""

    compare_operator: EnumCompareOperator = dataclasses.field(kw_only=True)  # 比较运算符的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.compare_operator.value


# ---------------------------------------- 计算运算符 ----------------------------------------

class EnumComputeOperator(enum.Enum):
    """计算运算符的枚举类"""
    PLUS = "+"  # 加法运算符
    SUBTRACT = "-"  # 减法运算符
    MULTIPLE = "*"  # 乘法运算符
    DIVIDE = "/"  # 除法运算符
    MOD = "%"  # 取模运算符
    CONCAT = "||"  # 字符串拼接运算符（仅 Oracle、DB2、PostgreSQL 中适用）


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTComputeOperator(ASTBase):
    """计算运算符"""

    compute_operator: EnumComputeOperator = dataclasses.field(kw_only=True)  # 计算运算符的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.compute_operator == EnumComputeOperator.MOD and data_source != SQLType.SQL_SERVER:
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 % 运算符")
        if (self.compute_operator == EnumComputeOperator.CONCAT
                and data_source not in {SQLType.ORACLE, SQLType.DB2, SQLType.POSTGRE_SQL}):
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 || 运算符")
        return self.compute_operator.value


# ---------------------------------------- 逻辑运算符 ----------------------------------------


class EnumLogicalOperator(enum.Enum):
    """逻辑运算符的枚举类"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLogicalOperator(ASTBase):
    """逻辑运算符"""

    logical_operator: EnumLogicalOperator = dataclasses.field(kw_only=True)  # 逻辑运算符的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.logical_operator.value
