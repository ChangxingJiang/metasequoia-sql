"""
语法逻辑测试：标识符
"""

from metasequoia_sql_new import LexFSM
from metasequoia_sql_new import parse

if __name__ == "__main__":
    print(parse(LexFSM("hello")))
    print(parse(LexFSM("hello1.`hello2`")))
    print(parse(LexFSM("hello1.hello2.hello3")))
    print(parse(LexFSM("hello1.hello2.hello3,hi1")))
