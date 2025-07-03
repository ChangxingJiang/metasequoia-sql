"""
函数表达式（function_expression）单元测试

测试 function_expression.py 中的语义组：
- FUNCTION_EXPRESSION: 函数表达式
- DATE_TIME_TYPE: 日期时间类型
- NOW_EXPRESSION: NOW 表达式
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_expression


class TestFunctionExpression(TestCase):
    """测试 function_expression 语义组
    
    测试各种函数表达式的解析，包括关键字函数、非关键字函数、冲突风险函数和常规函数
    """

    def test_char_function_without_charset(self):
        """测试 CHAR 函数（无字符集）"""
        node = parse_expression("CHAR(65, 66, 67)")
        self.assertIsInstance(node, ast.FunctionChar)
        self.assertEqual(len(node.param_list), 3)
        self.assertIsNone(node.charset_name)

    def test_char_function_with_charset(self):
        """测试 CHAR 函数（带字符集）"""
        node = parse_expression("CHAR(65, 66, 67 USING utf8)")
        self.assertIsInstance(node, ast.FunctionChar)
        self.assertEqual(len(node.param_list), 3)
        self.assertIsNotNone(node.charset_name)

    def test_current_user_function(self):
        """测试 CURRENT_USER 函数"""
        node = parse_expression("CURRENT_USER()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "current_user")
        self.assertEqual(len(node.param_list), 0)

    def test_date_function(self):
        """测试 DATE 函数"""
        node = parse_expression("DATE('2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "date")
        self.assertEqual(len(node.param_list), 1)

    def test_day_function(self):
        """测试 DAY 函数"""
        node = parse_expression("DAY('2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "day")
        self.assertEqual(len(node.param_list), 1)

    def test_hour_function(self):
        """测试 HOUR 函数"""
        node = parse_expression("HOUR('12:30:45')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "hour")
        self.assertEqual(len(node.param_list), 1)

    def test_insert_function(self):
        """测试 INSERT 函数"""
        node = parse_expression("INSERT('Hello', 2, 3, 'World')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "insert")
        self.assertEqual(len(node.param_list), 4)

    def test_interval_function_basic(self):
        """测试 INTERVAL 函数（基础形式）"""
        node = parse_expression("INTERVAL(1, 2)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "interval")
        self.assertEqual(len(node.param_list), 2)

    def test_interval_function_with_list(self):
        """测试 INTERVAL 函数（带列表）"""
        node = parse_expression("INTERVAL(1, 2, 3, 4)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "interval")
        self.assertEqual(len(node.param_list), 4)

    def test_json_value_function(self):
        """测试 JSON_VALUE 函数"""
        node = parse_expression("JSON_VALUE(column_name, '$.path')")
        self.assertIsInstance(node, ast.FunctionJsonValue)
        self.assertEqual(len(node.param_list), 2)

    def test_left_function(self):
        """测试 LEFT 函数"""
        node = parse_expression("LEFT('Hello', 2)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "left")
        self.assertEqual(len(node.param_list), 2)

    def test_minute_function(self):
        """测试 MINUTE 函数"""
        node = parse_expression("MINUTE('12:30:45')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "minute")
        self.assertEqual(len(node.param_list), 1)

    def test_month_function(self):
        """测试 MONTH 函数"""
        node = parse_expression("MONTH('2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "month")
        self.assertEqual(len(node.param_list), 1)

    def test_right_function(self):
        """测试 RIGHT 函数"""
        node = parse_expression("RIGHT('Hello', 2)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "right")
        self.assertEqual(len(node.param_list), 2)

    def test_second_function(self):
        """测试 SECOND 函数"""
        node = parse_expression("SECOND('12:30:45')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "second")
        self.assertEqual(len(node.param_list), 1)

    def test_time_function(self):
        """测试 TIME 函数"""
        node = parse_expression("TIME('12:30:45')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "time")
        self.assertEqual(len(node.param_list), 1)

    def test_timestamp_function_single_param(self):
        """测试 TIMESTAMP 函数（单参数）"""
        node = parse_expression("TIMESTAMP('2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "timestamp")
        self.assertEqual(len(node.param_list), 1)

    def test_timestamp_function_two_params(self):
        """测试 TIMESTAMP 函数（两参数）"""
        node = parse_expression("TIMESTAMP('2023-01-01', '12:30:45')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "timestamp")
        self.assertEqual(len(node.param_list), 2)

    def test_trim_function_default(self):
        """测试 TRIM 函数（默认形式）"""
        node = parse_expression("TRIM('  Hello  ')")
        self.assertIsInstance(node, ast.FunctionTrim)
        self.assertIsNone(node.chars_to_remove)

    def test_trim_function_with_chars(self):
        """测试 TRIM 函数（指定字符）"""
        node = parse_expression("TRIM('x' FROM 'xxxHelloxxx')")
        self.assertIsInstance(node, ast.FunctionTrim)
        self.assertIsNotNone(node.chars_to_remove)

    def test_trim_function_leading(self):
        """测试 TRIM 函数（LEADING）"""
        node = parse_expression("TRIM(LEADING FROM '  Hello  ')")
        self.assertIsInstance(node, ast.FunctionTrim)

    def test_trim_function_leading_with_chars(self):
        """测试 TRIM 函数（LEADING 带字符）"""
        node = parse_expression("TRIM(LEADING 'x' FROM 'xxxHelloxxx')")
        self.assertIsInstance(node, ast.FunctionTrim)

    def test_trim_function_trailing(self):
        """测试 TRIM 函数（TRAILING）"""
        node = parse_expression("TRIM(TRAILING FROM '  Hello  ')")
        self.assertIsInstance(node, ast.FunctionTrim)

    def test_trim_function_trailing_with_chars(self):
        """测试 TRIM 函数（TRAILING 带字符）"""
        node = parse_expression("TRIM(TRAILING 'x' FROM 'xxxHelloxxx')")
        self.assertIsInstance(node, ast.FunctionTrim)

    def test_trim_function_both(self):
        """测试 TRIM 函数（BOTH）"""
        node = parse_expression("TRIM(BOTH FROM '  Hello  ')")
        self.assertIsInstance(node, ast.FunctionTrim)

    def test_trim_function_both_with_chars(self):
        """测试 TRIM 函数（BOTH 带字符）"""
        node = parse_expression("TRIM(BOTH 'x' FROM 'xxxHelloxxx')")
        self.assertIsInstance(node, ast.FunctionTrim)

    def test_user_function(self):
        """测试 USER 函数"""
        node = parse_expression("USER()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "user")
        self.assertEqual(len(node.param_list), 0)

    def test_year_function(self):
        """测试 YEAR 函数"""
        node = parse_expression("YEAR('2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "year")
        self.assertEqual(len(node.param_list), 1)

    def test_adddate_function_basic(self):
        """测试 ADDDATE 函数（基础形式）"""
        node = parse_expression("ADDDATE('2023-01-01', 30)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "adddate")
        self.assertEqual(len(node.param_list), 2)

    def test_adddate_function_with_interval(self):
        """测试 ADDDATE 函数（带时间间隔）"""
        node = parse_expression("ADDDATE('2023-01-01', INTERVAL 1 MONTH)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "adddate")
        self.assertEqual(len(node.param_list), 2)

    def test_current_date_function(self):
        """测试 CURRENT_DATE 函数"""
        node = parse_expression("CURRENT_DATE()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "current_date")
        self.assertEqual(len(node.param_list), 0)

    def test_curtime_function(self):
        """测试 CURTIME 函数"""
        node = parse_expression("CURTIME()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "curtime")

    def test_curtime_function_with_precision(self):
        """测试 CURTIME 函数（带精度）"""
        node = parse_expression("CURTIME(3)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "curtime")
        self.assertEqual(len(node.param_list), 1)

    def test_extract_function(self):
        """测试 EXTRACT 函数"""
        node = parse_expression("EXTRACT(YEAR FROM '2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExtract)

    def test_get_format_function(self):
        """测试 GET_FORMAT 函数"""
        node = parse_expression("GET_FORMAT(DATE, 'EUR')")
        self.assertIsInstance(node, ast.FunctionGetFormat)

    def test_log_function_single_param(self):
        """测试 LOG 函数（单参数）"""
        node = parse_expression("LOG(10)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "log")
        self.assertEqual(len(node.param_list), 1)

    def test_log_function_two_params(self):
        """测试 LOG 函数（两参数）"""
        node = parse_expression("LOG(2, 8)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "log")
        self.assertEqual(len(node.param_list), 2)

    def test_position_function(self):
        """测试 POSITION 函数"""
        node = parse_expression("POSITION('llo' IN 'Hello')")
        self.assertIsInstance(node, ast.FunctionPosition)

    def test_subdate_function_basic(self):
        """测试 SUBDATE 函数（基础形式）"""
        node = parse_expression("SUBDATE('2023-01-01', 30)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "subdate")
        self.assertEqual(len(node.param_list), 2)

    def test_subdate_function_with_interval(self):
        """测试 SUBDATE 函数（带时间间隔）"""
        node = parse_expression("SUBDATE('2023-01-01', INTERVAL 1 MONTH)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "subdate")
        self.assertEqual(len(node.param_list), 2)

    def test_substring_function_with_length(self):
        """测试 SUBSTRING 函数（带长度）"""
        node = parse_expression("SUBSTRING('Hello', 2, 3)")
        self.assertIsInstance(node, ast.FunctionSubstring)
        self.assertIsNotNone(node.length)

    def test_substring_function_without_length(self):
        """测试 SUBSTRING 函数（不带长度）"""
        node = parse_expression("SUBSTRING('Hello', 2)")
        self.assertIsInstance(node, ast.FunctionSubstring)
        self.assertIsNone(node.length)

    def test_substring_function_from_for(self):
        """测试 SUBSTRING 函数（FROM FOR 语法）"""
        node = parse_expression("SUBSTRING('Hello' FROM 2 FOR 3)")
        self.assertIsInstance(node, ast.FunctionSubstring)
        self.assertIsNotNone(node.length)

    def test_substring_function_from_only(self):
        """测试 SUBSTRING 函数（仅 FROM 语法）"""
        node = parse_expression("SUBSTRING('Hello' FROM 2)")
        self.assertIsInstance(node, ast.FunctionSubstring)
        self.assertIsNone(node.length)

    def test_sysdate_function(self):
        """测试 SYSDATE 函数"""
        node = parse_expression("SYSDATE()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "sysdate")

    def test_timestamp_add_function(self):
        """测试 TIMESTAMP_ADD 函数"""
        node = parse_expression("TIMESTAMP_ADD(DAY, 1, '2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "timestamp_add")
        self.assertEqual(len(node.param_list), 3)

    def test_timestamp_diff_function(self):
        """测试 TIMESTAMP_DIFF 函数"""
        node = parse_expression("TIMESTAMP_DIFF(DAY, '2023-01-01', '2023-01-02')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "timestamp_diff")
        self.assertEqual(len(node.param_list), 3)

    def test_utc_date_function(self):
        """测试 UTC_DATE 函数"""
        node = parse_expression("UTC_DATE()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "utc_date")
        self.assertEqual(len(node.param_list), 0)

    def test_utc_time_function(self):
        """测试 UTC_TIME 函数"""
        node = parse_expression("UTC_TIME()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "utc_time")

    def test_utc_timestamp_function(self):
        """测试 UTC_TIMESTAMP 函数"""
        node = parse_expression("UTC_TIMESTAMP()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "utc_timestamp")

    def test_ascii_function(self):
        """测试 ASCII 函数"""
        node = parse_expression("ASCII('A')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "ascii")
        self.assertEqual(len(node.param_list), 1)

    def test_charset_function(self):
        """测试 CHARSET 函数"""
        node = parse_expression("CHARSET('Hello')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "charset")
        self.assertEqual(len(node.param_list), 1)

    def test_coalesce_function(self):
        """测试 COALESCE 函数"""
        node = parse_expression("COALESCE(column_name_1, column_name_2)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "coalesce")
        self.assertEqual(len(node.param_list), 2)

    def test_collation_function(self):
        """测试 COLLATION 函数"""
        node = parse_expression("COLLATION('Hello')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "collation")
        self.assertEqual(len(node.param_list), 1)

    def test_database_function(self):
        """测试 DATABASE 函数"""
        node = parse_expression("DATABASE()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "database")
        self.assertEqual(len(node.param_list), 0)

    def test_if_function(self):
        """测试 IF 函数"""
        node = parse_expression("IF(column_name > 0, 'positive', 'negative')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "if")
        self.assertEqual(len(node.param_list), 3)

    def test_format_function_two_params(self):
        """测试 FORMAT 函数（两参数）"""
        node = parse_expression("FORMAT(12345.6789, 2)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "format")
        self.assertEqual(len(node.param_list), 2)

    def test_format_function_three_params(self):
        """测试 FORMAT 函数（三参数）"""
        node = parse_expression("FORMAT(12345.6789, 2, 'de_DE')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "format")
        self.assertEqual(len(node.param_list), 3)

    def test_microsecond_function(self):
        """测试 MICROSECOND 函数"""
        node = parse_expression("MICROSECOND('12:30:45.123456')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "microsecond")
        self.assertEqual(len(node.param_list), 1)

    def test_mod_function(self):
        """测试 MOD 函数"""
        node = parse_expression("MOD(10, 3)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "mod")
        self.assertEqual(len(node.param_list), 2)

    def test_quarter_function(self):
        """测试 QUARTER 函数"""
        node = parse_expression("QUARTER('2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "quarter")
        self.assertEqual(len(node.param_list), 1)

    def test_repeat_function(self):
        """测试 REPEAT 函数"""
        node = parse_expression("REPEAT('Hello', 3)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "repeat")
        self.assertEqual(len(node.param_list), 2)

    def test_replace_function(self):
        """测试 REPLACE 函数"""
        node = parse_expression("REPLACE('Hello World', 'World', 'Universe')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "replace")
        self.assertEqual(len(node.param_list), 3)

    def test_reverse_function(self):
        """测试 REVERSE 函数"""
        node = parse_expression("REVERSE('Hello')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "reverse")
        self.assertEqual(len(node.param_list), 1)

    def test_row_count_function(self):
        """测试 ROW_COUNT 函数"""
        node = parse_expression("ROW_COUNT()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "row_count")
        self.assertEqual(len(node.param_list), 0)

    def test_truncate_function(self):
        """测试 TRUNCATE 函数"""
        node = parse_expression("TRUNCATE(12345.6789, 2)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "truncate")
        self.assertEqual(len(node.param_list), 2)

    def test_week_function_single_param(self):
        """测试 WEEK 函数（单参数）"""
        node = parse_expression("WEEK('2023-01-01')")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "week")
        self.assertEqual(len(node.param_list), 1)

    def test_week_function_two_params(self):
        """测试 WEEK 函数（两参数）"""
        node = parse_expression("WEEK('2023-01-01', 1)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "week")
        self.assertEqual(len(node.param_list), 2)

    def test_weight_string_function_basic(self):
        """测试 WEIGHT_STRING 函数（基础形式）"""
        node = parse_expression("WEIGHT_STRING('Hello')")
        self.assertIsInstance(node, ast.FunctionWeightString)
        self.assertFalse(node.binary_flag)

    def test_weight_string_function_as_char(self):
        """测试 WEIGHT_STRING 函数（AS CHAR）"""
        node = parse_expression("WEIGHT_STRING('Hello' AS CHAR(10))")
        self.assertIsInstance(node, ast.FunctionWeightString)
        self.assertFalse(node.binary_flag)

    def test_weight_string_function_as_binary(self):
        """测试 WEIGHT_STRING 函数（AS BINARY）"""
        node = parse_expression("WEIGHT_STRING('Hello' AS BINARY(10))")
        self.assertIsInstance(node, ast.FunctionWeightString)
        self.assertTrue(node.binary_flag)

    def test_weight_string_function_with_params(self):
        """测试 WEIGHT_STRING 函数（带参数）"""
        node = parse_expression("WEIGHT_STRING('Hello', 1, 2, 3)")
        self.assertIsInstance(node, ast.FunctionWeightString)

    def test_geometrycollection_function(self):
        """测试 GEOMETRYCOLLECTION 函数"""
        node = parse_expression("GEOMETRYCOLLECTION()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "geometrycollection")

    def test_linestring_function(self):
        """测试 LINESTRING 函数"""
        node = parse_expression("LINESTRING(POINT(0, 0), POINT(1, 1))")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "linestring")

    def test_multilinestring_function(self):
        """测试 MULTILINESTRING 函数"""
        node = parse_expression("MULTILINESTRING(LINESTRING(POINT(0, 0), POINT(1, 1)))")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "multilinestring")

    def test_multipoint_function(self):
        """测试 MULTIPOINT 函数"""
        node = parse_expression("MULTIPOINT(POINT(0, 0), POINT(1, 1))")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "multipoint")

    def test_multipolygon_function(self):
        """测试 MULTIPOLYGON 函数"""
        node = parse_expression("MULTIPOLYGON(POLYGON(LINESTRING(POINT(0, 0), POINT(1, 1), POINT(0, 0))))")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "multipolygon")

    def test_point_function(self):
        """测试 POINT 函数"""
        node = parse_expression("POINT(0, 0)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "point")
        self.assertEqual(len(node.param_list), 2)

    def test_polygon_function(self):
        """测试 POLYGON 函数"""
        node = parse_expression("POLYGON(LINESTRING(POINT(0, 0), POINT(1, 1), POINT(0, 0)))")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "polygon")

    def test_regular_function_single_name(self):
        """测试常规函数（单名称）"""
        node = parse_expression("my_function(column_name)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "my_function")
        self.assertEqual(len(node.param_list), 1)

    def test_regular_function_qualified_name(self):
        """测试常规函数（限定名称）"""
        node = parse_expression("schema_name.my_function(column_name)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.schema_name, "schema_name")
        self.assertEqual(node.function_name, "my_function")
        self.assertEqual(len(node.param_list), 1)


class TestDateTimeType(TestCase):
    """测试 date_time_type 语义组
    
    测试日期时间类型枚举值的解析
    """

    def test_date_type(self):
        """测试 DATE 类型"""
        node = parse_expression("GET_FORMAT(DATE, 'EUR')")
        self.assertIsInstance(node, ast.FunctionGetFormat)
        self.assertEqual(node.date_time_type, ast.DateTimeTypeEnum.DATE)

    def test_time_type(self):
        """测试 TIME 类型"""
        node = parse_expression("GET_FORMAT(TIME, 'EUR')")
        self.assertIsInstance(node, ast.FunctionGetFormat)
        self.assertEqual(node.date_time_type, ast.DateTimeTypeEnum.TIME)

    def test_timestamp_type(self):
        """测试 TIMESTAMP 类型"""
        node = parse_expression("GET_FORMAT(TIMESTAMP, 'EUR')")
        self.assertIsInstance(node, ast.FunctionGetFormat)
        self.assertEqual(node.date_time_type, ast.DateTimeTypeEnum.TIMESTAMP)

    def test_datetime_type(self):
        """测试 DATETIME 类型"""
        node = parse_expression("GET_FORMAT(DATETIME, 'EUR')")
        self.assertIsInstance(node, ast.FunctionGetFormat)
        self.assertEqual(node.date_time_type, ast.DateTimeTypeEnum.DATETIME)


class TestNowExpression(TestCase):
    """测试 now_expression 语义组
    
    测试 NOW 函数表达式的解析
    """

    def test_now_function_without_precision(self):
        """测试 NOW 函数（无精度）"""
        node = parse_expression("NOW()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "now")
        self.assertEqual(len(node.param_list), 0)

    def test_now_function_with_precision(self):
        """测试 NOW 函数（带精度）"""
        node = parse_expression("NOW(3)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "now")
        self.assertEqual(len(node.param_list), 1)