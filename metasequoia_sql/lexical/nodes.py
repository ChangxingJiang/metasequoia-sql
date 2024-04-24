"""
抽象语法树（AST）的节点类

所有抽象语法树的节点类均继承自抽象基类 AST 类，除 AST 类外，其他节点可以分为如下三种类型：
- 定值叶节点：不包含子节点，且 source 返回定值的对象
- 非定值叶节点：不包含子节点，但 source 返回值不固定的对象
- 中间节点（插入语节点）：包含子节点的节点
"""

import abc
import enum
from typing import List, Optional, Any, Set, Union

from metasequoia_sql.lexical.static import HEXADECIMAL_CHARACTER_SET, BINARY_CHARACTER_SET
from metasequoia_sql.errors import AstParseError

__all__ = [
    "AST", "ASTMark", "ASTSingle", "ASTParenthesis", "ASTLiteralInteger", "ASTLiteralFloat", "ASTLiteralString",
    "ASTLiteralHex", "ASTLiteralBool", "ASTLiteralBit", "ASTLiteralNull"
]


class ASTMark(enum.Enum):
    """抽象语法树节点标记"""
    SPACE = "<space>"
    NAME = "<name>"
    PARENTHESIS = "<parenthesis>"
    LITERAL = "<literal>"
    COMMENT = "<comment>"
    ARRAY_INDEX = "<array_index>"
    CUSTOM = "<custom>"  # 自定义标记（用于插件开发）


# 抽象语法树节点标记映射
MARK_HASH = {mark.value: mark for mark in ASTMark}


# ------------------------------ 抽象节点类 ------------------------------


class AST(abc.ABC):
    """抽象语法树（AST）节点类的抽象基类"""

    def __init__(self, marks: Optional[Set[ASTMark]] = None):
        self.marks: Set[ASTMark] = marks if marks is not None else set()

    @property
    @abc.abstractmethod
    def source(self) -> str:
        """返回当前节点的源代码"""

    @abc.abstractmethod
    def children(self) -> List["AST"]:
        """返回所有下游节点，若为叶子节点，则返回空列表"""
        return []

    def equals(self, other: Union[str, ASTMark]) -> bool:
        """判断当前 AST 节点是否与一段源代码相同"""
        if isinstance(other, ASTMark):
            return other in self.marks  # 枚举类的类型标记
        if other.startswith("<") and other.endswith(">"):
            return MARK_HASH.get(other) in self.marks  # 字符串格式的类型标记
        return self.source.upper() == other.upper()  # 字符串格式文本

    @property
    def literal_value(self) -> Any:
        """字面值的值"""
        return None


class ASTSingle(AST):
    """单元素节点"""

    def __init__(self, source: str, marks: Optional[Set[ASTMark]] = None):
        super().__init__(marks)
        self._source = source

    @property
    def source(self) -> str:
        """当前节点的源代码"""
        return self._source

    def children(self) -> List["AST"]:
        """返回所有下游节点，若为叶子节点，则返回空列表"""
        return []

    def __repr__(self) -> str:
        format_source = self.source.replace("\n", r"\n")
        return f"<{self.__class__.__name__} source={format_source}>"


class ASTParenthesis(AST):
    """插入语节点"""

    def __init__(self, tokens: List[AST], marks: Optional[Set[ASTMark]] = None):
        super().__init__(marks)
        self._tokens: List[AST] = tokens

    def children(self) -> List["AST"]:
        return self._tokens

    @property
    def source(self):
        return "(" + "".join(token.source for token in self._tokens) + ")"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} children={self.children()}>"


class ASTLiteralInteger(ASTSingle):
    """字面值整数"""

    def __init__(self, source: str, marks: Optional[Set[ASTMark]] = None):
        super().__init__(source, marks)
        self._value = int(source)

    @property
    def literal_value(self) -> int:
        return self._value

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralFloat(ASTSingle):
    """字面值浮点数"""

    def __init__(self, source: str, marks: Optional[Set[ASTMark]] = None):
        super().__init__(source, marks)
        self._value = float(source)

    @property
    def literal_value(self) -> float:
        return self._value

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralString(ASTSingle):
    """字面值字符串"""

    def __init__(self, source: str, marks: Optional[Set[ASTMark]] = None):
        super().__init__(source, marks)
        self._value = source[1:-1]  # 不包含引号的部分

    @property
    def literal_value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"'{self._value}'"


class ASTLiteralHex(ASTSingle):
    """十六进制字面值"""

    def __init__(self, source: str, marks: Optional[Set[ASTMark]] = None):
        super().__init__(source, marks)
        self._value = self._get_value(source)  # 获取十六进制字面值中的十六进制数值，如果格式不满足则返回 None
        if self._value is None:
            raise AstParseError(f"十六进制数不满足字符集要求: {source}")

    @classmethod
    def check(cls, origin: str):
        """判断是否为当前节点"""
        return cls._get_value(origin) is not None

    @staticmethod
    def _get_value(origin: str) -> Optional[str]:
        """获取十六进制字面值中的十六进制数值，如果格式不满足则返回 None"""
        # 检查是否满足如下 3 种字面值格式：x'01BF'、X'01BF'、0x01BF
        if (origin.startswith("x'") or origin.startswith("X'")) and origin.endswith("'"):
            value = origin[2:-1].upper()
        elif (origin.startswith("x\"") or origin.startswith("X\"")) and origin.endswith("\""):
            value = origin[2:-1].upper()
        elif origin.startswith("0x"):
            value = origin[2:].upper()
        else:
            return None

        # 检查十六进制中的数值是否满足字符集要求
        for ch in value:
            if ch not in HEXADECIMAL_CHARACTER_SET:
                return None

        return value

    @property
    def literal_value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"x'{self._value}'"


class ASTLiteralBool(ASTSingle):
    """布尔字面值"""

    def __init__(self, source: str, marks: Optional[Set[ASTMark]] = None):
        super().__init__(source, marks)
        self._value: bool = source.upper() == "TRUE"

    @classmethod
    def check(cls, origin: str) -> bool:
        """判断是否为当前节点"""
        return origin.upper() in {"TRUE", "FALSE"}

    @property
    def literal_value(self) -> bool:
        return self._value

    @property
    def source(self) -> str:
        return "TRUE" if self._value is True else "FALSE"


class ASTLiteralBit(ASTSingle):
    """位值字面值"""

    def __init__(self, source: str, marks: Optional[Set[ASTMark]] = None):
        super().__init__(source, marks)
        self._value = self._get_value(source)  # 获取二进制字面值中的二进制数值，如果格式不满足则返回 None
        if self._value is None:
            raise AstParseError(f"不满足格式要求的二进制字面值: origin={source}")

    @classmethod
    def check(cls, origin: str):
        """判断是否为当前节点"""
        return cls._get_value(origin) is not None

    @staticmethod
    def _get_value(origin: str) -> Optional[str]:
        """获取二进制字面值中的二进制数值，如果格式不满足则返回 None"""
        # 检查是否满足如下 3 种字面值格式：b'01'、B'01'、0b01
        if (origin.startswith("b'") or origin.startswith("B'")) and origin.endswith("'"):
            value = origin[2:-1].upper()
        elif (origin.startswith("b\"") or origin.startswith("B\"")) and origin.endswith("\""):
            value = origin[2:-1].upper()
        elif origin.startswith("0b"):
            value = origin[2:].upper()
        else:
            return None

        # 检查二进制中的数值是否满足字符集要求
        for ch in value:
            if ch not in BINARY_CHARACTER_SET:
                return None

        return value

    @property
    def literal_value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"b'{self._value}'"


class ASTLiteralNull(ASTSingle):
    """空值字面值"""

    @classmethod
    def check(cls, origin: str):
        """判断是否为当前节点"""
        return origin.upper() == "NULL"

    @property
    def literal_value(self) -> None:
        return None

    @property
    def source(self) -> str:
        return "NULL"
