"""
将 SQL 解析为 AST 抽象语法树的工具类
"""

import abc
import enum
from typing import Tuple, List, Optional, Union

from metasequoia_sql.errors import AstParseError


# ------------------------------ 抽象语法树节点对象 ------------------------------


class AST(abc.ABC):
    """所有 SQL 的 AST 节点类的抽象基类"""

    def __init__(self, origin: Optional[str],
                 start_lineno: Optional[int],
                 start_col_offset: Optional[int],
                 end_lineno: Optional[int],
                 end_col_offset: Optional[int]):
        self._origin = origin  # 源码
        self.start_lineno = start_lineno  # 代码开始的行数
        self.start_col_offset = start_col_offset  # 代码开始的列数
        self.end_lineno = end_lineno  # 代码结束的行数
        self.end_col_offset = end_col_offset  # 代码结束的列数

    # -------------------- 需要实现的方法 --------------------

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
    @abc.abstractmethod
    def children(self) -> List["AST"]:
        """返回所有下游节点，若为叶子节点，则返回空列表"""

    @property
    @abc.abstractmethod
    def is_whitespace(self) -> bool:
        """当前 AST 节点是否为空格（包括空格、换行符等）"""

    @property
    def origin(self):
        """返回当前节点的原始语句代码"""
        return self._origin

    def __repr__(self) -> str:
        return self.source

    def equals(self, other: str) -> bool:
        """判断当前 AST 节点是否与一段源代码相同"""
        return self.source.upper() == other.upper()


class ASTLeaf(AST, abc.ABC):
    """抽象语法树 AST 的叶子节点"""

    def __init__(self, origin: str, start_lineno: int, start_col_offset: int, end_lineno: int, end_col_offset: int):
        super().__init__(origin, start_lineno, start_col_offset, end_lineno, end_col_offset)

    @property
    def children(self) -> List["AST"]:
        return []

    def __new__(cls, source: str, start_lineno: int, start_col_offset: int, end_lineno: int, end_col_offset: int):
        if source == " ":
            obj = object.__new__(ASTSpace)  # 空格节点
        elif source == "\n":
            obj = object.__new__(ASTLineBreak)  # 换行符节点
        elif source == ",":
            obj = object.__new__(ASTComma)  # 逗号
        elif source == ";":
            obj = object.__new__(ASTSemicolon)  # 分号
        elif source.startswith("`") and source.endswith("`"):
            obj = object.__new__(ASTIdentifier)  # 标识符
        elif (source.startswith("\"") and source.endswith("\"")) or (source.startswith("'") and source.endswith("'")):
            obj = object.__new__(ASTString)  # 字符串
        elif source.isnumeric():
            obj = object.__new__(ASTNumber)  # 数字节点
        elif source.startswith("/*") and source.endswith("*/"):
            obj = object.__new__(ASTComment)  # 注释节点
        else:
            obj = object.__new__(ASTOtherLeaf)  # 其他节点
        obj.__init__(source, start_lineno, start_col_offset, end_lineno, end_col_offset)
        return obj


class ASTSpaceLeaf(ASTLeaf, abc.ABC):
    """空白字符的叶子结点的抽象类"""

    @property
    def is_whitespace(self) -> bool:
        """当前 AST 节点是否为空格（包括空格、换行符等）"""
        return True


class ASTNonSpaceLeaf(ASTLeaf, abc.ABC):
    """非空白字符的叶子结点的抽象类"""

    @property
    def is_whitespace(self) -> bool:
        """当前 AST 节点是否为空格（包括空格、换行符等）"""
        return False


class ASTSpace(ASTSpaceLeaf):
    """空白字符"""

    @property
    def source(self) -> str:
        return " "


class ASTLineBreak(ASTSpaceLeaf):
    """换行符"""

    @property
    def source(self) -> str:
        return "\n"


class ASTComma(ASTNonSpaceLeaf):
    """逗号"""

    @property
    def source(self) -> str:
        return ","


class ASTSemicolon(ASTNonSpaceLeaf):
    """分号"""

    @property
    def source(self) -> str:
        return ";"


class ASTNumber(ASTNonSpaceLeaf):
    """数字"""

    @property
    def source(self) -> str:
        return self._origin


class ASTString(ASTNonSpaceLeaf):
    """字符串"""

    @property
    def source(self) -> str:
        return self._origin


class ASTIdentifier(ASTNonSpaceLeaf):
    """标识符"""

    def __init__(self, origin: str, start_lineno: int, start_col_offset: int, end_lineno: int, end_col_offset: int):
        super().__init__(origin, start_lineno, start_col_offset, end_lineno, end_col_offset)
        self._value = self._origin.strip("`")

    @property
    def source(self) -> str:
        return f"`{self._value}`"

    def equals(self, other: str) -> bool:
        return self.source.upper() == other.upper() or self.source.upper() == other.upper()


class ASTComment(ASTNonSpaceLeaf):
    """注释"""

    @property
    def source(self) -> str:
        return self._origin


class ASTOtherLeaf(ASTNonSpaceLeaf):
    @property
    def source(self) -> str:
        return self._origin


class ASTInternal(AST):
    """抽象语法树 AST 的中间节点"""

    def __init__(self, origin: str, start_lineno: int, start_col_offset: int, end_lineno: int, end_col_offset: int,
                 tokens: List[AST]):
        super().__init__(origin, start_lineno, start_col_offset, end_lineno, end_col_offset)
        self._tokens: List[AST] = tokens  # 下级节点列表

    @property
    def is_whitespace(self) -> bool:
        """当前 AST 节点是否为空格（包括空格、换行符等）"""
        return False

    @property
    def source(self):
        return "".join(token.source for token in self._tokens)

    @property
    def children(self) -> List["AST"]:
        return self._tokens


class ASTStatement(ASTInternal):
    """【包含子节点的 AST 节点】完整 SQL 表达式"""


class ASTParenthesis(ASTInternal):
    """插入语节点"""

    def __init__(self, origin: str, start_lineno: int, start_col_offset: int, end_lineno: int, end_col_offset: int,
                 tokens: List[AST]):
        super().__init__(origin, start_lineno, start_col_offset, end_lineno, end_col_offset, tokens)
        self.start_mark = origin[0]
        self.end_mark = origin[-1]

    @property
    def source(self):
        return self.start_mark + super().source + self.end_mark


# ------------------------------ 抽象语法树解析对象 ------------------------------


class ParseStatus(enum.Enum):
    """SQL 源码的解析状态"""
    WAIT_FOR_NEW_TOKEN = enum.auto()  # 前一个字符是开头、空白字符或上一个 token 的结尾，正等待新的 token
    IS_IN_NORMAL = enum.auto()  # 当前正在正常词语中
    IS_IN_DOUBLE_QUOTE = enum.auto()  # 当前正在双引号 " 中
    IS_IN_SINGLE_QUOTE = enum.auto()  # 当前正在单引号 ' 中
    IS_IN_BACK_QUOTE = enum.auto()  # 当前正在反引号 ` 中
    IS_IN_EXPLAIN_1 = enum.auto()  # 当前在 # 标记的注释中
    IS_IN_EXPLAIN_2 = enum.auto()  # 当前在 /* 和 */ 标注的注释中
    FAIL = enum.auto()  # 无法解析的 SQL 格式


class ASTParser:
    def __init__(self, source: str):
        """

        Parameters
        ----------
        source : str
            SQL 源码
        """
        self.source: str = source.replace("\r\n", "\n")  # 将源码中的 \r\n 统一为 \n
        self.array: List[Tuple[str, int, int, int]] = text_to_char_array(self.source)
        self.status: ParseStatus = ParseStatus.WAIT_FOR_NEW_TOKEN
        self.now_token_lineno: int = 1  # 当前段落词语开始位置的行数
        self.now_token_offset: int = 0  # 当前段落词语开始位置的列号

    def parse(self) -> ASTStatement:
        """将 SQL 源码解析为 AST 节点

        Returns
        -------
        ASTStatement
            AST 根节点
        """
        last_ch = None  # 上一个字符
        stack: List[List[Union[Tuple[int, int, int], AST]]] = [[]]
        skip = False
        for i, (ch, idx, lineno, col_offset) in enumerate(self.array):
            if skip is True:
                skip = False
                continue

            # 计算当前行的下一个字符
            next_ch = self.array[i + 1][0] if i + 1 < len(self.array) and self.array[i + 1][2] == lineno else None

            if self.status == ParseStatus.WAIT_FOR_NEW_TOKEN:  # 前一个字符是空白字符
                if ch == " ":
                    stack[-1].append(ASTSpace(self.source[idx:idx + 1], lineno, col_offset, lineno, col_offset + 1))
                elif ch == "\n":
                    stack[-1].append(
                        ASTLineBreak(self.source[idx:idx + 1], lineno, col_offset, lineno, col_offset + 1))
                elif ch == "\"":
                    stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_DOUBLE_QUOTE
                elif ch == "'":
                    stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_SINGLE_QUOTE
                elif ch == "`":
                    stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_BACK_QUOTE
                elif ch == "#":
                    stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_EXPLAIN_1
                elif ch == "/":
                    if next_ch == "*":
                        stack[-1].append((idx, lineno, col_offset))
                        self.status = ParseStatus.IS_IN_EXPLAIN_2
                    else:
                        stack[-1].append((idx, lineno, col_offset))
                        self.status = ParseStatus.IS_IN_NORMAL
                elif ch == "(":
                    stack[-1].append((idx, lineno, col_offset))  # 插入语的语法树
                    stack.append([])
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
                elif ch == ")":
                    if len(stack) > 1:
                        tokens = stack.pop()
                        start_idx, start_lineno, start_col_offset = stack[-1].pop()
                        stack[-1].append(
                            ASTParenthesis(self.source[start_idx: idx + 1], start_lineno, start_col_offset, lineno,
                                           col_offset + 1, tokens))
                        self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
                    else:
                        raise AstParseError("')' 数量大于 '('")
                else:
                    stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_NORMAL
            elif self.status == ParseStatus.IS_IN_DOUBLE_QUOTE:
                if ch == "\"" and last_ch != "\\" and next_ch == "\"":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(
                        ASTLeaf(self.source[start_idx: idx + 1], start_lineno, start_col_offset,
                                lineno, col_offset + 1))
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
                elif ch == "\"" and last_ch != "\\":  # 满足 (last_ch == "\"" and stack[-1][-1][0] + 1 == idx and next_ch == "\"")
                    skip = True
            elif self.status == ParseStatus.IS_IN_SINGLE_QUOTE:
                if ch == "'" and last_ch != "\\" and not next_ch == "'":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(
                        ASTLeaf(self.source[start_idx: idx + 1], start_lineno, start_col_offset,
                                lineno, col_offset + 1))
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
                elif ch == "'" and last_ch != "\\":  # 满足 (last_ch == "'" and not stack[-1][-1][0] + 1 == idx and next_ch == "'")
                    skip = True
            elif self.status == ParseStatus.IS_IN_BACK_QUOTE:
                if ch == "`":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(
                        ASTLeaf(self.source[start_idx: idx + 1], start_lineno, start_col_offset, lineno,
                                col_offset + 1))
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
            elif self.status == ParseStatus.IS_IN_EXPLAIN_1:
                if ch == "\n":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(
                        ASTLeaf(self.source[start_idx: idx + 1], start_lineno, start_col_offset, lineno,
                                col_offset + 1))
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
            elif self.status == ParseStatus.IS_IN_EXPLAIN_2:
                if ch == "/" and last_ch == "*":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(
                        ASTLeaf(self.source[start_idx: idx + 1], start_lineno, start_col_offset, lineno,
                                col_offset + 1))
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
            elif self.status == ParseStatus.IS_IN_NORMAL:
                if ch in {" ", "\n", ",", ";", "+", "-", "*", "/", "="}:
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(ASTLeaf(self.source[start_idx: idx], start_lineno, start_col_offset, lineno,
                                             col_offset))
                    stack[-1].append(
                        ASTLeaf(self.source[idx:idx + 1], lineno, col_offset, lineno, col_offset + 1))
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
                elif ch == "\"":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    if start_idx + 1 == idx and self.source[start_idx: idx] == "b":  # 兼容类似字符串 b'0'
                        stack[-1].append((start_idx, start_lineno, start_col_offset))  # 将 b 视作字符串的一部分
                    else:
                        stack[-1].append(ASTLeaf(self.source[start_idx: idx], start_lineno, start_col_offset, lineno,
                                                 col_offset))
                        stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_DOUBLE_QUOTE
                elif ch == "'":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    if start_idx + 1 == idx and self.source[start_idx: idx] == "b":  # 兼容类似字符串 b'0'
                        stack[-1].append((start_idx, start_lineno, start_col_offset))  # 将 b 视作字符串的一部分
                    else:
                        stack[-1].append(ASTLeaf(self.source[start_idx: idx], start_lineno, start_col_offset, lineno,
                                                 col_offset))
                        stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_SINGLE_QUOTE
                elif ch == "`":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(ASTLeaf(self.source[start_idx: idx], start_lineno, start_col_offset, lineno,
                                             col_offset))
                    stack[-1].append((idx, lineno, col_offset))
                    self.status = ParseStatus.IS_IN_BACK_QUOTE
                elif ch == "(":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(ASTLeaf(self.source[start_idx: idx], start_lineno, start_col_offset, lineno,
                                             col_offset))
                    stack[-1].append((idx, lineno, col_offset))  # 插入语的语法树
                    stack.append([])
                    self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
                elif ch == ")":
                    start_idx, start_lineno, start_col_offset = stack[-1].pop()
                    stack[-1].append(ASTLeaf(self.source[start_idx: idx], start_lineno, start_col_offset, lineno,
                                             col_offset))
                    if len(stack) > 1:
                        tokens = stack.pop()
                        start_idx, start_lineno, start_col_offset = stack[-1].pop()
                        stack[-1].append(
                            ASTParenthesis(self.source[start_idx: idx + 1], start_lineno, start_col_offset, lineno,
                                           col_offset + 1, tokens))
                        self.status = ParseStatus.WAIT_FOR_NEW_TOKEN
                    else:
                        raise AstParseError("')' 数量大于 '('")
                else:
                    self.status = ParseStatus.IS_IN_NORMAL

            last_ch = ch

        if len(stack) > 1:
            raise AstParseError("'(' 数量大于 ')'")
        else:
            if self.status == ParseStatus.IS_IN_NORMAL:  # 末尾没有分号的情况
                start_idx, start_lineno, start_col_offset = stack[-1].pop()
                stack[-1].append(ASTLeaf(self.source[start_idx: self.array[-1][1] + 1],
                                         start_lineno, start_col_offset, self.array[-1][2], self.array[-1][3] + 1))
            return ASTStatement(self.source, self.array[0][2], self.array[0][3], self.array[-1][2],
                                self.array[-1][3], stack[0])


def dump(node: AST) -> str:
    """将 AST 节点序列化为 SQL 源码

    Parameters
    ----------
    node : AST
        AST 节点

    Returns
    -------
    str
        SQL 源码
    """
    return node.source


def text_to_char_array(text: str) -> List[Tuple[str, int, int, int]]:
    """将字符串转化为每个字符信息的列表

    Parameters
    ----------
    text : str
        字符串

    Returns
    -------
    列表中每个元素为一个字符；每个元素的元组中的第 0 个元素为字符，第 1 个字符为完整字符串中的下标，第 2 个字符为行号，第 3 个字符为列号
    """
    result: List[Tuple[str, int, int, int]] = []
    lineno: int = 1
    offset: int = 0
    for i, ch in enumerate(text):
        result.append((ch, i, lineno, offset))
        if ch != "\n":
            offset += 1
        else:  # 换行符
            lineno += 1
            offset = 0
    return result
