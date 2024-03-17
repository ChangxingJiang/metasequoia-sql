"""
ast 的解析方法
"""

import enum
import re
from typing import List, Optional

from metasequoia_sql.ast.nodes import *
from metasequoia_sql.common.text_scanner import TextScanner


class ASTBuilder(AST):
    """构造中的 AST 节点"""

    def __init__(self, text: Optional[List[str]] = None):
        self._text = text if text is not None else []

    @property
    def source(self) -> str:
        return "".join(self._text)

    def append(self, ch: str):
        """向构造中的 AST 节点添加一个文本元素"""
        self._text.append(ch)

    def __len__(self) -> int:
        return len(self._text)


class AstParseStatus(enum.Enum):
    """SQL 源码的解析状态"""
    WAIT_TOKEN = enum.auto()  # 前一个字符是开头、空白字符或上一个 token 的结尾，正等待新的 token
    IN_WORD = enum.auto()  # 当前正在正常词语中
    IN_DOUBLE_QUOTE = enum.auto()  # 当前正在双引号 " 中
    IN_SINGLE_QUOTE = enum.auto()  # 当前正在单引号 ' 中
    IN_BACK_QUOTE = enum.auto()  # 当前正在反引号 ` 中
    IN_EXPLAIN_1 = enum.auto()  # 当前在 # 标记的注释中
    IN_EXPLAIN_2 = enum.auto()  # 当前在 /* 和 */ 标注的注释中


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
        self._scanner: TextScanner = TextScanner(text.replace("\r\n", "\n"))
        self._status: AstParseStatus = AstParseStatus.WAIT_TOKEN
        self._cache: List[str] = []

    # ------------------------------ 上下文管理器属性 ------------------------------

    @property
    def stack(self) -> List[List[AST]]:
        return self._stack

    @property
    def scanner(self) -> TextScanner:
        return self._scanner

    @property
    def status(self) -> AstParseStatus:
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
        return self._scanner.next

    # ------------------------------ 当前缓存词语的相关方法 ------------------------------

    def stand_cache_get(self) -> str:
        """获取当前正在缓存的词语"""
        return "".join(self._cache)

    def stand_cache_reset(self) -> None:
        """重置当前正在缓存的词语"""
        self._cache = []

    def move_cache_add(self) -> None:
        """将当前指针位置的字符添加到缓存，并移动指针位置"""
        self._cache.append(self._scanner.get())

    def move_cache_reset_and_add(self) -> None:
        """重置当前正在缓存的词语，然后将当前指针位置的字符添加到缓存，并移动指针位置"""
        self.stand_cache_reset()
        self.move_cache_add()

    def stand_cache_get_and_reset(self) -> str:
        """获取当前正在缓存的词语，并重置词语缓存"""
        result = self.stand_cache_get()
        self.stand_cache_reset()
        return result

    # ------------------------------ 状态变化方法 ------------------------------

    def move_handle_space(self) -> None:
        """【移动指针】处理当前指针位置的空格"""
        self._scanner.move()
        self._stack[-1].append(ASTSpace())

    def move_handle_line_break(self) -> None:
        """【移动指针】处理当前指针位置的换行符"""
        self._scanner.move()
        self._stack[-1].append(ASTLineBreak())

    def handle_end_word(self) -> None:
        """【不移动指针】处理在当前指针位置的前一个字符结束的缓存词语（即当前指针位置是下一个词语的第一个字符）

        1. 获取并重置缓存词语
        2. 解析缓存词语并更新到节点树中
        3. 将状态更新为等待下一个节点
        """
        origin = self.stand_cache_get_and_reset()
        if origin == " ":
            self._stack[-1].append(ASTSpace())  # 空格
        elif origin == "\n":
            self._stack[-1].append(ASTLineBreak())  # 换行符
        elif origin == ",":
            self._stack[-1].append(ASTComma())  # 逗号
        elif origin == ";":
            self._stack[-1].append(ASTSemicolon())  # 分号
        elif re.match(r"^\d+$", origin):
            self._stack[-1].append(ASTLiteralInteger(origin))  # 字面值整数
        elif re.match(r"^\d+.\d+$", origin):
            self._stack[-1].append(ASTLiteralFloat(origin))  # 字面值浮点数
        elif (origin.startswith("\"") and origin.endswith("\"")) or (origin.startswith("'") and origin.endswith("'")):
            self._stack[-1].append(ASTLiteralString(origin))  # 字面值字符串
        elif origin.startswith("`") and origin.endswith("`"):
            self._stack[-1].append(ASTIdentifier(origin))  # 显式标识符
        elif origin.startswith("/*") and origin.endswith("*/"):
            self._stack[-1].append(ASTMultiLineComment(origin))  # 多行注释
        else:
            self._stack[-1].append(ASTOther(origin))
        self._stand_set_status(AstParseStatus.WAIT_TOKEN)

    # ------------------------------ 私有处理方法 ------------------------------

    def _stand_set_status(self, status: AstParseStatus) -> None:
        """设置状态"""
        self._status = status
