"""
名词解释
"""

import enum

from metasequoia_sql import ast
from metasequoia_sql.common.token_scanner import TokenScanner


@enum.unique
class ParseSelectStage(enum.StrEnum):
    """
    状态命名规则：{子句名}_{位置描述}
    """

    # TODO DISTINCT 关键字

    BEFORE_KEYWORD_SELECT = enum.auto()

    # 状态：在 SELECT 关键字之后
    # 目标匹配：DISTINCT；
    AFTER_KEYWORD_SELECT = enum.auto()

    # 状态：在 SELECT 关键字之后，或字段表达式后的逗号之后
    # 目标匹配：字段表达式
    SELECT_WAIT_COLUMN = "SELECT_WAIT_COLUMN_EXPRESSION"

    # 状态：在字段表达式之后，逗号之前
    # 目标匹配：下一个子句的关键字；下一个字段表达式；语句结束
    SELECT_AFTER_COLUMN = "SELECT_AFTER_COLUMN_EXPRESSION"

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
    HAVING_WAIT_CONDITION_EXPRESSION_OR = "HAVING_WAIT_CONDITION_EXPRESSION_OR"  # 在第一层的 OR 关键字之后
    HAVING_WAIT_CONDITION_EXPRESSION_AND = "HAVING_WAIT_CONDITION_EXPRESSION_AND"  # 在第一层的 AND 关键字之后

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

    STATEMENT_FINISH = enum.auto()


def parse_select(scanner: TokenScanner):
    """解析 SELECT 语句"""
    status = ParseSelectStage.BEFORE_KEYWORD_SELECT
    while status != ParseSelectStage.STATEMENT_FINISH:
        if status == ParseSelectStage.BEFORE_KEYWORD_SELECT:  # 状态：在关键字 SELECT 之前
            scanner.match("SELECT")  # 匹配：关键字 SELECT
            status = ParseSelectStage.SELECT_AFTER_COLUMN
        elif status == ParseSelectStage.SELECT_AFTER_COLUMN:  # 状态：在关键字 SELECT 之后
            if scanner.now.equals("DISTINCT"):  # 匹配：关键字 DISTINCT
                scanner.match("DISTINCT")
                status = ParseSelectStage.SELECT_WAIT_COLUMN
            else:
                pass



if __name__ == "__main__":
    print(parse_select(TokenScanner(ast.parse_as_tokens("trim(column1)"), ignore_space=True)))
