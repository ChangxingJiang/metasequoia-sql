"""
词法解析单元测试工具函数
"""

from typing import Tuple

from metasequoia_parser.common import Terminal

from metasequoia_sql.lexical.lex_fsm import LexFSM


def parse_one_token(text: str) -> Terminal:
    """从字符串 text 中解析一个 Token 并返回"""
    fsm = LexFSM(text)
    return fsm.lex()


def parse_two_token(text: str) -> Tuple[Terminal, Terminal]:
    """从字符串 text 中解析一个 Token 并返回"""
    fsm = LexFSM(text)
    token_1 = fsm.lex()
    token_2 = fsm.lex()
    return token_1, token_2


def parse_three_token(text: str) -> Tuple[Terminal, Terminal, Terminal]:
    """从字符串 text 中解析一个 Token 并返回"""
    fsm = LexFSM(text)
    token_1 = fsm.lex()
    token_2 = fsm.lex()
    token_3 = fsm.lex()
    return token_1, token_2, token_3


if __name__ == "__main__":
    # print(parse_one_token("3EFG"))
    print(parse_three_token("hello.SELECT"))
