"""
MySQL 专用的语法对象
"""

from metasequoia_sql.objects.common import *
from metasequoia_sql.objects.core import *

__all__ = ["DDLColumnTypeMySQL", "DDLColumnMySQL", "DDLPrimaryKeyMySQL", "DDLUniqueKeyMySQL", "DDLKeyMySQL",
           "DDLForeignKeyMySQL", "DDLFulltextKeyMysql", "DDLCreateTableStatementMySQL"]


class DDLColumnTypeMySQL(SQLColumnType):
    """【DDL】MySQL 的字段类型对象"""


class DDLColumnMySQL(DDLColumn):
    """【DDL】建表语句或修改表结构语句中的字段信息"""

    def __init__(self, column_name: str,
                 column_type: SQLGeneralExpression,
                 is_unsigned: bool = False,
                 is_zerofill: bool = False,
                 character_set: Optional[str] = None,
                 collate: Optional[str] = None,
                 is_allow_null: bool = False,
                 is_not_null: bool = False,
                 is_auto_increment: bool = False,
                 default: Optional[SQLGeneralExpression] = None,
                 on_update: Optional[SQLGeneralExpression] = None,
                 comment: Optional[str] = None
                 ):
        super().__init__(column_name, column_type, comment)
        self.is_unsigned: bool = is_unsigned
        self.is_zerofill: bool = is_zerofill
        self.character_set: Optional[str] = character_set
        self.collate: Optional[str] = collate
        self.is_allow_null: bool = is_allow_null  # 是否显式地允许 NULL 值
        self.is_not_null: bool = is_not_null
        self.is_auto_increment: bool = is_auto_increment
        self.default: Optional[SQLGeneralExpression] = default
        self.on_update: Optional[SQLGeneralExpression] = on_update

    def set_is_unsigned(self, is_unsigned: bool) -> None:
        self.is_unsigned = is_unsigned

    def set_is_allow_null(self, is_allow_null: bool) -> None:
        self.is_allow_null = is_allow_null

    def set_is_zerofill(self, is_zerofill: bool) -> None:
        self.is_zerofill = is_zerofill

    def set_character_set(self, character_set: Optional[str]) -> None:
        self.character_set = character_set

    def set_collate(self, collate: Optional[str]) -> None:
        self.collate = collate

    def set_is_not_null(self, is_not_null: bool) -> None:
        self.is_not_null = is_not_null

    def set_is_auto_increment(self, is_auto_increment: bool) -> None:
        self.is_auto_increment = is_auto_increment

    def set_default(self, default: Optional[str]):
        self.default = default

    def set_on_update(self, on_update: Optional[str]):
        self.on_update = on_update

    def source(self) -> str:
        res = f"{self._column_name} {self.column_type.source()}"
        if self.is_unsigned is True:
            res += " UNSIGNED"
        if self.is_zerofill is True:
            res += " ZEROFILL"
        if self.character_set is not None:
            res += f" CHARACTER SET {self.character_set}"
        if self.collate is not None:
            res += f" COLLATE {self.collate}"
        if self.is_allow_null is True:
            res += " NULL"
        if self.is_not_null is True:
            res += " NOT NULL"
        if self.is_auto_increment is True:
            res += " AUTO_INCREMENT"
        if self.default is not None:
            res += f" DEFAULT {self.default.source}"
        if self.on_update is not None:
            res += f" ON UPDATE {self.on_update.source}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


class DDLPrimaryKeyMySQL(DDLPrimaryKey):
    """【DDL】主键索引"""


class DDLUniqueKeyMySQL(DDLUniqueKey):
    """【DDL】唯一索引"""


class DDLKeyMySQL(DDLKey):
    """【DDL】索引"""


class DDLForeignKeyMySQL(DDLForeignKey):
    """【DDL】外键索引"""


class DDLFulltextKeyMysql(DDLFulltextKey):
    """【DDL】"""


class DDLCreateTableStatementMySQL(DDLCreateTableStatement):
    """CREATE TABLE 表达式"""

    def __init__(self,
                 schema_name: Optional[str] = None,
                 table_name: Optional[str] = None,
                 comment: Optional[str] = None,
                 if_not_exists: bool = False,
                 columns: Optional[List[DDLColumnMySQL]] = None,
                 primary_key: Optional[DDLPrimaryKeyMySQL] = None,
                 unique_key: Optional[List[DDLUniqueKeyMySQL]] = None,
                 key: Optional[List[DDLKeyMySQL]] = None,
                 fulltext_key: Optional[List[DDLFulltextKeyMysql]] = None,
                 foreign_key: List[DDLForeignKeyMySQL] = None,
                 engine: Optional[str] = None,
                 auto_increment: Optional[int] = None,
                 default_charset: Optional[str] = None,
                 collate: Optional[str] = None,
                 row_format: Optional[str] = None,
                 states_persistent: Optional[str] = None
                 ):
        super().__init__(schema_name=schema_name, table_name=table_name, comment=comment)
        self.if_not_exists = if_not_exists

        # 列信息
        self.columns = columns if columns is not None else []

        # 索引信息
        self.primary_key = primary_key
        self.unique_key = unique_key if unique_key is not None else []
        self.key = key if key is not None else []
        self.fulltext_key = fulltext_key if fulltext_key is not None else []
        self.foreign_key = foreign_key if foreign_key is not None else []

        # 表特性
        self.engine = engine
        self.auto_increment = auto_increment
        self.default_charset = default_charset
        self.collate = collate
        self.row_format = row_format
        self.states_persistent = states_persistent

    def set_collate(self, collate: Optional[str]) -> None:
        self.collate = collate

    def set_if_not_exists(self, if_not_exists: bool):
        self.if_not_exists = if_not_exists

    def set_primary_key(self, primary_key: DDLPrimaryKeyMySQL):
        self.primary_key = primary_key

    def remove_all_key(self):
        """移除所有索引"""
        self.primary_key = None
        self.unique_key = []
        self.key = []

    def add_unique_key(self, unique_key: DDLUniqueKeyMySQL):
        self.unique_key.append(unique_key)

    def add_key(self, key: DDLKeyMySQL):
        self.key.append(key)

    def add_foreign_key(self, foreign_key: DDLForeignKeyMySQL):
        self.foreign_key.append(foreign_key)

    def add_fulltext_key(self, fulltext_key: DDLFulltextKeyMysql):
        self.fulltext_key.append(fulltext_key)

    def set_engine(self, engine: Optional[str]):
        self.engine = engine

    def set_table_auto_increment(self, auto_increment: int):
        self.auto_increment = auto_increment

    def remove_table_auto_increment(self):
        self.auto_increment = None  # 移除表的自增属性
        for column in self.columns:
            column.set_is_auto_increment(False)  # 将每个字段的自增属性置为 False

    def set_default_charset(self, default_charset: Optional[str]):
        self.default_charset = default_charset

    def set_row_format(self, row_format: Optional[str]):
        self.row_format = row_format

    def remove_unsigned(self):
        """移除每个字段的 UNSIGNED 属性"""
        for column in self.columns:
            column.set_is_unsigned(False)

    def remove_on_update(self):
        """移除每个字段的 ON UPDATE 属性"""
        for column in self.columns:
            column.set_on_update(None)

    def remove_default(self):
        """移除每个字段的 DEFAULT 属性"""
        for column in self.columns:
            column.set_default(None)

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        for column in self.columns:
            old_column_type = column.column_type.name
            new_column_type = hashmap[old_column_type.upper()]
            column.column_type._name = new_column_type
            if remove_param is True:
                column.column_type._function_params = []

    def append_column(self, column: DDLColumnMySQL):
        """添加字段"""
        self.columns.append(column)

    def source(self, n_indent: int = 4) -> str:
        indentation = " " * n_indent  # 缩进字符串
        result = "CREATE TABLE"
        if self.if_not_exists is True:
            result += " IF NOT EXISTS"
        result += " "
        if self._schema_name is not None:
            result += f"`{self._schema_name}`."
        result += f"`{self._table_name}`(\n"
        columns_and_keys = []
        for column in self.columns:
            columns_and_keys.append(f"{indentation}{column.source()}")
        if self.primary_key is not None:
            columns_and_keys.append(f"{indentation}{self.primary_key.source}")
        for unique_key in self.unique_key:
            columns_and_keys.append(f"{indentation}{unique_key.source}")
        for key in self.key:
            columns_and_keys.append(f"{indentation}{key.source}")
        for fulltext_key in self.fulltext_key:
            columns_and_keys.append(f"{indentation}{fulltext_key.source}")
        for foreign_key in self.foreign_key:
            columns_and_keys.append(f"{indentation}{foreign_key.source}")
        result += ",\n".join(columns_and_keys)
        result += "\n)"
        if self.engine is not None:
            result += f" ENGINE = {self.engine}"
        if self.auto_increment is not None:
            result += f" AUTO_INCREMENT = {self.auto_increment}"
        if self.default_charset is not None:
            result += f" DEFAULT CHARSET = {self.default_charset}"
        if self.collate is not None:
            result += f" COLLATE = {self.collate}"
        if self.states_persistent is not None:
            result += f" STATS_PERSISTENT = {self.states_persistent}"
        if self._comment is not None:
            result += f" COMMENT = {self._comment}"
        result += ";"
        return result
