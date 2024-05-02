"""
在主逻辑中没有使用的静态常量
"""

# MySQL 保留字
MYSQL_KEYWORDS = {
    "ACTION", "ADD", "ALL", "ALTER", "ANALYZE", "AND", "AS", "ASC", "ASENSITIVE", "BEFORE", "BETWEEN", "BIGINT",
    "BINARY", "BIT", "BLOB", "BOTH", "BY", "CALL", "CASCADE", "CASE", "CHANGE", "CHAR", "CHARACTER", "CHECK", "COLLATE",
    "COLUMN", "CONDITION", "CONNECTION", "CONSTRAINT", "CONTINUE", "CONVERT", "CREATE", "CROSS", "CURRENT_DATE",
    "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_USER", "CURSOR", "DATABASE", "DATABASES", "DATE", "DAY_HOUR",
    "DAY_MICROSECOND", "DAY_MINUTE", "DAY_SECOND", "DEC", "DECIMAL", "DECLARE", "DEFAULT", "DELAYED", "DELETE", "DESC",
    "DESCRIBE", "DETERMINISTIC", "DISTINCT", "DISTINCTROW", "DIV", "DOUBLE", "DROP", "DUAL", "EACH", "ELSE", "ELSEIF",
    "ENCLOSED", "ENUM", "ESCAPED", "EXISTS", "EXIT", "EXPLAIN", "FALSE", "FETCH", "FLOAT", "FOR", "FORCE", "FOREIGN",
    "FROM", "FULLTEXT", "GOTO", "GRANT", "GROUP", "HAVING", "HIGH_PRIORITY", "HOUR_MICROSECOND", "HOUR_MINUTE",
    "HOUR_SECOND", "IF", "IGNORE", "IN", "INDEX", "INNER", "INOUT", "INSENSITIVE", "INSERT", "INT", "INTEGER",
    "INTERVAL", "INTO", "IS", "ITERATE", "JOIN", "KEY", "KEYS", "KILL", "LEADING", "LEAVE", "LEFT", "LIKE", "LIMIT",
    "LINES", "LOAD", "LOCALTIME", "LOCALTIMESTAMP", "LOCK", "LONG", "LONGBLOB", "LONGTEXT", "LOOP", "LOW_PRIORITY",
    "MATCH", "MEDIUMBLOB", "MEDIUMINT", "MEDIUMTEXT", "MIDDLEINT", "MINUTE_MICROSECOND", "MINUTE_SECOND", "MOD",
    "MODIFIES", "NATURAL", "NO", "NO_WRITE_TO_BINLOG", "NOT", "NULL", "NUMERIC", "OFFSET", "ON", "OPTIMIZE", "OPTION",
    "OPTIONALLY", "OR", "ORDER", "OUT", "OUTER", "OUTFILE", "PRECISION", "PRIMARY", "PROCEDURE", "PURGE", "READ",
    "READS", "REAL", "REFERENCES", "REGEXP", "RELEASE", "RENAME", "REPEAT", "REPLACE", "REQUIRE", "RESTRICT", "RETURN",
    "REVOKE", "RIGHT", "RLIKE", "SCHEMA", "SCHEMAS", "SECOND_MICROSECOND", "SELECT", "SENSITIVE", "SEPARATOR", "SET",
    "SHOW", "SMALLINT", "SONAME", "SPATIAL", "SPECIFIC", "SQL", "SQL_BIG_RESULT", "SQL_CALC_FOUND_ROWS",
    "SQL_SMALL_RESULT", "SQLEXCEPTION", "SQLSTATE", "SQLWARNING", "SSL", "STARTING", "STRAIGHT_JOIN", "TABLE",
    "TERMINATED", "TEXT", "THEN", "TIME", "TIMESTAMP", "TINYBLOB", "TINYINT", "TINYTEXT", "TO", "TRAILING", "TRIGGER",
    "TRUE", "UNDO", "UNION", "UNIQUE", "UNLOCK", "UNSIGNED", "UPDATE", "USAGE", "USE", "USING", "UTC_DATE", "UTC_TIME",
    "UTC_TIMESTAMP", "VALUES", "VARBINARY", "VARCHAR", "VARCHARACTER", "VARYING", "WHEN", "WHERE", "WHILE", "WITH",
    "WRITE", "XOR", "YEAR_MONTH", "ZEROFILL"
}

# MySQL 的数据类型：key 为数据类型名称，value 为数据类型支持的最少参数数量和最多参数数量
MYSQL_DATA_TYPE = {
    "CHAR": (0, 1),  # 1 ~ 255 个字符串的定长串；它的长度必须在创建时指定，否则 MySQL 假定为 CHAR(1)
    "ENUM": (1, 65536),  # 接受最多 65536 个串组成的一个预定义集合的某个串
    "LONGTEXT": (0, 1),  # 与 TEXT 相同，但最大长度为 4GB
    "MEDIUMTEXT": (0, 1),  # 与 TEXT 相同，但最大长度为 16K
    "SET": (1, 64),  # 接受最多 64 个串组成的一个预定义集合的零个或多个串
    "TEXT": (0, 1),  # 最大长度为 64K 的变长文本
    "TINYTEXT": (0, 1),  # 与 TEXT 相同，但最大长度为 255 字节
    "VARCHAR": (0, 1),  # 长度可变，最多不超过 65536 个字节的变长串
    "BIT": (0, 1),  # 位字段，1 ~ 64 位。（在 MySQL 5 之前，BIT 在功能上等价于 TINYINT）
    "BIGINT": (0, 1),  # 整数值，支持 -9223372036854775808 ~ 9223372036854775807（如果是 UNSIGNED，为 0 ~ 18446744073709551615）的数
    "BOOLEAN": (0, 0),  # 布尔标志，或者位 0 或者为 1，主要用于开 / 关标志
    "BOOL": (0, 0),  # 布尔标志，或者位 0 或者为 1，主要用于开 / 关标志
    "DECIMAL": (0, 2),  # 精度可变的浮点值
    "DEC": (0, 2),  # 精度可变的浮点值
    "DOUBLE": (0, 1),  # 双精度浮点数
    "FLOAT": (0, 1),  # 单精度浮点数
    "INT": (0, 1),  # 整数值，支持 -2147463648 ~ 2147483647（如果是 UNSIGNED，为 0 ~ 4294967295）的数
    "INTEGER": (0, 1),  # 整数值，支持 -2147463648 ~ 2147483647（如果是 UNSIGNED，为 0 ~ 4294967295）的数
    "MEDIUMINT": (0, 1),  # 整数值，支持 -8388608 ~ 8388607（如果是 UNSIGNED，为 0 ~ 16777215）的数
    "REAL": (0, 1),  # 4 字节的浮点值
    "SMALLINT": (0, 1),  # 整数值，支持 -32768 ~ 32767（如果是 UNSIGNED，为 0 ~ 65536）的数
    "TINYINT": (0, 1),  # 整数值，支持 -128 ~ 127（如果是 UNSIGNED，为 0 ~ 255）的数
    "DATE": (0, 0),  # 表示 1000-01-01 ~ 9999-12-31 的日期，格式为 YYYY-MM-DD
    "DATETIME": (0, 0),  # DATE 和 TIME 的组合
    "TIMESTAMP": (0, 0),  # 功能和 DATETIME 相同（但范围较小）
    "TIME": (0, 0),  # 格式为 HH:MM:SS
    "YEAR": (0, 0),  # 用两位数字表示，范围是 70（1970年）~ 69（2069年）；用四位数字表示，范围是 1901 年 ~ 2155 年
    "TINYBLOB": (0, 1),  # 二进制数据类型，最大长度为 255 字节
    "BLOB": (0, 1),  # 二进制数据类型，最大长度为 64KB
    "MEDIUMBLOB": (0, 1),  # 二进制数据类型，最大长度为 16MB
    "LONGBLOB": (0, 1),  # 二进制数据类型，最大长度为 4GB
}

# 将每个 Mysql 类型转换为 Hive 类型  TODO 待整理所有主逻辑中未使用的静态常量
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
