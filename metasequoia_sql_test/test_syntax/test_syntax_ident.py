"""
语法逻辑测试：标识符
"""

from metasequoia_sql_new import LexFSM
from metasequoia_sql_new import parse

if __name__ == "__main__":
    lex = LexFSM("hello")
    print(parse(LexFSM("hello")))
