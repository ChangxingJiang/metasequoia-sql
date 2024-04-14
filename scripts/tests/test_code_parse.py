"""
metasequoia_sql.core.parser 的单元测试
"""

import unittest

from metasequoia_sql import *


class TestCoreParser(unittest.TestCase):
    """core.parser 的单元测试"""

    def test_compare_operator(self):
        """测试判断、解析比较运算符"""
        self.assertTrue(check_compare_operator("= 3"))
        self.assertTrue(check_compare_operator("< 3"))
        self.assertTrue(check_compare_operator("<= 3"))
        self.assertTrue(check_compare_operator("> 3"))
        self.assertTrue(check_compare_operator(">= 3"))
        self.assertTrue(check_compare_operator("!= 3"))
        self.assertTrue(check_compare_operator("<> 3"))
        self.assertFalse(check_compare_operator("3 + 3"))
        self.assertEqual(parse_compare_operator("= 3").source(DataSource.MYSQL), "=")
        self.assertEqual(parse_compare_operator("< 3").source(DataSource.MYSQL), "<")
        self.assertEqual(parse_compare_operator("<= 3").source(DataSource.MYSQL), "<=")
        self.assertEqual(parse_compare_operator("> 3").source(DataSource.MYSQL), ">")
        self.assertEqual(parse_compare_operator(">= 3").source(DataSource.MYSQL), ">=")
        self.assertEqual(parse_compare_operator("!= 3").source(DataSource.MYSQL), "!=")
        self.assertEqual(parse_compare_operator("<> 3").source(DataSource.MYSQL), "!=")

    def test_compute_operator(self):
        """测试判断、解析计算运算符"""
        self.assertTrue(check_compute_operator("+ 3"))
        self.assertTrue(check_compute_operator("- 3"))
        self.assertTrue(check_compute_operator("* 3"))
        self.assertTrue(check_compute_operator("/ 3"))
        self.assertTrue(check_compute_operator("% 3"))
        self.assertTrue(check_compute_operator("|| 3"))
        self.assertFalse(check_compute_operator("3 + 3"))
        self.assertEqual(parse_compute_operator("+ 3").source(DataSource.MYSQL), "+")
        self.assertEqual(parse_compute_operator("- 3").source(DataSource.MYSQL), "-")
        self.assertEqual(parse_compute_operator("* 3").source(DataSource.MYSQL), "*")
        self.assertEqual(parse_compute_operator("/ 3").source(DataSource.MYSQL), "/")
        self.assertEqual(parse_compute_operator("% 3").source(DataSource.SQL_SERVER), "%")
        self.assertEqual(parse_compute_operator("|| 'A'").source(DataSource.ORACLE), "||")

    def test_logical_operator(self):
        """测试判断、解析逻辑运算符"""
        self.assertTrue(check_logical_operator("AND a > 1"))
        self.assertTrue(check_logical_operator("OR a > 1"))
        self.assertFalse(check_logical_operator("a > 1"))
        self.assertEqual(parse_logical_operator("AND a > 1").source(DataSource.MYSQL), "AND")
        self.assertEqual(parse_logical_operator("OR a > 1").source(DataSource.MYSQL), "OR")

    def test_literal_expression(self):
        """测试判断、解析字面值表达式"""
        self.assertTrue(check_literal_expression("1 WHERE"))
        self.assertTrue(check_literal_expression("2.5 WHERE"))
        self.assertTrue(check_literal_expression("'a' WHERE"))
        self.assertTrue(check_literal_expression("x'3f' WHERE"))
        self.assertTrue(check_literal_expression("TRUE WHERE"))
        self.assertTrue(check_literal_expression("true WHERE"))
        self.assertTrue(check_literal_expression("False WHERE"))
        self.assertTrue(check_literal_expression("b'1' WHERE"))
        self.assertTrue(check_literal_expression("null WHERE"))
        self.assertTrue(check_literal_expression("NULL WHERE"))
        self.assertFalse(check_literal_expression("cnt WHERE"))
        self.assertFalse(check_literal_expression("table_name.column_name WHERE"))
        self.assertEqual(parse_literal_expression("1 WHERE").source(DataSource.MYSQL), "1")
        self.assertEqual(parse_literal_expression("2.5 WHERE").source(DataSource.MYSQL), "2.5")
        self.assertEqual(parse_literal_expression("'a' WHERE").source(DataSource.MYSQL), "'a'")
        self.assertEqual(parse_literal_expression("x'3f' WHERE").source(DataSource.MYSQL), "x'3F'")
        self.assertEqual(parse_literal_expression("TRUE WHERE").source(DataSource.MYSQL), "TRUE")
        self.assertEqual(parse_literal_expression("true WHERE").source(DataSource.MYSQL), "TRUE")
        self.assertEqual(parse_literal_expression("False WHERE").source(DataSource.MYSQL), "FALSE")
        self.assertEqual(parse_literal_expression("b'1' WHERE").source(DataSource.MYSQL), "b'1'")
        self.assertEqual(parse_literal_expression("null WHERE").source(DataSource.MYSQL), "NULL")
        self.assertEqual(parse_literal_expression("NULL WHERE").source(DataSource.MYSQL), "NULL")

    def test_column_name_expression(self):
        """测试判断、解析列名表达式"""
        self.assertFalse(check_column_name_expression("schema.function(param) AND"))
        self.assertFalse(check_column_name_expression("`schema`.`function`(param) AND"))
        self.assertTrue(check_column_name_expression("schema.column AND"))
        self.assertTrue(check_column_name_expression("`schema`.`column` AND"))
        self.assertFalse(check_column_name_expression("trim(column_name) AND"))
        self.assertFalse(check_column_name_expression("2.5 WHERE"))
        self.assertTrue(check_column_name_expression("column_name WHERE"))
        self.assertEqual(parse_column_name_expression("schema.column AND").source(DataSource.MYSQL), "schema.column")
        self.assertEqual(parse_column_name_expression("`s`.`c` AND").source(DataSource.MYSQL), "`s`.`c`")
        self.assertEqual(parse_column_name_expression("column_name WHERE").source(DataSource.MYSQL), "column_name")

    def test_function_expression(self):
        """测试判断、解析函数表达式"""
        self.assertTrue(check_function_expression("schema.function(param) AND"))
        self.assertTrue(check_function_expression("`schema`.`function`(param) AND"))
        self.assertTrue(check_function_expression("trim(column_name) AND"))
        self.assertFalse(check_function_expression("2.5 WHERE"))
        self.assertFalse(check_function_expression("column_name WHERE"))
        self.assertEqual(parse_function_expression("schema.function(param) AND").source(DataSource.MYSQL),
                         "schema.function(param)")
        self.assertEqual(parse_function_expression("`schema`.`function`(param) AND").source(DataSource.MYSQL),
                         "`schema`.`function`(param)")
        self.assertEqual(parse_function_expression("trim(column_name) AND").source(DataSource.MYSQL),
                         "trim(column_name)")

    def test_bool_expression(self):
        """测试解析布尔值表达式"""
        self.assertEqual(parse_bool_expression("column1 > 3").source(DataSource.MYSQL), "column1 > 3")
        self.assertEqual(parse_bool_expression("t2.column1 > 3").source(DataSource.MYSQL), "t2.column1 > 3")
        self.assertEqual(parse_bool_expression("t2.column1 + 3 > 3").source(DataSource.MYSQL), "t2.column1 + 3 > 3")
        self.assertEqual(parse_bool_expression("column1 BETWEEN 3 AND 4").source(DataSource.MYSQL),
                         "column1 BETWEEN 3 AND 4")
        self.assertEqual(parse_bool_expression("column1 + 3 BETWEEN 3 AND 4").source(DataSource.MYSQL),
                         "column1 + 3 BETWEEN 3 AND 4")

    def test_window_expression(self):
        """测试判断、解析窗口表达式"""
        self.assertTrue(check_window_expression("ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) AS column3"))
        self.assertFalse(check_window_expression("3 + 5"))
        self.assertEqual(
            parse_window_expression("ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) AS column3").source(
                DataSource.MYSQL),
            "ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2)")

    def test_wildcard_expression(self):
        """测试判断、解析通配符表达式"""
        self.assertTrue(check_wildcard_expression("*"))
        self.assertTrue(check_wildcard_expression("t1.*"))
        self.assertFalse(check_wildcard_expression("t1"))
        self.assertEqual(parse_wildcard_expression("*").source(DataSource.MYSQL), "*")
        self.assertEqual(parse_wildcard_expression("t1.*").source(DataSource.MYSQL), "t1.*")

    def test_condition_expression(self):
        """测试解析条件表达式"""
        self.assertEqual(parse_condition_expression("column1 > 3 AND column2 > 2 WHERE").source(DataSource.MYSQL),
                         "column1 > 3 AND column2 > 2")
        self.assertEqual(parse_condition_expression("column1 > 3 OR column2 > 2 WHERE").source(DataSource.MYSQL),
                         "column1 > 3 OR column2 > 2")
        self.assertEqual(
            parse_condition_expression("column1 > 3 OR column2 BETWEEN 2 AND 4 WHERE").source(DataSource.MYSQL),
            "column1 > 3 OR column2 BETWEEN 2 AND 4")

    def test_case_expression(self):
        """测试判断、解析 CASE 表达式"""
        self.assertTrue(check_case_expression("CASE WHEN 2 THEN 3 ELSE 4 END"))
        self.assertFalse(check_case_expression("3 + 5"))
        self.assertEqual(parse_case_expression("CASE WHEN a > 2 THEN 3 ELSE 4 END").source(DataSource.MYSQL),
                         "CASE WHEN a > 2 THEN 3 ELSE 4 END")

    def test_table_name_expression(self):
        """测试解析报名表达式"""
        self.assertEqual(parse_table_name_expression("table1.column1 AS t1").source(DataSource.MYSQL), "table1.column1")

    def test_alias_expression(self):
        """测试判断、解析别名表达式"""
        self.assertTrue(check_alias_expression("t1"))
        self.assertTrue(check_alias_expression("AS t1"))
        self.assertFalse(check_alias_expression("WHERE"))
        self.assertEqual(parse_alias_expression("t1").source(DataSource.MYSQL), "AS t1")
        self.assertEqual(parse_alias_expression("AS t1").source(DataSource.MYSQL), "AS t1")

    def test_join_expression(self):
        """测试解析关联表达式"""
        self.assertEqual(parse_join_expression("ON t1.column1 = t2.column2").source(DataSource.MYSQL),
                         "ON t1.column1 = t2.column2")
        self.assertEqual(parse_join_expression("USING(column1, column2)").source(DataSource.MYSQL),
                         "USING(column1, column2)")
        self.assertEqual(parse_join_expression("using(column1, column2)").source(DataSource.MYSQL),
                         "using(column1, column2)")

    def test_table_expression(self):
        """测试解析表表达式"""
        self.assertEquals(parse_table_expression("schema1.table1 AS t1").source(DataSource.MYSQL),
                          "schema1.table1 AS t1")

    def test_column_expression(self):
        """测试解析列表达式"""
        self.assertEqual(parse_column_expression("table1.column1 AS t1").source(DataSource.MYSQL),
                         "table1.column1 AS t1")
        self.assertEqual(parse_column_expression("3 + 5 AS t1").source(DataSource.MYSQL),
                         "3 + 5 AS t1")
        self.assertEqual(parse_column_expression("TRIM(column1) AS t1").source(DataSource.MYSQL),
                         "TRIM(column1) AS t1")

    def test_select_clause(self):
        """测试判断、解析 SELECT 子句"""
        self.assertTrue(check_select_clause("SELECT column1 AS c1, TRIM(column2) AS c2 FROM table1"))
        self.assertTrue(check_select_clause("SELECT column1 AS c1"))
        self.assertFalse(check_select_clause("FROM table1"))
        self.assertEqual(
            parse_select_clause("SELECT column1 AS c1, TRIM(column2) AS c2 FROM table1").source(DataSource.MYSQL),
            "SELECT column1 AS c1, TRIM(column2) AS c2")
        self.assertEqual(parse_select_clause("SELECT column1 AS c1").source(DataSource.MYSQL), "SELECT column1 AS c1")

    def test_from_clause(self):
        """测试判断、解析 FROM 子句"""
        self.assertTrue(check_from_clause("FROM schema1.table1 AS t1"))
        self.assertTrue(check_from_clause("FROM schema1.table1 AS t1, schema2.table2 AS t2"))
        self.assertFalse(check_from_clause("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1"))
        self.assertEqual(parse_from_clause("FROM schema1.table1 AS t1").source(DataSource.MYSQL),
                         "FROM schema1.table1 AS t1")
        self.assertEqual(parse_from_clause("FROM schema1.table1 AS t1, schema2.table2 AS t2").source(DataSource.MYSQL),
                         "FROM schema1.table1 AS t1, schema2.table2 AS t2")

    def test_join_clause(self):
        """测试判断、解析 JOIN 子句"""
        self.assertTrue(check_join_clause("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1"))
        self.assertTrue(check_join_clause("LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1"))
        self.assertFalse(check_join_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertEqual(
            parse_join_clause("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1").source(DataSource.MYSQL),
            "LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1")
        self.assertEqual(
            parse_join_clause("LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1").source(DataSource.MYSQL),
            "LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1")

    def test_where_clause(self):
        """测试判断、解析 WHERE 子句"""
        self.assertTrue(check_where_clause("WHERE column1 > 3 AND column2 > 2"))
        self.assertTrue(check_where_clause("WHERE column1 > 3 OR column2 > 2"))
        self.assertTrue(check_where_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertFalse(check_where_clause("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertEqual(parse_where_clause("WHERE column1 > 3 AND column2 > 2").source(DataSource.MYSQL),
                         "WHERE column1 > 3 AND column2 > 2")
        self.assertEqual(parse_where_clause("WHERE column1 > 3 OR column2 > 2").source(DataSource.MYSQL),
                         "WHERE column1 > 3 OR column2 > 2")
        self.assertEqual(parse_where_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4").source(DataSource.MYSQL),
                         "WHERE column1 > 3 OR column2 BETWEEN 2 AND 4")

    def test_group_by_clause(self):
        """测试判断、解析 GROUP BY 子句"""
        self.assertTrue(check_group_by_clause("GROUP BY column1, column2"))
        self.assertTrue(check_group_by_clause("GROUP BY trim(column1) ASC, column2"))
        self.assertFalse(check_group_by_clause("WHERE trim(column1) IS NOT NULL"))
        self.assertEqual(parse_group_by_clause("GROUP BY column1, column2").source(DataSource.MYSQL),
                         "GROUP BY column1, column2")
        self.assertEqual(parse_group_by_clause("GROUP BY trim(column1), column2").source(DataSource.MYSQL),
                         "GROUP BY trim(column1), column2")

    def test_having_clause(self):
        """测试判断、解析 HAVING 子句"""
        self.assertTrue(check_having_clause("HAVING column1 > 3 AND column2 > 2"))
        self.assertTrue(check_having_clause("HAVING column1 > 3 OR column2 > 2"))
        self.assertTrue(check_having_clause("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertFalse(check_having_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertEqual(parse_having_clause("HAVING column1 > 3 AND column2 > 2").source(DataSource.MYSQL),
                         "HAVING column1 > 3 AND column2 > 2")
        self.assertEqual(parse_having_clause("HAVING column1 > 3 OR column2 > 2").source(DataSource.MYSQL),
                         "HAVING column1 > 3 OR column2 > 2")
        self.assertEqual(parse_having_clause("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4").source(DataSource.MYSQL),
                         "HAVING column1 > 3 OR column2 BETWEEN 2 AND 4")

    def test_order_by_clause(self):
        """测试判断、解析 ORDER BY 子句"""
        self.assertTrue(check_order_by_clause("ORDER BY column1, column2"))
        self.assertTrue(check_order_by_clause("ORDER BY column1, column2 DESC"))
        self.assertTrue(check_order_by_clause("ORDER BY trim(column1) ASC, column2"))
        self.assertFalse(check_order_by_clause("WHERE trim(column1) IS NOT NULL"))
        self.assertEqual(parse_order_by_clause("ORDER BY column1, column2").source(DataSource.MYSQL),
                         "ORDER BY column1, column2")
        self.assertEqual(parse_order_by_clause("ORDER BY column1, column2 DESC").source(DataSource.MYSQL),
                         "ORDER BY column1, column2 DESC")
        self.assertEqual(parse_order_by_clause("ORDER BY trim(column1) ASC, column2").source(DataSource.MYSQL),
                         "ORDER BY trim(column1), column2")

    def test_limit_clause(self):
        """测试判断、解析 LIMIT 子句"""
        self.assertTrue(check_limit_clause("LIMIT 2, 5"))
        self.assertTrue(check_limit_clause("LIMIT 5 OFFSET 2"))
        self.assertFalse(check_limit_clause("ORDER BY column1"))
        self.assertEqual(parse_limit_clause("LIMIT 2, 5").source(DataSource.MYSQL), "LIMIT 2, 5")
        self.assertEqual(parse_limit_clause("LIMIT 5 OFFSET 2").source(DataSource.MYSQL), "LIMIT 2, 5")
