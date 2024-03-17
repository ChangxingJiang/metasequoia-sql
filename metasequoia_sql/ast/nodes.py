import abc
from typing import List, Optional

from metasequoia_sql.errors import AstParseError

__all__ = [
    "AST",
    "ASTSpace", "ASTLineBreak", "ASTComma", "ASTSemicolon", "ASTEqual",
    "ASTComputeOperator",  # 计算运算符
    "ASTCompareOperator",  # 比较运算符
    "ASTLiteralInteger", "ASTLiteralFloat", "ASTLiteralString", "ASTIdentifier",
    "ASTSimpleLineComment", "ASTMultiLineComment",
    "ASTParenthesis",
    "ASTStatement",
    "ASTOther"
]


# ------------------------------ 抽象节点类 ------------------------------


class AST(abc.ABC):
    """AST 节点类的抽象基类"""

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
            format_source = self.source.replace("\n", r"\n")
            return f"<{self.__class__.__name__} source={format_source}>"

    def equals(self, other: str) -> bool:
        """判断当前 AST 节点是否与一段源代码相同"""
        return self.source.upper() == other.upper()

    def append(self, ch: str) -> None:
        """节点构造器的方法，用于向节点中添加一个字符"""
        raise AstParseError("已构造完成的 AST 节点不允许修改")


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


class ASTEqual(AST):
    """等号"""

    @property
    def source(self) -> str:
        return "="


class ASTComputeOperator(AST):
    """算术操作符"""

    def __init__(self, origin: str):
        if origin not in {"+", "-", "*", "/"}:
            raise AstParseError(f"初始化 ASTComputeOperator 节点失败: origin={origin}")
        self._origin = origin

    @property
    def source(self) -> str:
        return self._origin


class ASTCompareOperator(AST):
    """比较运算符（不含等号）"""

    def __init__(self, origin: str):
        if origin not in {"<>", "!=", "<", "<=", ">", ">="}:
            raise AstParseError(f"初始化 ASTCompareOperator 节点失败: origin={origin}")
        self._origin = origin

    @property
    def source(self) -> str:
        return self._origin


class ASTLiteralInteger(AST):
    """字面值整数"""

    def __init__(self, origin: str):
        self._value = int(origin)

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralFloat(AST):
    """字面值浮点数"""

    def __init__(self, origin: str):
        self._value = float(origin)

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralString(AST):
    """字面值字符串"""

    def __init__(self, origin: str):
        self._value = origin[1:-1]  # 不包含引号的部分

    @property
    def source(self) -> str:
        return f"'{self._value}'"


class ASTIdentifier(AST):
    """显式标识符"""

    def __init__(self, origin: str):
        self._value = origin[1:-1]

    @property
    def source(self) -> str:
        return f"`{self._value}`"


class ASTSimpleLineComment(AST):
    """单行注释"""

    def __init__(self, origin: str):
        self._value = origin

    @property
    def source(self) -> str:
        return self._value


class ASTMultiLineComment(AST):
    """多行注释"""

    def __init__(self, origin: str):
        self._value = origin

    @property
    def source(self) -> str:
        return self._value


class ASTParenthesis(AST):
    """插入语节点"""

    def __init__(self, tokens: List[AST], start_mark: str, end_mark: str):
        self._tokens: List[AST] = tokens
        self.start_mark = start_mark
        self.end_mark = end_mark

    @property
    def children(self) -> List["AST"]:
        return self._tokens

    @property
    def source(self):
        return self.start_mark + "".join(token.source for token in self._tokens) + self.end_mark


class ASTStatement(AST):
    """【包含子节点的 AST 节点】完整 SQL 表达式"""

    def __init__(self, tokens: List[AST]):
        self._tokens: List[AST] = tokens  # 下级节点列表

    @property
    def source(self):
        return "".join(token.source for token in self._tokens)

    @property
    def children(self) -> List["AST"]:
        return self._tokens


class ASTOther(AST):
    """未知节点"""

    def __init__(self, origin: Optional[str]):
        self._origin = origin

    @property
    def source(self) -> str:
        return self._origin
