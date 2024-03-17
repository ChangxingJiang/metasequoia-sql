import abc
from typing import List, Optional


# ------------------------------ 抽象节点类 ------------------------------


class AST(abc.ABC):
    """AST 节点类的抽象基类"""

    def __init__(self, origin: Optional[str]):
        self._origin = origin

    @property
    def origin(self) -> str:
        return self._origin

    @property
    @abc.abstractmethod
    def source(self) -> str:
        """返回当前节点的源代码

        TODO 子节点应该根据自己解析的源代码生成源代码，而不是直接返回原始源代码

        Returns
        -------
        str
            当前 AST 节点的源代码
        """
        return self._origin

    @property
    def children(self) -> List["AST"]:
        """返回所有下游节点，若为叶子节点，则返回空列表"""
        return []

    @property
    def is_whitespace(self) -> bool:
        """当前节点是否为空格（包括空格、换行符等）"""
        return False

    def __str__(self) -> str:
        return self.source

    def __repr__(self) -> str:
        if len(self.children) > 0:
            return f"<{self.__class__.__name__} children={self.children}>"
        else:
            return f"<{self.__class__.__name__} source={self.source}>"

    def equals(self, other: str) -> bool:
        """判断当前 AST 节点是否与一段源代码相同"""
        return self.source.upper() == other.upper()


# ------------------------------ 具体节点类 ------------------------------


class ASTSpace(AST):
    """空格符"""

    @property
    def is_whitespace(self) -> bool:
        return True

    @property
    def source(self) -> str:
        return " "


class ASTLineBreak(AST):
    """换行符"""

    @property
    def is_whitespace(self) -> bool:
        return True

    @property
    def source(self) -> str:
        return "\n"


class ASTComma(AST):
    """逗号"""

    @property
    def source(self) -> str:
        return ","


class ASTSemicolon(AST):
    """分号"""

    @property
    def source(self) -> str:
        return ";"


class ASTLiteralInteger(AST):
    """字面值整数"""

    def __init__(self, origin: str):
        super().__init__(origin)
        self._value = int(origin)

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralFloat(AST):
    """字面值浮点数"""

    def __init__(self, origin: str):
        super().__init__(origin)
        self._value = float(origin)

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralString(AST):
    """字面值字符串"""

    def __init__(self, origin: str):
        super().__init__(origin)
        self._value = origin[1:-1]  # 不包含引号的部分

    @property
    def source(self) -> str:
        return f"'{self._value}'"


class ASTIdentifier(AST):
    """显式标识符"""

    def __init__(self, origin: str):
        super().__init__(origin)
        self._value = self._origin[1:-1]

    @property
    def source(self) -> str:
        return f"`{self._value}`"


class ASTMultiLineComment(AST):
    """多行注释"""

    @property
    def source(self) -> str:
        return self._origin
