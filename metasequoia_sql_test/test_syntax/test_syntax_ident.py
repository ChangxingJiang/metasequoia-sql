"""
语法逻辑测试：标识符
"""

from metasequoia_sql_new import LexFSM
from metasequoia_sql_new import parse

if __name__ == "__main__":
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
    print(parse(LexFSM("name1, name2 + 3 DESC")))  # ORDER BY 子句
    print(parse(LexFSM("name1 ASC, name2 + 3 DESC")))  # ORDER BY 子句
