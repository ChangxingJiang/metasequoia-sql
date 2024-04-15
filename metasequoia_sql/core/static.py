"""
静态常量
"""

__all__ = ["WINDOW_FUNCTION_NAME_SET", "AGGREGATION_FUNCTION_NAME_SET"]

# 窗口函数名称集合
WINDOW_FUNCTION_NAME_SET = {"ROW_NUMBER", "RANK", "DENSE_RANK", "SUM", "MIN", "MAX", "AVG", "LAG", "LEAD",
                            "FIRST_VALUE", "LAST_VALUE", "NTILE"}

# 聚合函数名称集合
AGGREGATION_FUNCTION_NAME_SET = {"COUNT", "SUM", "MIN", "MAX", "AVG"}
