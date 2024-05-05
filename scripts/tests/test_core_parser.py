"""
metasequoia_sql.core.parser 的单元测试
"""

import unittest

from metasequoia_sql import *


class TestCoreParser(unittest.TestCase):
    """core.parser 的单元测试"""

    def test_compare_operator(self):
        """测试判断、解析比较运算符"""
        self.assertTrue(SQLParser.check_compare_operator("= 3"))
        self.assertTrue(SQLParser.check_compare_operator("< 3"))
        self.assertTrue(SQLParser.check_compare_operator("<= 3"))
        self.assertTrue(SQLParser.check_compare_operator("> 3"))
        self.assertTrue(SQLParser.check_compare_operator(">= 3"))
        self.assertTrue(SQLParser.check_compare_operator("!= 3"))
        self.assertTrue(SQLParser.check_compare_operator("<> 3"))
        self.assertFalse(SQLParser.check_compare_operator("3 + 3"))
        self.assertEqual(SQLParser.parse_compare_operator("= 3").source(SQLType.MYSQL), "=")
        self.assertEqual(SQLParser.parse_compare_operator("< 3").source(SQLType.MYSQL), "<")
        self.assertEqual(SQLParser.parse_compare_operator("<= 3").source(SQLType.MYSQL), "<=")
        self.assertEqual(SQLParser.parse_compare_operator("> 3").source(SQLType.MYSQL), ">")
        self.assertEqual(SQLParser.parse_compare_operator(">= 3").source(SQLType.MYSQL), ">=")
        self.assertEqual(SQLParser.parse_compare_operator("!= 3").source(SQLType.MYSQL), "!=")
        self.assertEqual(SQLParser.parse_compare_operator("<> 3").source(SQLType.MYSQL), "!=")

    def test_compute_operator(self):
        """测试判断、解析计算运算符"""
        self.assertTrue(SQLParser.check_compute_operator("+ 3"))
        self.assertTrue(SQLParser.check_compute_operator("- 3"))
        self.assertTrue(SQLParser.check_compute_operator("* 3"))
        self.assertTrue(SQLParser.check_compute_operator("/ 3"))
        self.assertTrue(SQLParser.check_compute_operator("% 3"))
        self.assertTrue(SQLParser.check_compute_operator("|| 3"))
        self.assertFalse(SQLParser.check_compute_operator("3 + 3"))
        self.assertEqual(SQLParser.parse_compute_operator("+ 3").source(SQLType.MYSQL), "+")
        self.assertEqual(SQLParser.parse_compute_operator("- 3").source(SQLType.MYSQL), "-")
        self.assertEqual(SQLParser.parse_compute_operator("* 3").source(SQLType.MYSQL), "*")
        self.assertEqual(SQLParser.parse_compute_operator("/ 3").source(SQLType.MYSQL), "/")
        self.assertEqual(SQLParser.parse_compute_operator("% 3").source(SQLType.SQL_SERVER), "%")
        self.assertEqual(SQLParser.parse_compute_operator("|| 'A'").source(SQLType.ORACLE), "||")

    def test_logical_operator(self):
        """测试判断、解析逻辑运算符"""
        self.assertTrue(SQLParser.check_logical_operator("AND a > 1"))
        self.assertTrue(SQLParser.check_logical_operator("OR a > 1"))
        self.assertFalse(SQLParser.check_logical_operator("a > 1"))
        self.assertEqual(SQLParser.parse_logical_operator("AND a > 1").source(SQLType.MYSQL), "AND")
        self.assertEqual(SQLParser.parse_logical_operator("OR a > 1").source(SQLType.MYSQL), "OR")

    def test_literal_expression(self):
        """测试判断、解析字面值表达式"""
        self.assertTrue(SQLParser.check_literal_expression("1 WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("2.5 WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("'a' WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("x'3f' WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("TRUE WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("true WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("False WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("b'1' WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("null WHERE"))
        self.assertTrue(SQLParser.check_literal_expression("NULL WHERE"))
        self.assertFalse(SQLParser.check_literal_expression("cnt WHERE"))
        self.assertFalse(SQLParser.check_literal_expression("table_name.column_name WHERE"))
        self.assertEqual(SQLParser.parse_literal_expression("1 WHERE", unary_operator=None).source(SQLType.MYSQL), "1")
        self.assertEqual(SQLParser.parse_literal_expression("2.5 WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "2.5")
        self.assertEqual(SQLParser.parse_literal_expression("'a' WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "'a'")
        self.assertEqual(SQLParser.parse_literal_expression("x'3f' WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "x'3f'")
        self.assertEqual(SQLParser.parse_literal_expression("TRUE WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "TRUE")
        self.assertEqual(SQLParser.parse_literal_expression("true WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "true")
        self.assertEqual(SQLParser.parse_literal_expression("False WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "False")
        self.assertEqual(SQLParser.parse_literal_expression("b'1' WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "b'1'")
        self.assertEqual(SQLParser.parse_literal_expression("null WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "null")
        self.assertEqual(SQLParser.parse_literal_expression("NULL WHERE", unary_operator=None).source(SQLType.MYSQL),
                         "NULL")

    def test_column_name_expression(self):
        """测试判断、解析列名表达式"""
        self.assertFalse(SQLParser.check_column_name_expression("schema.function(param) AND"))
        self.assertFalse(SQLParser.check_column_name_expression("`schema`.`function`(param) AND"))
        self.assertTrue(SQLParser.check_column_name_expression("schema.column AND"))
        self.assertTrue(SQLParser.check_column_name_expression("`schema`.`column` AND"))
        self.assertFalse(SQLParser.check_column_name_expression("trim(column_name) AND"))
        self.assertFalse(SQLParser.check_column_name_expression("2.5 WHERE"))
        self.assertTrue(SQLParser.check_column_name_expression("column_name WHERE"))
        self.assertEqual(
            SQLParser.parse_column_name_expression("schema.column AND", unary_operator=None).source(SQLType.MYSQL),
            "`schema`.`column`")
        self.assertEqual(
            SQLParser.parse_column_name_expression("`s`.`c` AND", unary_operator=None).source(SQLType.MYSQL), "`s`.`c`")
        self.assertEqual(
            SQLParser.parse_column_name_expression("column_name WHERE", unary_operator=None).source(SQLType.MYSQL),
            "`column_name`")

    def test_function_expression(self):
        """测试判断、解析函数表达式"""
        self.assertTrue(SQLParser.check_function_expression("schema.function(param) AND"))
        self.assertTrue(SQLParser.check_function_expression("`schema`.`function`(param) AND"))
        self.assertTrue(SQLParser.check_function_expression("trim(column_name) AND"))
        self.assertFalse(SQLParser.check_function_expression("2.5 WHERE"))
        self.assertFalse(SQLParser.check_function_expression("column_name WHERE"))
        self.assertEqual(SQLParser.parse_function_expression("schema.function(param) AND").source(SQLType.MYSQL),
                         "`schema`.function(`param`)")
        self.assertEqual(SQLParser.parse_function_expression("`schema`.`function`(param) AND").source(SQLType.MYSQL),
                         "`schema`.function(`param`)")
        self.assertEqual(SQLParser.parse_function_expression("trim(`column_name`) AND").source(SQLType.MYSQL),
                         "trim(`column_name`)")

    def test_bool_expression(self):
        """测试解析布尔值表达式"""
        self.assertEqual(SQLParser.parse_condition_expression("column1 > 3").source(SQLType.MYSQL), "`column1` > 3")
        self.assertEqual(SQLParser.parse_condition_expression("t2.column1 > 3").source(SQLType.MYSQL),
                         "`t2`.`column1` > 3")
        self.assertEqual(SQLParser.parse_condition_expression("t2.column1 + 3 > 3").source(SQLType.MYSQL),
                         "`t2`.`column1` + 3 > 3")
        self.assertEqual(SQLParser.parse_condition_expression("column1 BETWEEN 3 AND 4").source(SQLType.MYSQL),
                         "`column1` BETWEEN 3 AND 4")
        self.assertEqual(SQLParser.parse_condition_expression("column1 + 3 BETWEEN 3 AND 4").source(SQLType.MYSQL),
                         "`column1` + 3 BETWEEN 3 AND 4")

    def test_window_expression(self):
        """测试判断、解析窗口表达式"""
        self.assertTrue(
            SQLParser.check_window_expression("ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) AS column3"))
        self.assertFalse(SQLParser.check_window_expression("3 + 5"))
        self.assertEqual(
            SQLParser.parse_window_expression(
                "ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) AS column3", unary_operator=None).source(
                SQLType.MYSQL),
            "ROW_NUMBER() OVER (PARTITION BY `column1` ORDER BY `column2`)")

    def test_wildcard_expression(self):
        """测试判断、解析通配符表达式"""
        self.assertTrue(SQLParser.check_wildcard_expression("*"))
        self.assertTrue(SQLParser.check_wildcard_expression("t1.*"))
        self.assertFalse(SQLParser.check_wildcard_expression("t1"))
        self.assertEqual(SQLParser.parse_wildcard_expression("*", unary_operator=None).source(SQLType.MYSQL), "*")
        self.assertEqual(SQLParser.parse_wildcard_expression("t1.*", unary_operator=None).source(SQLType.MYSQL), "t1.*")

    def test_condition_expression(self):
        """测试解析条件表达式"""
        self.assertEqual(
            SQLParser.parse_general_expression("column1 > 3 AND column2 > 2 WHERE").source(SQLType.MYSQL),
            "`column1` > 3 AND `column2` > 2")
        self.assertEqual(SQLParser.parse_general_expression("column1 > 3 OR column2 > 2 WHERE").source(SQLType.MYSQL),
                         "`column1` > 3 OR `column2` > 2")
        self.assertEqual(
            SQLParser.parse_general_expression("column1 > 3 OR column2 BETWEEN 2 AND 4 WHERE").source(SQLType.MYSQL),
            "`column1` > 3 OR `column2` BETWEEN 2 AND 4")

    def test_case_expression(self):
        """测试判断、解析 CASE 表达式"""
        self.assertTrue(SQLParser.check_case_expression("CASE WHEN 2 THEN 3 ELSE 4 END"))
        self.assertFalse(SQLParser.check_case_expression("3 + 5"))
        self.assertEqual(
            SQLParser.parse_case_expression("CASE WHEN a > 2 THEN 3 ELSE 4 END", unary_operator=None).source(
                SQLType.MYSQL),
            "CASE WHEN `a` > 2 THEN 3 ELSE 4 END")

    def test_table_name_expression(self):
        """测试解析报名表达式"""
        self.assertEqual(SQLParser.parse_table_name_expression("schema1.table1 AS t1").source(SQLType.MYSQL),
                         "`schema1.table1`")

    def test_alias_expression(self):
        """测试判断、解析别名表达式"""
        self.assertTrue(SQLParser.check_alias_expression("t1"))
        self.assertTrue(SQLParser.check_alias_expression("AS t1"))
        self.assertFalse(SQLParser.check_alias_expression("WHERE"))
        self.assertEqual(SQLParser.parse_alias_expression("t1").source(SQLType.MYSQL), "AS t1")
        self.assertEqual(SQLParser.parse_alias_expression("AS t1").source(SQLType.MYSQL), "AS t1")

    def test_join_expression(self):
        """测试解析关联表达式"""
        self.assertEqual(SQLParser.parse_join_expression("ON t1.column1 = t2.column2").source(SQLType.MYSQL),
                         "ON `t1`.`column1` = `t2`.`column2`")
        self.assertEqual(SQLParser.parse_join_expression("USING(column1, column2)").source(SQLType.MYSQL),
                         "USING(`column1`, `column2`)")
        self.assertEqual(SQLParser.parse_join_expression("using(column1, column2)").source(SQLType.MYSQL),
                         "using(`column1`, `column2`)")

    def test_table_expression(self):
        """测试解析表表达式"""
        self.assertEquals(SQLParser.parse_table_expression("schema1.table1 AS t1").source(SQLType.MYSQL),
                          "`schema1.table1` AS t1")

    def test_column_expression(self):
        """测试解析列表达式"""
        self.assertEqual(SQLParser.parse_column_expression("table1.column1 AS t1").source(SQLType.MYSQL),
                         "`table1`.`column1` AS t1")
        self.assertEqual(SQLParser.parse_column_expression("3 + 5 AS t1").source(SQLType.MYSQL),
                         "3 + 5 AS t1")
        self.assertEqual(SQLParser.parse_column_expression("TRIM(column1) AS t1").source(SQLType.MYSQL),
                         "TRIM(`column1`) AS t1")

    def test_select_clause(self):
        """测试判断、解析 SELECT 子句"""
        self.assertTrue(SQLParser.check_select_clause("SELECT column1 AS c1, TRIM(column2) AS c2 FROM table1"))
        self.assertTrue(SQLParser.check_select_clause("SELECT column1 AS c1"))
        self.assertFalse(SQLParser.check_select_clause("FROM table1"))
        self.assertEqual(
            SQLParser.parse_select_clause("SELECT column1 AS c1, TRIM(column2) AS c2 FROM table1").source(
                SQLType.MYSQL),
            "SELECT `column1` AS c1, TRIM(`column2`) AS c2")
        self.assertEqual(SQLParser.parse_select_clause("SELECT column1 AS c1").source(SQLType.MYSQL),
                         "SELECT `column1` AS c1")

    def test_from_clause(self):
        """测试判断、解析 FROM 子句"""
        self.assertTrue(SQLParser.check_from_clause("FROM schema1.table1 AS t1"))
        self.assertTrue(SQLParser.check_from_clause("FROM schema1.table1 AS t1, schema2.table2 AS t2"))
        self.assertFalse(SQLParser.check_from_clause("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1"))
        self.assertEqual(SQLParser.parse_from_clause("FROM schema1.table1 AS t1").source(SQLType.MYSQL),
                         "FROM `schema1.table1` AS t1")
        self.assertEqual(
            SQLParser.parse_from_clause("FROM schema1.table1 AS t1, schema2.table2 AS t2").source(SQLType.MYSQL),
            "FROM `schema1.table1` AS t1, `schema2.table2` AS t2")

    def test_join_clause(self):
        """测试判断、解析 JOIN 子句"""
        self.assertTrue(SQLParser.check_join_clause("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1"))
        self.assertTrue(SQLParser.check_join_clause("LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1"))
        self.assertFalse(SQLParser.check_join_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertEqual(
            SQLParser.parse_join_clause("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1").source(SQLType.MYSQL),
            "LEFT JOIN `table2` AS t2 ON `t1`.`column1` = `t2`.`column1`")
        self.assertEqual(
            SQLParser.parse_join_clause("LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1").source(
                SQLType.MYSQL),
            "LEFT JOIN `schema2.table2` AS t2 ON `t1`.`column1` = `t2`.`column1`")

    def test_where_clause(self):
        """测试判断、解析 WHERE 子句"""
        self.assertTrue(SQLParser.check_where_clause("WHERE column1 > 3 AND column2 > 2"))
        self.assertTrue(SQLParser.check_where_clause("WHERE column1 > 3 OR column2 > 2"))
        self.assertTrue(SQLParser.check_where_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertFalse(SQLParser.check_where_clause("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertEqual(SQLParser.parse_where_clause("WHERE column1 > 3 AND column2 > 2").source(SQLType.MYSQL),
                         "WHERE `column1` > 3 AND `column2` > 2")
        self.assertEqual(SQLParser.parse_where_clause("WHERE column1 > 3 OR column2 > 2").source(SQLType.MYSQL),
                         "WHERE `column1` > 3 OR `column2` > 2")
        self.assertEqual(
            SQLParser.parse_where_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4").source(SQLType.MYSQL),
            "WHERE `column1` > 3 OR `column2` BETWEEN 2 AND 4")

    def test_group_by_clause(self):
        """测试判断、解析 GROUP BY 子句"""
        self.assertTrue(SQLParser.check_group_by_clause("GROUP BY column1, column2"))
        self.assertTrue(SQLParser.check_group_by_clause("GROUP BY trim(column1) ASC, column2"))
        self.assertFalse(SQLParser.check_group_by_clause("WHERE trim(column1) IS NOT NULL"))
        self.assertEqual(SQLParser.parse_group_by_clause("GROUP BY column1, column2").source(SQLType.MYSQL),
                         "GROUP BY `column1`, `column2`")
        self.assertEqual(SQLParser.parse_group_by_clause("GROUP BY trim(column1), column2").source(SQLType.MYSQL),
                         "GROUP BY trim(`column1`), `column2`")

    def test_having_clause(self):
        """测试判断、解析 HAVING 子句"""
        self.assertTrue(SQLParser.check_having_clause("HAVING column1 > 3 AND column2 > 2"))
        self.assertTrue(SQLParser.check_having_clause("HAVING column1 > 3 OR column2 > 2"))
        self.assertTrue(SQLParser.check_having_clause("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertFalse(SQLParser.check_having_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
        self.assertEqual(SQLParser.parse_having_clause("HAVING column1 > 3 AND column2 > 2").source(SQLType.MYSQL),
                         "HAVING `column1` > 3 AND `column2` > 2")
        self.assertEqual(SQLParser.parse_having_clause("HAVING column1 > 3 OR column2 > 2").source(SQLType.MYSQL),
                         "HAVING `column1` > 3 OR `column2` > 2")
        self.assertEqual(
            SQLParser.parse_having_clause("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4").source(SQLType.MYSQL),
            "HAVING `column1` > 3 OR `column2` BETWEEN 2 AND 4")

    def test_order_by_clause(self):
        """测试判断、解析 ORDER BY 子句"""
        self.assertTrue(SQLParser.check_order_by_clause("ORDER BY column1, column2"))
        self.assertTrue(SQLParser.check_order_by_clause("ORDER BY column1, column2 DESC"))
        self.assertTrue(SQLParser.check_order_by_clause("ORDER BY trim(column1) ASC, column2"))
        self.assertFalse(SQLParser.check_order_by_clause("WHERE trim(column1) IS NOT NULL"))
        self.assertEqual(SQLParser.parse_order_by_clause("ORDER BY column1, column2").source(SQLType.MYSQL),
                         "ORDER BY `column1`, `column2`")
        self.assertEqual(SQLParser.parse_order_by_clause("ORDER BY column1, column2 DESC").source(SQLType.MYSQL),
                         "ORDER BY `column1`, `column2` DESC")
        self.assertEqual(SQLParser.parse_order_by_clause("ORDER BY trim(column1) ASC, column2").source(SQLType.MYSQL),
                         "ORDER BY trim(`column1`), `column2`")

    def test_limit_clause(self):
        """测试判断、解析 LIMIT 子句"""
        self.assertTrue(SQLParser.check_limit_clause("LIMIT 2, 5"))
        self.assertTrue(SQLParser.check_limit_clause("LIMIT 5 OFFSET 2"))
        self.assertFalse(SQLParser.check_limit_clause("ORDER BY column1"))
        self.assertEqual(SQLParser.parse_limit_clause("LIMIT 2, 5").source(SQLType.MYSQL), "LIMIT 2, 5")
        self.assertEqual(SQLParser.parse_limit_clause("LIMIT 5 OFFSET 2").source(SQLType.MYSQL), "LIMIT 2, 5")

    def test_set_statement(self):
        """测试 SET 语句"""
        self.assertTrue((SQLParser.parse_set_statement("SET a.c = b")).source(), "SET a.c = b")

    def test_parse_config_string_expression(self):
        """测试 parse_config_string_expression 方法"""
        demo_sql = "spark.sql.hive.metastorePartitionPruning=true"
        ast_node = SQLParser.parse_config_string_expression(demo_sql)
        self.assertEqual(ast_node.name, "spark.sql.hive.metastorePartitionPruning")
        self.assertEqual(ast_node.value, "true")

        demo_sql = "hive.lock.sleep.between.retries=1000ms"
        ast_node = SQLParser.parse_config_string_expression(demo_sql)
        self.assertEqual(ast_node.name, "hive.lock.sleep.between.retries")
        self.assertEqual(ast_node.value, "1000ms")

        demo_sql = "spark.serializer=org.apache.spark.serializer.KryoSerializer"
        ast_node = SQLParser.parse_config_string_expression(demo_sql)
        self.assertEqual(ast_node.name, "spark.serializer")
        self.assertEqual(ast_node.value, "org.apache.spark.serializer.KryoSerializer")

        demo_sql = "spark.hadoop.parquet.enable.summary-metadata=false"
        ast_node = SQLParser.parse_config_string_expression(demo_sql)
        self.assertEqual(ast_node.name, "spark.hadoop.parquet.enable.summary-metadata")
        self.assertEqual(ast_node.value, "false")