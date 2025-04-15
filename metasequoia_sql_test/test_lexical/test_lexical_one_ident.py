"""
测试解析单个标识符类型的 Token
"""

import unittest

from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType
from metasequoia_sql_test.common import parse_one_token


class TestLexicalOneIdent(unittest.TestCase):
    """测试解析单个标识符类型的 Token"""

    def test_ident(self):
        """测试解析标识符"""
        terminal = parse_one_token("abc")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("abc", terminal.symbol_value)

        terminal = parse_one_token("hello")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("hello", terminal.symbol_value)

        terminal = parse_one_token("水杉")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("水杉", terminal.symbol_value)

        terminal = parse_one_token("b")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("b", terminal.symbol_value)

        terminal = parse_one_token("B")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("B", terminal.symbol_value)

        terminal = parse_one_token("x")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("x", terminal.symbol_value)

        terminal = parse_one_token("X")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("X", terminal.symbol_value)

        terminal = parse_one_token("n")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("n", terminal.symbol_value)

        terminal = parse_one_token("N")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("N", terminal.symbol_value)

        terminal = parse_one_token("0b")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("0b", terminal.symbol_value)

        terminal = parse_one_token("0B")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("0B", terminal.symbol_value)

        terminal = parse_one_token("0x")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("0x", terminal.symbol_value)

        terminal = parse_one_token("0X")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("0X", terminal.symbol_value)

        terminal = parse_one_token("bbb")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("bbb", terminal.symbol_value)

        terminal = parse_one_token("BBB")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("BBB", terminal.symbol_value)

        terminal = parse_one_token("xxx")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("xxx", terminal.symbol_value)

        terminal = parse_one_token("XXX")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("XXX", terminal.symbol_value)

        terminal = parse_one_token("nnn")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("nnn", terminal.symbol_value)

        terminal = parse_one_token("NNN")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("NNN", terminal.symbol_value)

        terminal = parse_one_token("035ABC")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("035ABC", terminal.symbol_value)

        terminal = parse_one_token("035_DEF")
        self.assertEqual(TType.IDENT, terminal.symbol_id)
        self.assertEqual("035_DEF", terminal.symbol_value)

        terminal = parse_one_token("3EFG")
        self.assertEqual(TType.SYSTEM_ABORT, terminal.symbol_id)

        terminal = parse_one_token("0.3EFG")
        self.assertEqual(TType.SYSTEM_ABORT, terminal.symbol_id)

    def test_ident_quoted(self):
        """测试解析含引号的标识符"""
        terminal = parse_one_token("`abc`")
        self.assertEqual(TType.IDENT_QUOTED, terminal.symbol_id)
        self.assertEqual("abc", terminal.symbol_value)

        terminal = parse_one_token("`hello`")
        self.assertEqual(TType.IDENT_QUOTED, terminal.symbol_id)
        self.assertEqual("hello", terminal.symbol_value)

        terminal = parse_one_token("`水杉`")
        self.assertEqual(TType.IDENT_QUOTED, terminal.symbol_id)
        self.assertEqual("水杉", terminal.symbol_value)
