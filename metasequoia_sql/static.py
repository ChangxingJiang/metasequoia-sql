"""将每个 Mysql 类型转换为 Hive 类型"""
HASHMAP_MYSQL_TO_HIVE = {
    # 串数据类型
    "CHAR": "STRING",
    "VARCHAR": "STRING",
    "ENUM": "STRING",
    "SET": "STRING",
    "TINYTEXT": "STRING",
    "TEXT": "STRING",
    "MEDIUMTEXT": "STRING",
    "LONGTEXT": "STRING",
    "JSON": "STRING",
    # 数值数据类型
    "BIT": "TINYINT",
    "BOOLEAN": "TINYINT",
    "BOOL": "TINYINT",
    "TINYINT": "TINYINT",
    "SMALLINT": "SMALLINT",
    "MEDIUMINT": "BIGINT",
    "BIGINT": "BIGINT",
    "INT": "INT",
    "INTEGER": "INT",
    "FLOAT": "FLOAT",
    "REAL": "FLOAT",
    "DOUBLE": "DOUBLE",
    "DECIMAL": "DECIMAL",
    "DEC": "DECIMAL",
    # 日期和时间数据类型
    "DATE": "STRING",
    "TIME": "STRING",
    "DATETIME": "STRING",
    "TIMESTAMP": "STRING",
    "YEAR": "INT",
    # 二进制数据类型
    "BLOB": "STRING",
    "MEDIUMBLOB": "STRING",
    "LONGBLOB": "STRING",
    "TINYBLOB": "STRING",
    "BINARY": "STRING",
    "VARBINARY": "STRING"
}