"""
词法解析器的有限状态自动机
"""

from metasequoia_parser.common import Terminal
from metasequoia_parser.lexical import LexicalFSM

from metasequoia_sql_new.lexical.lex_constants import LEX_SKIP_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_START_STATE_MAP
from metasequoia_sql_new.lexical.lex_states import LexStates
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "LexFSM"
]


class LexFSM(LexicalFSM):
    """SQL 词法解析器"""

    def __init__(self, text: str):
        super().__init__(text)
        self.length = len(text)

        self.state: LexStates = LexStates.LEX_START  # 当前自动机状态
        self.idx: int = 0  # 当前下标

        self.start_idx: int = 0  # 当前终结符的开始下标

    def lex(self) -> Terminal:
        """解析并生成一个终结符"""
        while True:
            if terminal := LEX_ACTION_MAP[self.state](self) is not None:
                return terminal

    def skip(self) -> None:
        """"""
        while self.idx < self.length and self.text[self.idx] in LEX_SKIP_CHARSET:
            self.idx += 1

    def start_token(self) -> None:
        """开始当前 Token"""
        self.start_idx = self.idx


def lex_start_action(fsm: LexFSM) -> None:
    """处理 LEX_START 状态的逻辑，指向空白字符后的第 1 个有效字符"""
    ch = fsm.text[fsm.idx]
    while LEX_START_STATE_MAP[ch] == LexStates.LEX_SKIP:
        fsm.idx += 1
        if fsm.idx == fsm.length:
            fsm.state = LexStates.LEX_EOF
        ch = fsm.text[fsm.idx]
    fsm.start_token()
    fsm.state = LEX_START_STATE_MAP[ch]


def lex_plus_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_PLUS 状态的逻辑，指向 "+" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_PLUS, value="+")


# 处理各种状态的映射关系
LEX_ACTION_MAP = {
    LexStates.LEX_START: lex_start_action,
    LexStates.LEX_PLUS: lex_plus_action
}
