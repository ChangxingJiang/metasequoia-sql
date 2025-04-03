"""
词法解析器的有限状态自动机
"""

from typing import Optional

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
        self.state = LexStates.LEX_START
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


def lex_caret_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_CARET 状态的逻辑，指向 "^" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_CARET, value="^")


def lex_tilde_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_TILDE 状态的逻辑，指向 "~" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_TILDE, value="~")


def lex_percent_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_PERCENT 状态的逻辑，指向 "%" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_PERCENT, value="%")


def lex_sub_action(fsm: LexFSM) -> Optional[Terminal]:
    """处理 LEX_SUB 状态的逻辑，指向符号后的下一个字符

    尝试解析元素：`--`、`->`、`->>`、`-`
    """
    ch = fsm.text[fsm.idx + 1]  # "-" 之后的下一个字符
    if ch == "-":
        fsm.idx += 2
        fsm.state = LexStates.LEX_COMMENT
        return None
    if ch == ">":
        ch = fsm.text[fsm.idx + 1]  # "->" 之后的下一个字符
        if ch == ">":
            fsm.idx += 3
            return Terminal(symbol_id=TType.OPERATOR_SUB_GT_GT, value="->>")
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_SUB_GT, value="->")
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_SUB, value="-")


def lex_lt_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_LT 状态的逻辑，指向符号后的下一个字符

    尝试解析元素：`<>`、`<<`、`<=`、`<=>`、`<`
    """
    ch = fsm.text[fsm.idx + 1]
    if ch == ">":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_BANG_EQ, value="<>")
    if ch == "<":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_LT_LT, value="<<")
    if ch == "=":
        ch = fsm.text[fsm.idx + 2]
        if ch == ">":
            fsm.idx += 3
            return Terminal(symbol_id=TType.OPERATOR_LT_EQ_GT, value="<=>")
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_LT_EQ, value="<=")
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_LT, value="<")


def lex_ques_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_QUES 状态的逻辑，指向 "?" 后的下一个字符 TODO 待增加预编译模式的检查"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.PARAM_MARKER, value="?")


def lex_eq_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_PERCENT 状态的逻辑，指向 "=" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_EQ, value="=")


def lex_star_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_STAR 状态的逻辑，指向 "*" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_STAR, value="*")


def lex_lparen_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_LPAREN 状态的逻辑，指向 "(" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_LPAREN, value="(")


def lex_rparen_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_RPAREN 状态的逻辑，指向 ")" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_RPAREN, value=")")


def lex_comma_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_COMMA 状态的逻辑，指向 "," 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_COMMA, value=",")


def lex_lbrace_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_LBRACE 状态的逻辑，指向 "{" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_LBRACE, value="{")


def lex_rbrace_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_LBRACE 状态的逻辑，指向 "}" 后的下一个字符"""
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_RBRACE, value="}")


# 处理各种状态的映射关系
LEX_ACTION_MAP = {
    LexStates.LEX_START: lex_start_action,
    LexStates.LEX_EOF: None,
    LexStates.LEX_END: None,
    LexStates.LEX_CHAR: None,
    LexStates.LEX_ERROR: None,
    LexStates.LEX_PLUS: lex_plus_action,
    LexStates.LEX_CARET: lex_caret_action,
    LexStates.LEX_TILDE: lex_tilde_action,
    LexStates.LEX_PERCENT: lex_percent_action,
    LexStates.LEX_SUB: lex_sub_action,
    LexStates.LEX_LT: lex_lt_action,
    LexStates.LEX_GT: None,
    LexStates.LEX_QUES: lex_ques_action,
    LexStates.LEX_EQ: lex_eq_action,
    LexStates.LEX_STAR: lex_star_action,
    LexStates.LEX_SLASH: None,
    LexStates.LEX_BANG: None,
    LexStates.LEX_AMP: None,
    LexStates.LEX_BAR: None,
    LexStates.LEX_COLON: None,
    LexStates.LEX_LPAREN: lex_lparen_action,
    LexStates.LEX_RPAREN: lex_rparen_action,
    LexStates.LEX_COMMA: lex_comma_action,
    LexStates.LEX_LBRACE: lex_lbrace_action,
    LexStates.LEX_RBRACE: lex_rbrace_action,
    LexStates.LEX_IDENT_OR_HEX: None,
    LexStates.LEX_HEX_NUMBER: None,
    LexStates.LEX_IDENT_OR_BIN: None,
    LexStates.LEX_BIN_NUMBER: None,
    LexStates.LEX_IDENT: None,
    LexStates.LEX_DELIMITER: None,
    LexStates.LEX_STRING: None,
    LexStates.LEX_STRING_OR_DELIMITER: None,
    LexStates.LEX_IDENT_OR_NCHAR: None,
    LexStates.LEX_IDENT_SEP_START: None,
    LexStates.LEX_IDENT_START: None,
    LexStates.LEX_ZERO: None,
    LexStates.LEX_NUMBER: None,
    LexStates.LEX_NUMBER_DOT: None,
    LexStates.LEX_NUMBER_E: None,
    LexStates.LEX_DOT: None,
    LexStates.LEX_COMMENT: None,
    LexStates.LEX_LONG_COMMENT: None,
    LexStates.LEX_DOLLAR: None,
    LexStates.LEX_SEMICOLON: None,
    LexStates.LEX_AT: None,
    LexStates.LEX_AT_AT: None,
    LexStates.LEX_AT_AT_END: None,
    LexStates.LEX_AT_END: None,
}
