# pylint: disable=E0401,E0611

"""
语法解析器

屏蔽 pylint E0401：parser 将对外暴露
屏蔽 pylint E0611：parser 文件将在编译阶段生成
"""

from metasequoia_sql.syntax.parser import parse
