"""
MySQL 专用的语法对象
"""

from metasequoia_sql.objects.core import *

__all__ = ["DDLCreateTableStatementMySQL"]


class DDLCreateTableStatementMySQL(DDLCreateTableStatement):
    """CREATE TABLE 表达式"""

    def __init__(self,
                 schema_name: Optional[str] = None,
                 table_name: Optional[str] = None,
                 comment: Optional[str] = None,
                 if_not_exists: bool = False,
                 columns: Optional[List[DDLColumnExpression]] = None,
                 primary_key: Optional[DDLPrimaryIndexExpression] = None,
                 unique_key: Optional[List[DDLUniqueIndexExpression]] = None,
                 key: Optional[List[DDLNormalIndexExpression]] = None,
                 fulltext_key: Optional[List[DDLFulltextIndexExpression]] = None,
                 foreign_key: List[DDLForeignKeyExpression] = None,
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

    def set_if_not_exists(self, if_not_exists: bool):
        self.if_not_exists = if_not_exists

    def set_primary_key(self, primary_key: DDLPrimaryIndexExpression):
        self.primary_key = primary_key

    def add_unique_key(self, unique_key: DDLUniqueIndexExpression):
        self.unique_key.append(unique_key)

    def add_key(self, key: DDLNormalIndexExpression):
        self.key.append(key)

    def add_foreign_key(self, foreign_key: DDLForeignKeyExpression):
        self.foreign_key.append(foreign_key)

    def add_fulltext_key(self, fulltext_key: DDLFulltextIndexExpression):
        self.fulltext_key.append(fulltext_key)

    def set_engine(self, engine: Optional[str]):
        self.engine = engine

    def set_table_auto_increment(self, auto_increment: int):
        self.auto_increment = auto_increment

    def set_default_charset(self, default_charset: Optional[str]):
        self.default_charset = default_charset

    def set_row_format(self, row_format: Optional[str]):
        self.row_format = row_format

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        for column in self.columns:
            old_column_type = column.column_type.name
            new_column_type = hashmap[old_column_type.upper()]
            column.column_type._name = new_column_type
            if remove_param is True:
                column.column_type._function_params = []

    def append_column(self, column: DDLColumnExpression):
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
            columns_and_keys.append(f"{indentation}{column.source}")
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
