"""
metasequoia_sql_old.core.parser 的单元测试
"""

import unittest

from metasequoia_sql_old import *


class TestCoreParser(unittest.TestCase):
    """core.parser 的单元测试"""

    def test_compare_operator(self):
        """测试判断、解析比较运算符"""
        self.assertEqual(SQLParser.parse_compare_operator("= 3").source(SQLType.MYSQL), "=")
        self.assertEqual(SQLParser.parse_compare_operator("< 3").source(SQLType.MYSQL), "<")
        self.assertEqual(SQLParser.parse_compare_operator("<= 3").source(SQLType.MYSQL), "<=")
        self.assertEqual(SQLParser.parse_compare_operator("> 3").source(SQLType.MYSQL), ">")
        self.assertEqual(SQLParser.parse_compare_operator(">= 3").source(SQLType.MYSQL), ">=")
        self.assertEqual(SQLParser.parse_compare_operator("!= 3").source(SQLType.MYSQL), "!=")
        self.assertEqual(SQLParser.parse_compare_operator("<> 3").source(SQLType.MYSQL), "!=")

    def test_compute_operator(self):
        """测试判断、解析计算运算符"""
        self.assertEqual(SQLParser.parse_compute_operator("+ 3").source(SQLType.MYSQL), "+")
        self.assertEqual(SQLParser.parse_compute_operator("- 3").source(SQLType.MYSQL), "-")
        self.assertEqual(SQLParser.parse_compute_operator("* 3").source(SQLType.MYSQL), "*")
        self.assertEqual(SQLParser.parse_compute_operator("/ 3").source(SQLType.MYSQL), "/")
        self.assertEqual(SQLParser.parse_compute_operator("% 3").source(SQLType.SQL_SERVER), "%")

    def test_literal_expression(self):
        """测试判断、解析字面值表达式"""
        self.assertEqual(SQLParser.parse_literal_expression("1 WHERE").source(SQLType.MYSQL), "1")
        self.assertEqual(SQLParser.parse_literal_expression("2.5 WHERE").source(SQLType.MYSQL), "2.5")
        self.assertEqual(SQLParser.parse_literal_expression("'a' WHERE").source(SQLType.MYSQL), "'a'")
        self.assertEqual(SQLParser.parse_literal_expression("x'3f' WHERE").source(SQLType.MYSQL), "x'3f'")
        self.assertEqual(SQLParser.parse_literal_expression("TRUE WHERE").source(SQLType.MYSQL), "TRUE")
        self.assertEqual(SQLParser.parse_literal_expression("true WHERE").source(SQLType.MYSQL), "true")
        self.assertEqual(SQLParser.parse_literal_expression("False WHERE").source(SQLType.MYSQL), "False")
        self.assertEqual(SQLParser.parse_literal_expression("b'1' WHERE").source(SQLType.MYSQL), "b'1'")
        self.assertEqual(SQLParser.parse_literal_expression("null WHERE").source(SQLType.MYSQL), "null")
        self.assertEqual(SQLParser.parse_literal_expression("NULL WHERE").source(SQLType.MYSQL), "NULL")

    def test_column_name_expression(self):
        """测试判断、解析列名表达式"""
        self.assertEqual(SQLParser.parse_column_name_expression("schema.column AND").source(SQLType.MYSQL),
                         "`schema`.`column`")
        self.assertEqual(SQLParser.parse_column_name_expression("`s`.`c` AND").source(SQLType.MYSQL), "`s`.`c`")
        self.assertEqual(SQLParser.parse_column_name_expression("column_name WHERE").source(SQLType.MYSQL),
                         "`column_name`")

    def test_function_expression(self):
        """测试判断、解析函数表达式"""
        self.assertEqual(SQLParser.parse_function_expression("schema.function(param) AND").source(SQLType.MYSQL),
                         "`schema`.function(`param`)")
        self.assertEqual(SQLParser.parse_function_expression("`schema`.`function`(param) AND").source(SQLType.MYSQL),
                         "`schema`.function(`param`)")
        self.assertEqual(SQLParser.parse_function_expression("trim(`column_name`) AND").source(SQLType.MYSQL),
                         "trim(`column_name`)")
        self.assertEqual(SQLParser.parse_function_expression("rand() AND").source(SQLType.MYSQL),
                         "rand()")

    def test_window_expression(self):
        """测试判断、解析窗口表达式"""
        self.assertEqual(
            SQLParser.parse_window_expression(
                "ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) AS column3").source(
                SQLType.MYSQL),
            "ROW_NUMBER() OVER (PARTITION BY `column1` ORDER BY `column2`)")

    def test_wildcard_expression(self):
        """测试判断、解析通配符表达式"""
        self.assertEqual(SQLParser.parse_wildcard_expression("*").source(SQLType.MYSQL), "*")
        self.assertEqual(SQLParser.parse_wildcard_expression("t1.*").source(SQLType.MYSQL), "t1.*")

    def test_condition_expression(self):
        """测试解析条件表达式"""
        self.assertEqual(
            SQLParser.parse_logical_or_level_expression("column1 > 3 AND column2 > 2 WHERE").source(SQLType.MYSQL),
            "`column1` > 3 AND `column2` > 2")
        self.assertEqual(SQLParser.parse_logical_or_level_expression("column1 > 3 OR column2 > 2 WHERE").source(SQLType.MYSQL),
                         "`column1` > 3 OR `column2` > 2")
        self.assertEqual(
            SQLParser.parse_logical_or_level_expression("column1 > 3 OR column2 BETWEEN 2 AND 4 WHERE").source(SQLType.MYSQL),
            "`column1` > 3 OR `column2` BETWEEN 2 AND 4")

    def test_case_expression(self):
        """测试判断、解析 CASE 表达式"""
        self.assertEqual(
            SQLParser.parse_case_expression("CASE WHEN a > 2 THEN 3 ELSE 4 END").source(
                SQLType.MYSQL),
            "CASE WHEN `a` > 2 THEN 3 ELSE 4 END")

    def test_table_name_expression(self):
        """测试解析报名表达式"""
        self.assertEqual(SQLParser.parse_table_name_expression("schema1.table1 AS t1").source(SQLType.MYSQL),
                         "`schema1.table1`")

    def test_alias_expression(self):
        """测试判断、解析别名表达式"""
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
        self.assertEqual(SQLParser.parse_from_table("schema1.table1 AS t1").source(SQLType.MYSQL),
                         "`schema1.table1` AS t1")

    def test_column_expression(self):
        """测试解析列表达式"""
        self.assertEqual(SQLParser.parse_select_column("table1.column1 AS t1").source(SQLType.MYSQL),
                         "`table1`.`column1` AS t1")
        self.assertEqual(SQLParser.parse_select_column("3 + 5 AS t1").source(SQLType.MYSQL),
                         "3 + 5 AS t1")
        self.assertEqual(SQLParser.parse_select_column("TRIM(column1) AS t1").source(SQLType.MYSQL),
                         "TRIM(`column1`) AS t1")

    def test_select_clause(self):
        """测试判断、解析 SELECT 子句"""
        self.assertEqual(
            SQLParser.parse_select_clause("SELECT column1 AS c1, TRIM(column2) AS c2 FROM table1").source(
                SQLType.MYSQL),
            "SELECT `column1` AS c1, TRIM(`column2`) AS c2")
        self.assertEqual(SQLParser.parse_select_clause("SELECT column1 AS c1").source(SQLType.MYSQL),
                         "SELECT `column1` AS c1")

    def test_from_clause(self):
        """测试判断、解析 FROM 子句"""
        self.assertEqual(SQLParser.parse_from_clause("FROM schema1.table1 AS t1").source(SQLType.MYSQL),
                         "FROM `schema1.table1` AS t1")
        self.assertEqual(
            SQLParser.parse_from_clause("FROM schema1.table1 AS t1, schema2.table2 AS t2").source(SQLType.MYSQL),
            "FROM `schema1.table1` AS t1, `schema2.table2` AS t2")

    def test_join_clause(self):
        """测试判断、解析 JOIN 子句"""
        self.assertEqual(
            SQLParser.parse_join_clause("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1").source(SQLType.MYSQL),
            "LEFT JOIN `table2` AS t2 ON `t1`.`column1` = `t2`.`column1`")
        self.assertEqual(
            SQLParser.parse_join_clause("LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1").source(
                SQLType.MYSQL),
            "LEFT JOIN `schema2.table2` AS t2 ON `t1`.`column1` = `t2`.`column1`")

    def test_where_clause(self):
        """测试判断、解析 WHERE 子句"""
        self.assertEqual(SQLParser.parse_where_clause("WHERE column1 > 3 AND column2 > 2").source(SQLType.MYSQL),
                         "WHERE `column1` > 3 AND `column2` > 2")
        self.assertEqual(SQLParser.parse_where_clause("WHERE column1 > 3 OR column2 > 2").source(SQLType.MYSQL),
                         "WHERE `column1` > 3 OR `column2` > 2")
        self.assertEqual(
            SQLParser.parse_where_clause("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4").source(SQLType.MYSQL),
            "WHERE `column1` > 3 OR `column2` BETWEEN 2 AND 4")

    def test_having_clause(self):
        """测试判断、解析 HAVING 子句"""
        self.assertEqual(SQLParser.parse_having_clause("HAVING column1 > 3 AND column2 > 2").source(SQLType.MYSQL),
                         "HAVING `column1` > 3 AND `column2` > 2")
        self.assertEqual(SQLParser.parse_having_clause("HAVING column1 > 3 OR column2 > 2").source(SQLType.MYSQL),
                         "HAVING `column1` > 3 OR `column2` > 2")
        self.assertEqual(
            SQLParser.parse_having_clause("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4").source(SQLType.MYSQL),
            "HAVING `column1` > 3 OR `column2` BETWEEN 2 AND 4")

    def test_order_by_clause(self):
        """测试判断、解析 ORDER BY 子句"""
        self.assertEqual(SQLParser.parse_order_by_clause("ORDER BY column1, column2").source(SQLType.MYSQL),
                         "ORDER BY `column1`, `column2`")
        self.assertEqual(SQLParser.parse_order_by_clause("ORDER BY column1, column2 DESC").source(SQLType.MYSQL),
                         "ORDER BY `column1`, `column2` DESC")
        self.assertEqual(SQLParser.parse_order_by_clause("ORDER BY trim(column1) ASC, column2").source(SQLType.MYSQL),
                         "ORDER BY trim(`column1`), `column2`")

    def test_limit_clause(self):
        """测试判断、解析 LIMIT 子句"""
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

    def test_parse_element_level_node(self):
        """测试 parse_element_level_node 方法"""
        demo_sql = "1"
        ast_node = SQLParser.parse_element_level_expression(demo_sql)
        self.assertEqual(ast_node.source(), "1")

        demo_sql = "(1)"
        ast_node = SQLParser.parse_element_level_expression(demo_sql)
        self.assertEqual(ast_node.source(), "1")

        demo_sql = "((1))"
        ast_node = SQLParser.parse_element_level_expression(demo_sql)
        self.assertEqual(ast_node.source(), "1")

        demo_sql = "((column_name))"
        ast_node = SQLParser.parse_element_level_expression(demo_sql)
        self.assertEqual(ast_node.source(), "`column_name`")

    def test_parse_unary_level_node(self):
        """测试 parse_parse_unary_level_node 方法"""
        demo_sql = "~1"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.operator.source(), "~")
        self.assertEqual(ast_node.expression.source(), "1")

        demo_sql = "(~1)"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.operator.source(), "~")
        self.assertEqual(ast_node.expression.source(), "1")

        demo_sql = "((~1))"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.operator.source(), "~")
        self.assertEqual(ast_node.expression.source(), "1")

        demo_sql = "+1"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.operator.source(), "+")
        self.assertEqual(ast_node.expression.source(), "1")

        demo_sql = "-1"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.operator.source(), "-")
        self.assertEqual(ast_node.expression.source(), "1")

        demo_sql = "1"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.value, "1")
        self.assertEqual(ast_node.as_int(), 1)

        demo_sql = "~~1"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.operator.source(), "~")
        self.assertEqual(ast_node.expression.operator.source(), "~")
        self.assertEqual(ast_node.expression.expression.source(), "1")

        demo_sql = "!!1"
        ast_node = SQLParser.parse_unary_level_expression(demo_sql)
        self.assertEqual(ast_node.operator.source(), "!")
        self.assertEqual(ast_node.expression.operator.source(), "!")
        self.assertEqual(ast_node.expression.expression.source(), "1")

    def test_parse_xor_level_node(self):
        """测试 parse_parse_xor_level_node 方法"""
        demo_sql = "3 ^ 1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "^")
        self.assertEqual(ast_node.after_value.source(), "1")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "(3 ^ 1)"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "^")
        self.assertEqual(ast_node.after_value.source(), "1")
        self.assertEqual(ast_node.source(), "3 ^ 1")

        demo_sql = "3 ^ ~1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "^")
        self.assertIsInstance(ast_node.after_value, node.ASTUnaryExpression)
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.source(), "1")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "3 ^ 1 ^ 4"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertIsInstance(ast_node.before_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.operator.source(), "^")
        self.assertEqual(ast_node.before_value.after_value.source(), "1")
        self.assertEqual(ast_node.operator.source(), "^")
        self.assertEqual(ast_node.after_value.source(), "4")
        self.assertEqual(ast_node.source(), demo_sql)

    def test_parse_monomial_level_node(self):
        """测试 parse_monomial_level_node 方法"""
        demo_sql = "3 * ~1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "*")
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.source(), "1")

        demo_sql = "(3 * ~1)"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "*")
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.source(), "1")

        demo_sql = "3 / ~1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "/")
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.source(), "1")

        demo_sql = "3 DIV ~1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "/")
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.source(), "1")

        demo_sql = "3 % ~1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "%")
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.source(), "1")

        demo_sql = "3 MOD ~1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "%")
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.source(), "1")

        demo_sql = "3 % ~~1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "%")
        self.assertEqual(ast_node.after_value.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.operator.source(), "~")
        self.assertEqual(ast_node.after_value.expression.expression.source(), "1")

        demo_sql = "3 * ~1 / 4"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.operator.source(), "*")
        self.assertEqual(ast_node.before_value.after_value.operator.source(), "~")
        self.assertEqual(ast_node.before_value.after_value.expression.source(), "1")
        self.assertEqual(ast_node.operator.source(), "/")
        self.assertEqual(ast_node.after_value.source(), "4")

    def test_parse_polynomial_level_node(self):
        """测试 parse_polynomial_level_node 方法"""
        demo_sql = "3 + 4"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "+")
        self.assertEqual(ast_node.after_value.source(), "4")

        demo_sql = "(3 + 4)"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "+")
        self.assertEqual(ast_node.after_value.source(), "4")

        demo_sql = "3 + 4 * 5"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "+")
        self.assertEqual(ast_node.after_value.before_value.source(), "4")
        self.assertEqual(ast_node.after_value.operator.source(), "*")
        self.assertEqual(ast_node.after_value.after_value.source(), "5")

        demo_sql = "(3 + 4) * 5"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.operator.source(), "+")
        self.assertEqual(ast_node.before_value.after_value.source(), "4")
        self.assertEqual(ast_node.operator.source(), "*")
        self.assertEqual(ast_node.after_value.source(), "5")

        demo_sql = "3 + 4 - 5"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.operator.source(), "+")
        self.assertEqual(ast_node.before_value.after_value.source(), "4")
        self.assertEqual(ast_node.operator.source(), "-")
        self.assertEqual(ast_node.after_value.source(), "5")

    def test_parse_shift_level_node(self):
        """测试 parse_shift_level_node 方法"""
        demo_sql = "3 << 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "<<")
        self.assertEqual(ast_node.after_value.source(), "2")

        demo_sql = "(3 << 2)"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "<<")
        self.assertEqual(ast_node.after_value.source(), "2")

        demo_sql = "3 << 2 >> 1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertIsInstance(ast_node.before_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.operator.source(), "<<")
        self.assertEqual(ast_node.before_value.after_value.source(), "2")
        self.assertEqual(ast_node.operator.source(), ">>")
        self.assertEqual(ast_node.after_value.source(), "1")

    def test_parse_bitwise_and_level_node(self):
        """测试 parse_bitwise_and_level_node 方法"""
        demo_sql = "3 & 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.after_value.source(), "2")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "(3 & 2)"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.after_value.source(), "2")
        self.assertEqual(ast_node.source(), "3 & 2")

        demo_sql = "3 & 2 & 1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertIsInstance(ast_node.before_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.after_value.source(), "2")
        self.assertEqual(ast_node.after_value.source(), "1")
        self.assertEqual(ast_node.source(), demo_sql)

    def test_parse_bitwise_or_level_node(self):
        """测试 parse_bitwise_or_level_node 方法"""
        demo_sql = "3 | 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertIsInstance(ast_node, node.ASTComputeExpression)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.after_value.source(), "2")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "(3 | 2)"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertIsInstance(ast_node, node.ASTComputeExpression)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.after_value.source(), "2")
        self.assertEqual(ast_node.source(), "3 | 2")

        demo_sql = "3 | 2 | 1"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertIsInstance(ast_node.before_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.after_value.source(), "2")
        self.assertEqual(ast_node.after_value.source(), "1")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "3 + 1 * 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "+")
        self.assertIsInstance(ast_node.after_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.after_value.before_value.source(), "1")
        self.assertEqual(ast_node.after_value.operator.source(), "*")
        self.assertEqual(ast_node.after_value.after_value.source(), "2")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "3 - 1 * 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "-")
        self.assertIsInstance(ast_node.after_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.after_value.before_value.source(), "1")
        self.assertEqual(ast_node.after_value.operator.source(), "*")
        self.assertEqual(ast_node.after_value.after_value.source(), "2")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "3 & 1 * 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertIsInstance(ast_node.after_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.after_value.before_value.source(), "1")
        self.assertEqual(ast_node.after_value.operator.source(), "*")
        self.assertEqual(ast_node.after_value.after_value.source(), "2")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "3 | 1 * 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "3")
        self.assertIsInstance(ast_node.after_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.after_value.before_value.source(), "1")
        self.assertEqual(ast_node.after_value.operator.source(), "*")
        self.assertEqual(ast_node.after_value.after_value.source(), "2")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "3 ^ 1 * 2"
        ast_node = SQLParser.parse_compute_expression(demo_sql)
        self.assertIsInstance(ast_node.before_value, node.ASTComputeExpression)
        self.assertEqual(ast_node.before_value.before_value.source(), "3")
        self.assertEqual(ast_node.before_value.after_value.source(), "1")
        self.assertEqual(ast_node.operator.source(), "*")
        self.assertEqual(ast_node.after_value.source(), "2")
        self.assertEqual(ast_node.source(), demo_sql)

    def test_parse_keyword_condition_level_node(self):
        """测试 parse_keyword_condition_level_node 方法"""

        demo_sql = "EXISTS (SELECT 1)"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.value.source(), "(SELECT 1)")

        demo_sql = "(EXISTS (SELECT 1))"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.value.source(), "(SELECT 1)")

        demo_sql = "a BETWEEN 2 AND 3"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "`a`")
        self.assertFalse(ast_node.is_not)
        self.assertEqual(ast_node.from_value.source(), "2")
        self.assertEqual(ast_node.to_value.source(), "3")

        demo_sql = "a NOT BETWEEN 2 AND 3"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "`a`")
        self.assertTrue(ast_node.is_not)
        self.assertEqual(ast_node.from_value.source(), "2")
        self.assertEqual(ast_node.to_value.source(), "3")

        demo_sql = "2 IS TRUE"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "2")
        self.assertFalse(ast_node.is_not)
        self.assertEqual(ast_node.after_value.source(), "TRUE")

        demo_sql = "2 IN ('0')"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "2")
        self.assertFalse(ast_node.is_not)
        self.assertEqual(ast_node.after_value.source(), "('0')")

        demo_sql = "2 LIKE 'a%'"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "2")
        self.assertFalse(ast_node.is_not)
        self.assertEqual(ast_node.after_value.source(), "'a%'")

        demo_sql = "2 RLIKE 'a%'"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "2")
        self.assertFalse(ast_node.is_not)
        self.assertEqual(ast_node.after_value.source(), "'a%'")

        demo_sql = "2 REGEXP 'a%'"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "2")
        self.assertFalse(ast_node.is_not)
        self.assertEqual(ast_node.after_value.source(), "'a%'")

        demo_sql = "2 IS TRUE IN ('0')"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "2")
        self.assertFalse(ast_node.before_value.is_not)
        self.assertEqual(ast_node.before_value.after_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "('0')")

        demo_sql = "2 IS NOT TRUE NOT IN ('0')"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "2")
        self.assertTrue(ast_node.before_value.is_not)
        self.assertEqual(ast_node.before_value.after_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "('0')")

    def test_parse_operator_condition_level(self):
        """测试 parse_operator_condition_leve 方法"""

        demo_sql = "2 IS NOT TRUE NOT IN ('0')"
        ast_node = SQLParser.parse_keyword_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "2")
        self.assertTrue(ast_node.before_value.is_not)
        self.assertEqual(ast_node.before_value.after_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "('0')")

        demo_sql = "column1 > 3"
        ast_node = SQLParser.parse_operator_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "`column1`")
        self.assertEqual(ast_node.operator.source(), ">")
        self.assertEqual(ast_node.after_value.source(), "3")

        demo_sql = "(column1 > 3)"
        ast_node = SQLParser.parse_operator_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "`column1`")
        self.assertEqual(ast_node.operator.source(), ">")
        self.assertEqual(ast_node.after_value.source(), "3")

        demo_sql = "column1 > 3 < 1"
        ast_node = SQLParser.parse_operator_condition_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "`column1`")
        self.assertEqual(ast_node.before_value.operator.source(), ">")
        self.assertEqual(ast_node.before_value.after_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "<")
        self.assertEqual(ast_node.after_value.source(), "1")

    def test_parse_logical_not_level(self):
        """测试 parse_logical_not_level 方法"""

        demo_sql = "column1 > 3 < 1"
        ast_node = SQLParser.parse_logical_not_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.before_value.source(), "`column1`")
        self.assertEqual(ast_node.before_value.operator.source(), ">")
        self.assertEqual(ast_node.before_value.after_value.source(), "3")
        self.assertEqual(ast_node.operator.source(), "<")
        self.assertEqual(ast_node.after_value.source(), "1")

        demo_sql = "NOT column1 > 3 < 1"
        ast_node = SQLParser.parse_logical_not_level_expression(demo_sql)
        self.assertEqual(ast_node.expression.before_value.before_value.source(), "`column1`")
        self.assertEqual(ast_node.expression.before_value.operator.source(), ">")
        self.assertEqual(ast_node.expression.before_value.after_value.source(), "3")
        self.assertEqual(ast_node.expression.operator.source(), "<")
        self.assertEqual(ast_node.expression.after_value.source(), "1")
        self.assertEqual(ast_node.source(), "NOT `column1` > 3 < 1")

        demo_sql = "(NOT column1 > 3 < 1)"
        ast_node = SQLParser.parse_logical_not_level_expression(demo_sql)
        self.assertEqual(ast_node.expression.before_value.before_value.source(), "`column1`")
        self.assertEqual(ast_node.expression.before_value.operator.source(), ">")
        self.assertEqual(ast_node.expression.before_value.after_value.source(), "3")
        self.assertEqual(ast_node.expression.operator.source(), "<")
        self.assertEqual(ast_node.expression.after_value.source(), "1")
        self.assertEqual(ast_node.source(), "NOT `column1` > 3 < 1")

    def test_parse_logical_and_level(self):
        """测试 parse_logical_and_level 方法"""

        demo_sql = "NOT column1 > 3 < 1"
        ast_node = SQLParser.parse_logical_and_level_expression(demo_sql)
        self.assertEqual(ast_node.expression.before_value.before_value.source(), "`column1`")
        self.assertEqual(ast_node.expression.before_value.operator.source(), ">")
        self.assertEqual(ast_node.expression.before_value.after_value.source(), "3")
        self.assertEqual(ast_node.expression.operator.source(), "<")
        self.assertEqual(ast_node.expression.after_value.source(), "1")
        self.assertEqual(ast_node.source(), "NOT `column1` > 3 < 1")

        demo_sql = "TRUE AND FALSE"
        ast_node = SQLParser.parse_logical_and_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "FALSE")
        self.assertEqual(ast_node.source(), demo_sql)

        demo_sql = "(TRUE AND FALSE)"
        ast_node = SQLParser.parse_logical_and_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "FALSE")
        self.assertEqual(ast_node.source(), "TRUE AND FALSE")

    def test_parse_logical_xor_level(self):
        """测试 parse_logical_xor_level 方法"""

        demo_sql = "NOT column1 > 3 < 1"
        ast_node = SQLParser.parse_logical_xor_level_expression(demo_sql)
        self.assertEqual(ast_node.expression.before_value.before_value.source(), "`column1`")
        self.assertEqual(ast_node.expression.before_value.operator.source(), ">")
        self.assertEqual(ast_node.expression.before_value.after_value.source(), "3")
        self.assertEqual(ast_node.expression.operator.source(), "<")
        self.assertEqual(ast_node.expression.after_value.source(), "1")

        demo_sql = "TRUE XOR FALSE"
        ast_node = SQLParser.parse_logical_xor_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "FALSE")
        self.assertEqual(ast_node.source(), "TRUE XOR FALSE")

        demo_sql = "(TRUE XOR FALSE)"
        ast_node = SQLParser.parse_logical_xor_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "FALSE")
        self.assertEqual(ast_node.source(), "TRUE XOR FALSE")

    def test_parse_logical_or_level(self):
        """测试 parse_logical_or_level 方法"""

        demo_sql = "NOT column1 > 3 < 1"
        ast_node = SQLParser.parse_logical_or_level_expression(demo_sql)
        self.assertEqual(ast_node.expression.before_value.before_value.source(), "`column1`")
        self.assertEqual(ast_node.expression.before_value.operator.source(), ">")
        self.assertEqual(ast_node.expression.before_value.after_value.source(), "3")
        self.assertEqual(ast_node.expression.operator.source(), "<")
        self.assertEqual(ast_node.expression.after_value.source(), "1")

        demo_sql = "TRUE OR FALSE"
        ast_node = SQLParser.parse_logical_or_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "FALSE")
        self.assertEqual(ast_node.source(), "TRUE OR FALSE")

        demo_sql = "(TRUE OR FALSE)"
        ast_node = SQLParser.parse_logical_or_level_expression(demo_sql)
        self.assertEqual(ast_node.before_value.source(), "TRUE")
        self.assertEqual(ast_node.after_value.source(), "FALSE")
        self.assertEqual(ast_node.source(), "TRUE OR FALSE")

    def test_group_by_clause(self):
        """测试判断、解析 GROUP BY 子句"""
        demo_sql = "GROUP BY column1, column2"
        ast_node = SQLParser.parse_group_by_clause(demo_sql)
        self.assertEqual(ast_node.columns[0].source(), "`column1`")
        self.assertEqual(ast_node.columns[1].source(), "`column2`")

        demo_sql = ("GROUP BY column1, column2 "
                    "GROUPING SETS (column1, column2, (column1, column2))")
        ast_node = SQLParser.parse_group_by_clause(demo_sql)
        self.assertEqual(ast_node.columns[0].source(), "`column1`")
        self.assertEqual(ast_node.columns[1].source(), "`column2`")
        self.assertEqual(ast_node.grouping_sets.grouping_list[0][0].source(), "`column1`")
        self.assertEqual(ast_node.grouping_sets.grouping_list[1][0].source(), "`column2`")
        self.assertEqual(ast_node.grouping_sets.grouping_list[2][0].source(), "`column1`")
        self.assertEqual(ast_node.grouping_sets.grouping_list[2][1].source(), "`column2`")

        demo_sql = ("GROUP BY column1, column2 "
                    "GROUPING SETS (column1, column2, (column1, column2))"
                    "WITH CUBE")
        ast_node = SQLParser.parse_group_by_clause(demo_sql)
        self.assertTrue(ast_node.with_cube)

        demo_sql = ("GROUP BY column1, column2 "
                    "GROUPING SETS (column1, column2, (column1, column2))"
                    "WITH ROLLUP")
        ast_node = SQLParser.parse_group_by_clause(demo_sql)
        self.assertTrue(ast_node.with_rollup)

    def test_parse_join_on_expression(self):
        """测试 test_parse_join_on_expression 方法"""
