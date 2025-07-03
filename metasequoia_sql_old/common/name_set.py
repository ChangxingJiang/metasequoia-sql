"""
名称集的静态常量
"""

__all__ = ["WINDOW_FUNCTION_NAME_SET", "AGGREGATION_FUNCTION_NAME_SET", "GLOBAL_VARIABLE_NAME_SET"]

# 窗口函数名称集合
WINDOW_FUNCTION_NAME_SET = {"ROW_NUMBER", "RANK", "DENSE_RANK",
                            "SUM", "MIN", "MAX", "AVG", "COUNT",
                            "LAG", "LEAD", "FIRST_VALUE", "LAST_VALUE", "NTILE",
                            "COLLECT_SET", "COLLECT_LIST", "CONCAT",  # 也可以直接将结果合并
                            }

# 聚合函数名称集合
AGGREGATION_FUNCTION_NAME_SET = {"COUNT", "SUM", "MIN", "MAX", "AVG"}

# 全局变量名称集合
GLOBAL_VARIABLE_NAME_SET = {"CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT DATE", "CURRENT TIME",
                            "CURRENT TIMESTAMP"}
