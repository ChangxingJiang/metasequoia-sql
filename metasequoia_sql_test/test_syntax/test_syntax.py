"""
语法逻辑测试：标识符
"""

from metasequoia_sql import LexFSM
from metasequoia_sql import parse_expression

if __name__ == "__main__":
    print(parse_expression("hello"))

    # 标识符
    # print(parse(LexFSM("hello")))
    # print(parse(LexFSM("hello1.`hello2`")))
    # print(parse(LexFSM("hello1.hello2.hello3")))
    # print(parse(LexFSM("hello1.hello2.hello3,hi1")))
    # print(parse(LexFSM("ST_COLLECT")))
    # print(parse(LexFSM("ADDDATE")))
    # print(parse(LexFSM("SUPER")))

    # 字面值
    # print(parse(LexFSM("1234")))
    # print(parse(LexFSM("0x0B")))
    # print(parse(LexFSM("0b10")))
    # print(parse(LexFSM("'abcd'")))
    # print(parse(LexFSM("n'abcd'")))
    # print(parse(LexFSM("null")))
    # print(parse(LexFSM("true")))
    # print(parse(LexFSM("false")))
    # print(parse(LexFSM("1.3")))
    # print(parse(LexFSM("1.3e-6")))
    # print(parse(LexFSM("'ab' 'cd'")))
    # print(parse(LexFSM("-3")))
    # print(parse(LexFSM("+3")))
    # print(parse(LexFSM("-3.5")))
    # print(parse(LexFSM("+3.5")))

    # 表达式
    # print(parse(LexFSM("3 + 5")))
    # print(parse(LexFSM("3 + 5 * 2")))
    # print(parse(LexFSM("3 + 5 * ~2")))
    # print(parse(LexFSM("'abc' + 5 * ~abc")))
    # print(parse(LexFSM("3 DIV 5 + 2")))
    # print(parse(LexFSM("3 MOD 5 + 2")))
    # print(parse(LexFSM("3 + 5 MEMBER OF ('[2,3,5]')")))
    # print(parse(LexFSM("name NOT LIKE '%abc%'")))
    # print(parse(LexFSM("name IS NULL")))
    # print(parse(LexFSM("name IS NOT NULL")))
    # print(parse(LexFSM("name > 3")))
    # print(parse(LexFSM("name1 XOR name2")))
    # print(parse(LexFSM("name1 AND name2")))
    # print(parse(LexFSM("NOT name2")))
    # print(parse(LexFSM("name1 IS TRUE")))

    # DQL 语句
    # print(parse(LexFSM("name1, name2 + 3")))  # GROUP BY 子句
    # print(parse(LexFSM("ORDER BY name1, name2 + 3 DESC")))  # ORDER BY 子句
    # print(parse(LexFSM("ORDER BY name1 ASC, name2 + 3 DESC")))  # ORDER BY 子句
    # print(parse(LexFSM("")))  # ORDER BY 子句

    # 窗口子句
    # print(parse(LexFSM("1 PRECEDING")))
    # print(parse(LexFSM("INTERVAL name + 1 YEAR PRECEDING")))
    # print(parse(LexFSM("CURRENT ROW")))
    # print(parse(LexFSM("UNBOUNDED PRECEDING")))
    # print(parse(LexFSM("OVER window_name")))
    # print(parse(LexFSM("OVER (window_name PARTITION BY field1, field2 ORDER BY field3, field4 DESC)")))
    # print(parse(LexFSM("OVER (window_name PARTITION BY field1 ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)")))

    # 测试语义组：opt_charset
    # print(parse(LexFSM("ASCII")))
    # print(parse(LexFSM("ASCII BINARY")))
    # print(parse(LexFSM("BINARY ASCII")))
    # print(parse(LexFSM("UNICODE")))
    # print(parse(LexFSM("UNICODE BINARY")))
    # print(parse(LexFSM("BINARY UNICODE")))
    # print(parse(LexFSM("BYTE")))
    # print(parse(LexFSM("BINARY")))
    # print(parse(LexFSM("CHAR SET charset_name")))
    # print(parse(LexFSM("CHARSET charset_name")))
    # print(parse(LexFSM("CHAR SET charset_name BINARY")))
    # print(parse(LexFSM("BINARY CHAR SET charset_name")))

    # 字段类型
    # print(parse(LexFSM("ENUM ('a', 'b', 'c') BINARY")))
    # print(parse(LexFSM("BLOB (3)")))
    # print(parse(LexFSM("NVARCHAR (15) BINARY ")))
    # print(parse(LexFSM("VARCHAR (15) BINARY ")))

    # Json 表配置
    # print(parse(LexFSM("NULL ON EMPTY")))
    # print(parse(LexFSM("ERROR ON ERROR")))
    # print(parse(LexFSM("NULL ON EMPTY DEFAULT 0 ON ERROR")))

    # 测试 in_sum_expr
    # print(parse(LexFSM("ALL 3 + 5 * 2")))

    # 测试 sum_expr
    # print(parse(LexFSM("max(distinct a)")))
    # print(parse(LexFSM("min(3 + 5 * 2)")))
    # print(parse(LexFSM("group_concat(distinct 3 + 5 * 2, field1 order by field1 separator ',')")))

    #
    print(parse(LexFSM("SELECT * FROM table_name")))
