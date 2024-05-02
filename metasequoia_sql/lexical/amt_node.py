"""
抽象词法树（AMT）的节点类

所有抽象词法树的节点类均继承自抽象基类 AMT 类，除 AMT 类外，其他节点可以分为如下三种类型：
- 定值叶节点：不包含子节点，且 source 返回定值的对象
- 非定值叶节点：不包含子节点，但 source 返回值不固定的对象
- 中间节点（插入语节点）：包含子节点的节点
"""

import abc
import enum
from typing import List, Optional, Set, Union

__all__ = ["AMTBase", "AMTMark", "AMTBaseSingle", "AMTBaseParenthesis"]


class AMTMark(enum.Enum):
    """抽象语法树节点标记"""
    SPACE = "<space>"
    NAME = "<name>"
    PARENTHESIS = "<parenthesis>"
    LITERAL = "<literal>"
    LITERAL_HEX = "<literal_hex>"
    LITERAL_BIT = "<literal_bit>"
    LITERAL_INT = "<literal_int>"
    LITERAL_FLOAT = "<literal_float>"
    COMMENT = "<comment>"
    ARRAY_INDEX = "<array_index>"
    CUSTOM_1 = "<custom_1>"  # 自定义标记（用于插件开发）
    CUSTOM_2 = "<custom_2>"  # 自定义标记（用于插件开发）
    CUSTOM_3 = "<custom_3>"  # 自定义标记（用于插件开发）
    CUSTOM_4 = "<custom_4>"  # 自定义标记（用于插件开发）
    CUSTOM_5 = "<custom_5>"  # 自定义标记（用于插件开发）
    CUSTOM_6 = "<custom_6>"  # 自定义标记（用于插件开发）
    CUSTOM_7 = "<custom_7>"  # 自定义标记（用于插件开发）
    CUSTOM_8 = "<custom_8>"  # 自定义标记（用于插件开发）
    CUSTOM_9 = "<custom_9>"  # 自定义标记（用于插件开发）
    CUSTOM_10 = "<custom_10>"  # 自定义标记（用于插件开发）


# 抽象语法树节点标记映射
MARK_HASH = {mark.value: mark for mark in AMTMark}


# ------------------------------ 抽象节点类 ------------------------------


class AMTBase(abc.ABC):
    """抽象词法树（AMT）节点类的抽象基类"""

    def __init__(self, marks: Optional[Set[AMTMark]] = None):
        self.marks: Set[AMTMark] = marks if marks is not None else set()

    @property
    @abc.abstractmethod
    def source(self) -> str:
        """返回当前节点的源代码"""

    @abc.abstractmethod
    def children(self) -> List["AMTBase"]:
        """返回所有下游节点，若为叶子节点，则返回空列表"""
        return []

    def equals(self, other: Union[str, AMTMark]) -> bool:
        """判断当前 AMT 节点是否与一段源代码相同"""
        if isinstance(other, AMTMark):
            return other in self.marks  # 枚举类的类型标记
        if other.startswith("<") and other.endswith(">"):
            return MARK_HASH.get(other) in self.marks  # 字符串格式的类型标记
        return self.source.upper() == other.upper()  # 字符串格式文本


class AMTBaseSingle(AMTBase):
    """单元素节点"""

    def __init__(self, source: str, marks: Optional[Set[AMTMark]] = None):
        super().__init__(marks)
        self._source = source

    @property
    def source(self) -> str:
        """当前节点的源代码"""
        return self._source

    def children(self) -> List["AMTBase"]:
        """返回所有下游节点，若为叶子节点，则返回空列表"""
        return []

    def __repr__(self) -> str:
        format_source = self.source.replace("\n", r"\n")
        return f"<{self.__class__.__name__} source={format_source}>"


class AMTBaseParenthesis(AMTBase):
    """插入语节点"""

    def __init__(self, tokens: List[AMTBase], marks: Optional[Set[AMTMark]] = None):
        super().__init__(marks)
        self._tokens: List[AMTBase] = tokens

    def children(self) -> List["AMTBase"]:
        return self._tokens

    @property
    def source(self):
        return "(" + "".join(token.source for token in self._tokens) + ")"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} children={self.children()}>"
