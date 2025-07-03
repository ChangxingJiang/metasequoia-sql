# pylint: disable=E0401,E0611

"""
水杉 SQL 解析器

屏蔽 pylint E0401：parser 将对外暴露
屏蔽 pylint E0611：parser 文件将在编译阶段生成
"""

from metasequoia_sql import ast
from metasequoia_sql.lexical import LexFSM
from metasequoia_sql.syntax import parse
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ast",
    "parse_statement",
    "parse_expression",
]


def parse_statement(sql: str):
    """解析 SQL 语句

    Parameters
    ----------
    sql : str
        SQL 语句
    """
    return parse(LexFSM(sql))


def parse_expression(sql: str):
    """解析 SQL 表达式

    Parameters
    ----------
    sql : str
        SQL 表达式
    """
    return parse(LexFSM(sql, mark=TType.GRAMMAR_EXPRESSION))
