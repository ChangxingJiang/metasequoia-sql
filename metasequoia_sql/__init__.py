# pylint: disable=E0401,E0611

"""
水杉 SQL 解析器

屏蔽 pylint E0401：parser 将对外暴露
屏蔽 pylint E0611：parser 文件将在编译阶段生成
"""

from metasequoia_sql.lexical import LexFSM
from metasequoia_sql.syntax import parse

__all__ = [
    "parse_statement"
]


def parse_statement(sql: str):
    """
    解析 SQL 语句
    """
    return parse(LexFSM(sql))
