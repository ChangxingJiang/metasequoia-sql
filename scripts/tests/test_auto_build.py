import unittest
from typing import List

from metasequoia_sql import *
from scripts.demo_sql.sql_basic_tutorial import *
from metasequoia_sql.analyzer import *
from metasequoia_sql.common import ordered_distinct


def format_source_column_list(columns: List[QuoteColumn]):
    return ordered_distinct([column.source() for column in columns])


class TestSqlBasicTutorial(unittest.TestCase):
    def test_sbt_ch02_01(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_01)
        self.assertEqual(["shohin_id", "shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_02(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_02)
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_03(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_03)
        self.assertEqual(["shohin_id", "shohin_mei", "shohin_bunrui", "hanbai_tanka", "shiire_tanka", "torokubi"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "shohin_bunrui", "hanbai_tanka", "shiire_tanka", "torokubi"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_04(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_04)
        self.assertEqual(["shohin_id", "shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_05(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_05)
        self.assertEqual(["shohin_id", "shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_06(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_06)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_07(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_07)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_08(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_08)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_09(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_09)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_10(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_10)
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_11(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_11)
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_13(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_13)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_14(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_14)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_15(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_15)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_16(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_16)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_17(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_17)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_18(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_18)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_19(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_19)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_20(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_20)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_21(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_21)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["torokubi"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_22(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_22)
        self.assertEqual(["shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_24(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_24)
        self.assertEqual(["chr"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["chr"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["chr"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Chars"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Chars"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_25(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_25)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_26(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_26)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_27(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_27)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_28(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_28)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_29(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_29)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_30(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_30)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_31(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_31)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_32(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_32)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_33(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_33)
        self.assertEqual(["shohin_mei", "shiire_tanka", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_34(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_34)
        self.assertEqual(["shohin_mei", "shiire_tanka", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_35(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_35)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_36(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_36)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_a_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_A_DB2)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_a_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_A_ORACLE)
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch02_a_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH02_A_SQLSERVER)

    def test_sbt_ch03_01(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_01)
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_02(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_02)
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_04(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_04)
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_05(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_05)
        self.assertEqual(["hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_06(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_06)
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_07(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_07)
        self.assertEqual(["hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_08(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_08)
        self.assertEqual(["hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_09(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_09)
        self.assertEqual(["torokubi"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["torokubi"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_10(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_10)
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_11(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_11)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_12(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_12)
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_13(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_13)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_14(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_14)
        self.assertEqual(["shiire_tanka", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_15(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_15)
        self.assertEqual(["shiire_tanka", "*", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_16(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_16)
        self.assertEqual(["shohin_mei", "shiire_tanka", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_17(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_17)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_18(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_18)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_19(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_19)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_20(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_20)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentHavingClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_21(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_21)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_22(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_22)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_23(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_23)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentHavingClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_24(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_24)
        self.assertEqual(["shohin_bunrui", "*", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei"], 
                         format_source_column_list(CurrentHavingClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_25(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_25)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentHavingClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_26(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_26)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_27(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_27)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_28(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_28)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_29(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_29)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_30(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_30)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_31(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_31)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_32(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_32)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_33(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_33)
        self.assertEqual(["shohin_mei", "hanbai_tanka", "shiire_tanka", "shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_34(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_34)
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_35_1(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_35_1)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_35_2(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_35_2)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_a_1(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_A_1)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch03_a_2(self):
        statement = SQLParser.parse_select_statement(SBT_CH03_A_2)
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_01(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_01)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_03(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_03)
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["ShohinSum"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["ShohinSum"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_09_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_09_ORACLE)
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_09_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_09_SQLSERVER)
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_10_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_10_ORACLE)
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_10_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_10_SQLSERVER)
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "cnt_shohin"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_11(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_11)
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_12(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_12)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_13(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_13)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_14(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_14)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentHavingClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_15(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_15)
        self.assertEqual(["hanbai_tanka", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_16_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_16_ORACLE)
        self.assertEqual(["shohin_bunrui", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch05_16_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH05_16_SQLSERVER)
        self.assertEqual(["shohin_bunrui", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_02(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_02)
        self.assertEqual(["m"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["m"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_03_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_03_ORACLE)
        self.assertEqual(["n", "p"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["n", "p"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_03_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_03_SQLSERVER)
        self.assertEqual(["n", "p"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["n", "p"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_04(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_04)
        self.assertEqual(["m", "n"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["m", "n"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleMath"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_06_mysql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_06_MYSQL)
        self.assertEqual(["str1", "str2"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1", "str2"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_06_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_06_ORACLE)
        self.assertEqual(["str1", "str2"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1", "str2"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_06_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_06_SQLSERVER)
        self.assertEqual(["str1", "str2"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1", "str2"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_07_mysql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_07_MYSQL)
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_07_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_07_ORACLE)
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_08_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_08_ORACLE)
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_08_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_08_SQLSERVER)
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_09(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_09)
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_10(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_10)
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_11_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_11_ORACLE)
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_11_postgresql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_11_POSTGRESQL)
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_11_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_11_SQLSERVER)
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_12(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_12)
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_13_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_13_DB2)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_13_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_13_ORACLE)
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_13_postgresql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_13_POSTGRESQL)

    def test_sbt_ch06_13_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_13_SQLSERVER)

    def test_sbt_ch06_14_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_14_DB2)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_14_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_14_ORACLE)
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_14_postgresql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_14_POSTGRESQL)

    def test_sbt_ch06_14_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_14_SQLSERVER)

    def test_sbt_ch06_15_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_15_DB2)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_15_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_15_ORACLE)
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_15_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_15_SQLSERVER)

    def test_sbt_ch06_16_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_16_DB2)
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_16_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_16_ORACLE)
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_16_postgresql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_16_POSTGRESQL)
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_16_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_16_SQLSERVER)
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["YEAR", "MONTH", "DAY", "HOUR", "MINUTE", "SECOND"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_17_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_17_DB2)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_17_mysql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_17_MYSQL)

    def test_sbt_ch06_17_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_17_ORACLE)
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_17_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_17_SQLSERVER)
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_18_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_18_DB2)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_18_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_18_ORACLE)
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["DUAL"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_18_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_18_SQLSERVER)

    def test_sbt_ch06_19_db2(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_19_DB2)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_19_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_19_ORACLE)
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SYSIBM.SYSDUMMY1"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_19_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_19_SQLSERVER)

    def test_sbt_ch06_20(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_20)
        self.assertEqual(["str2"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str2"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_22(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_22)
        self.assertEqual(["*", "strcol"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["strcol"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_23(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_23)
        self.assertEqual(["*", "strcol"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["strcol"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_24(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_24)
        self.assertEqual(["*", "strcol"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["strcol"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_25(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_25)
        self.assertEqual(["*", "strcol"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["strcol"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_26(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_26)
        self.assertEqual(["*", "strcol"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["*"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["strcol"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleLike"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_27(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_27)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_28(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_28)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_29(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_29)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_30(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_30)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_31(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_31)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_32(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_32)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_33(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_33)
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shiire_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shiire_tanka"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_36(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_36)
        self.assertEqual(["shohin_mei", "hanbai_tanka", "shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_37(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_37)
        self.assertEqual(["shohin_mei", "hanbai_tanka", "shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_38_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_38_ORACLE)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_38_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_38_SQLSERVER)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_39_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_39_ORACLE)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_39_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_39_SQLSERVER)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_40_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_40_ORACLE)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_40_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_40_SQLSERVER)
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_41(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_41)
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_43(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_43)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_7_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_7_SQLSERVER)
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["str1", "str2", "str3"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["SampleStr"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_a(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_A)
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_b_mysql(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_B_MYSQL)
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch06_b_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH06_B_ORACLE)
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_03(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_03)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_04(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_04)
        self.assertEqual(["shohin_id", "shohin_mei", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_05(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_05)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_06(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_06)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_07_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_07_ORACLE)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_07_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_07_SQLSERVER)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin", "Shohin2"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_08_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_08_ORACLE)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin2", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin2", "Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_08_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_08_SQLSERVER)
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin2", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin2", "Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_09_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_09_ORACLE)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "S.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_09_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_09_SQLSERVER)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "S.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_10_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_10_ORACLE)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "S.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_10_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_10_SQLSERVER)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "S.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_11_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_11_ORACLE)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "TS.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_11_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_11_SQLSERVER)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "TS.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_12_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_12_ORACLE)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "TS.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_12_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_12_SQLSERVER)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "TS.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "S.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "TenpoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_14_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_14_ORACLE)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo", "S.shohin_id", "ZS.shohin_id", "ZS.souko_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id", "ZS.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["ZS.souko_id"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin", "ZaikoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "ZaikoShohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_14_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_14_SQLSERVER)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo", "S.shohin_id", "ZS.shohin_id", "ZS.souko_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "ZS.zaiko_suryo"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id", "ZS.shohin_id"], 
                         format_source_column_list(CurrentJoinClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["ZS.souko_id"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin", "ZaikoShohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin", "ZaikoShohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_15_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_15_ORACLE)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_15_sqlserver(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_15_SQLSERVER)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllJoinClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_16(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_16)
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka", "S.shohin_id"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.tenpo_id", "TS.tenpo_mei", "TS.shohin_id", "S.shohin_mei", "S.hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TS.shohin_id", "S.shohin_id", "TS.tenpo_id"], 
                         format_source_column_list(CurrentWhereClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["TenpoShohin", "Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch07_b(self):
        statement = SQLParser.parse_select_statement(SBT_CH07_B)
        self.assertEqual(statement.select_clause.distinct, True)
        self.assertEqual(["emp"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["emp"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["EmpSkills", "Skills"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["EmpSkills"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_01(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_01)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_02(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_02)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_03(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_03)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_04(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_04)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_05(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_05)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_07(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_07)
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_id", "shohin_mei", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_08(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_08)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_09(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_09)
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_mei", "shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka"], 
                         format_source_column_list(CurrentOrderByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_10(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_10)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_11(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_11)
        self.assertEqual(["hanbai_tanka", "shohin_bunrui"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["hanbai_tanka", "shohin_bunrui"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_12_mysql(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_12_MYSQL)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_12_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_12_ORACLE)
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_13(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_13)
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_14_mysql(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_14_MYSQL)
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_14_oracle(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_14_ORACLE)
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_15(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_15)
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_16(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_16)
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_17(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_17)
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))

    def test_sbt_ch08_18(self):
        statement = SQLParser.parse_select_statement(SBT_CH08_18)
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi", "hanbai_tanka"], 
                         format_source_column_list(CurrentSelectClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["shohin_bunrui", "torokubi"], 
                         format_source_column_list(CurrentGroupByClauseUsedQuoteColumn.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllUsedQuoteTables.handle(statement)))
        self.assertEqual(["Shohin"], 
                         format_source_column_list(AllFromClauseUsedQuoteColumn.handle(statement)))


if __name__ == "__main__":
    unittest.main()

