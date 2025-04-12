"""
词法解析器自动机状态的枚举类
"""

import enum

__all__ = [
    "LexStates"
]


class LexStates(enum.IntEnum):
    """
    词法解析器自动机状态的枚举类
    """

    # 开始和结束状态
    LEX_START = enum.auto()  # 初始状态
    LEX_EOF = enum.auto()  # \x00（结束字符）
    LEX_SKIP = enum.auto()  # 跳过当前字符：这个状态不会保留到字符处理结束
    LEX_ERROR = enum.auto()  # 异常字符：这个状态仅出现在初始状态转移规则的哈希表中，表示异常

    # 运算符
    LEX_PLUS = enum.auto()  # +
    LEX_CARET = enum.auto()  # ^
    LEX_TILDE = enum.auto()  # ~
    LEX_PERCENT = enum.auto()  # %
    LEX_SUB = enum.auto()  # -
    LEX_LT = enum.auto()  # <
    LEX_GT = enum.auto()  # >
    LEX_QUES = enum.auto()  # ?
    LEX_EQ = enum.auto()  # =
    LEX_STAR = enum.auto()  # *
    LEX_SLASH = enum.auto()  # /
    LEX_BANG = enum.auto()  # !
    LEX_AMP = enum.auto()  # &
    LEX_BAR = enum.auto()  # |
    LEX_COLON = enum.auto()  # :
    LEX_LPAREN = enum.auto()  # (
    LEX_RPAREN = enum.auto()  # )
    LEX_COMMA = enum.auto()  # ,
    LEX_LBRACE = enum.auto()  # {
    LEX_RBRACE = enum.auto()  # }

    # 十六进制字面值
    LEX_IDENT_OR_HEX = enum.auto()  # [xX] (标识符 or 十六进制字面值)
    LEX_HEX_NUMBER = enum.auto()  # [xX]' (十六进制字面值)

    # 二进制字面值
    LEX_IDENT_OR_BIN = enum.auto()  # [bB] (标识符 or 二进制字面值)
    LEX_BIN_NUMBER = enum.auto()  # [bB]' (二进制字面值)

    # 标识符和关键字
    LEX_IDENT = enum.auto()  # (标识符)
    LEX_DELIMITER = enum.auto()  # ` (定界标识符)

    # 字符串字面值
    LEX_STRING = enum.auto()  # ' (字符串)
    LEX_STRING_OR_DELIMITER = enum.auto()  # " (字符串 or 定界标识符)
    LEX_IDENT_OR_NCHAR = enum.auto()  # [nN] (标识符 or Unicode 字符串)
    LEX_IDENT_SEP_START = enum.auto()  # 初始状态，下一个 token 是 "."
    LEX_IDENT_START = enum.auto()  # 初始状态，下一个 token 是标识符

    # 数值字面值
    LEX_ZERO = enum.auto()  # 0
    LEX_NUMBER = enum.auto()  # [0-9]+
    LEX_NUMBER_DOT = enum.auto()  # [0-9]+.
    LEX_NUMBER_E = enum.auto()  # [0-9]+(\.[0-9]+)?[eE]
    LEX_DOT = enum.auto()  # \.

    # 注释
    LEX_COMMENT = enum.auto()  # # 或 --
    LEX_LONG_COMMENT = enum.auto()  # /*

    # 其他元素
    LEX_SEMICOLON = enum.auto()  # ;
    LEX_AT = enum.auto()  # @
    LEX_AT_AT = enum.auto()  # @@
    LEX_AT_AT_END = enum.auto()  # 前两个 Token 分别是 @ 和 @
    LEX_AT_END = enum.auto()  # 上一个 Token 是 @
