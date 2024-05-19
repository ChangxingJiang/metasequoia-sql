"""
单元测试自动生成工具
"""

import json
import os
import subprocess
from typing import List, Dict

from metasequoia_sql import *
from metasequoia_sql.analyzer import (QuoteColumn, CurrentUsedQuoteColumn, CurrentSelectClauseUsedQuoteColumn,
                                      CurrentJoinClauseUsedQuoteColumn, CurrentWhereClauseUsedQuoteColumn,
                                      CurrentGroupByClauseUsedQuoteColumn, CurrentHavingClauseUsedQuoteColumn,
                                      CurrentOrderByClauseUsedQuoteColumn, AllUsedQuoteTables,
                                      AllFromClauseUsedQuoteColumn, AllJoinClauseUsedQuoteColumn,
                                      CurrentColumnSelectToDirectQuoteHash)
from metasequoia_sql.analyzer.node import StandardColumn
from metasequoia_sql.common import ordered_distinct
from scripts.demo_sql import sql_basic_tutorial


def format_rule_1(columns: List[QuoteColumn]) -> List[str]:
    return ordered_distinct([column.source() for column in columns])


def format_rule_2(columns: Dict[StandardColumn, List[QuoteColumn]]):
    return {key.source(): format_rule_1(value) for key, value in columns.items()}


def make_sql_basic_tutorial(force: bool = False):
    """构造《SQL基础教程》代码的单元测试代码"""
    # 计算 Python 单元测试脚本文件的路径
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_path, "scripts", "tests", "test_auto_build.py")

    # 执行单元测试，需有限保证旧单元测试正常运行才能重新生成单元测试代码
    if os.path.exists(file_path):
        result = subprocess.run(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0 and not force:
            print("旧单元测试不通过，无法生成新单元测试!")
            return

    # 开始生成文件
    with open(file_path, "w", encoding="UTF-8") as file:
        # 生成引用信息
        file.write("import unittest\n")
        file.write("from typing import List, Dict\n")
        file.write("\n")
        file.write("from metasequoia_sql import *\n")
        file.write("from metasequoia_sql.analyzer import *\n")
        file.write("from metasequoia_sql.analyzer.node import StandardColumn\n")
        file.write("from metasequoia_sql.common import ordered_distinct\n")
        file.write("from scripts.demo_sql.sql_basic_tutorial import *\n")
        file.write("\n")
        file.write("\n")
        file.write("def format_rule_1(columns: List[QuoteColumn]):\n")
        file.write("    return ordered_distinct([column.source() for column in columns])\n")
        file.write("\n")
        file.write("\n")
        file.write("def format_rule_2(columns: Dict[StandardColumn, List[QuoteColumn]]):\n")
        file.write("    return {key.source(): format_rule_1(value) for key, value in columns.items()}\n")
        file.write("\n")
        file.write("\n")
        file.write("class TestSqlBasicTutorial(unittest.TestCase):\n")

        # 遍历生成每一个 SQL 的解析器
        for name in dir(sql_basic_tutorial):  # 遍历 scripts.demo_sql.sql_basic.tutorial 中的每一个属性
            if not name.startswith("SBT"):
                continue  # 跳过所有不是 SBT 开头的属性

            # 词法分析
            sql = getattr(sql_basic_tutorial, name)

            if not sql.startswith("SELECT"):
                continue  # 当前只处理 SELECT 语句

            # 语法分析并打印结果
            print(f"---------- name: {name} ----------")
            print("【原始代码】")
            print(sql.strip("\n"))

            statement = SQLParser.parse_select_statement(sql)
            sql_type = SQLType.MYSQL
            if name in {"SBT_CH06_03_SQLSERVER"}:
                sql_type = SQLType.SQL_SERVER
            if name in {"SBT_CH06_06_ORACLE", "SBT_CH06_07_ORACLE", "SBT_CH06_41", "SBT_CH06_A", "SBT_CH06_B_ORACLE"}:
                sql_type = SQLType.ORACLE
            if name in {"SBT_CH06_13_DB2", "SBT_CH06_14_DB2", "SBT_CH06_15_DB2", "SBT_CH06_16_DB2"}:
                sql_type = SQLType.DB2
            print("【格式化代码】")
            print(statement.source(sql_type))

            # 构造单元测试代码
            file.write(f"    def test_{name.lower()}(self):\n")
            file.write(f"        statement = SQLParser.parse_select_statement({name})\n")

            if isinstance(statement, ASTSingleSelectStatement):
                print(f"DISTINCT: {statement.select_clause.distinct}", )
                if statement.select_clause.distinct is True:
                    file.write("        self.assertEqual(statement.select_clause.distinct, True)\n")

            # 分析器测试
            for check_analyzer in [CurrentUsedQuoteColumn,
                                   CurrentSelectClauseUsedQuoteColumn,
                                   CurrentJoinClauseUsedQuoteColumn,
                                   CurrentWhereClauseUsedQuoteColumn,
                                   CurrentGroupByClauseUsedQuoteColumn,
                                   CurrentHavingClauseUsedQuoteColumn,
                                   CurrentOrderByClauseUsedQuoteColumn,
                                   AllUsedQuoteTables,
                                   AllFromClauseUsedQuoteColumn,
                                   AllJoinClauseUsedQuoteColumn,
                                   ]:
                method_result = format_rule_1(check_analyzer.handle(statement))
                if method_result:
                    method_result_dump = json.dumps(method_result, ensure_ascii=False)
                    file.write(
                        f"        self.assertEqual({method_result_dump}, \n"
                        f"                         format_rule_1({check_analyzer.__name__}.handle(statement)))\n")

            # 分析器测试
            for check_analyzer in [CurrentColumnSelectToDirectQuoteHash,
                                   ]:
                method_result = format_rule_2(check_analyzer.handle(statement))
                if method_result:
                    method_result_dump = json.dumps(method_result, ensure_ascii=False)
                    file.write(
                        f"        self.assertEqual({method_result_dump}, \n"
                        f"                         format_rule_2({check_analyzer.__name__}.handle(statement)))\n")

            file.write("\n")

        file.write("\n")
        file.write("if __name__ == \"__main__\":\n")
        file.write("    unittest.main()\n")
        file.write("\n")


if __name__ == "__main__":
    make_sql_basic_tutorial(force=True)
