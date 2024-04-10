import unittest

from metasequoia_sql.common import build_token_scanner
from metasequoia_sql.parser.common import parse_select_statement
from scripts.demo.sql_basic_tutorial import *


class TestSqlBasicTutorial(unittest.TestCase):
    def test_sbt_ch02_01(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_01))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_02(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_02))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["*"])

    def test_sbt_ch02_03(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_03))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shohin_bunrui", "hanbai_tanka", "shiire_tanka", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shohin_bunrui", "hanbai_tanka", "shiire_tanka", "torokubi"])

    def test_sbt_ch02_04(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_04))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_05(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_05))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_06(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_06))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch02_07(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_07))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch02_08(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_08))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka"])

    def test_sbt_ch02_09(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_09))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi"])

    def test_sbt_ch02_10(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_10))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch02_11(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_11))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch02_13(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_13))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_14(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_14))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_15(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_15))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_16(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_16))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_17(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_17))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka"])

    def test_sbt_ch02_18(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_18))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_19(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_19))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_20(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_20))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_21(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_21))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_where_used_column_list(), ["torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])

    def test_sbt_ch02_22(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_22))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch02_24(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_24))
        self.assertEqual(statement.get_from_used_table_list(), ["Chars"])
        self.assertEqual(statement.get_used_table_list(), ["Chars"])
        self.assertEqual(statement.get_select_used_column_list(), ["chr"])
        self.assertEqual(statement.get_where_used_column_list(), ["chr"])
        self.assertEqual(statement.get_used_column_list(), ["chr"])

    def test_sbt_ch02_25(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_25))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_26(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_26))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_27(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_27))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_28(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_28))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_29(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_29))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_30(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_30))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_31(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_31))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_32(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_32))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_33(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_33))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_34(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_34))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_35(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_35))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])

    def test_sbt_ch02_36(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_36))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])

    def test_sbt_ch02_a_db2(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_A_DB2))
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])

    def test_sbt_ch02_a_oracle(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_A_ORACLE))
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])

    def test_sbt_ch02_a_sqlserver(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH02_A_SQLSERVER))

    def test_sbt_ch03_01(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_01))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["*"])

    def test_sbt_ch03_02(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_02))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka"])

    def test_sbt_ch03_04(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_04))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch03_05(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_05))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_06(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_06))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch03_07(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_07))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_08(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_08))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_09(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_09))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["torokubi"])

    def test_sbt_ch03_10(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_10))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch03_11(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_11))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch03_12(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_12))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch03_13(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_13))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_14(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_14))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka", "*"])

    def test_sbt_ch03_15(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_15))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka", "*"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka", "*", "shohin_bunrui"])

    def test_sbt_ch03_16(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_16))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka", "*"])

    def test_sbt_ch03_17(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_17))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_18(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_18))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_19(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_19))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_where_used_column_list(), ["*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_20(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_20))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_21(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_21))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_22(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_22))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch03_23(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_23))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch03_24(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_24))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*", "shohin_mei"])

    def test_sbt_ch03_25(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_25))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_26(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_26))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_27(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_27))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_28(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_28))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_29(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_29))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_30(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_30))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_31(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_31))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_32(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_32))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_33(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_33))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka", "shohin_id"])

    def test_sbt_ch03_34(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_34))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_35_1(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_35_1))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_35_2(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_35_2))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_a_1(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_A_1))
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch03_a_2(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH03_A_2))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch05_01(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_01))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch05_03(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_03))
        self.assertEqual(statement.get_from_used_table_list(), ["ShohinSum"])
        self.assertEqual(statement.get_used_table_list(), ["ShohinSum"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_09_oracle(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_09_ORACLE))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_09_sqlserver(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_09_SQLSERVER))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_10_oracle(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_10_ORACLE))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_10_sqlserver(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_10_SQLSERVER))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_11(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_11))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch05_12(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_12))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch05_13(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_13))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch05_14(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_14))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch05_15(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_15))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shohin_bunrui"])

    def test_sbt_ch05_16_oracle(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_16_ORACLE))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch05_16_sqlserver(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH05_16_SQLSERVER))
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch06_02(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH06_02))
        self.assertEqual(statement.get_from_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_select_used_column_list(), ["m"])
        self.assertEqual(statement.get_used_column_list(), ["m"])

    def test_sbt_ch06_03_oracle(self):
        statement = parse_select_statement(build_token_scanner(SBT_CH06_03_ORACLE))
        self.assertEqual(statement.get_from_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_select_used_column_list(), ["n", "p"])
        self.assertEqual(statement.get_used_column_list(), ["n", "p"])

