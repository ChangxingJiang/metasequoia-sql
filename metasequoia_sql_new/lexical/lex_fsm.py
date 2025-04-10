"""
词法解析器的有限状态自动机
"""

from typing import Optional

from metasequoia_parser.common import Terminal
from metasequoia_parser.lexical import LexicalFSM

from metasequoia_sql_new.lexical.lex_constants import LEX_BIN_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_BIN_MARK_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_ESCAPE_HASH
from metasequoia_sql_new.lexical.lex_constants import LEX_E_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_HEX_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_HEX_MARK_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_IDENT_MAP
from metasequoia_sql_new.lexical.lex_constants import LEX_IGNORE_ESCAPE_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_LINE_BREAK_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_PLUS_MINUS_SIGN_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_SPACE_CHARSET
from metasequoia_sql_new.lexical.lex_constants import LEX_START_STATE_MAP
from metasequoia_sql_new.lexical.lex_states import LexStates
from metasequoia_sql_new.terminal import KEYWORD_TO_TERMINAL_MAP
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "LexFSM"
]


class LexFSM(LexicalFSM):
    """SQL 词法解析器"""

    def __init__(self, text: str):
        text += "\x00"
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


def _find_end_mark(fsm: LexFSM, mark: str) -> str:
    """寻找对应的闭引号字符（mark），返回构造的字符串

    指针位置：
    1. 在开始时，指针指向开括号的下 1 个字符
    1. 如果遍历到输入流的末尾，则将指针指向末尾字符
    2. 如果遍历到闭括号字符，则将指针指向括号后的下一个字符

    其他处理逻辑：
    1. 将字符串中转义的 \n、\t、\r、\b、\0 恢复为原始字符
    2. 将转义符转移的闭引号字符恢复为原始字符
    3. 将连续两个转移的闭引号字符恢复为原始字符
    """
    result = []
    ch = fsm.text[fsm.idx]
    while ch != "\x00":
        if ch == "\\":
            ch = fsm.text[fsm.idx + 1]
            fsm.idx += 2
            if escaped := LEX_ESCAPE_HASH.get(ch):
                result.append(escaped)  # 处理转义符 \n、\t、\r、\b、\0
            elif ch in LEX_IGNORE_ESCAPE_CHARSET:
                result.append("\\")
                result.append(ch)
            else:
                result.append(ch)
        elif ch == mark:
            if fsm.text[fsm.idx + 1] == mark:
                fsm.idx += 2
                result.append(mark)
            else:
                return "".join(result)
        else:
            fsm.idx += 1
            result.append(ch)
        fsm.idx += 1
        ch = fsm.text[fsm.idx + 1]


def lex_start_action(fsm: LexFSM) -> None:
    """处理 LEX_START 状态的逻辑，指向空白字符后的第 1 个有效字符"""
    ch = fsm.text[fsm.idx]
    while LEX_START_STATE_MAP[ch] == LexStates.LEX_SKIP:
        fsm.idx += 1
        if fsm.idx == fsm.length:
            fsm.state = LexStates.LEX_EOF
        ch = fsm.text[fsm.idx]
    fsm.start_idx = fsm.idx
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

    如果将状态置为 LEX_COMMENT，则指向 `--` 符号后的下一个字符
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


def lex_gt_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_GT 状态的逻辑，指向符号后的下一个字符

    尝试解析元素：`>>`、`>=`、`>`
    """
    ch = fsm.text[fsm.idx + 1]
    if ch == ">":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_GT_GT, value=">>")
    if ch == "=":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_GT_EQ, value=">=")
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_GT, value=">")


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


def lex_slash_action(fsm: LexFSM) -> Optional[Terminal]:
    """处理 LEX_SLASH 状态的逻辑，指向符号后的下一个字符

    尝试匹配元素：`/*`、`/`
    """
    ch = fsm.text[fsm.idx + 1]
    if ch == "*":
        fsm.idx += 2
        fsm.state = LexStates.LEX_LONG_COMMENT
        return None
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_BANG, value="!")


def lex_bang_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_BANG 状态的逻辑，指向符号后的下一个字符

    尝试匹配元素：`!=`、`!`
    """
    ch = fsm.text[fsm.idx + 1]
    if ch == "=":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_BANG_EQ, value="!=")
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_BANG, value="!")


def lex_amp_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_AMP 状态的逻辑，指向符号后的下一个字符

    尝试匹配元素：`&&`、`&`
    """
    ch = fsm.text[fsm.idx + 1]
    if ch == "&":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_AMP_AMP, value="&&")
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_AMP, value="&")


def lex_bar_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_BAR 状态的逻辑，指向符号后的下一个字符

    尝试匹配元素：`||`、`|`
    """
    ch = fsm.text[fsm.idx + 1]
    if ch == "|":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_BAR_BAR, value="||")
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_BAR, value="|")


def lex_colon_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_COLON 状态的逻辑，指向符号后的下一个字符

    尝试匹配元素：`:=`、`:`
    """
    ch = fsm.text[fsm.idx + 1]
    if ch == "=":
        fsm.idx += 2
        return Terminal(symbol_id=TType.OPERATOR_COLON_EQ, value=":=")
    fsm.idx += 1
    return Terminal(symbol_id=TType.OPERATOR_COLON, value=":")


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


def lex_ident_or_hex_action(fsm: LexFSM) -> None:
    """处理 LEX_IDENT_OR_HEX 状态的逻辑，指向 x' 或 x 后的下一个字符"""
    ch = fsm.text[fsm.idx + 1]
    if ch == "'":
        fsm.idx += 2
        fsm.state = LexStates.LEX_HEX_NUMBER
        return None
    fsm.idx += 1
    fsm.state = LexStates.LEX_IDENT
    return None


def lex_hex_number_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_HEX_NUMBER 状态的逻辑，指向当前元素之后的第 1 个字符"""
    fsm.idx += 1
    ch = fsm.text[fsm.idx]
    while ch in LEX_HEX_CHARSET:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]
    if ch != "'":
        return Terminal(symbol_id=TType.SYSTEM_ABORT, value=None)
    fsm.idx += 1
    return Terminal(symbol_id=TType.LITERAL_HEX_NUM, value=fsm.text[fsm.start_idx + 2: fsm.idx - 1])


def lex_ident_or_bin_action(fsm: LexFSM) -> None:
    """处理 LEX_IDENT_OR_BIN 状态的逻辑，指向 b' 或 b 后的下一个字符"""
    ch = fsm.text[fsm.idx + 1]
    if ch == "'":
        fsm.idx += 2
        fsm.state = LexStates.LEX_BIN_NUMBER
        return None
    fsm.idx += 1
    fsm.state = LexStates.LEX_IDENT
    return None


def lex_bin_number_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_BIN_NUMBER 状态的逻辑，指向当前元素之后的第 1 个字符"""
    fsm.idx += 1
    ch = fsm.text[fsm.idx]
    while ch in LEX_BIN_CHARSET:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]
    if ch != "'":
        return Terminal(symbol_id=TType.SYSTEM_ABORT, value=None)
    fsm.idx += 1
    return Terminal(symbol_id=TType.LITERAL_BIN_NUM, value=fsm.text[fsm.start_idx + 2: fsm.idx - 1])


def lex_ident_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_IDENT 状态的逻辑，指向当前元素之后的第 1 个字符"""
    # 不断匹配数字、字母和多字节字符直至遇到其他字符
    fsm.idx += 1
    ch = fsm.text[fsm.idx]
    while LEX_IDENT_MAP.get(ch, True) is True:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]

    # 获取当前标识符 or 关键字
    ident_or_keyword = fsm.text[fsm.start_idx: fsm.idx]

    # 跳过后续空格
    while ch in LEX_SPACE_CHARSET:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]

    # 判断下一个字符是否为 . 且之后也是标识符
    if ch == "." and LEX_IDENT_MAP.get(ch, True) is True:
        fsm.state = LexStates.LEX_IDENT_SEP_START
        return Terminal(symbol_id=TType.IDENT, value=ident_or_keyword)

    # 判断当前语法元素是否为关键字
    if keyword_type := KEYWORD_TO_TERMINAL_MAP.get(ident_or_keyword.lower()):
        return Terminal(symbol_id=keyword_type, value=ident_or_keyword)

    return Terminal(symbol_id=TType.IDENT, value=ident_or_keyword)


def lex_string_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_STRING 状态的逻辑，指向当前元素之后的第 1 个字符"""
    mark = fsm.text[fsm.idx]
    fsm.idx += 1
    value = _find_end_mark(fsm, mark)
    return Terminal(symbol_id=TType.LITERAL_TEXT_STRING, value=value)


def lex_ident_or_nchar_action(fsm: LexFSM) -> Optional[Terminal]:
    """处理 LEX_IDENT_OR_NCHAR 状态的逻辑

    1. 如果将状态置为 LEX_IDENT，则指向 IDENT 中的第 1 个字符
    """
    ch = fsm.text[fsm.idx + 1]
    if ch != "'":
        fsm.state = LexStates.LEX_IDENT
        return None
    fsm.idx += 2
    value = _find_end_mark(fsm, "'")
    return Terminal(symbol_id=TType.LITERAL_NCHAR_STRING, value=value)


def lex_ident_sep_start_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_IDENT_SEP_START 状态的逻辑，指向当前元素后的第 1 个字符"""
    assert fsm.text[fsm.idx] == "."
    fsm.idx += 1
    if LEX_IDENT_MAP.get(fsm.text[fsm.idx], True) is True:
        fsm.state = LexStates.LEX_IDENT_START
    else:
        fsm.state = LexStates.LEX_START
    return Terminal(symbol_id=TType.OPERATOR_DOT, value=".")


def lex_ident_start_action(fsm: LexFSM) -> Terminal:
    """处理 LEX_IDENT_START 状态的逻辑，指向当前元素后的第 1 个字符"""
    # 不断匹配数字、字母和多字节字符直至遇到其他字符
    fsm.idx += 1
    ch = fsm.text[fsm.idx]
    while LEX_IDENT_MAP.get(ch, True) is True:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]

    # 获取当前标识符 or 关键字
    ident = fsm.text[fsm.start_idx: fsm.idx]

    # 跳过后续空格
    while ch in LEX_SPACE_CHARSET:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]

    # 判断下一个字符是否为 . 且之后也是标识符
    if ch == "." and LEX_IDENT_MAP.get(ch, True) is True:
        fsm.state = LexStates.LEX_IDENT_SEP_START

    return Terminal(symbol_id=TType.IDENT, value=ident)


def lex_zero_action(fsm: LexFSM) -> Optional[Terminal]:
    """处理 LEX_ZERO 状态的逻辑

    1. 如果返回 Token 则指向元素之后的第 1 个字符
    2. 如果将状态置为 LEX_IDENT，则指向 IDENT 中的字符
    3. 如果将状态置为 LEX_NUMBER，则仍然指向字符 '0'
    """
    ch = fsm.text[fsm.idx + 1]
    if ch in LEX_BIN_MARK_CHARSET:
        fsm.idx += 2
        ch = fsm.text[fsm.idx]
        while ch in LEX_BIN_CHARSET:
            fsm.idx += 1
            ch = fsm.text[fsm.idx]
        if LEX_IDENT_MAP.get(ch, True) is True and fsm.idx - fsm.start_idx > 2:
            return Terminal(symbol_id=TType.LITERAL_BIN_NUM, value=fsm.text[fsm.start_idx + 2: fsm.idx])
        fsm.idx -= 1  # 如果是 0x 则需要将指针向前移动 1 个字符
        fsm.state = LexStates.LEX_IDENT
        return None
    if ch in LEX_HEX_MARK_CHARSET:
        fsm.idx += 2
        ch = fsm.text[fsm.idx]
        while ch in LEX_HEX_CHARSET:
            fsm.idx += 1
            ch = fsm.text[fsm.idx]
        if LEX_IDENT_MAP.get(ch, True) is True and fsm.idx - fsm.start_idx > 2:
            return Terminal(symbol_id=TType.LITERAL_HEX_NUM, value=fsm.text[fsm.start_idx + 2: fsm.idx])
        fsm.idx -= 1
        fsm.state = LexStates.LEX_IDENT
        return None
    fsm.state = LexStates.LEX_NUMBER
    return None


def lex_number_action(fsm: LexFSM) -> Optional[Terminal]:
    """处理 LEX_NUMBER 状态的逻辑

    1. 如果将状态置为 LEX_NUMBER_E，则指向 'e' 字符
    2. 如果将状态置为 LEX_NUMBER_DOT，则指向 '.' 字符
    3. 如果将状态置为 LEX_IDENT，则指向数字后的第 1 个字符
    4. 如果返回 Token 则指向元素之后的第 1 个字符
    """
    fsm.idx += 1
    ch = fsm.text[fsm.idx]
    while ch.isdigit():
        fsm.idx += 1
        ch = fsm.text[fsm.idx]
    if ch in LEX_E_CHARSET:
        fsm.state = LexStates.LEX_NUMBER_E
        return None
    if ch == ".":
        fsm.state = LexStates.LEX_NUMBER_DOT
        return None
    if LEX_IDENT_MAP.get(ch, True) is True:
        fsm.state = LexStates.LEX_IDENT
        return None
    return Terminal(symbol_id=TType.LITERAL_INT_NUM, value=fsm.text[fsm.start_idx: fsm.idx])


def lex_number_dot_action(fsm: LexFSM) -> Optional[Terminal]:
    """处理 LEX_NUMBER_DOT 状态的逻辑

    1. 如果将状态置为 LEX_NUMBER_E，则指向 'e' 字符
    2. 如果将状态置为 LEX_IDENT，则指向数字后的第 1 个字符
    3. 如果返回 Token 则指向元素之后的第 1 个字符
    """
    fsm.idx += 1
    ch = fsm.text[fsm.idx]
    while ch.isdigit():
        fsm.idx += 1
        ch = fsm.text[fsm.idx]
    if ch in LEX_E_CHARSET:
        fsm.state = LexStates.LEX_NUMBER_E
        return None
    if LEX_IDENT_MAP.get(ch, True) is True:
        fsm.state = LexStates.LEX_IDENT
        return None
    return Terminal(symbol_id=TType.LITERAL_DECIMAL_NUM, value=fsm.text[fsm.start_idx: fsm.idx])


def lex_number_e_action(fsm: LexFSM) -> Optional[Terminal]:
    """处理 LEX_NUMBER_E 状态的逻辑

    1. 如果将状态置为 LEX_IDENT，则指向数字后的第 1 个字符
    2. 如果返回 Token 则指向元素之后的第 1 个字符
    """
    fsm.idx += 1
    ch = fsm.text[fsm.idx]
    if ch in LEX_PLUS_MINUS_SIGN_CHARSET:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]
    if not ch.isdigit():
        return Terminal(symbol_id=TType.SYSTEM_ABORT, value=None)
    while ch.isdigit():
        fsm.idx += 1
        ch = fsm.text[fsm.idx]
    if LEX_IDENT_MAP.get(ch, True) is True:
        fsm.state = LexStates.LEX_IDENT
        return None
    return Terminal(symbol_id=TType.LITERAL_FLOAT_NUM, value=fsm.text[fsm.start_idx: fsm.idx])


def lex_dot_action(fsm: LexFSM) -> None:
    """处理 LEX_DOT 状态的逻辑

    1. 如果将状态置为 LEX_NUMBER_DOT，则指向 '.' 字符
    2. 如果将状态置为 LEX_IDENT_SEP_START，则指向 '.' 字符 TODO 这里与 MySQL 不同，后续需要兼容
    """
    ch = fsm.text[fsm.idx + 1]
    if ch.isdigit():
        fsm.state = LexStates.LEX_NUMBER_DOT
        return None
    fsm.state = LexStates.LEX_IDENT_SEP_START
    return None


def lex_comment_action(fsm: LexFSM) -> None:
    """处理 LEX_COMMENT 状态的逻辑，指向当前语法元素后的下 1 个字符"""
    ch = fsm.text[fsm.idx]
    while ch not in LEX_LINE_BREAK_CHARSET:
        fsm.idx += 1
        ch = fsm.text[fsm.idx]
    fsm.state = LexStates.LEX_START
    return None


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
    LexStates.LEX_GT: lex_gt_action,
    LexStates.LEX_QUES: lex_ques_action,
    LexStates.LEX_EQ: lex_eq_action,
    LexStates.LEX_STAR: lex_star_action,
    LexStates.LEX_SLASH: lex_slash_action,
    LexStates.LEX_BANG: lex_bang_action,
    LexStates.LEX_AMP: lex_amp_action,
    LexStates.LEX_BAR: lex_bar_action,
    LexStates.LEX_COLON: lex_colon_action,
    LexStates.LEX_LPAREN: lex_lparen_action,
    LexStates.LEX_RPAREN: lex_rparen_action,
    LexStates.LEX_COMMA: lex_comma_action,
    LexStates.LEX_LBRACE: lex_lbrace_action,
    LexStates.LEX_RBRACE: lex_rbrace_action,
    LexStates.LEX_IDENT_OR_HEX: lex_ident_or_hex_action,
    LexStates.LEX_HEX_NUMBER: lex_hex_number_action,
    LexStates.LEX_IDENT_OR_BIN: lex_ident_or_bin_action,
    LexStates.LEX_BIN_NUMBER: lex_bin_number_action,
    LexStates.LEX_IDENT: lex_ident_action,
    LexStates.LEX_DELIMITER: None,
    LexStates.LEX_STRING: lex_string_action,
    LexStates.LEX_STRING_OR_DELIMITER: lex_ident_or_nchar_action,
    LexStates.LEX_IDENT_OR_NCHAR: lex_ident_or_nchar_action,
    LexStates.LEX_IDENT_SEP_START: lex_ident_sep_start_action,
    LexStates.LEX_IDENT_START: lex_ident_start_action,
    LexStates.LEX_ZERO: lex_zero_action,
    LexStates.LEX_NUMBER: lex_number_action,
    LexStates.LEX_NUMBER_DOT: lex_number_dot_action,
    LexStates.LEX_NUMBER_E: lex_number_e_action,
    LexStates.LEX_DOT: lex_dot_action,
    LexStates.LEX_COMMENT: lex_comment_action,
    LexStates.LEX_LONG_COMMENT: None,
    LexStates.LEX_DOLLAR: None,
    LexStates.LEX_SEMICOLON: None,
    LexStates.LEX_AT: None,
    LexStates.LEX_AT_AT: None,
    LexStates.LEX_AT_AT_END: None,
    LexStates.LEX_AT_END: None,
}
