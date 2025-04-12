"""
测试解析 1 个运算符类型 Token
"""

import unittest

from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType
from metasequoia_sql_test.common import parse_one_token


class TestLexicalOneTokenOperator(unittest.TestCase):
    """测试解析单个运算符类型的 Token"""

    def test_operator_plus(self):
        """测试解析 `+` 运算符"""
        terminal = parse_one_token("+")
        self.assertEqual(TType.OPERATOR_PLUS, terminal.symbol_id)
        self.assertEqual("+", terminal.symbol_value)

    def test_operator_caret(self):
        """测试解析 `^` 运算符"""
        terminal = parse_one_token("^")
        self.assertEqual(TType.OPERATOR_CARET, terminal.symbol_id)
        self.assertEqual("^", terminal.symbol_value)

    def test_operator_tilde(self):
        """测试解析 `~` 运算符"""
        terminal = parse_one_token("~")
        self.assertEqual(TType.OPERATOR_TILDE, terminal.symbol_id)
        self.assertEqual("~", terminal.symbol_value)

    def test_operator_percent(self):
        """测试解析 `%` 运算符"""
        terminal = parse_one_token("%")
        self.assertEqual(TType.OPERATOR_PERCENT, terminal.symbol_id)
        self.assertEqual("%", terminal.symbol_value)

    def test_operator_sub(self):
        """测试解析 `-` 运算符"""
        terminal = parse_one_token("-")
        self.assertEqual(TType.OPERATOR_SUB, terminal.symbol_id)
        self.assertEqual("-", terminal.symbol_value)

    def test_operator_lt(self):
        """测试解析 `<` 运算符"""
        terminal = parse_one_token("<")
        self.assertEqual(TType.OPERATOR_LT, terminal.symbol_id)
        self.assertEqual("<", terminal.symbol_value)

    def test_operator_gt(self):
        """测试解析 `>` 运算符"""
        terminal = parse_one_token(">")
        self.assertEqual(TType.OPERATOR_GT, terminal.symbol_id)
        self.assertEqual(">", terminal.symbol_value)

    def test_operator_ques(self):
        """测试解析 `?` 运算符"""
        terminal = parse_one_token("?")
        self.assertEqual(TType.PARAM_MARKER, terminal.symbol_id)
        self.assertEqual("?", terminal.symbol_value)

    def test_operator_eq(self):
        """测试解析 `=` 运算符"""
        terminal = parse_one_token("=")
        self.assertEqual(TType.OPERATOR_EQ, terminal.symbol_id)
        self.assertEqual("=", terminal.symbol_value)

    def test_operator_star(self):
        """测试解析 `*` 运算符"""
        terminal = parse_one_token("*")
        self.assertEqual(TType.OPERATOR_STAR, terminal.symbol_id)
        self.assertEqual("*", terminal.symbol_value)

    def test_operator_slash(self):
        """测试解析 `/` 运算符"""
        terminal = parse_one_token("/")
        self.assertEqual(TType.OPERATOR_SLASH, terminal.symbol_id)
        self.assertEqual("/", terminal.symbol_value)

    def test_operator_bang(self):
        """测试解析 `!` 运算符"""
        terminal = parse_one_token("!")
        self.assertEqual(TType.OPERATOR_BANG, terminal.symbol_id)
        self.assertEqual("!", terminal.symbol_value)

    def test_operator_amp(self):
        """测试解析 `&` 运算符"""
        terminal = parse_one_token("&")
        self.assertEqual(TType.OPERATOR_AMP, terminal.symbol_id)
        self.assertEqual("&", terminal.symbol_value)

    def test_operator_bar(self):
        """测试解析 `|` 运算符"""
        terminal = parse_one_token("|")
        self.assertEqual(TType.OPERATOR_BAR, terminal.symbol_id)
        self.assertEqual("|", terminal.symbol_value)

    def test_operator_colon(self):
        """测试解析 `:` 运算符"""
        terminal = parse_one_token(":")
        self.assertEqual(TType.OPERATOR_COLON, terminal.symbol_id)
        self.assertEqual(":", terminal.symbol_value)

    def test_operator_lparan(self):
        """测试解析 `(` 运算符"""
        terminal = parse_one_token("(")
        self.assertEqual(TType.OPERATOR_LPAREN, terminal.symbol_id)
        self.assertEqual("(", terminal.symbol_value)

    def test_operator_rparan(self):
        """测试解析 `)` 运算符"""
        terminal = parse_one_token(")")
        self.assertEqual(TType.OPERATOR_RPAREN, terminal.symbol_id)
        self.assertEqual(")", terminal.symbol_value)

    def test_operator_comma(self):
        """测试解析 `,` 运算符"""
        terminal = parse_one_token(",")
        self.assertEqual(TType.OPERATOR_COMMA, terminal.symbol_id)
        self.assertEqual(",", terminal.symbol_value)

    def test_operator_lbrace(self):
        """测试解析 `{` 运算符"""
        terminal = parse_one_token("{")
        self.assertEqual(TType.OPERATOR_LBRACE, terminal.symbol_id)
        self.assertEqual("{", terminal.symbol_value)

    def test_operator_rbrace(self):
        """测试解析 `}` 运算符"""
        terminal = parse_one_token("}")
        self.assertEqual(TType.OPERATOR_RBRACE, terminal.symbol_id)
        self.assertEqual("}", terminal.symbol_value)

    def test_operator_dot(self):
        """测试解析 `.` 运算符"""
        terminal = parse_one_token(".")
        self.assertEqual(TType.OPERATOR_DOT, terminal.symbol_id)
        self.assertEqual(".", terminal.symbol_value)

    def test_operator_at(self):
        """测试解析 `@` 运算符"""
        terminal = parse_one_token("@")
        self.assertEqual(TType.OPERATOR_AT, terminal.symbol_id)
        self.assertEqual("@", terminal.symbol_value)

    def test_operator_semicolon(self):
        """测试解析 `;` 运算符"""
        terminal = parse_one_token(";")
        self.assertEqual(TType.OPERATOR_SEMICOLON, terminal.symbol_id)
        self.assertEqual(";", terminal.symbol_value)

    def test_operator_amp_amp(self):
        """测试解析 `&&` 运算符"""
        terminal = parse_one_token("&&")
        self.assertEqual(TType.OPERATOR_AMP_AMP, terminal.symbol_id)
        self.assertEqual("&&", terminal.symbol_value)

    def test_operator_lt_eq_gt(self):
        """测试解析 `<=>` 运算符"""
        terminal = parse_one_token("<=>")
        self.assertEqual(TType.OPERATOR_LT_EQ_GT, terminal.symbol_id)
        self.assertEqual("<=>", terminal.symbol_value)

    def test_operator_gt_eq(self):
        """测试解析 `>=` 运算符"""
        terminal = parse_one_token(">=")
        self.assertEqual(TType.OPERATOR_GT_EQ, terminal.symbol_id)
        self.assertEqual(">=", terminal.symbol_value)

    def test_operator_lt_eq(self):
        """测试解析 `<=` 运算符"""
        terminal = parse_one_token("<=")
        self.assertEqual(TType.OPERATOR_LT_EQ, terminal.symbol_id)
        self.assertEqual("<=", terminal.symbol_value)

    def test_operator_bang_eq(self):
        """测试解析 `!=` 运算符或 `<>` 运算符"""
        terminal = parse_one_token("!=")
        self.assertEqual(TType.OPERATOR_BANG_EQ, terminal.symbol_id)
        self.assertEqual("!=", terminal.symbol_value)
        terminal = parse_one_token("<>")
        self.assertEqual(TType.OPERATOR_BANG_EQ, terminal.symbol_id)
        self.assertEqual("<>", terminal.symbol_value)

    def test_operator_bar_bar(self):
        """测试解析 `||` 运算符"""
        terminal = parse_one_token("||")
        self.assertEqual(TType.OPERATOR_BAR_BAR, terminal.symbol_id)
        self.assertEqual("||", terminal.symbol_value)

    def test_operator_lt_lt(self):
        """测试解析 `<<` 运算符"""
        terminal = parse_one_token("<<")
        self.assertEqual(TType.OPERATOR_LT_LT, terminal.symbol_id)
        self.assertEqual("<<", terminal.symbol_value)

    def test_operator_gt_gt(self):
        """测试解析 `>>` 运算符"""
        terminal = parse_one_token(">>")
        self.assertEqual(TType.OPERATOR_GT_GT, terminal.symbol_id)
        self.assertEqual(">>", terminal.symbol_value)

    def test_operator_sub_gt(self):
        """测试解析 `->` 运算符"""
        terminal = parse_one_token("->")
        self.assertEqual(TType.OPERATOR_SUB_GT, terminal.symbol_id)
        self.assertEqual("->", terminal.symbol_value)

    def test_operator_sub_gt_gt(self):
        """测试解析 `->>` 运算符"""
        terminal = parse_one_token("->>")
        self.assertEqual(TType.OPERATOR_SUB_GT_GT, terminal.symbol_id)
        self.assertEqual("->>", terminal.symbol_value)

    def test_operator_colon_eq(self):
        """测试解析 `:=` 运算符"""
        terminal = parse_one_token(":=")
        self.assertEqual(TType.OPERATOR_COLON_EQ, terminal.symbol_id)
        self.assertEqual(":=", terminal.symbol_value)
