from metasequoia_parser.common import Terminal

from metasequoia_sql_new.lexical.lex_fsm import LexFSM


def parse_one_token(text: str) -> Terminal:
    """从字符串 text 中解析一个 Token 并返回"""
    fsm = LexFSM(text)
    return fsm.lex()


if __name__ == "__main__":
    print(parse_one_token("3EFG"))
