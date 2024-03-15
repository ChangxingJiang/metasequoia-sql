"""
名词解释

column expression (字段表达式)：在 SELECT 子句中字段的表达式，可能是字段名或计算函数（可能包含别名）
table expression（表名表达式）：在 FROM 和 JOIN 子句中表示表的表达式，可能是表名或子表插入语（可能包含别名）
join expression（关联表达式）：在 JOIN 子句中表示关联方式的表达式，可能是 ON 或 USING
condition expression（条件表达式）：在 WHERE 子句中表示筛选条件的表达式，允许使用 OR 或 JOIN 拼接为新的条件表达式（可能为插入语）
limit expression（限制表达式）：在 LIMIT 子句中的表达式，可能为 x,y 格式或 x OFFSET y 格式
"""

import enum

from metasequoia_sql import ast
from metasequoia_sql.parser.common_parser import SqlParser


@enum.unique
class SelectParseStage(enum.StrEnum):
    """
    状态命名规则：{子句名}_{位置描述}
    """

    # 状态：在 SELECT 关键字之前
    # 目标匹配：SELECT 关键字
    STATEMENT_BEFORE = "STATEMENT_BEFORE"

    # 状态：在 SELECT 关键字之后，或字段表达式后的逗号之后
    # 目标匹配：字段表达式
    SELECT_WAIT_COLUMN_EXPRESSION = "SELECT_WAIT_COLUMN_EXPRESSION"

    # 状态：在字段表达式之后，逗号之前
    # 目标匹配：下一个子句的关键字；下一个字段表达式；语句结束
    SELECT_AFTER_COLUMN_EXPRESSION = "SELECT_AFTER_COLUMN_EXPRESSION"

    # 状态：在 FROM 关键字之后，或 FROM 子句表名表达式后的逗号之后
    # 目标匹配：表名表达式
    FROM_WAIT_TABLE_EXPRESSION = "FROM_WAIT_TABLE_EXPRESSION"

    # 状态：在 FROM 子句的表名表达式之后，逗号之前
    # 目标匹配：下一个子句的关键字；下一个表名表达式；语句结束
    FROM_AFTER_TABLE_EXPRESSION = "FROM_AFTER_TABLE_EXPRESSION"

    # 状态：在 JOIN 关键字之后，或 JOIN 子句的表名表达式之后
    # 目标匹配：表名表达式
    JOIN_WAIT_TABLE_EXPRESSION = "JOIN_WAIT_TABLE_EXPRESSION"

    # 状态：在 JOIN 子句的表名表达式之后，关联表达式之前
    # 目标匹配：关联表达式
    JOIN_WAIT_JOIN_EXPRESSION = "JOIN_WAIT_JOIN_EXPRESSION"

    # 状态：在 JOIN 子句的关联表达式之后
    # 目标匹配：下一个子句的关键字；下一个 JOIN 子句；语句结束
    JOIN_AFTER_JOIN_EXPRESSION = "JOIN_AFTER_JOIN_EXPRESSION"

    # 状态：在 WHERE 关键字、WHERE 子句的 OR 关键字、WHERE 子句的 AND 关键字之后；在条件表达式之前
    # 目标匹配：条件表达式
    WHERE_WAIT_CONDITION_EXPRESSION_FIRST = "WHERE_WAIT_CONDITION_EXPRESSION_FIRST"  # 在 WHERE 关键字之后
    WHERE_WAIT_CONDITION_EXPRESSION_OR = "WHERE_WAIT_CONDITION_EXPRESSION_OR"  # 在第一层的 OR 关键字之后
    WHERE_WAIT_CONDITION_EXPRESSION_AND = "WHERE_WAIT_CONDITION_EXPRESSION_AND"  # 在第一层的 AND 关键字之后

    # 状态：在 WHERE 子句的条件表达式之后
    # 目标匹配：AND 关键字、OR 关键字；下一个子句的关键字；语句结束
    WHERE_AFTER_CONDITION_EXPRESSION_OR = "WHERE_AFTER_CONDITION_EXPRESSION_OR"  # 上一个条件表达式是 OR 关键字之后
    WHERE_AFTER_CONDITION_EXPRESSION_AND = "WHERE_AFTER_CONDITION_EXPRESSION_AND"  # 上一个条件表达式是 AND 关键字之后

    # 状态：在 GROUP BY 关键字之后，在字段表达式之前
    # 目标匹配：字段表达式
    GROUP_BY_WAIT_COLUMN_EXPRESSION = "GROUP_BY_WAIT_COLUMN_EXPRESSION"

    # 状态：在 GROUP BY 子句的字段表达式之后，逗号之前
    # 目标匹配：下一个字段表达式；下一个子句的关键字；语句结束
    GROUP_BY_AFTER_COLUMN_EXPRESSION = "GROUP_BY_AFTER_COLUMN_EXPRESSION"

    # 状态：在 HAVING 关键字之后，在条件表达式之前
    # 目标匹配：条件表达式
    HAVING_WAIT_CONDITION_EXPRESSION_FIRST = "HAVING_WAIT_CONDITION_EXPRESSION_FIRST"  # 在 HAVING 关键字之后
    HAVING_WAIT_CONDITION_EXPRESSION_OR = "HAVING_WAIT_CONDITION_EXPRESSION_FIRST"  # 在第一层的 OR 关键字之后
    HAVING_WAIT_CONDITION_EXPRESSION_AND = "HAVING_WAIT_CONDITION_EXPRESSION_FIRST"  # 在第一层的 AND 关键字之后

    # 状态：在 HAVING 子句的条件表达式之后
    # 目标匹配：AND 关键字、OR 关键字；下一个子句的关键字；语句结束
    HAVING_AFTER_CONDITION_EXPRESSION_OR = "HAVING_AFTER_CONDITION_EXPRESSION_OR"  # 上一个条件表达式是 OR 关键字之后
    HAVING_AFTER_CONDITION_EXPRESSION_AND = "HAVING_AFTER_CONDITION_EXPRESSION_AND"  # 上一个条件表达式是 AND 关键字之后

    # 状态：在 ORDER BY 关键字之后，在字段表达式之前
    # 目标匹配：条件表达式
    ORDER_BY_WAIT_COLUMN_EXPRESSION = "ORDER_BY_WAIT_COLUMN_EXPRESSION"

    # 状态：在 ORDER BY 子句的字段表达式之后，逗号之前
    # 目标匹配：下一个字段表达式；下一个子句的关键字；语句结束
    ORDER_BY_AFTER_COLUMN_EXPRESSION = "ORDER_BY_AFTER_COLUMN_EXPRESSION"

    # 状态：在 LIMIT 关键字之后，限制表达式之前
    # 目标匹配：限制表达式
    LIMIT_WAIT_LIMIT_EXPRESSION = "LIMIT_WAIT_LIMIT_EXPRESSION"

    # 状态：在 LIMIT 子句的限制表达式之后
    # 目标匹配：语句结束
    LIMIT_AFTER_LIMIT_EXPRESSION = "LIMIT_AFTER_LIMIT_EXPRESSION"


class SelectParser(SqlParser):
    """Hive 的 SELECT 语句解析器"""

    def __init__(self, root: ast.ASTInternal):
        pass


if __name__ == "__main__":
    from demo_sql import *

    result: ast.ASTStatement = ast.ASTParser(DEMO_MYSQL_MCC_15_2_3_1).parse()
    print(result.__repr__())
