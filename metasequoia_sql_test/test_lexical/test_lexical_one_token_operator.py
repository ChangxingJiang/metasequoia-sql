"""
测试解析 1 个运算符类型 Token
"""

import unittest

from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType
from metasequoia_sql_test.common import parse_one_token


class TestLexicalOneTokenOperator(unittest.TestCase):
    """测试解析 1 个运算符类型 Token"""

    def test_operator_plus(self):
        self.assertEqual(TType.OPERATOR_PLUS, parse_one_token("+").symbol_id)

    #     OPERATOR_PLUS = enum.auto()  # OPERATOR : +
#     OPERATOR_CARET = enum.auto()  # OPERATOR : ^
#     OPERATOR_TILDE = enum.auto()  # OPERATOR : ~
#     OPERATOR_PERCENT = enum.auto()  # OPERATOR : %
#     OPERATOR_SUB = enum.auto()  # OPERATOR : -
#     OPERATOR_LT = enum.auto()  # OPERATOR : <
#     OPERATOR_GT = enum.auto()  # OPERATOR : >
#     OPERATOR_QUES = enum.auto()  # OPERATOR : ?
#     OPERATOR_EQ = enum.auto()  # OPERATOR : =
#     OPERATOR_STAR = enum.auto()  # OPERATOR : *
#     OPERATOR_SLASH = enum.auto()  # OPERATOR : /
#     OPERATOR_BANG = enum.auto()  # OPERATOR : !
#     OPERATOR_AMP = enum.auto()  # OPERATOR : &
#     OPERATOR_BAR = enum.auto()  # OPERATOR : |
#     OPERATOR_COLON = enum.auto()  # OPERATOR : :
#     OPERATOR_LPAREN = enum.auto()  # OPERATOR : (
#     OPERATOR_RPAREN = enum.auto()  # OPERATOR : )
#     OPERATOR_COMMA = enum.auto()  # OPERATOR : ,
#     OPERATOR_LBRACE = enum.auto()  # OPERATOR : {
#     OPERATOR_RBRACE = enum.auto()  # OPERATOR : }
#     OPERATOR_DOT = enum.auto()  # OPERATOR : .
#     OPERATOR_AT = enum.auto()  # OPERATOR : @
#     OPERATOR_SEMICOLON = enum.auto()  # OPERATOR : ;
#     OPERATOR_DOLLAR = enum.auto()  # OPERATOR : $
