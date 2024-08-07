"""
抽象词法树（AMT）的节点类

所有抽象词法树的节点类均继承自抽象基类 AMT 类，除 AMT 类外，其他节点可以分为如下三种类型：
- 定值叶节点：不包含子节点，且 source 返回定值的对象
- 非定值叶节点：不包含子节点，但 source 返回值不固定的对象
- 中间节点（插入语节点）：包含子节点的节点
"""

import abc
import enum
from typing import List, Union, Set

__all__ = ["AMTBase", "AMTMark", "AMTSingle", "AMTParenthesis", "AMTSlice"]


class AMTMark(enum.IntEnum):
    """抽象语法树节点标记

    使用整型枚举值，每个标签为一个二进制数，用于实现状态压缩，提高计算性能
    """
    NONE = 0
    SPACE = 1 << 0
    NAME = 1 << 1
    PARENTHESIS = 1 << 2
    LITERAL = 1 << 3
    LITERAL_HEX = 1 << 4
    LITERAL_BIT = 1 << 5
    LITERAL_INT = 1 << 6
    LITERAL_FLOAT = 1 << 7
    COMMENT = 1 << 8
    ARRAY_INDEX = 1 << 9
    CUSTOM_1 = 1 << 22  # 自定义标记（用于插件开发）
    CUSTOM_2 = 1 << 23  # 自定义标记（用于插件开发）
    CUSTOM_3 = 1 << 24  # 自定义标记（用于插件开发）
    CUSTOM_4 = 1 << 25  # 自定义标记（用于插件开发）
    CUSTOM_5 = 1 << 26  # 自定义标记（用于插件开发）
    CUSTOM_6 = 1 << 27  # 自定义标记（用于插件开发）
    CUSTOM_7 = 1 << 28  # 自定义标记（用于插件开发）
    CUSTOM_8 = 1 << 29  # 自定义标记（用于插件开发）
    CUSTOM_9 = 1 << 30  # 自定义标记（用于插件开发）
    CUSTOM_10 = 1 << 31  # 自定义标记（用于插件开发）


# ------------------------------ 抽象节点类 ------------------------------


class AMTBase(abc.ABC):
    # pylint: disable=E1101
    """抽象词法树（AMT）节点类的抽象基类"""

    __slots__ = ["marks", "source", "children"]

    def equals(self, other: Union[str, AMTMark]) -> Union[bool, int]:
        """判断当前抽象词法树节点是否等价于 other

        Parameters
        ----------
        other : Union[str, AMTMark]
            字符串格式的源码，或 AMTMark 格式的标记

        Returns
        -------
        Union[bool, int]
            如果当前抽象词法树节点等价于 other，则返回真值，否则返回假值
        """
        if isinstance(other, AMTMark):
            return other & self.marks  # 枚举类的类型标记
        return self.source.upper() == other.upper()  # 字符串格式文本

    def has_mark(self, other: AMTMark) -> Union[bool, int]:
        """判断当前 AMT 节点是否包含标记 mark"""
        return self.marks & other

    def source_equal(self, other: str) -> bool:
        """判断当前 AMT 节点的源代码是否等于 token（适用于比较运算符）"""
        return self.source == other

    def source_equal_use_upper(self, other: str) -> bool:
        """判断当前 AMT 节点的源代码的 **大写形式** 是否等于 token（适用于比较关键字）"""
        return self.source.upper() == other

    def source_in_set_use_upper(self, other: Set[str]) -> bool:
        """判断当前 AMT 节点的源代码的 **大写形式** 是否等于 token（适用于比较关键字）"""
        return self.source.upper() in other

    def _get_mark_name_list(self) -> List[str]:
        """获取状态压缩的 Mark 对应的标签名称列表"""
        result = []
        for mark in AMTMark:
            if self.marks & mark.value:
                result.append(mark.name)
        return result


class AMTSingle(AMTBase):
    """单元素节点"""

    def __init__(self, source: str, marks: int = 0):
        self.marks = marks
        self.source = source
        self.children = []

    def __repr__(self) -> str:
        source_str = self.source.replace("\n", r"\n")
        mark_str = "|".join(self._get_mark_name_list())
        return f"<{self.__class__.__name__} source=\"{source_str}\" marks={mark_str}>"


class AMTParenthesisBase(AMTBase):
    """插入语节点的基类"""

    def __init__(self, children: List[AMTBase], marks: int = 0):
        self.marks = marks
        self.source = "(" + "".join(token.source for token in children) + ")"
        self.children: List[AMTBase] = children

    def equals(self, other: Union[str, AMTMark]) -> Union[bool, int]:
        """判断当前抽象词法树节点是否等价于 other

        Parameters
        ----------
        other : Union[str, AMTMark]
            字符串格式的源码，或 AMTMark 格式的标记

        Returns
        -------
        Union[bool, int]
            如果当前抽象词法树节点等价于 other，则返回真值，否则返回假值
        """
        if isinstance(other, AMTMark):
            return other & self.marks  # 枚举类的类型标记
        return False  # 插入语不尝试匹配源码值

    def __repr__(self) -> str:
        mark_str = "|".join(self._get_mark_name_list())
        return f"<{self.__class__.__name__} children={self.children} marks={mark_str}>"


class AMTParenthesis(AMTParenthesisBase):
    """一般插入语节点"""


class AMTSlice(AMTParenthesisBase):
    """抽取插入语节点"""
