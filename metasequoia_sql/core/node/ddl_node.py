"""
抽象语法树（AST）的 DDL 类节点
"""

import abc
import dataclasses
from typing import Optional, Tuple, Dict

from metasequoia_sql.core.node.abc_node import ASTBase
from metasequoia_sql.core.node.objects import (
    ASTGeneralExpression, ASTTableNameExpression, ASTConfigNameExpression, ASTConfigValueExpression
)
from metasequoia_sql.core.node.sql_type import SQLType
from metasequoia_sql.errors import SqlParseError

__all__ = [
    "ASTColumnTypeExpression",  # 字段类型表达式
    "ASTDefineColumnExpression",  # 字段定义表达式

    "ASTIndexColumn",  # 索引声明表达式中的字段
    "ASTIndexExpressionBase",  # 索引声明表达式（抽象类）
    "ASTPrimaryIndexExpression",  # 主键索引声明表达式
    "ASTUniqueIndexExpression",  # 唯一键索引声明表达式
    "ASTNormalIndexExpression",  # 普通索引声明表达式
    "ASTFulltextIndexExpression",  # 全文本索引声明表达式

    "ASTForeignKeyExpression",  # 声明外键表达式

    "ASTCreateTableStatement",  # 建表语句（CREATE TABLE）
]


# ---------------------------------------- 字段类型表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnTypeExpression(ASTBase):
    """字段类型表达式"""

    name: str = dataclasses.field(kw_only=True)
    params: Optional[Tuple[ASTGeneralExpression, ...]] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.params is None or data_source == SQLType.HIVE:
            return self.name
        # MySQL 标准导出逗号间没有空格
        type_params = "(" + ",".join([param.source(data_source) for param in self.params]) + ")"
        return f"{self.name}{type_params}"


# ---------------------------------------- 声明字段表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTDefineColumnExpression(ASTBase):
    # pylint: disable=R0902 忽略对象属性过多的问题
    """声明字段表达式"""

    column_name: str = dataclasses.field(kw_only=True)
    column_type: ASTColumnTypeExpression = dataclasses.field(kw_only=True)
    is_unsigned: bool = dataclasses.field(kw_only=True, default=False)
    is_zerofill: bool = dataclasses.field(kw_only=True, default=False)
    character_set: Optional[str] = dataclasses.field(kw_only=True, default=None)
    collate: Optional[str] = dataclasses.field(kw_only=True, default=None)
    is_allow_null: bool = dataclasses.field(kw_only=True, default=False)
    is_not_null: bool = dataclasses.field(kw_only=True, default=False)
    is_auto_increment: bool = dataclasses.field(kw_only=True, default=False)
    default: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True, default=None)
    on_update: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True, default=None)
    comment: Optional[str] = dataclasses.field(kw_only=True, default=None)

    @property
    def column_name_without_quote(self) -> str:
        """返回没有被引号框柱的列名"""
        return self.column_name

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        res = f"`{self.column_name}` {self.column_type.source(data_source)}"
        res += " UNSIGNED" if self.is_unsigned is True and data_source == SQLType.MYSQL else ""
        if self.is_zerofill is True and data_source == SQLType.MYSQL:
            res += " ZEROFILL"
        if self.character_set is not None and data_source == SQLType.MYSQL:
            res += f" CHARACTER SET {self.character_set}"
        if self.collate is not None and data_source == SQLType.MYSQL:
            res += f" COLLATE {self.collate}"
        if self.is_allow_null is True and data_source == SQLType.MYSQL:
            res += " NULL"
        if self.is_not_null is True and data_source == SQLType.MYSQL:
            res += " NOT NULL"
        if self.is_auto_increment is True and data_source == SQLType.MYSQL:
            res += " AUTO_INCREMENT"
        if self.default is not None and data_source == SQLType.MYSQL:
            res += f" DEFAULT {self.default.source(data_source)}"
        if self.on_update is not None and data_source == SQLType.MYSQL:
            res += f" ON UPDATE {self.on_update.source(data_source)}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


# ---------------------------------------- 声明索引表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTIndexColumn(ASTBase):
    """索引声明表达式中的字段"""

    name: str = dataclasses.field(kw_only=True)  # 字段名
    max_length: Optional[int] = dataclasses.field(kw_only=True, default=None)  # 最大长度

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.max_length is None:
            return f"`{self.name}`"
        return f"`{self.name}`({self.max_length})"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTIndexExpressionBase(ASTBase, abc.ABC):
    """声明索引表达式"""

    name: Optional[str] = dataclasses.field(kw_only=True, default=None)
    columns: Tuple[ASTIndexColumn, ...] = dataclasses.field(kw_only=True)
    using: Optional[str] = dataclasses.field(kw_only=True, default=None)
    comment: Optional[str] = dataclasses.field(kw_only=True, default=None)
    key_block_size: Optional[int] = dataclasses.field(kw_only=True, default=None)

    def _source(self, data_source: SQLType, index_type: str):
        if self.columns is None:
            return ""
        name_str = f" {self.name}" if self.name is not None else ""
        columns_str = ",".join([f"{column.source(data_source)}" for column in self.columns])
        using_str = f" USING {self.using}" if self.using is not None else ""
        comment_str = f" COMMENT {self.comment}" if self.comment is not None else ""
        config_str = f" KEY_BLOCK_SIZE={self.key_block_size}" if self.key_block_size is not None else ""
        return f"{index_type}{name_str} ({columns_str}){using_str}{comment_str}{config_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTPrimaryIndexExpression(ASTIndexExpressionBase):
    """主键索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(data_source, "PRIMARY KEY")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUniqueIndexExpression(ASTIndexExpressionBase):
    """唯一键索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(data_source, "UNIQUE KEY")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTNormalIndexExpression(ASTIndexExpressionBase):
    """普通索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(data_source, "KEY")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFulltextIndexExpression(ASTIndexExpressionBase):
    """全文本索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(data_source, "FULLTEXT KEY")


# ---------------------------------------- 声明外键表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTForeignKeyExpression(ASTBase):
    """声明外键表达式"""

    constraint_name: str = dataclasses.field(kw_only=True)
    slave_columns: Tuple[str, ...] = dataclasses.field(kw_only=True)
    master_table_name: str = dataclasses.field(kw_only=True)
    master_columns: Tuple[str, ...] = dataclasses.field(kw_only=True)
    on_delete_cascade: bool = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        slave_columns_str = ", ".join([f"{column}" for column in self.slave_columns])
        master_columns_str = ", ".join([f"{column}" for column in self.master_columns])
        on_delete_cascade_str = " ON DELETE CASCADE" if self.on_delete_cascade else ""
        return (f"CONSTRAINT {self.constraint_name} FOREIGN KEY ({slave_columns_str}) "
                f"REFERENCES {self.master_table_name} ({master_columns_str}){on_delete_cascade_str}")


# ---------------------------------------- CREATE TABLE 语句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCreateTableStatement(ASTBase):
    # pylint: disable=R0902 忽略对象属性过多的问题

    """【DDL】CREATE TABLE 语句"""

    table_name: ASTTableNameExpression = dataclasses.field(kw_only=True)
    if_not_exists: bool = dataclasses.field(kw_only=True)
    columns: Optional[Tuple[ASTDefineColumnExpression, ...]] = dataclasses.field(kw_only=True)
    primary_key: Optional[ASTPrimaryIndexExpression] = dataclasses.field(kw_only=True)
    unique_key: Optional[Tuple[ASTUniqueIndexExpression, ...]] = dataclasses.field(kw_only=True)
    key: Optional[Tuple[ASTNormalIndexExpression, ...]] = dataclasses.field(kw_only=True)
    fulltext_key: Optional[Tuple[ASTFulltextIndexExpression, ...]] = dataclasses.field(kw_only=True)
    foreign_key: Tuple[ASTForeignKeyExpression, ...] = dataclasses.field(kw_only=True)
    partitioned_by: Tuple[ASTDefineColumnExpression, ...] = dataclasses.field(kw_only=True)
    comment: Optional[str] = dataclasses.field(kw_only=True)
    engine: Optional[str] = dataclasses.field(kw_only=True)
    auto_increment: Optional[int] = dataclasses.field(kw_only=True)
    default_charset: Optional[str] = dataclasses.field(kw_only=True)
    collate: Optional[str] = dataclasses.field(kw_only=True)
    row_format: Optional[str] = dataclasses.field(kw_only=True)
    states_persistent: Optional[str] = dataclasses.field(kw_only=True)
    row_format_serde: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    stored_as_inputformat: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    outputformat: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    location: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    tblproperties: Optional[Tuple[Tuple[ASTConfigNameExpression, ASTConfigValueExpression], ...]] = dataclasses.field(
        kw_only=True, default=None)  # Hive

    def set_table_name(self, table_name_expression: ASTTableNameExpression) -> "ASTCreateTableStatement":
        """设置表名并返回新对象"""
        table_params = self.get_params_dict()
        table_params["table_name"] = table_name_expression
        return ASTCreateTableStatement(**table_params)

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        table_params = self.get_params_dict()
        new_columns = []
        for old_column in self.columns:
            column_params = old_column.get_params_dict()
            column_params["column_type"] = ASTColumnTypeExpression(
                name=hashmap[old_column.column_type.name.upper()],
                params=None if remove_param else old_column.column_type.params)
            new_columns.append(ASTDefineColumnExpression(**column_params))
        table_params["columns"] = new_columns
        return ASTCreateTableStatement(**table_params)

    def append_column(self, column: ASTDefineColumnExpression):
        """添加字段"""
        table_params = self.get_params_dict()
        table_params["columns"] += (column,)
        return ASTCreateTableStatement(**table_params)

    def append_partition_by_column(self, column: ASTDefineColumnExpression):
        """添加分区字段"""
        table_params = self.get_params_dict()
        table_params["partitioned_by"] += (column,)
        return ASTCreateTableStatement(**table_params)

    def source(self, data_source: SQLType, n_indent: int = 2) -> str:
        """返回语法节点的 SQL 源码"""
        if data_source == SQLType.MYSQL:
            return self._source_mysql(n_indent=n_indent)
        if data_source == SQLType.HIVE:
            return self._source_hive(n_indent=n_indent)
        raise SqlParseError(f"暂不支持的数据类型: {data_source}")

    def _source_mysql(self, n_indent: int):
        indentation = " " * n_indent  # 缩进字符串
        result = f"{self._title_str(SQLType.MYSQL)} (\n"
        columns_and_keys = []
        for column in self.columns:
            columns_and_keys.append(f"{indentation}{column.source(SQLType.MYSQL)}")
        if self.primary_key is not None:
            columns_and_keys.append(f"{indentation}{self.primary_key.source(SQLType.MYSQL)}")
        for unique_key in self.unique_key:
            columns_and_keys.append(f"{indentation}{unique_key.source(SQLType.MYSQL)}")
        for key in self.key:
            columns_and_keys.append(f"{indentation}{key.source(SQLType.MYSQL)}")
        for fulltext_key in self.fulltext_key:
            columns_and_keys.append(f"{indentation}{fulltext_key.source(SQLType.MYSQL)}")
        for foreign_key in self.foreign_key:
            columns_and_keys.append(f"{indentation}{foreign_key.source(SQLType.MYSQL)}")
        result += ",\n".join(columns_and_keys)
        result += "\n)"
        result += f" ENGINE={self.engine}" if self.engine is not None else ""
        result += f" AUTO_INCREMENT={self.auto_increment}" if self.auto_increment is not None else ""
        result += f" DEFAULT CHARSET={self.default_charset}" if self.default_charset is not None else ""
        result += f" COLLATE={self.collate}" if self.collate is not None else ""
        result += f" ROW_FORMAT={self.row_format}" if self.row_format is not None else ""
        result += f" STATS_PERSISTENT={self.states_persistent}" if self.states_persistent is not None else ""
        result += f" COMMENT={self.comment}" if self.comment is not None else ""
        return result

    def _source_hive(self, n_indent: int):
        indentation = " " * n_indent  # 缩进字符串
        result = f" {self._title_str(SQLType.HIVE)}(\n"
        columns_and_keys = []
        for column in self.columns:
            columns_and_keys.append(f"{indentation}{column.source(SQLType.HIVE)}")
        result += ",\n".join(columns_and_keys)
        result += "\n)"
        if self.comment is not None:
            result += f" COMMENT {self.comment}"
        if len(self.partitioned_by) > 0:
            partition_columns = []
            for column in self.partitioned_by:
                partition_columns.append(column.source(SQLType.HIVE))
            partition_str = ", ".join(partition_columns)
            result += f" PARTITIONED BY ({partition_str})"
        result += f" ROW FORMAT SERDE {self.row_format_serde}" if self.row_format_serde is not None else ""
        result += (f" STORED AS INPUTFORMAT {self.stored_as_inputformat}"
                   if self.stored_as_inputformat is not None else "")
        result += f" OUTPUTFORMAT {self.outputformat}" if self.outputformat is not None else ""
        result += f" LOCATION {self.location}" if self.location is not None else ""
        if len(self.tblproperties) > 0:
            tblproperties_str = ", ".join([f"{config_name.source(SQLType.HIVE)}={config_value.source(SQLType.HIVE)}"
                                           for config_name, config_value in self.tblproperties])
            result += f"TBLPROPERTIES ({tblproperties_str})"
        return result

    def _title_str(self, data_source: SQLType) -> str:
        is_not_exists_str = " IF NOT EXISTS" if self.if_not_exists is True else ""
        return f"CREATE TABLE{is_not_exists_str} {self.table_name.source(data_source)}"
