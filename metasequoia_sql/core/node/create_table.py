"""
抽象语法树（AST）节点：CREATE TABLE 语句
"""

import abc
import dataclasses
from typing import Optional, Tuple, Dict

from metasequoia_sql.core.node.abc_node import ASTBase
from metasequoia_sql.core.node.dql_node import ASTExpressionBase, ASTTableNameExpression
from metasequoia_sql.core.sql_type import SQLType
from metasequoia_sql.errors import SqlParseError

__all__ = [
    "ASTConfigNameExpression",  # 配置名称表达式
    "ASTConfigValueExpression",  # 配置值表达式

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


# ---------------------------------------- 配置名称和配置值表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTConfigNameExpression(ASTBase):
    """配置名称表达式"""

    config_name: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_name


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTConfigValueExpression(ASTBase):
    """配置值表达式"""

    config_value: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_value


# ---------------------------------------- 字段类型表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnTypeExpression(ASTBase):
    """字段类型表达式"""

    name: str = dataclasses.field(kw_only=True)
    params: Optional[Tuple[ASTExpressionBase, ...]] = dataclasses.field(kw_only=True, default=None)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.params is None or sql_type == SQLType.HIVE:
            return self.name
        # MySQL 标准导出逗号间没有空格
        type_params = "(" + ",".join([param.source(sql_type) for param in self.params]) + ")"
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
    default: Optional[ASTExpressionBase] = dataclasses.field(kw_only=True, default=None)
    on_update: Optional[ASTExpressionBase] = dataclasses.field(kw_only=True, default=None)
    comment: Optional[str] = dataclasses.field(kw_only=True, default=None)

    @property
    def column_name_without_quote(self) -> str:
        """返回没有被引号框柱的列名"""
        return self.column_name

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        res = f"`{self.column_name}` {self.column_type.source(sql_type)}"
        res += " UNSIGNED" if self.is_unsigned is True and sql_type == SQLType.MYSQL else ""
        if self.is_zerofill is True and sql_type == SQLType.MYSQL:
            res += " ZEROFILL"
        if self.character_set is not None and sql_type == SQLType.MYSQL:
            res += f" CHARACTER SET {self.character_set}"
        if self.collate is not None and sql_type == SQLType.MYSQL:
            res += f" COLLATE {self.collate}"
        if self.is_allow_null is True and sql_type == SQLType.MYSQL:
            res += " NULL"
        if self.is_not_null is True and sql_type == SQLType.MYSQL:
            res += " NOT NULL"
        if self.is_auto_increment is True and sql_type == SQLType.MYSQL:
            res += " AUTO_INCREMENT"
        if self.default is not None and sql_type == SQLType.MYSQL:
            res += f" DEFAULT {self.default.source(sql_type)}"
        if self.on_update is not None and sql_type == SQLType.MYSQL:
            res += f" ON UPDATE {self.on_update.source(sql_type)}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


# ---------------------------------------- 声明索引表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTIndexColumn(ASTBase):
    """索引声明表达式中的字段"""

    name: str = dataclasses.field(kw_only=True)  # 字段名
    max_length: Optional[int] = dataclasses.field(kw_only=True, default=None)  # 最大长度

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
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

    def _source(self, sql_type: SQLType, index_type: str):
        if self.columns is None:
            return ""
        name_str = f" {self.name}" if self.name is not None else ""
        columns_str = ",".join([f"{column.source(sql_type)}" for column in self.columns])
        using_str = f" USING {self.using}" if self.using is not None else ""
        comment_str = f" COMMENT {self.comment}" if self.comment is not None else ""
        config_str = f" KEY_BLOCK_SIZE={self.key_block_size}" if self.key_block_size is not None else ""
        return f"{index_type}{name_str} ({columns_str}){using_str}{comment_str}{config_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTPrimaryIndexExpression(ASTIndexExpressionBase):
    """主键索引声明表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(sql_type, "PRIMARY KEY")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUniqueIndexExpression(ASTIndexExpressionBase):
    """唯一键索引声明表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(sql_type, "UNIQUE KEY")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTNormalIndexExpression(ASTIndexExpressionBase):
    """普通索引声明表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(sql_type, "KEY")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFulltextIndexExpression(ASTIndexExpressionBase):
    """全文本索引声明表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return self._source(sql_type, "FULLTEXT KEY")


# ---------------------------------------- 声明外键表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTForeignKeyExpression(ASTBase):
    """声明外键表达式"""

    constraint_name: str = dataclasses.field(kw_only=True)
    slave_columns: Tuple[str, ...] = dataclasses.field(kw_only=True)
    master_table_name: str = dataclasses.field(kw_only=True)
    master_columns: Tuple[str, ...] = dataclasses.field(kw_only=True)
    on_delete_cascade: bool = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
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
    primary_key: Optional[ASTPrimaryIndexExpression] = dataclasses.field(kw_only=True)  # MySQL
    unique_key: Optional[Tuple[ASTUniqueIndexExpression, ...]] = dataclasses.field(kw_only=True)  # MySQL
    key: Optional[Tuple[ASTNormalIndexExpression, ...]] = dataclasses.field(kw_only=True)  # MySQL
    fulltext_key: Optional[Tuple[ASTFulltextIndexExpression, ...]] = dataclasses.field(kw_only=True)  # MySQL
    foreign_key: Tuple[ASTForeignKeyExpression, ...] = dataclasses.field(kw_only=True)  # MySQL
    partitioned_by: Tuple[ASTDefineColumnExpression, ...] = dataclasses.field(kw_only=True)  # Hive
    comment: Optional[str] = dataclasses.field(kw_only=True)  # MySQL
    engine: Optional[str] = dataclasses.field(kw_only=True)  # MySQL
    auto_increment: Optional[int] = dataclasses.field(kw_only=True)  # MySQL
    default_charset: Optional[str] = dataclasses.field(kw_only=True)  # MySQL
    collate: Optional[str] = dataclasses.field(kw_only=True)  # MySQL
    row_format: Optional[str] = dataclasses.field(kw_only=True)  # MySQL
    states_persistent: Optional[str] = dataclasses.field(kw_only=True)  # MySQL
    row_format_serde: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    stored_as_inputformat: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    outputformat: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    location: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    tblproperties: Optional[Tuple[Tuple[ASTConfigNameExpression, ASTConfigValueExpression], ...]] = dataclasses.field(
        kw_only=True, default=None)  # Hive

    def set_table_name(self, table_name_expression: ASTTableNameExpression) -> "ASTCreateTableStatement":
        """设置表名并返回新对象"""
        params = self.get_params_dict()
        params["table_name"] = table_name_expression
        return ASTCreateTableStatement(**params)

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        params = self.get_params_dict()
        new_columns = []
        for old_column in self.columns:
            column_params = old_column.get_params_dict()
            column_params["column_type"] = ASTColumnTypeExpression(
                name=hashmap[old_column.column_type.name.upper()],
                params=None if remove_param else old_column.column_type.params)
            new_columns.append(ASTDefineColumnExpression(**column_params))
        params["columns"] = new_columns
        return ASTCreateTableStatement(**params)

    def append_column(self, column: ASTDefineColumnExpression):
        """添加字段"""
        params = self.get_params_dict()
        params["columns"] += (column,)
        return ASTCreateTableStatement(**params)

    def append_partition_by_column(self, column: ASTDefineColumnExpression):
        """添加分区字段"""
        params = self.get_params_dict()
        params["partitioned_by"] += (column,)
        return ASTCreateTableStatement(**params)

    def source(self, sql_type: SQLType = SQLType.DEFAULT, n_indent: int = 2) -> str:
        """返回语法节点的 SQL 源码"""
        if sql_type == SQLType.MYSQL:
            return self._source_mysql(n_indent=n_indent)
        if sql_type == SQLType.HIVE:
            return self._source_hive(n_indent=n_indent)
        raise SqlParseError(f"暂不支持的数据类型: {sql_type}")

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

    def _title_str(self, sql_type: SQLType) -> str:
        is_not_exists_str = " IF NOT EXISTS" if self.if_not_exists is True else ""
        return f"CREATE TABLE{is_not_exists_str} {self.table_name.source(sql_type)}"
