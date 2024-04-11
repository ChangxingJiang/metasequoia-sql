"""
单元测试自动生成工具
"""

import json
import os
import subprocess

from metasequoia_sql.common import build_token_scanner
from metasequoia_sql.parser.expression import parse_select_statement, maybe_select_statement
from metasequoia_sql.objects.core import SQLSingleSelectStatement
from metasequoia_sql.objects import DataSource
from scripts.demo import sql_basic_tutorial


def make_sql_basic_tutorial(force: bool = False):
    """构造《SQL基础教程》代码的单元测试代码"""
    # 计算 Python 单元测试脚本文件的路径
    project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_path, "auto_test", "sql_basic_tutorial.py")

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
        file.write("\n")
        file.write("from metasequoia_sql.common import build_token_scanner\n")
        file.write("from metasequoia_sql.parser.common import parse_select_statement\n")
        file.write("from scripts.demo.sql_basic_tutorial import *\n")
        file.write("\n")
        file.write("\n")

        # 生成类名
        file.write("class TestSqlBasicTutorial(unittest.TestCase):\n")

        # 遍历生成每一个 SQL 的解析器
        for name in dir(sql_basic_tutorial):  # 遍历 scripts.demo.sql_basic.tutorial 中的每一个属性
            if not name.startswith("SBT"):
                continue  # 跳过所有不是 SBT 开头的属性

            # 词法分析
            sql = getattr(sql_basic_tutorial, name)
            scanner = build_token_scanner(sql)

            if not maybe_select_statement(scanner):
                continue  # 当前只处理 SELECT 语句

            # 语法分析并打印结果
            print(f"---------- name: {name} ----------")
            print("【原始代码】")
            print(sql.strip("\n"))

            statement = parse_select_statement(scanner)
            data_source = DataSource.MYSQL
            if name in {"SBT_CH06_03_SQLSERVER"}:
                data_source = DataSource.SQL_SERVER
            if name in {"SBT_CH06_06_ORACLE", "SBT_CH06_07_ORACLE", "SBT_CH06_41", "SBT_CH06_A", "SBT_CH06_B_ORACLE"}:
                data_source = DataSource.ORACLE
            print("【格式化代码】")
            print(statement.source(data_source))

            print("【分析结果】")
            print(f"SELECT_USED_COLUMN: {json.dumps(statement.get_select_used_column_list(), ensure_ascii=False)}")
            print(f"USED_TABLE: {json.dumps(statement.get_from_used_table_list(), ensure_ascii=False)}")
            print(f"WHERE_USED_COLUMN: {json.dumps(statement.get_where_used_column_list(), ensure_ascii=False)}")
            print(f"GROUP_BY_USED_COLUMN: {json.dumps(statement.get_group_by_used_column_list(), ensure_ascii=False)}")
            print(f"HAVING_USED_COLUMN: {json.dumps(statement.get_having_used_column_list(), ensure_ascii=False)}")
            print(f"ORDER_BY_USED_COLUMN: {json.dumps(statement.get_order_by_used_column_list(), ensure_ascii=False)}")

            # 构造单元测试代码
            file.write(f"    def test_{name.lower()}(self):\n")
            file.write(f"        statement = parse_select_statement(build_token_scanner({name}))\n")

            if isinstance(statement, SQLSingleSelectStatement):
                print(f"DISTINCT: {statement.select_clause.distinct}", )
                if statement.select_clause.distinct is True:
                    file.write("        self.assertEqual(statement.select_clause.distinct, True)\n")

            # 返回列表的方法
            for method_name in [
                "get_from_used_table_list",
                "get_join_used_table_list",
                "get_used_table_list",
                "get_select_used_column_list",
                "get_where_used_column_list",
                "get_group_by_used_column_list",
                "get_having_used_column_list",
                "get_order_by_used_column_list",
                "get_used_column_list"
            ]:
                method_result = getattr(statement, method_name)()
                method_result_dump = json.dumps(method_result, ensure_ascii=False)
                print(f"statement.{method_name}: {method_result_dump}")
                if len(method_result) > 0:
                    file.write(f"        self.assertEqual(statement.{method_name}(), {method_result_dump})\n")

            file.write("\n")

        file.write("\n")
        file.write("if __name__ == \"__main__\":\n")
        file.write("    unittest.main()\n")
        file.write("\n")


if __name__ == "__main__":
    make_sql_basic_tutorial()
