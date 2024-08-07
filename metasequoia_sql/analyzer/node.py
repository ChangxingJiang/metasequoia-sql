"""
分析器的基本节点类

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
    """标准表名对象"""

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

    def source(self):
        """引用字段的源代码"""
        return self.column_name


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteColumn:
    """引用字段对象"""

    table_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 所属表名
    column_name: Optional[str] = dataclasses.field(kw_only=True)  # 字段名（为空时表示没有直接使用字段的聚集函数）
    column_idx: Optional[int] = dataclasses.field(kw_only=True, default=None)  # 字段序号（仅在 GROUP BY 和 ORDER BY 语句中使用）

    def source(self):
        """引用字段的源代码"""
        return f"{self.table_name}.{self.column_name}" if self.table_name else f"{self.column_name}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SourceColumn:
    """源字段对象"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 所属模式名
    table_name: str = dataclasses.field(kw_only=True)  # 所属表名
    column_name: Optional[str] = dataclasses.field(kw_only=True)  # 字段名（为空时表示没有直接使用字段的聚集函数）
