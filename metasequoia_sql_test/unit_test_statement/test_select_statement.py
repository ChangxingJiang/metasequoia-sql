"""
SELECT 语句单元测试

测试语义组：select_statement 及其相关语义组
"""

import unittest

from metasequoia_sql import parse_statement
from metasequoia_sql.ast.basic.ident import Identifier
from metasequoia_sql.ast.expression.general_expression import ExpressionWithAlias, Row, TableWild, Wild
from metasequoia_sql.ast.statement.select_statement import (ExplicitTable, QueryExcept, QueryExpression, QueryIntersect,
                                                            QueryUnion, SelectOption, SelectStatement, SimpleQuery,
                                                            TableValueConstructor, UnionOption)


class TestSelectStatement(unittest.TestCase):
    """测试 SELECT 语句解析"""

    def test_basic_select_star(self):
        """测试基本的 SELECT * 语句"""
        sql = "SELECT *"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_expr = node.query_expression
        self.assertIsInstance(query_expr, QueryExpression)
        self.assertIsInstance(query_expr.query_body, SimpleQuery)

        simple_query = query_expr.query_body
        self.assertEqual(simple_query.select_option, SelectOption.DEFAULT)
        self.assertEqual(len(simple_query.select_item_list), 1)
        self.assertIsInstance(simple_query.select_item_list[0], Wild)

    def test_select_with_columns(self):
        """测试 SELECT 指定列的语句"""
        sql = "SELECT column_name_1, column_name_2"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertEqual(len(simple_query.select_item_list), 2)
        self.assertIsInstance(simple_query.select_item_list[0], ExpressionWithAlias)
        self.assertIsInstance(simple_query.select_item_list[1], ExpressionWithAlias)

    def test_select_with_alias(self):
        """测试 SELECT 带别名的语句"""
        sql = "SELECT column_name_1 AS alias_1, column_name_2 alias_2"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertEqual(len(simple_query.select_item_list), 2)
        item1 = simple_query.select_item_list[0]
        item2 = simple_query.select_item_list[1]
        self.assertIsInstance(item1, ExpressionWithAlias)
        self.assertIsInstance(item2, ExpressionWithAlias)
        self.assertEqual(item1.alias, "alias_1")
        self.assertEqual(item2.alias, "alias_2")

    def test_select_table_wild(self):
        """测试 SELECT 表通配符的语句"""
        sql = "SELECT table_name.*"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertEqual(len(simple_query.select_item_list), 1)
        self.assertIsInstance(simple_query.select_item_list[0], TableWild)
        table_wild = simple_query.select_item_list[0]
        self.assertIsNone(table_wild.schema_name)
        self.assertEqual(table_wild.table_name, "table_name")

    def test_select_schema_table_wild(self):
        """测试 SELECT 模式表通配符的语句"""
        sql = "SELECT database_name.table_name.*"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertEqual(len(simple_query.select_item_list), 1)
        self.assertIsInstance(simple_query.select_item_list[0], TableWild)
        table_wild = simple_query.select_item_list[0]
        self.assertEqual(table_wild.schema_name, "database_name")
        self.assertEqual(table_wild.table_name, "table_name")

    def test_select_with_from_clause(self):
        """测试 SELECT 带 FROM 子句的语句"""
        sql = "SELECT * FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertIsNotNone(simple_query.from_clause)
        self.assertIsInstance(simple_query.from_clause, list)
        self.assertEqual(len(simple_query.from_clause), 1)

    def test_select_with_where_clause(self):
        """测试 SELECT 带 WHERE 子句的语句"""
        sql = "SELECT * FROM table_name WHERE column_name = 1"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertIsNotNone(simple_query.where_clause)

    def test_select_with_group_by_clause(self):
        """测试 SELECT 带 GROUP BY 子句的语句"""
        sql = "SELECT column_name_1, COUNT(*) FROM table_name GROUP BY column_name_1"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertIsNotNone(simple_query.group_by_clause)

    def test_select_with_having_clause(self):
        """测试 SELECT 带 HAVING 子句的语句"""
        sql = "SELECT column_name_1, COUNT(*) FROM table_name GROUP BY column_name_1 HAVING COUNT(*) > 1"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertIsNotNone(simple_query.having_clause)

    def test_select_with_order_by_clause(self):
        """测试 SELECT 带 ORDER BY 子句的语句"""
        sql = "SELECT * FROM table_name ORDER BY column_name_1"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_expr = node.query_expression
        self.assertIsInstance(query_expr, QueryExpression)
        self.assertIsNotNone(query_expr.order_clause)

    def test_select_with_limit_clause(self):
        """测试 SELECT 带 LIMIT 子句的语句"""
        sql = "SELECT * FROM table_name LIMIT 10"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_expr = node.query_expression
        self.assertIsInstance(query_expr, QueryExpression)
        self.assertIsNotNone(query_expr.limit_clause)

    def test_select_with_limit_offset_clause(self):
        """测试 SELECT 带 LIMIT OFFSET 子句的语句"""
        sql = "SELECT * FROM table_name LIMIT 10 OFFSET 5"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_expr = node.query_expression
        self.assertIsInstance(query_expr, QueryExpression)
        self.assertIsNotNone(query_expr.limit_clause)

    def test_select_option_distinct(self):
        """测试 SELECT DISTINCT 选项"""
        sql = "SELECT DISTINCT column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.DISTINCT)

    def test_select_option_all(self):
        """测试 SELECT ALL 选项"""
        sql = "SELECT ALL column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.ALL)

    def test_select_option_high_priority(self):
        """测试 SELECT HIGH_PRIORITY 选项"""
        sql = "SELECT HIGH_PRIORITY column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.HIGH_PRIORITY)

    def test_select_option_straight_join(self):
        """测试 SELECT STRAIGHT_JOIN 选项"""
        sql = "SELECT STRAIGHT_JOIN column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.STRAIGHT_JOIN)

    def test_select_option_sql_small_result(self):
        """测试 SELECT SQL_SMALL_RESULT 选项"""
        sql = "SELECT SQL_SMALL_RESULT column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.SQL_SMALL_RESULT)

    def test_select_option_sql_big_result(self):
        """测试 SELECT SQL_BIG_RESULT 选项"""
        sql = "SELECT SQL_BIG_RESULT column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.SQL_BIG_RESULT)

    def test_select_option_sql_buffer_result(self):
        """测试 SELECT SQL_BUFFER_RESULT 选项"""
        sql = "SELECT SQL_BUFFER_RESULT column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.SQL_BUFFER_RESULT)

    def test_select_option_sql_calc_found_rows(self):
        """测试 SELECT SQL_CALC_FOUND_ROWS 选项"""
        sql = "SELECT SQL_CALC_FOUND_ROWS column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.SQL_CALC_FOUND_ROWS)

    def test_select_option_sql_no_cache(self):
        """测试 SELECT SQL_NO_CACHE 选项"""
        sql = "SELECT SQL_NO_CACHE column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertEqual(simple_query.select_option & SelectOption.SQL_NO_CACHE, SelectOption.SQL_NO_CACHE)

    def test_select_multiple_options(self):
        """测试 SELECT 多个选项组合"""
        sql = "SELECT DISTINCT HIGH_PRIORITY column_name FROM table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertTrue(simple_query.select_option & SelectOption.DISTINCT)
        self.assertTrue(simple_query.select_option & SelectOption.HIGH_PRIORITY)

    def test_table_value_constructor(self):
        """测试 VALUES 表值构造器"""
        sql = "VALUES ROW(1, 'test'), ROW(2, 'test2')"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, TableValueConstructor)

        self.assertEqual(len(query_body.row_list), 2)
        self.assertIsInstance(query_body.row_list[0], Row)
        self.assertIsInstance(query_body.row_list[1], Row)

    def test_explicit_table(self):
        """测试 TABLE 显式表语句"""
        sql = "TABLE table_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, ExplicitTable)

        self.assertIsInstance(query_body.table_ident, Identifier)

    def test_union_default(self):
        """测试 UNION 默认选项"""
        sql = "SELECT column_name_1 FROM table_name_1 UNION SELECT column_name_2 FROM table_name_2"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, QueryUnion)

        self.assertEqual(query_body.union_option, UnionOption.DEFAULT)
        self.assertIsInstance(query_body.left_operand, SimpleQuery)
        self.assertIsInstance(query_body.right_operand, SimpleQuery)

    def test_union_distinct(self):
        """测试 UNION DISTINCT"""
        sql = "SELECT column_name_1 FROM table_name_1 UNION DISTINCT SELECT column_name_2 FROM table_name_2"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, QueryUnion)

        self.assertEqual(query_body.union_option, UnionOption.DISTINCT)

    def test_union_all(self):
        """测试 UNION ALL"""
        sql = "SELECT column_name_1 FROM table_name_1 UNION ALL SELECT column_name_2 FROM table_name_2"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, QueryUnion)

        self.assertEqual(query_body.union_option, UnionOption.ALL)

    def test_except_query(self):
        """测试 EXCEPT 查询"""
        sql = "SELECT column_name_1 FROM table_name_1 EXCEPT SELECT column_name_2 FROM table_name_2"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, QueryExcept)

        self.assertEqual(query_body.union_option, UnionOption.DEFAULT)

    def test_intersect_query(self):
        """测试 INTERSECT 查询"""
        sql = "SELECT column_name_1 FROM table_name_1 INTERSECT SELECT column_name_2 FROM table_name_2"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, QueryIntersect)

        self.assertEqual(query_body.union_option, UnionOption.DEFAULT)

    def test_nested_union(self):
        """测试嵌套 UNION 查询"""
        sql = """
        SELECT column_name_1 FROM table_name_1 
        UNION 
        SELECT column_name_2 FROM table_name_2 
        UNION 
        SELECT column_name_3 FROM table_name_3
        """
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_body = node.query_expression.query_body
        self.assertIsInstance(query_body, QueryUnion)

    def test_parenthesized_query(self):
        """测试带括号的查询"""
        sql = "(SELECT column_name FROM table_name)"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        self.assertIsInstance(node.query_expression, QueryExpression)

    def test_complex_select_with_all_clauses(self):
        """测试包含所有子句的复杂 SELECT 语句"""
        sql = """
        SELECT DISTINCT column_name_1, column_name_2 
        FROM table_name_1 t1 
        JOIN table_name_2 t2 ON t1.id = t2.id 
        WHERE t1.column_name_1 > 0 
        GROUP BY column_name_1 
        HAVING COUNT(*) > 1 
        ORDER BY column_name_1 DESC 
        LIMIT 10 OFFSET 5
        """
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_expr = node.query_expression
        self.assertIsInstance(query_expr, QueryExpression)

        simple_query = query_expr.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        # 验证各个子句都存在
        self.assertTrue(simple_query.select_option & SelectOption.DISTINCT)
        self.assertIsNotNone(simple_query.from_clause)
        self.assertIsNotNone(simple_query.where_clause)
        self.assertIsNotNone(simple_query.group_by_clause)
        self.assertIsNotNone(simple_query.having_clause)
        self.assertIsNotNone(query_expr.order_clause)
        self.assertIsNotNone(query_expr.limit_clause)

    def test_select_with_subquery(self):
        """测试包含子查询的 SELECT 语句"""
        sql = "SELECT column_name_1 FROM table_name_1 WHERE column_name_2 IN (SELECT column_name_3 FROM table_name_2)"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        self.assertIsNotNone(simple_query.where_clause)

    def test_select_with_with_clause(self):
        """测试带 WITH 子句的 SELECT 语句"""
        sql = """
        WITH cte AS (SELECT column_name_1 FROM table_name_1) 
        SELECT * FROM cte
        """
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        query_expr = node.query_expression
        self.assertIsInstance(query_expr, QueryExpression)
        self.assertIsNotNone(query_expr.with_clause)

    def test_select_mixed_items(self):
        """测试混合选择项（列、表达式、通配符）"""
        sql = "SELECT *, column_name_1, table_name.*, column_name_2 + 1 AS calculated"
        node = parse_statement(sql)

        self.assertIsInstance(node, SelectStatement)
        simple_query = node.query_expression.query_body
        self.assertIsInstance(simple_query, SimpleQuery)

        # 验证包含不同类型的选择项
        self.assertEqual(len(simple_query.select_item_list), 4)
        self.assertIsInstance(simple_query.select_item_list[0], Wild)
        self.assertIsInstance(simple_query.select_item_list[1], ExpressionWithAlias)
        self.assertIsInstance(simple_query.select_item_list[2], TableWild)
        self.assertIsInstance(simple_query.select_item_list[3], ExpressionWithAlias)
