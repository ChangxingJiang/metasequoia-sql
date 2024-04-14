import unittest

from metasequoia_sql import *
from scripts.demo.sql_basic_tutorial import *


class TestSqlBasicTutorial(unittest.TestCase):
    def test_sbt_ch02_01(self):
        statement = parse_select_statement(SBT_CH02_01)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_02(self):
        statement = parse_select_statement(SBT_CH02_02)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["*"])

    def test_sbt_ch02_03(self):
        statement = parse_select_statement(SBT_CH02_03)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shohin_bunrui", "hanbai_tanka", "shiire_tanka", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shohin_bunrui", "hanbai_tanka", "shiire_tanka", "torokubi"])

    def test_sbt_ch02_04(self):
        statement = parse_select_statement(SBT_CH02_04)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_05(self):
        statement = parse_select_statement(SBT_CH02_05)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_06(self):
        statement = parse_select_statement(SBT_CH02_06)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch02_07(self):
        statement = parse_select_statement(SBT_CH02_07)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch02_08(self):
        statement = parse_select_statement(SBT_CH02_08)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka"])

    def test_sbt_ch02_09(self):
        statement = parse_select_statement(SBT_CH02_09)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi"])

    def test_sbt_ch02_10(self):
        statement = parse_select_statement(SBT_CH02_10)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch02_11(self):
        statement = parse_select_statement(SBT_CH02_11)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch02_13(self):
        statement = parse_select_statement(SBT_CH02_13)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_14(self):
        statement = parse_select_statement(SBT_CH02_14)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_15(self):
        statement = parse_select_statement(SBT_CH02_15)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_16(self):
        statement = parse_select_statement(SBT_CH02_16)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shiire_tanka"])

    def test_sbt_ch02_17(self):
        statement = parse_select_statement(SBT_CH02_17)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka"])

    def test_sbt_ch02_18(self):
        statement = parse_select_statement(SBT_CH02_18)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_19(self):
        statement = parse_select_statement(SBT_CH02_19)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_20(self):
        statement = parse_select_statement(SBT_CH02_20)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_21(self):
        statement = parse_select_statement(SBT_CH02_21)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_where_used_column_list(), ["torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])

    def test_sbt_ch02_22(self):
        statement = parse_select_statement(SBT_CH02_22)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch02_24(self):
        statement = parse_select_statement(SBT_CH02_24)
        self.assertEqual(statement.get_from_used_table_list(), ["Chars"])
        self.assertEqual(statement.get_used_table_list(), ["Chars"])
        self.assertEqual(statement.get_select_used_column_list(), ["chr"])
        self.assertEqual(statement.get_where_used_column_list(), ["chr"])
        self.assertEqual(statement.get_used_column_list(), ["chr"])

    def test_sbt_ch02_25(self):
        statement = parse_select_statement(SBT_CH02_25)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_26(self):
        statement = parse_select_statement(SBT_CH02_26)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_27(self):
        statement = parse_select_statement(SBT_CH02_27)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_28(self):
        statement = parse_select_statement(SBT_CH02_28)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_29(self):
        statement = parse_select_statement(SBT_CH02_29)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch02_30(self):
        statement = parse_select_statement(SBT_CH02_30)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_31(self):
        statement = parse_select_statement(SBT_CH02_31)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_32(self):
        statement = parse_select_statement(SBT_CH02_32)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_33(self):
        statement = parse_select_statement(SBT_CH02_33)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_34(self):
        statement = parse_select_statement(SBT_CH02_34)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch02_35(self):
        statement = parse_select_statement(SBT_CH02_35)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])

    def test_sbt_ch02_36(self):
        statement = parse_select_statement(SBT_CH02_36)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "torokubi"])

    def test_sbt_ch02_a_db2(self):
        statement = parse_select_statement(SBT_CH02_A_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])

    def test_sbt_ch02_a_oracle(self):
        statement = parse_select_statement(SBT_CH02_A_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])

    def test_sbt_ch02_a_sqlserver(self):
        statement = parse_select_statement(SBT_CH02_A_SQLSERVER)

    def test_sbt_ch03_01(self):
        statement = parse_select_statement(SBT_CH03_01)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["*"])

    def test_sbt_ch03_02(self):
        statement = parse_select_statement(SBT_CH03_02)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka"])

    def test_sbt_ch03_04(self):
        statement = parse_select_statement(SBT_CH03_04)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch03_05(self):
        statement = parse_select_statement(SBT_CH03_05)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_06(self):
        statement = parse_select_statement(SBT_CH03_06)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch03_07(self):
        statement = parse_select_statement(SBT_CH03_07)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_08(self):
        statement = parse_select_statement(SBT_CH03_08)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_09(self):
        statement = parse_select_statement(SBT_CH03_09)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["torokubi"])

    def test_sbt_ch03_10(self):
        statement = parse_select_statement(SBT_CH03_10)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch03_11(self):
        statement = parse_select_statement(SBT_CH03_11)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch03_12(self):
        statement = parse_select_statement(SBT_CH03_12)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch03_13(self):
        statement = parse_select_statement(SBT_CH03_13)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_14(self):
        statement = parse_select_statement(SBT_CH03_14)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka", "*"])

    def test_sbt_ch03_15(self):
        statement = parse_select_statement(SBT_CH03_15)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shiire_tanka", "*"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shiire_tanka", "*", "shohin_bunrui"])

    def test_sbt_ch03_16(self):
        statement = parse_select_statement(SBT_CH03_16)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka", "*"])

    def test_sbt_ch03_17(self):
        statement = parse_select_statement(SBT_CH03_17)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_18(self):
        statement = parse_select_statement(SBT_CH03_18)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_19(self):
        statement = parse_select_statement(SBT_CH03_19)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_where_used_column_list(), ["*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_20(self):
        statement = parse_select_statement(SBT_CH03_20)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_21(self):
        statement = parse_select_statement(SBT_CH03_21)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_22(self):
        statement = parse_select_statement(SBT_CH03_22)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch03_23(self):
        statement = parse_select_statement(SBT_CH03_23)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch03_24(self):
        statement = parse_select_statement(SBT_CH03_24)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*", "shohin_mei"])

    def test_sbt_ch03_25(self):
        statement = parse_select_statement(SBT_CH03_25)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_26(self):
        statement = parse_select_statement(SBT_CH03_26)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_27(self):
        statement = parse_select_statement(SBT_CH03_27)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_28(self):
        statement = parse_select_statement(SBT_CH03_28)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_29(self):
        statement = parse_select_statement(SBT_CH03_29)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_30(self):
        statement = parse_select_statement(SBT_CH03_30)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_31(self):
        statement = parse_select_statement(SBT_CH03_31)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_32(self):
        statement = parse_select_statement(SBT_CH03_32)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_33(self):
        statement = parse_select_statement(SBT_CH03_33)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "shiire_tanka", "shohin_id"])

    def test_sbt_ch03_34(self):
        statement = parse_select_statement(SBT_CH03_34)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "*"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["*"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "*"])

    def test_sbt_ch03_35_1(self):
        statement = parse_select_statement(SBT_CH03_35_1)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_35_2(self):
        statement = parse_select_statement(SBT_CH03_35_2)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka", "shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch03_a_1(self):
        statement = parse_select_statement(SBT_CH03_A_1)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch03_a_2(self):
        statement = parse_select_statement(SBT_CH03_A_2)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch05_01(self):
        statement = parse_select_statement(SBT_CH05_01)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka", "shiire_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka", "shiire_tanka"])

    def test_sbt_ch05_03(self):
        statement = parse_select_statement(SBT_CH05_03)
        self.assertEqual(statement.get_from_used_table_list(), ["ShohinSum"])
        self.assertEqual(statement.get_used_table_list(), ["ShohinSum"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_09_oracle(self):
        statement = parse_select_statement(SBT_CH05_09_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_09_sqlserver(self):
        statement = parse_select_statement(SBT_CH05_09_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_10_oracle(self):
        statement = parse_select_statement(SBT_CH05_10_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_10_sqlserver(self):
        statement = parse_select_statement(SBT_CH05_10_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "cnt_shohin"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "cnt_shohin"])

    def test_sbt_ch05_11(self):
        statement = parse_select_statement(SBT_CH05_11)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka"])

    def test_sbt_ch05_12(self):
        statement = parse_select_statement(SBT_CH05_12)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch05_13(self):
        statement = parse_select_statement(SBT_CH05_13)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch05_14(self):
        statement = parse_select_statement(SBT_CH05_14)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_having_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch05_15(self):
        statement = parse_select_statement(SBT_CH05_15)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shohin_bunrui"])

    def test_sbt_ch05_16_oracle(self):
        statement = parse_select_statement(SBT_CH05_16_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka", "S1.shohin_bunrui", "S2.shohin_bunrui", "shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka", "S1.shohin_bunrui", "S2.shohin_bunrui"])

    def test_sbt_ch05_16_sqlserver(self):
        statement = parse_select_statement(SBT_CH05_16_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka", "S1.shohin_bunrui", "S2.shohin_bunrui", "shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "shohin_mei", "hanbai_tanka", "S1.shohin_bunrui", "S2.shohin_bunrui"])

    def test_sbt_ch06_02(self):
        statement = parse_select_statement(SBT_CH06_02)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_select_used_column_list(), ["m"])
        self.assertEqual(statement.get_used_column_list(), ["m"])

    def test_sbt_ch06_03_oracle(self):
        statement = parse_select_statement(SBT_CH06_03_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_select_used_column_list(), ["n", "p"])
        self.assertEqual(statement.get_used_column_list(), ["n", "p"])

    def test_sbt_ch06_03_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_03_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_select_used_column_list(), ["n", "p"])
        self.assertEqual(statement.get_used_column_list(), ["n", "p"])

    def test_sbt_ch06_04(self):
        statement = parse_select_statement(SBT_CH06_04)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_used_table_list(), ["SampleMath"])
        self.assertEqual(statement.get_select_used_column_list(), ["m", "n"])
        self.assertEqual(statement.get_used_column_list(), ["m", "n"])

    def test_sbt_ch06_06_mysql(self):
        statement = parse_select_statement(SBT_CH06_06_MYSQL)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1", "str2"])
        self.assertEqual(statement.get_used_column_list(), ["str1", "str2"])

    def test_sbt_ch06_06_oracle(self):
        statement = parse_select_statement(SBT_CH06_06_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1", "str2"])
        self.assertEqual(statement.get_used_column_list(), ["str1", "str2"])

    def test_sbt_ch06_06_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_06_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1", "str2"])
        self.assertEqual(statement.get_used_column_list(), ["str1", "str2"])

    def test_sbt_ch06_07_mysql(self):
        statement = parse_select_statement(SBT_CH06_07_MYSQL)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1", "str2", "str3"])
        self.assertEqual(statement.get_used_column_list(), ["str1", "str2", "str3"])

    def test_sbt_ch06_07_oracle(self):
        statement = parse_select_statement(SBT_CH06_07_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1", "str2", "str3"])
        self.assertEqual(statement.get_where_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1", "str2", "str3"])

    def test_sbt_ch06_08_oracle(self):
        statement = parse_select_statement(SBT_CH06_08_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1"])

    def test_sbt_ch06_08_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_08_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1"])

    def test_sbt_ch06_09(self):
        statement = parse_select_statement(SBT_CH06_09)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1"])
        self.assertEqual(statement.get_where_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1"])

    def test_sbt_ch06_10(self):
        statement = parse_select_statement(SBT_CH06_10)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1", "str2", "str3"])
        self.assertEqual(statement.get_used_column_list(), ["str1", "str2", "str3"])

    def test_sbt_ch06_11_oracle(self):
        statement = parse_select_statement(SBT_CH06_11_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1"])

    def test_sbt_ch06_11_postgresql(self):
        statement = parse_select_statement(SBT_CH06_11_POSTGRESQL)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1"])

    def test_sbt_ch06_11_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_11_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1"])

    def test_sbt_ch06_12(self):
        statement = parse_select_statement(SBT_CH06_12)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1"])
        self.assertEqual(statement.get_where_used_column_list(), ["str1"])
        self.assertEqual(statement.get_used_column_list(), ["str1"])

    def test_sbt_ch06_13_db2(self):
        statement = parse_select_statement(SBT_CH06_13_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_DATE"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_DATE"])

    def test_sbt_ch06_13_oracle(self):
        statement = parse_select_statement(SBT_CH06_13_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_DATE"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_DATE"])

    def test_sbt_ch06_13_postgresql(self):
        statement = parse_select_statement(SBT_CH06_13_POSTGRESQL)
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_DATE"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_DATE"])

    def test_sbt_ch06_13_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_13_SQLSERVER)
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_14_db2(self):
        statement = parse_select_statement(SBT_CH06_14_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_14_oracle(self):
        statement = parse_select_statement(SBT_CH06_14_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_14_postgresql(self):
        statement = parse_select_statement(SBT_CH06_14_POSTGRESQL)
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIME"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIME"])

    def test_sbt_ch06_14_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_14_SQLSERVER)
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_15_db2(self):
        statement = parse_select_statement(SBT_CH06_15_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_15_oracle(self):
        statement = parse_select_statement(SBT_CH06_15_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_15_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_15_SQLSERVER)
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_16_db2(self):
        statement = parse_select_statement(SBT_CH06_16_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_16_oracle(self):
        statement = parse_select_statement(SBT_CH06_16_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_16_postgresql(self):
        statement = parse_select_statement(SBT_CH06_16_POSTGRESQL)
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP"])

    def test_sbt_ch06_16_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_16_SQLSERVER)
        self.assertEqual(statement.get_select_used_column_list(), ["CURRENT_TIMESTAMP", "YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"])
        self.assertEqual(statement.get_used_column_list(), ["CURRENT_TIMESTAMP", "YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"])

    def test_sbt_ch06_17_db2(self):
        statement = parse_select_statement(SBT_CH06_17_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])

    def test_sbt_ch06_17_mysql(self):
        statement = parse_select_statement(SBT_CH06_17_MYSQL)

    def test_sbt_ch06_17_oracle(self):
        statement = parse_select_statement(SBT_CH06_17_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])

    def test_sbt_ch06_17_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_17_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])

    def test_sbt_ch06_18_db2(self):
        statement = parse_select_statement(SBT_CH06_18_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])

    def test_sbt_ch06_18_oracle(self):
        statement = parse_select_statement(SBT_CH06_18_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["DUAL"])
        self.assertEqual(statement.get_used_table_list(), ["DUAL"])

    def test_sbt_ch06_18_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_18_SQLSERVER)

    def test_sbt_ch06_19_db2(self):
        statement = parse_select_statement(SBT_CH06_19_DB2)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])

    def test_sbt_ch06_19_oracle(self):
        statement = parse_select_statement(SBT_CH06_19_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["SYSIBM.SYSDUMMY1"])
        self.assertEqual(statement.get_used_table_list(), ["SYSIBM.SYSDUMMY1"])

    def test_sbt_ch06_19_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_19_SQLSERVER)

    def test_sbt_ch06_20(self):
        statement = parse_select_statement(SBT_CH06_20)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str2"])
        self.assertEqual(statement.get_used_column_list(), ["str2"])

    def test_sbt_ch06_22(self):
        statement = parse_select_statement(SBT_CH06_22)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_where_used_column_list(), ["strcol"])
        self.assertEqual(statement.get_used_column_list(), ["*", "strcol"])

    def test_sbt_ch06_23(self):
        statement = parse_select_statement(SBT_CH06_23)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_where_used_column_list(), ["strcol"])
        self.assertEqual(statement.get_used_column_list(), ["*", "strcol"])

    def test_sbt_ch06_24(self):
        statement = parse_select_statement(SBT_CH06_24)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_where_used_column_list(), ["strcol"])
        self.assertEqual(statement.get_used_column_list(), ["*", "strcol"])

    def test_sbt_ch06_25(self):
        statement = parse_select_statement(SBT_CH06_25)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_where_used_column_list(), ["strcol"])
        self.assertEqual(statement.get_used_column_list(), ["*", "strcol"])

    def test_sbt_ch06_26(self):
        statement = parse_select_statement(SBT_CH06_26)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_used_table_list(), ["SampleLike"])
        self.assertEqual(statement.get_select_used_column_list(), ["*"])
        self.assertEqual(statement.get_where_used_column_list(), ["strcol"])
        self.assertEqual(statement.get_used_column_list(), ["*", "strcol"])

    def test_sbt_ch06_27(self):
        statement = parse_select_statement(SBT_CH06_27)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka"])

    def test_sbt_ch06_28(self):
        statement = parse_select_statement(SBT_CH06_28)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka"])

    def test_sbt_ch06_29(self):
        statement = parse_select_statement(SBT_CH06_29)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch06_30(self):
        statement = parse_select_statement(SBT_CH06_30)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch06_31(self):
        statement = parse_select_statement(SBT_CH06_31)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch06_32(self):
        statement = parse_select_statement(SBT_CH06_32)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch06_33(self):
        statement = parse_select_statement(SBT_CH06_33)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shiire_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shiire_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shiire_tanka"])

    def test_sbt_ch06_36(self):
        statement = parse_select_statement(SBT_CH06_36)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_id", "tenpo_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "shohin_id", "tenpo_id"])

    def test_sbt_ch06_37(self):
        statement = parse_select_statement(SBT_CH06_37)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_id", "tenpo_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "shohin_id", "tenpo_id"])

    def test_sbt_ch06_38_oracle(self):
        statement = parse_select_statement(SBT_CH06_38_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])

    def test_sbt_ch06_38_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_38_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])

    def test_sbt_ch06_39_oracle(self):
        statement = parse_select_statement(SBT_CH06_39_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])

    def test_sbt_ch06_39_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_39_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])

    def test_sbt_ch06_40_oracle(self):
        statement = parse_select_statement(SBT_CH06_40_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])

    def test_sbt_ch06_40_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_40_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "hanbai_tanka", "*", "TS.tenpo_id", "TS.shohin_id", "S.shohin_id"])

    def test_sbt_ch06_41(self):
        statement = parse_select_statement(SBT_CH06_41)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch06_43(self):
        statement = parse_select_statement(SBT_CH06_43)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui"])

    def test_sbt_ch06_7_sqlserver(self):
        statement = parse_select_statement(SBT_CH06_7_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_used_table_list(), ["SampleStr"])
        self.assertEqual(statement.get_select_used_column_list(), ["str1", "str2", "str3"])
        self.assertEqual(statement.get_used_column_list(), ["str1", "str2", "str3"])

    def test_sbt_ch06_a(self):
        statement = parse_select_statement(SBT_CH06_A)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch06_b_mysql(self):
        statement = parse_select_statement(SBT_CH06_B_MYSQL)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch06_b_oracle(self):
        statement = parse_select_statement(SBT_CH06_B_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui"])

    def test_sbt_ch07_03(self):
        statement = parse_select_statement(SBT_CH07_03)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch07_04(self):
        statement = parse_select_statement(SBT_CH07_04)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_where_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "shohin_bunrui"])

    def test_sbt_ch07_05(self):
        statement = parse_select_statement(SBT_CH07_05)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch07_06(self):
        statement = parse_select_statement(SBT_CH07_06)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch07_07_oracle(self):
        statement = parse_select_statement(SBT_CH07_07_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch07_07_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_07_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "Shohin2"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch07_08_oracle(self):
        statement = parse_select_statement(SBT_CH07_08_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin2", "Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin2", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch07_08_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_08_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin2", "Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin2", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["shohin_id"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei"])

    def test_sbt_ch07_09_oracle(self):
        statement = parse_select_statement(SBT_CH07_09_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_09_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_09_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_10_oracle(self):
        statement = parse_select_statement(SBT_CH07_10_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["TS.tenpo_id"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_10_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_10_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["TS.tenpo_id"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_11_oracle(self):
        statement = parse_select_statement(SBT_CH07_11_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_11_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_11_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_12_oracle(self):
        statement = parse_select_statement(SBT_CH07_12_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "TenpoShohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_12_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_12_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin", "TenpoShohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])

    def test_sbt_ch07_14_oracle(self):
        statement = parse_select_statement(SBT_CH07_14_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin", "ZaikoShohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin", "ZaikoShohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo"])
        self.assertEqual(statement.get_where_used_column_list(), ["ZS.souko_id"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo", "ZS.souko_id"])

    def test_sbt_ch07_14_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_14_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin", "ZaikoShohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin", "ZaikoShohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo"])
        self.assertEqual(statement.get_where_used_column_list(), ["ZS.souko_id"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo", "ZS.souko_id"])

    def test_sbt_ch07_15_oracle(self):
        statement = parse_select_statement(SBT_CH07_15_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"])

    def test_sbt_ch07_15_sqlserver(self):
        statement = parse_select_statement(SBT_CH07_15_SQLSERVER)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin"])
        self.assertEqual(statement.get_join_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"])

    def test_sbt_ch07_16(self):
        statement = parse_select_statement(SBT_CH07_16)
        self.assertEqual(statement.get_from_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["TenpoShohin", "Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"])
        self.assertEqual(statement.get_where_used_column_list(), ["TS.shohin_id", "S.shohin_id", "TS.tenpo_id"])
        self.assertEqual(statement.get_used_column_list(), ["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "S.shohin_id"])

    def test_sbt_ch07_b(self):
        statement = parse_select_statement(SBT_CH07_B)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(statement.get_from_used_table_list(), ["EmpSkills"])
        self.assertEqual(statement.get_used_table_list(), ["EmpSkills"])
        self.assertEqual(statement.get_select_used_column_list(), ["emp"])
        self.assertEqual(statement.get_where_used_column_list(), ["skill", "ES1.emp", "ES2.emp"])
        self.assertEqual(statement.get_used_column_list(), ["emp", "skill", "ES1.emp", "ES2.emp"])

    def test_sbt_ch08_01(self):
        statement = parse_select_statement(SBT_CH08_01)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_02(self):
        statement = parse_select_statement(SBT_CH08_02)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_03(self):
        statement = parse_select_statement(SBT_CH08_03)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_04(self):
        statement = parse_select_statement(SBT_CH08_04)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch08_05(self):
        statement = parse_select_statement(SBT_CH08_05)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch08_06(self):
        statement = parse_select_statement(SBT_CH08_06)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch08_07(self):
        statement = parse_select_statement(SBT_CH08_07)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_id", "shohin_mei", "hanbai_tanka"])

    def test_sbt_ch08_08(self):
        statement = parse_select_statement(SBT_CH08_08)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_09(self):
        statement = parse_select_statement(SBT_CH08_09)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_order_by_used_column_list(), ["hanbai_tanka"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_mei", "shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_10(self):
        statement = parse_select_statement(SBT_CH08_10)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_11(self):
        statement = parse_select_statement(SBT_CH08_11)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["hanbai_tanka", "shohin_bunrui"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["hanbai_tanka", "shohin_bunrui"])

    def test_sbt_ch08_12_mysql(self):
        statement = parse_select_statement(SBT_CH08_12_MYSQL)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_12_oracle(self):
        statement = parse_select_statement(SBT_CH08_12_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "hanbai_tanka"])

    def test_sbt_ch08_13(self):
        statement = parse_select_statement(SBT_CH08_13)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])

    def test_sbt_ch08_14_mysql(self):
        statement = parse_select_statement(SBT_CH08_14_MYSQL)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])

    def test_sbt_ch08_14_oracle(self):
        statement = parse_select_statement(SBT_CH08_14_ORACLE)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])

    def test_sbt_ch08_15(self):
        statement = parse_select_statement(SBT_CH08_15)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])

    def test_sbt_ch08_16(self):
        statement = parse_select_statement(SBT_CH08_16)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])

    def test_sbt_ch08_17(self):
        statement = parse_select_statement(SBT_CH08_17)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])

    def test_sbt_ch08_18(self):
        statement = parse_select_statement(SBT_CH08_18)
        self.assertEqual(statement.get_from_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_used_table_list(), ["Shohin"])
        self.assertEqual(statement.get_select_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])
        self.assertEqual(statement.get_group_by_used_column_list(), ["shohin_bunrui", "torokubi"])
        self.assertEqual(statement.get_used_column_list(), ["shohin_bunrui", "torokubi", "hanbai_tanka"])


if __name__ == "__main__":
    unittest.main()

