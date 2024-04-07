"""
抽象语法树（AST）的节点类

所有抽象语法树的节点类均继承自抽象基类 AST 类，除 AST 类外，其他节点可以分为如下三种类型：
- 定值叶节点：不包含子节点，且 source 返回定值的对象
- 非定值叶节点：不包含子节点，但 source 返回值不固定的对象
- 中间节点（插入语节点）：包含子节点的节点
"""

import abc
from typing import List, Optional, Any

from metasequoia_sql.errors import AstParseError
from metasequoia_sql.static import HEXADECIMAL_CHARACTER_SET, BINARY_CHARACTER_SET

__all__ = [
    "AST",
    # 固定值节点类
    "ASTSpace", "ASTLineBreak", "ASTComma", "ASTSemicolon",

    "ASTCommon",

    # 字面值节点类
    "ASTLiteralInteger",
    "ASTLiteralFloat",
    "ASTLiteralString",
    "ASTLiteralHex",
    "ASTLiteralBool",
    "ASTLiteralBit",
    "ASTLiteralNull",

    # 其他节点类
    "ASTIdentifier",
    "ASTParenthesis",
    "ASTStatement",
    "ASTOther"
]


# ------------------------------ 抽象节点类 ------------------------------


class AST(abc.ABC):
    """抽象语法树（AST）节点类的抽象基类"""

    @classmethod
    def check(cls, origin: str) -> bool:
        """返回是否满足当前节点的格式要求"""
        # TODO 待改为抽象方法
        return True

    @property
    @abc.abstractmethod
    def source(self) -> str:
        """返回当前节点的源代码

        Returns
        -------
        str
            当前 AST 节点的源代码
        """

    @property
    def children(self) -> List["AST"]:
        """返回所有下游节点，若为叶子节点，则返回空列表"""
        return []

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """AST 节点的对象描述

        描述信息样式如下（其中第 3 中情况需要在子类中重写此方法）：
        1. 中间节点：<{节点类名} children={子节点的对象描述}>
        2. 非定值叶节点：<{节点类名} source={节点源码}>
        3. 定值叶节点：<{节点类型}>
        """
        if len(self.children) > 0:
            return f"<{self.__class__.__name__} children={self.children}>"
        else:
            format_source = self.source.replace("\n", r"\n")
            return f"<{self.__class__.__name__} source={format_source}>"

    def __hash__(self):
        return hash(self.source)

    def equals(self, other: str) -> bool:
        """判断当前 AST 节点是否与一段源代码相同"""
        return self.source.upper() == other.upper()

    # ------------------------------ 获取查询是否属于某种类型节点的方法 ------------------------------

    @property
    def is_space(self) -> bool:
        """当前节点是否为空格（包括空格、换行符等）"""
        return False

    @property
    def is_comma(self) -> bool:
        """当前节点是否为逗号"""
        return False

    @property
    def is_semicolon(self) -> bool:
        """当前节点是否为分号"""
        return False

    @property
    def is_maybe_name(self) -> bool:
        """当前节点是否可能为函数名称"""
        return False

    @property
    def is_parenthesis(self) -> bool:
        """当前节点是否为插入语"""
        return False

    @property
    def is_compute_operator(self) -> bool:
        """当前节点是否为计算运算符"""
        return False

    @property
    def is_compare_operator(self) -> bool:
        """当前节点是否为比较运算符"""
        return False

    @property
    def is_logical_operator(self) -> bool:
        """当前节点是否为逻辑运算符"""
        return False

    @property
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return False

    @property
    def is_dot(self) -> bool:
        """是否为点符号"""
        return False

    @property
    def literal_value(self) -> Any:
        """字面值的值"""
        return None

    @property
    def is_maybe_wildcard(self) -> bool:
        """当前节点是否可能为通配符"""
        return False

    @property
    def is_comment(self) -> bool:
        """当前节点是否为注释"""
        return False

    @property
    def is_multiline_comment(self) -> bool:
        """当前节点是否为多行注释"""
        return False


# ------------------------------ 定值叶节点类 ------------------------------


class ASTSpace(AST):
    """空格符"""

    @property
    def is_space(self) -> bool:
        return True

    @property
    def source(self) -> str:
        return " "

    def __repr__(self) -> str:
        return "<ASTSpace>"


class ASTLineBreak(AST):
    """换行符"""

    @property
    def is_space(self) -> bool:
        return True

    @property
    def source(self) -> str:
        return "\n"

    def __repr__(self) -> str:
        return "<ASTLineBreak>"


class ASTComma(AST):
    """逗号"""

    @property
    def is_comma(self) -> bool:
        """当前节点是否为逗号"""
        return True

    @property
    def source(self) -> str:
        return ","

    def __repr__(self) -> str:
        return "<ASTComma>"


class ASTSemicolon(AST):
    """分号"""

    @property
    def is_semicolon(self) -> bool:
        """当前节点是否为分号"""
        return True

    @property
    def source(self) -> str:
        return ";"

    def __repr__(self) -> str:
        return "<ASTSemicolon>"


# ------------------------------ 非定值叶节点 ------------------------------


class ASTCommon(AST):
    """通用节点"""

    def __init__(self,
                 source: str,
                 is_keyword: bool = False,
                 is_compute_operator: bool = False,
                 is_compare_operator: bool = False,
                 is_logical_operator: bool = False,
                 is_dot: bool = False,
                 is_maybe_name: bool = False,
                 is_maybe_wildcard: bool = False,
                 is_comma: bool = False,
                 is_comment: bool = False,
                 is_multiline_comment: bool = False):
        """通用节点构造器

        Parameters
        ----------
        source : str
            当前节点的源代码（格式化后的）
        is_keyword : bool, default = False
            当前节点是否为关键词
        is_compute_operator : bool, default = False
            当前节点是否为计算运算符
        is_compare_operator : bool, default = False
            当前节点是否为比较运算符
        is_logical_operator : bool, default = False
            当前节点是否为比较运算符
        is_dot : bool, default = False
            当前节点是否为点号
        is_maybe_name : bool, default = False
            当前节点是否可能为名称（表名、函数名或列名）
        is_maybe_wildcard : bool, default = False
            当前节点是否可能为通配符
        is_comma : bool, default = False
            当前节点是否为逗号
        is_comment : bool, default = False
            当前节点是否为注释
        is_multiline_comment : bool, default = False
            当前节点是否为多行注释
        """
        self._source = source
        self._is_keyword = is_keyword
        self._is_compute_operator = is_compute_operator
        self._is_compare_operator = is_compare_operator
        self._is_logical_operator = is_logical_operator
        self._is_dot = is_dot
        self._is_maybe_name = is_maybe_name
        self._is_maybe_wildcard = is_maybe_wildcard
        self._is_comma = is_comma
        self._is_comment = is_comment
        self._is_multiline_comment = is_multiline_comment

    @property
    def is_keyword(self) -> bool:
        """当前节点是否为关键词"""
        return self._is_keyword

    @property
    def is_compute_operator(self) -> bool:
        """当前节点是否为计算运算符"""
        return self._is_compute_operator

    @property
    def is_compare_operator(self) -> bool:
        """当前节点是否为比较运算符"""
        return self._is_compare_operator

    @property
    def is_logical_operator(self) -> bool:
        """当前节点是否为逻辑运算符"""
        return self._is_logical_operator

    @property
    def is_dot(self) -> bool:
        """当前节点是否为点号"""
        return self._is_dot

    @property
    def is_maybe_name(self) -> bool:
        """当前节点是否可能为函数名称"""
        return self._is_maybe_name

    @property
    def is_maybe_wildcard(self) -> bool:
        """当前节点是否可能为通配符"""
        return self._is_maybe_wildcard

    @property
    def is_comma(self) -> bool:
        """当前节点是否为逗号"""
        return self._is_comma

    @property
    def is_comment(self) -> bool:
        """当前节点是否为注释"""
        return self._is_comment

    @property
    def is_multiline_comment(self) -> bool:
        """当前节点是否为多行注释"""
        return self._is_multiline_comment

    @property
    def source(self) -> str:
        """当前节点的源代码（格式化后的）"""
        return self._source


class ASTLiteralInteger(AST):
    """字面值整数"""

    def __init__(self, origin: str):
        self._value = int(origin)

    @property
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return True

    @property
    def literal_value(self) -> int:
        return self._value

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralFloat(AST):
    """字面值浮点数"""

    def __init__(self, origin: str):
        self._value = float(origin)

    @property
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return True

    @property
    def literal_value(self) -> float:
        return self._value

    @property
    def source(self) -> str:
        return f"{self._value}"


class ASTLiteralString(AST):
    """字面值字符串"""

    def __init__(self, origin: str):
        self._value = origin[1:-1]  # 不包含引号的部分

    @property
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return True

    @property
    def literal_value(self) -> str:
        return self._value

    @property
    def is_maybe_name(self) -> bool:
        return True

    @property
    def source(self) -> str:
        return f"'{self._value}'"


class ASTLiteralHex(AST):
    """十六进制字面值"""

    def __init__(self, origin: str):
        self._value = self._get_value(origin)  # 获取十六进制字面值中的十六进制数值，如果格式不满足则返回 None
        if self._value is None:
            raise AstParseError(f"不满足格式要求的十六进制字面值: origin={origin}")

    @classmethod
    def check(cls, origin: str):
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
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return True

    @property
    def literal_value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"x'{self._value}'"


class ASTLiteralBool(AST):
    """布尔字面值"""

    def __init__(self, origin: str):
        self._value: bool = (origin.upper() == "TRUE")

    @classmethod
    def check(cls, origin: str) -> bool:
        return origin.upper() in {"TRUE", "FALSE"}

    @property
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return True

    @property
    def literal_value(self) -> bool:
        return self._value

    @property
    def source(self) -> str:
        return "TRUE" if self._value is True else "FALSE"


class ASTLiteralBit(AST):
    """位值字面值"""

    def __init__(self, origin: str):
        self._value = self._get_value(origin)  # 获取二进制字面值中的二进制数值，如果格式不满足则返回 None
        if self._value is None:
            raise AstParseError(f"不满足格式要求的二进制字面值: origin={origin}")

    @classmethod
    def check(cls, origin: str):
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
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return True

    @property
    def literal_value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"b'{self._value}'"


class ASTLiteralNull(AST):
    """空值字面值"""

    @classmethod
    def check(cls, origin: str):
        return origin.upper() == "NULL"

    @property
    def is_literal(self) -> bool:
        """当前节点是否为字面值"""
        return True

    @property
    def literal_value(self) -> None:
        return None

    @property
    def source(self) -> str:
        return f"NULL"


class ASTIdentifier(AST):
    """显式标识符"""

    def __init__(self, origin: str):
        self._value = origin[1:-1]

    @property
    def is_maybe_name(self) -> bool:
        """当前节点是否可能为函数名称"""
        return True

    @property
    def source(self) -> str:
        return f"`{self._value}`"


class ASTOther(AST):
    """未知节点"""

    # TODO 子节点应该根据自己解析的源代码生成源代码，而不是直接返回原始源代码

    def __init__(self, origin: Optional[str]):
        self._origin = origin

    @property
    def is_maybe_name(self) -> bool:
        """当前节点是否可能为函数名称"""
        return True

    @property
    def source(self) -> str:
        return self._origin


# ------------------------------ 中间节点 ------------------------------


class ASTParenthesis(AST):
    """插入语节点"""

    def __init__(self, tokens: List[AST], start_mark: str, end_mark: str):
        self._tokens: List[AST] = tokens
        self.start_mark = start_mark
        self.end_mark = end_mark

    @property
    def is_parenthesis(self) -> bool:
        """当前节点是否为插入语"""
        return True

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
