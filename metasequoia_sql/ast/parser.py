"""
ast 的解析方法
"""

from typing import Optional, List

from metasequoia_sql.ast.nodes import AST


class ASTBuilder(AST):
    """构造中的 AST 节点"""

    def __init__(self, text: Optional[List[str]] = None):
        super().__init__(None)
        self._text = text if text is not None else []

    @property
    def source(self) -> str:
        return "".join(self._text)

    def append(self, ch: str):
        """向构造中的 AST 节点添加一个文本元素"""
        self._text.append(ch)

    def __len__(self) -> int:
        return len(self._text)
