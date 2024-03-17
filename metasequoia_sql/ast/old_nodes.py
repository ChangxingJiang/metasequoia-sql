"""
将 SQL 解析为 AST 抽象语法树的工具类
"""

import re

from metasequoia_sql.ast.nodes import *


# ------------------------------ 抽象语法树节点对象 ------------------------------


class ASTLeaf(AST, abc.ABC):
    """抽象语法树 AST 的叶子节点"""

    def __init__(self, origin: str):
        super().__init__(origin)

    def __new__(cls, origin: str):
        if origin == " ":
            obj = object.__new__(ASTSpace)  # 空格节点
        elif origin == "\n":
            obj = object.__new__(ASTLineBreak)  # 换行符节点
        elif origin == ",":
            obj = object.__new__(ASTComma)  # 逗号
        elif origin == ";":
            obj = object.__new__(ASTSemicolon)  # 分号
        elif re.match(r"^\d+$", origin):
            obj = object.__new__(ASTLiteralInteger)  # 字面值整数
        elif re.match(r"^\d+.\d+$", origin):
            obj = object.__new__(ASTLiteralFloat)  # 字面值浮点数
        elif (origin.startswith("\"") and origin.endswith("\"")) or (origin.startswith("'") and origin.endswith("'")):
            obj = object.__new__(ASTLiteralString)  # 字面值字符串
        elif origin.startswith("/*") and origin.endswith("*/"):
            obj = object.__new__(ASTMultiLineComment)  # 多行注释
        else:
            obj = object.__new__(ASTOtherLeaf)  # 其他节点
        obj.__init__(origin)
        return obj


class ASTOtherLeaf(AST):
    def __init__(self, origin: Optional[str]):
        super().__init__(origin)
        print(f"other leaf: {origin}")

    @property
    def source(self) -> str:
        return self._origin
