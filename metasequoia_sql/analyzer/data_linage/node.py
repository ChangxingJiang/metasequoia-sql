"""
基础节点类

标准表名对象（`StandardTable`）包含表可选的所属模式名（`schema_name`）和必选的表名（`table_name`）两个属性。
标准字段对象（`StandardColumn`）包含必选的字段序号（`column_idx`）、字段名（`column_name`）两个属性。
引用字段对象（`QuoteColumn`）包含可选的字段所属表名（`table_name`）以及必选的字段名（`column_name`）两个属性。
源字段对象（`SourceColumn`）包含可选的字段所属模式名（`schema_name`），以及必选的所属表名（`table_name`）和字段名（`column_name`）三个属性。
"""

import dataclasses
from typing import Optional

__all__ = ["StandardTable", "StandardColumn", "QuoteColumn", "SourceColumn"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class StandardTable:
    """标准表名对象

    TODO 待支持子查询的形式
    """

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 所属模式名
    table_name: str = dataclasses.field(kw_only=True)  # 表名

    def source(self):
        """引用字段的源代码"""
        return f"{self.schema_name}.{self.table_name}" if self.schema_name else f"{self.table_name}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class StandardColumn:
    """标准字段对象"""

    column_idx: int = dataclasses.field(kw_only=True)  # 字段序号
    column_name: str = dataclasses.field(kw_only=True)  # 字段名


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteColumn:
    """引用字段对象"""

    table_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 所属表名
    column_name: str = dataclasses.field(kw_only=True)  # 字段名


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SourceColumn:
    """源字段对象"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 所属模式名
    table_name: str = dataclasses.field(kw_only=True)  # 所属表名
    column_name: str = dataclasses.field(kw_only=True)  # 字段名
