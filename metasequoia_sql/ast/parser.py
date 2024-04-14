"""
ast 的解析方法
"""

import enum
import re
from typing import List

from metasequoia_sql.ast.nodes import (AST, ASTMark, ASTSingle, ASTLiteralInteger, ASTLiteralFloat, ASTLiteralString,
                                       ASTLiteralHex, ASTLiteralBool, ASTLiteralBit, ASTLiteralNull, ASTParenthesis)
from metasequoia_sql.common.text_scanner import TextScanner
from metasequoia_sql.errors import AstParseError


class AstParseStatus(enum.Enum):
    """SQL 源码的解析状态"""
    WAIT_TOKEN = enum.auto()  # 前一个字符是开头、空白字符或上一个 token 的结尾，正等待新的 token
    IN_WORD = enum.auto()  # 当前正在正常词语中
    IN_DOUBLE_QUOTE = enum.auto()  # 当前正在双引号 " 中
    IN_SINGLE_QUOTE = enum.auto()  # 当前正在单引号 ' 中
    IN_BACK_QUOTE = enum.auto()  # 当前正在反引号 ` 中
    IN_EXPLAIN_1 = enum.auto()  # 当前在 # 或 -- 标记的单行注释中
    IN_EXPLAIN_2 = enum.auto()  # 当前在 /* 和 */ 标注的多行注释中


class AstParseContext:
    """词法解析状态机的上下文管理器

    - 以 move_ 为前缀的方法，会移动指针位置
    - 以 stand_ 为前缀的方法，不会移动指针位置

    Attributes
    ----------
    _stack : List[List[AST]]
        当前已解析的节点树。使用多层栈维护，每一层栈表示一层插入语。
    _scanner : TextScanner
        源代码遍历器
    _status : AstParseStatus
        状态机状态
    _cache : List[str]
        当前正在缓存的词语
    """

    def __init__(self, text: str):
        self._stack: List[List[AST]] = [[]]
        self._scanner: TextScanner = TextScanner(list(text.replace("\r\n", "\n")))
        self._status: AstParseStatus = AstParseStatus.WAIT_TOKEN
        self._cache: List[str] = []

    # ------------------------------ 上下文管理器属性 ------------------------------

    @property
    def stack(self) -> List[List[AST]]:
        """获取当前自动机词语栈"""
        return self._stack

    @property
    def scanner(self) -> TextScanner:
        """获取当前的文本扫描器"""
        return self._scanner

    @property
    def status(self) -> AstParseStatus:
        """获取当前自动机状态"""
        return self._status

    @property
    def last_ch(self) -> str:
        """当前指针位置的上一个字符"""
        return self._scanner.last

    @property
    def now_ch(self) -> str:
        """当前指针位置的字符"""
        return self._scanner.now

    @property
    def next_ch(self) -> str:
        """当前指针位置的下一个字符"""
        return self._scanner.next1

    @property
    def is_finish(self) -> bool:
        """若当前上下文已匹配结束则返回 True，否则返回 False"""
        return self._scanner.is_finish

    # ------------------------------ 当前缓存词语的相关方法 ------------------------------

    def cache_get(self) -> str:
        """获取当前正在缓存的词语"""
        return "".join(self._cache)

    def cache_reset(self) -> None:
        """重置当前正在缓存的词语"""
        self._cache = []

    def cache_add(self) -> None:
        """将当前指针位置的字符添加到缓存，并移动指针位置"""
        self._cache.append(self._scanner.pop())

    def cache_reset_and_add(self) -> None:
        """【移动指针】重置当前正在缓存的词语，然后将当前指针位置的字符添加到缓存，并移动指针位置"""
        self.cache_reset()
        self.cache_add()

    def cache_get_and_reset(self) -> str:
        """获取当前正在缓存的词语，并重置词语缓存"""
        result = self.cache_get()
        self.cache_reset()
        return result

    # ------------------------------ 状态变化方法 ------------------------------

    def handle_left_parenthesis(self) -> None:
        """【移动指针】处理当前指针位置的左括号"""
        self.scanner.pop()
        self.stack.append([])

    def handle_right_parenthesis(self) -> None:
        """【移动指针】处理当前指针位置的右括号"""
        if len(self.stack) <= 1:
            raise AstParseError(f"当前 ')' 数量大于 '(': pos={self.scanner.pos}")

        self.scanner.pop()
        tokens = self.stack.pop()
        self.stack[-1].append(ASTParenthesis(tokens, {ASTMark.PARENTHESIS}))

    def handle_end_word(self) -> None:
        """【不移动指针】处理在当前指针位置的前一个字符结束的缓存词语（即当前指针位置是下一个词语的第一个字符）

        1. 获取并重置缓存词语
        2. 解析缓存词语并更新到节点树中
        3. 将状态更新为等待下一个节点
        """
        origin = self.cache_get_and_reset()
        # 空格、换行符
        if origin in {" ", "\n"}:
            self.stack[-1].append(ASTSingle(origin, {ASTMark.SPACE}))
        # 逗号、分号、点号、等号、计算运算符（含通配符）、比较运算符
        elif origin in {",", ";", ".", "=", "+", "-", "/", "%", "||", "<>", "!=", "<", "<=", ">", ">="}:
            self.stack[-1].append(ASTSingle(origin))
        # 子句核心关键词
        elif origin.upper() in {"SELECT", "FROM", "LATERAL", "VIEW", "JOIN", "ON", "WHERE", "GROUP", "BY", "HAVING",
                                "ORDER", "LIMIT", "UNION", "EXCEPT", "MINUS", "INTERSECT"}:
            self.stack[-1].append(ASTSingle(origin))
        # 下标
        elif origin.startswith("[") and origin.endswith("]"):
            self.stack[-1].append(ASTSingle(origin, {ASTMark.ARRAY_INDEX}))
        # 逻辑运算符
        elif origin.upper() in {"AND", "NOT", "OR"}:
            self.stack[-1].append(ASTSingle(origin.upper()))
        # 字面值整数
        elif re.match(r"^[+-]?\d+$", origin):
            self.stack[-1].append(ASTLiteralInteger(origin, {ASTMark.LITERAL}))
        # 字面值小数或浮点数
        elif re.match(r"^[+-]?\d+.\d+(E\d+)?$", origin):
            self.stack[-1].append(ASTLiteralFloat(origin, {ASTMark.LITERAL}))
        # 字面值字符串（包含字面值日期和时间）
        elif (origin.startswith("\"") and origin.endswith("\"")) or (origin.startswith("'") and origin.endswith("'")):
            self.stack[-1].append(ASTLiteralString(origin, {ASTMark.LITERAL, ASTMark.NAME}))
        # 十六进制字面值节点
        elif ASTLiteralHex.check(origin) is True:
            self.stack[-1].append(ASTLiteralHex(origin, {ASTMark.LITERAL}))
        # 布尔字面值节点
        elif ASTLiteralBool.check(origin) is True:
            self.stack[-1].append(ASTLiteralBool(origin, {ASTMark.LITERAL}))
        # 位值字面值节点
        elif ASTLiteralBit.check(origin) is True:
            self.stack[-1].append(ASTLiteralBit(origin, {ASTMark.LITERAL}))
        # 空值字面值节点
        elif ASTLiteralNull.check(origin) is True:
            self.stack[-1].append(ASTLiteralNull(origin, {ASTMark.LITERAL}))
        # 显式标识符
        elif origin.startswith("`") and origin.endswith("`"):
            self.stack[-1].append(ASTSingle(origin, {ASTMark.NAME}))
        # 单行注释
        elif origin.startswith("#") or origin.startswith("--"):
            self.stack[-1].append(ASTSingle(origin, {ASTMark.COMMENT}))
        # 多行注释
        elif origin.startswith("/*") and origin.endswith("*/"):
            self.stack[-1].append(ASTSingle(origin, {ASTMark.COMMENT}))
        else:
            self.stack[-1].append(ASTSingle(origin, {ASTMark.NAME}))

    def cache_add_and_handle_end_word(self) -> None:
        """【移动指针】先将当前指针位置的字符添加到缓存并移动指针位置，然后处理在刚缓存的字符结束的缓存词语（即调用时的指针位置为当前词语的最后一个字符）"""
        self.cache_add()
        self.handle_end_word()

    # ------------------------------ 私有处理方法 ------------------------------

    def set_status(self, status: AstParseStatus) -> None:
        """设置状态"""
        self._status = status
