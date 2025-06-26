"""
关联表（joined table）
"""

from enum import IntEnum
from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Ident

__all__ = [
    "EnumJoinType",
    "JoinedTableBase",
    "JoinedTableOn",
    "JoinedTableUsing",
    "CrossJoinedTable",
    "NaturalJoinedTable",
]


class EnumJoinType(IntEnum):
    """关联类型"""

    NATURAL_INNER = 1  # 自然内（内）关联
    NATURAL_RIGHT = 2  # 自然右（外）关联
    NATURAL_LEFT = 3  # 自然左（外）关联

    JOIN = 4  # 内关联
    INNER_JOIN = 5  # 内关联
    CROSS_JOIN = 6  # 笛卡尔积（内）关联
    STRAIGHT_JOIN = 7  # 指定关联顺序的内关联

    LEFT_OUTER_JOIN = 8  # 左（外）关联
    RIGHT_OUTER_JOIN = 9  # 右（外）关联


class JoinedTableBase(Table):
    """关联表"""

    __slots__ = ["_left_operand", "_right_operand", "_join_type"]

    def __init__(self, left_operand: Table, right_operand: Table, join_type: EnumJoinType):
        """
        初始化关联表

        Parameters
        ----------
        left_operand : Table
            左操作数表
        right_operand : Table
            右操作数表
        join_type : EnumJoinType
            关联类型
        """
        self._left_operand = left_operand
        self._right_operand = right_operand
        self._join_type = join_type

    @property
    def left_operand(self) -> Table:
        """
        左操作数表

        Returns
        -------
        Table
            左操作数表
        """
        return self._left_operand

    @property
    def right_operand(self) -> Table:
        """
        右操作数表

        Returns
        -------
        Table
            右操作数表
        """
        return self._right_operand

    @property
    def join_type(self) -> EnumJoinType:
        """
        关联类型

        Returns
        -------
        EnumJoinType
            关联类型
        """
        return self._join_type


class JoinedTableOn(JoinedTableBase):
    """通过 ON 条件关联表"""

    __slots__ = ["_on_condition"]

    def __init__(self, left_operand: Table, right_operand: Table, join_type: EnumJoinType, on_condition: Expression):
        super().__init__(left_operand, right_operand, join_type)
        self._on_condition = on_condition

    @property
    def on_condition(self) -> Expression:
        """
        ON 条件表达式

        Returns
        -------
        Expression
            ON 条件表达式
        """
        return self._on_condition


class JoinedTableUsing(JoinedTableBase):
    """通过 USING 条件关联表"""

    __slots__ = ["_using_list"]

    def __init__(self, left_operand: Table, right_operand: Table, join_type: EnumJoinType, using_list: List["Ident"]):
        super().__init__(left_operand, right_operand, join_type)
        self._using_list = using_list

    @property
    def using_list(self) -> List["Ident"]:
        """
        USING 列名列表

        Returns
        -------
        List[Ident]
            USING 列名列表
        """
        return self._using_list


class CrossJoinedTable(JoinedTableBase):
    """CROSS JOIN 表"""


class NaturalJoinedTable(JoinedTableBase):
    """NATURAL JOIN 表"""
