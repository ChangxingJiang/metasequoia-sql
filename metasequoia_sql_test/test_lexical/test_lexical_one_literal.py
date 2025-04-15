"""
测试解析单个字面值类型的 Token
"""

import unittest

from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType
from metasequoia_sql_test.common import parse_one_token


class TestLexicalOneLiteral(unittest.TestCase):
    """测试解析单个字面值类型的 Token"""

    def test_literal_bin_num(self):
        """测试解析二进制字面值"""
        terminal = parse_one_token("0b01")
        self.assertEqual(TType.LITERAL_BIN_NUM, terminal.symbol_id)
        self.assertEqual("01", terminal.symbol_value)
        terminal = parse_one_token("0b11")
        self.assertEqual(TType.LITERAL_BIN_NUM, terminal.symbol_id)
        self.assertEqual("11", terminal.symbol_value)
        terminal = parse_one_token("0B11")
        self.assertEqual(TType.LITERAL_BIN_NUM, terminal.symbol_id)
        self.assertEqual("11", terminal.symbol_value)
        terminal = parse_one_token("b'01'")
        self.assertEqual(TType.LITERAL_BIN_NUM, terminal.symbol_id)
        self.assertEqual("01", terminal.symbol_value)
        terminal = parse_one_token("b'11'")
        self.assertEqual(TType.LITERAL_BIN_NUM, terminal.symbol_id)
        self.assertEqual("11", terminal.symbol_value)
        terminal = parse_one_token("B'11'")
        self.assertEqual(TType.LITERAL_BIN_NUM, terminal.symbol_id)
        self.assertEqual("11", terminal.symbol_value)

    def test_literal_hex_num(self):
        """测试解析十六进制字面值"""
        terminal = parse_one_token("0x0F")
        self.assertEqual(TType.LITERAL_HEX_NUM, terminal.symbol_id)
        self.assertEqual("0F", terminal.symbol_value)
        terminal = parse_one_token("0xC1")
        self.assertEqual(TType.LITERAL_HEX_NUM, terminal.symbol_id)
        self.assertEqual("C1", terminal.symbol_value)
        terminal = parse_one_token("0XC1")
        self.assertEqual(TType.LITERAL_HEX_NUM, terminal.symbol_id)
        self.assertEqual("C1", terminal.symbol_value)
        terminal = parse_one_token("x'0F'")
        self.assertEqual(TType.LITERAL_HEX_NUM, terminal.symbol_id)
        self.assertEqual("0F", terminal.symbol_value)
        terminal = parse_one_token("x'C1'")
        self.assertEqual(TType.LITERAL_HEX_NUM, terminal.symbol_id)
        self.assertEqual("C1", terminal.symbol_value)
        terminal = parse_one_token("X'C1'")
        self.assertEqual(TType.LITERAL_HEX_NUM, terminal.symbol_id)
        self.assertEqual("C1", terminal.symbol_value)

    def test_literal_decimal_num(self):
        """测试解析小数字面值"""
        terminal = parse_one_token("0.01")
        self.assertEqual(TType.LITERAL_DECIMAL_NUM, terminal.symbol_id)
        self.assertEqual("0.01", terminal.symbol_value)
        terminal = parse_one_token(".02")
        self.assertEqual(TType.LITERAL_DECIMAL_NUM, terminal.symbol_id)
        self.assertEqual(".02", terminal.symbol_value)
        terminal = parse_one_token("3.03")
        self.assertEqual(TType.LITERAL_DECIMAL_NUM, terminal.symbol_id)
        self.assertEqual("3.03", terminal.symbol_value)

    def test_literal_float_num(self):
        """测试解析浮点数字面值"""
        terminal = parse_one_token("1e-6")
        self.assertEqual(TType.LITERAL_FLOAT_NUM, terminal.symbol_id)
        self.assertEqual("1e-6", terminal.symbol_value)
        terminal = parse_one_token("1.3E8")
        self.assertEqual(TType.LITERAL_FLOAT_NUM, terminal.symbol_id)
        self.assertEqual("1.3E8", terminal.symbol_value)
        terminal = parse_one_token(".3e5")
        self.assertEqual(TType.LITERAL_FLOAT_NUM, terminal.symbol_id)
        self.assertEqual(".3e5", terminal.symbol_value)

    def test_literal_int_num(self):
        """测试解析整数字面值"""
        # 短整型
        terminal = parse_one_token("3")
        self.assertEqual(TType.LITERAL_INT_NUM, terminal.symbol_id)
        self.assertEqual("3", terminal.symbol_value)
        terminal = parse_one_token("123456789")
        self.assertEqual(TType.LITERAL_INT_NUM, terminal.symbol_id)
        self.assertEqual("123456789", terminal.symbol_value)

        # 长整型
        terminal = parse_one_token("123456789123456789")
        self.assertEqual(TType.LITERAL_INT_NUM, terminal.symbol_id)
        self.assertEqual("123456789123456789", terminal.symbol_value)

        # 无符号长整型
        terminal = parse_one_token("12345678912345678912")
        self.assertEqual(TType.LITERAL_INT_NUM, terminal.symbol_id)
        self.assertEqual("12345678912345678912", terminal.symbol_value)

    def test_literal_string(self):
        """测试解析整数字面值"""
        terminal = parse_one_token("'abcd'")
        self.assertEqual(TType.LITERAL_TEXT_STRING, terminal.symbol_id)
        self.assertEqual("abcd", terminal.symbol_value)
        terminal = parse_one_token("'abc\\'d'")
        self.assertEqual(TType.LITERAL_TEXT_STRING, terminal.symbol_id)
        self.assertEqual("abc'd", terminal.symbol_value)
        terminal = parse_one_token("'abc\\\\d'")
        self.assertEqual(TType.LITERAL_TEXT_STRING, terminal.symbol_id)
        self.assertEqual("abc\\d", terminal.symbol_value)
