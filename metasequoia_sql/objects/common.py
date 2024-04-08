"""
通用的 SQL 语法对象
"""

import abc
from typing import Optional, List

__all__ = [
    # ---------- 抽象基类 ----------
    "SQLBase",

    # ---------- 其他类型 ----------
    "DDLColumn",
    "DDLPrimaryKey",
    "DDLUniqueKey",
    "DDLKey", "DDLForeignKey", "DDLFulltextKey", "DDLCreateTableStatement"
]


# ------------------------------ 抽象基类 ------------------------------


class SQLBase(abc.ABC):
    @property
    @abc.abstractmethod
    def source(self) -> str:
        """返回 SQL 源码"""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} source={self.source}>"


# ------------------------------ DDL 相关通用类 ------------------------------

class DDLColumn(SQLBase):
    """【DDL】建表语句中的字段信息"""

    def __init__(self, column_name: str, column_type, comment: Optional[str] = None):
        self._column_name = column_name.strip("`")
        self._column_type = column_type
        self._comment = comment

    @property
    def column_name(self):
        return self.get_column_name()

    @property
    def column_type(self):
        return self._column_type

    @property
    def comment(self):
        return self._comment

    def get_column_name(self, with_quote: bool = True):
        if with_quote:
            return f"`{self._column_name}`"
        else:
            return self._column_name

    def set_column_name(self, column_name: str) -> None:
        self._column_name = column_name

    def set_column_type(self, column_type) -> None:
        self._column_type = column_type

    def set_comment(self, comment: Optional[str]) -> None:
        self._comment = comment

    @property
    def source(self) -> str:
        res = f"{self._column_name} {self.column_type.source}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


class DDLPrimaryKey(SQLBase):
    def __init__(self, column: str):
        self._column: str = column

    @property
    def column(self) -> str:
        return self._column

    @property
    def source(self) -> str:
        return f"PRIMARY KEY ({self._column})" if self._column is not None else ""


class DDLUniqueKey(SQLBase):
    def __init__(self, name: str, columns: List[str]):
        self._name = name
        self._columns = columns

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> List[str]:
        return self._columns

    @property
    def source(self) -> str:
        if len(self.columns) > 0:
            columns_str = ", ".join([f"{column}" for column in self.columns])
            return f"UNIQUE KEY {self.name} ({columns_str})"


class DDLKey(SQLBase):
    def __init__(self, name: str, columns: List[str]):
        self._name: str = name
        self._columns: List[str] = columns

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> List[str]:
        return self._columns

    @property
    def source(self) -> str:
        if len(self.columns) > 0:
            columns_str = ", ".join([f"{column}" for column in self.columns])
            return f"KEY {self.name} ({columns_str})"


class DDLFulltextKey(SQLBase):
    def __init__(self, name: str, columns: List[str]):
        self._name: str = name
        self._columns: List[str] = columns

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> List[str]:
        return self._columns

    @property
    def source(self) -> str:
        if len(self.columns) > 0:
            columns_str = ", ".join([f"{column}" for column in self.columns])
            return f"FULLTEXT KEY {self.name} ({columns_str})"


class DDLForeignKey(SQLBase):
    def __init__(self, constraint_name: str, slave_columns: List[str], master_table_name: str,
                 master_columns: List[str]):
        """

        Parameters
        ----------
        constraint_name : str
            外键约束名称
        slave_columns : List[str]
            从表的字段
        master_table_name : str
            主表名称
        master_columns : List[str]
            主表的字段名
        """
        self.constraint_name = constraint_name
        self.slave_columns = slave_columns
        self.master_table_name = master_table_name
        self.master_columns = master_columns

    @property
    def source(self) -> str:
        slave_columns_str = ", ".join([f"{column}" for column in self.slave_columns])
        master_columns_str = ", ".join([f"{column}" for column in self.master_columns])
        return f"CONSTRAINT {self.constraint_name} FOREIGN KEY({slave_columns_str}) REFERENCES {self.master_table_name}({master_columns_str})"


# ------------------------------ 表达式层级 ------------------------------


class DDLCreateTableStatement(SQLBase, abc.ABC):
    """【DDL】CREATE TABLE 语句"""

    def __init__(self,
                 schema_name: Optional[str] = None,
                 table_name: Optional[str] = None,
                 comment: Optional[str] = None):
        self._schema_name = schema_name
        self._table_name = table_name
        self._comment = comment

    @property
    def schema_name(self):
        return self._schema_name

    def set_schema_name(self, schema_name: str):
        self._schema_name = schema_name

    @property
    def table_name(self):
        return self._table_name

    def set_table_name(self, table_name: str):
        self._table_name = table_name

    @property
    def comment(self):
        return self._comment

    def set_comment(self, comment: str):
        self._comment = comment
