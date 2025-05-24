"""
测试解析多个 Token
"""

import unittest

from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType
from metasequoia_sql_test.common import parse_two_token
from metasequoia_sql_test.common import parse_three_token


class TestLexicalMultiToken(unittest.TestCase):
    """测试解析多个 Token"""

    def test_after_ident(self):
        """测试 IDENT 类型终结符后的终结符"""
        terminal_1, terminal_2 = parse_two_token("abc def")
        self.assertEqual(TType.IDENT, terminal_1.symbol_id)
        self.assertEqual("abc", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("def", terminal_2.symbol_value)

        terminal_1, terminal_2 = parse_two_token("hello hello")
        self.assertEqual(TType.IDENT, terminal_1.symbol_id)
        self.assertEqual("hello", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("hello", terminal_2.symbol_value)

        terminal_1, terminal_2 = parse_two_token("hello 水杉")
        self.assertEqual(TType.IDENT, terminal_1.symbol_id)
        self.assertEqual("hello", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("水杉", terminal_2.symbol_value)

        terminal_1, terminal_2 = parse_two_token("`hello` 水杉")
        self.assertEqual(TType.IDENT_QUOTED, terminal_1.symbol_id)
        self.assertEqual("hello", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("水杉", terminal_2.symbol_value)

    def test_after_keyword(self):
        """测试 KEYWORD 类型终结符后的终结符"""
        terminal_1, terminal_2 = parse_two_token("SELECT def")
        self.assertEqual(TType.KEYWORD_SELECT, terminal_1.symbol_id)
        self.assertEqual("SELECT", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("def", terminal_2.symbol_value)

        terminal_1, terminal_2 = parse_two_token("SELECT hello")
        self.assertEqual(TType.KEYWORD_SELECT, terminal_1.symbol_id)
        self.assertEqual("SELECT", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("hello", terminal_2.symbol_value)

        terminal_1, terminal_2 = parse_two_token("SELECT 水杉")
        self.assertEqual(TType.KEYWORD_SELECT, terminal_1.symbol_id)
        self.assertEqual("SELECT", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("水杉", terminal_2.symbol_value)

    def test_after_literal(self):
        """测试 LITERAL 类型终结符后的终结符"""
        terminal_1, terminal_2 = parse_two_token("3 def")
        self.assertEqual(TType.LITERAL_INT_NUM, terminal_1.symbol_id)
        self.assertEqual("3", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("def", terminal_2.symbol_value)

        terminal_1, terminal_2 = parse_two_token("3.5 hello")
        self.assertEqual(TType.LITERAL_DECIMAL_NUM, terminal_1.symbol_id)
        self.assertEqual("3.5", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("hello", terminal_2.symbol_value)

        terminal_1, terminal_2 = parse_two_token("'abc' 水杉")
        self.assertEqual(TType.LITERAL_TEXT_STRING, terminal_1.symbol_id)
        self.assertEqual("abc", terminal_1.symbol_value)
        self.assertEqual(TType.IDENT, terminal_2.symbol_id)
        self.assertEqual("水杉", terminal_2.symbol_value)

    def test_after_dot(self):
        """测试 . 之后的终结符"""
        terminal_1, terminal_2, terminal_3 = parse_three_token("hello.SELECT")
        self.assertEqual(TType.IDENT, terminal_1.symbol_id)
        self.assertEqual("hello", terminal_1.symbol_value)
        self.assertEqual(TType.OPERATOR_DOT, terminal_2.symbol_id)
        self.assertEqual(".", terminal_2.symbol_value)
        self.assertEqual(TType.IDENT, terminal_3.symbol_id)
        self.assertEqual("SELECT", terminal_3.symbol_value)
