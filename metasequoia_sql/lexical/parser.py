"""
抽象词法树（AMT）的解析方法
"""

import enum
import re
from typing import List, Union

from metasequoia_sql.lexical.nodes import (AMTBase, AMTMark, AMTBaseSingle, AMTLiteralInteger, AMTLiteralFloat, AMTLiteralString,
                                           AMTLiteralHex, AMTLiteralBool, AMTLiteralBit, AMTLiteralNull, AMTBaseParenthesis)
from metasequoia_sql.common.text_scanner import TextScanner
from metasequoia_sql.errors import AMTParseError


class AstParseStatus(enum.Enum):
    """SQL 源码的解析状态"""
    WAIT_TOKEN = enum.auto()  # 前一个字符是开头、空白字符或上一个 token 的结尾，正等待新的 token
    IN_WORD = enum.auto()  # 当前正在正常词语中
    IN_DOUBLE_QUOTE = enum.auto()  # 当前正在双引号 " 中
    IN_SINGLE_QUOTE = enum.auto()  # 当前正在单引号 ' 中
    IN_BACK_QUOTE = enum.auto()  # 当前正在反引号 ` 中
    IN_EXPLAIN_1 = enum.auto()  # 当前在 # 或 -- 标记的单行注释中
    IN_EXPLAIN_2 = enum.auto()  # 当前在 /* 和 */ 标注的多行注释中


class ASTParser:
    """抽象语法树解析器

    Attributes
    ----------
    _stack : List[List[AMTBase]]
        当前已解析的节点树。使用多层栈维护，每一层栈表示一层插入语。
    _scanner : TextScanner
        源代码遍历器
    _status : AstParseStatus
        状态机状态
    _cache : List[str]
        当前正在缓存的词语
    """

    def __init__(self, text: str):
        self._stack: List[List[AMTBase]] = [[]]
        self._scanner: TextScanner = TextScanner(self._preproc_text(text))
        self._status: Union[AstParseStatus, object] = AstParseStatus.WAIT_TOKEN
        self._cache: List[str] = []

    @staticmethod
    def _preproc_text(text):
        return text.replace("\r\n", "\n").replace("\t", " ").replace("　", " ")

    # ------------------------------ 上下文管理器属性 ------------------------------

    @property
    def stack(self) -> List[List[AMTBase]]:
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

    def start_parenthesis(self) -> None:
        """【移动指针】处理当前指针位置的左括号"""
        self.scanner.pop()
        self.stack.append([])

    def end_parenthesis(self) -> None:
        """【移动指针】处理当前指针位置的右括号"""
        if len(self.stack) <= 1:
            raise AMTParseError(f"当前 ')' 数量大于 '(': pos={self.scanner.pos}")

        self.scanner.pop()
        tokens = self.stack.pop()
        self.stack[-1].append(AMTBaseParenthesis(tokens, {AMTMark.PARENTHESIS}))

    def handle_end_word(self) -> None:
        """【不移动指针】处理在当前指针位置的前一个字符结束的缓存词语（即当前指针位置是下一个词语的第一个字符）

        1. 获取并重置缓存词语
        2. 解析缓存词语并更新到节点树中
        3. 将状态更新为等待下一个节点
        """
        origin = self.cache_get_and_reset()
        # 空格、换行符
        if origin in {" ", "\n"}:
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.SPACE}))
        # 逗号、分号、点号、等号、计算运算符（含通配符）、比较运算符、子句核心关键词、逻辑运算符
        elif origin.upper() in {",", ";", ".", "=", "+", "-", "/", "%", "||", "<>", "!=", "<", "<=", ">", ">=",
                                "SELECT", "FROM", "LATERAL", "VIEW", "JOIN", "ON", "WHERE", "GROUP", "BY", "HAVING",
                                "ORDER", "LIMIT", "UNION", "EXCEPT", "MINUS", "INTERSECT",
                                "AND", "NOT", "OR"}:
            self.stack[-1].append(AMTBaseSingle(origin))
        # 下标
        elif origin.startswith("[") and origin.endswith("]"):
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.ARRAY_INDEX}))
        # 字面值整数
        elif re.match(r"^[+-]?\d+$", origin):
            self.stack[-1].append(AMTLiteralInteger(origin, {AMTMark.LITERAL}))
        # 字面值小数或浮点数
        elif re.match(r"^[+-]?\d+.\d+(E\d+)?$", origin):
            self.stack[-1].append(AMTLiteralFloat(origin, {AMTMark.LITERAL}))
        # 字面值字符串（包含字面值日期和时间）
        elif (origin.startswith("\"") and origin.endswith("\"")) or (origin.startswith("'") and origin.endswith("'")):
            self.stack[-1].append(AMTLiteralString(origin, {AMTMark.LITERAL, AMTMark.NAME}))
        # 十六进制字面值节点
        elif AMTLiteralHex.check(origin) is True:
            self.stack[-1].append(AMTLiteralHex(origin, {AMTMark.LITERAL}))
        # 布尔字面值节点
        elif AMTLiteralBool.check(origin) is True:
            self.stack[-1].append(AMTLiteralBool(origin, {AMTMark.LITERAL}))
        # 位值字面值节点
        elif AMTLiteralBit.check(origin) is True:
            self.stack[-1].append(AMTLiteralBit(origin, {AMTMark.LITERAL}))
        # 空值字面值节点
        elif AMTLiteralNull.check(origin) is True:
            self.stack[-1].append(AMTLiteralNull(origin, {AMTMark.LITERAL}))
        # 显式标识符
        elif origin.startswith("`") and origin.endswith("`"):
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.NAME}))
        # 单行注释
        elif origin.startswith("#") or origin.startswith("--"):
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.COMMENT}))
        # 多行注释
        elif origin.startswith("/*") and origin.endswith("*/"):
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.COMMENT}))
        else:
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.NAME}))

    def cache_add_and_handle_end_word(self) -> None:
        """【移动指针】先将当前指针位置的字符添加到缓存并移动指针位置，然后处理在刚缓存的字符结束的缓存词语（即调用时的指针位置为当前词语的最后一个字符）"""
        self.cache_add()
        self.handle_end_word()

    # ------------------------------ 私有处理方法 ------------------------------

    def set_status(self, status: Union[AstParseStatus, object]) -> None:
        """设置状态"""
        self._status = status

    # ------------------------------ 自动机执行方法 ------------------------------
    def parse(self):
        """执行文本解析自动机"""
        while not self.scanner.is_finish:
            self.handle_change()

        # 处理最后一个词语
        self.handle_last()

        if len(self.stack) > 1:
            for item in self.stack:
                print(item)
            raise AMTParseError(f"在解析过程中，`(` 数量大于 `)`，相差数量 = {len(self.stack) - 1}")

    def handle_change(self):
        """处理一次的变化"""
        if self.status == AstParseStatus.WAIT_TOKEN:  # 前一个字符是空白字符
            if self.scanner.now == "/" and self.scanner.next1 == "*":
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2)
            elif self.scanner.now in {" ", "\n", ",", ";", "=", "+", "*", "/", ".", "%"}:
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.handle_end_word()
            elif self.scanner.now == "-" and not (self.scanner.last == "-" or self.scanner.next1 == "-"):
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.handle_end_word()
            elif self.scanner.now == "\"":
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif self.scanner.now == "'":
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
            elif self.scanner.now == "`":
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_BACK_QUOTE)
            elif self.scanner.now == "#" or (self.scanner.now == "-" and self.scanner.next1 == "-"):
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_EXPLAIN_1)
            elif self.scanner.now == "(":
                self.start_parenthesis()  # 【移动指针】处理当前指针位置的左括号
            elif self.scanner.now == ")":
                self.end_parenthesis()  # 【移动指针】处理当前指针位置的右括号
            else:
                self.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_WORD)
        elif (self.status == AstParseStatus.IN_DOUBLE_QUOTE and
              self.scanner.last != "\\" and self.scanner.now == "\"" and not self.scanner.next1 == "\""):
            self.cache_add_and_handle_end_word()
            self.set_status(AstParseStatus.WAIT_TOKEN)
        # 当前指针位置字符为双引号字符串中的 "" 转义中的第 1 个字符
        elif (self.status == AstParseStatus.IN_DOUBLE_QUOTE and
              self.scanner.last != "\\" and self.scanner.now == "\"" and self.scanner.next1 == "\""):
            self.cache_add()
            self.cache_add()
        elif (self.status == AstParseStatus.IN_SINGLE_QUOTE and
              self.scanner.last != "\\" and self.scanner.now == "'" and not self.scanner.next1 == "'"):
            self.cache_add_and_handle_end_word()
            self.set_status(AstParseStatus.WAIT_TOKEN)
        # 当前指针位置字符为单引号字符串中的 '' 转义中的第 1 个字符
        elif (self.status == AstParseStatus.IN_SINGLE_QUOTE and
              self.scanner.last != "\\" and self.scanner.now == "'" and self.scanner.next1 == "'"):
            self.cache_add()
            self.cache_add()
        elif self.status == AstParseStatus.IN_BACK_QUOTE and self.scanner.now == "`":
            self.cache_add_and_handle_end_word()
            self.set_status(AstParseStatus.WAIT_TOKEN)
        elif self.status == AstParseStatus.IN_EXPLAIN_1 and self.scanner.now == "\n":
            self.handle_end_word()
            self.set_status(AstParseStatus.WAIT_TOKEN)
        elif self.status == AstParseStatus.IN_EXPLAIN_2 and self.scanner.last == "*" and self.scanner.now == "/":
            self.cache_add_and_handle_end_word()
            self.set_status(AstParseStatus.WAIT_TOKEN)
        elif self.status == AstParseStatus.IN_WORD:
            if self.scanner.now in {" ", "\n", ",", ";", "+", "-", "*", "/", "`", "<", "!", "%", ""}:
                self.handle_end_word()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == "|" and self.scanner.last != "|":
                self.handle_end_word()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == "=" and self.scanner.last not in {"!", "<", ">"}:
                self.handle_end_word()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == ">" and self.scanner.last != "<":
                self.handle_end_word()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            # 前面不完全为数字时，出现点号
            elif self.scanner.now == "." and not self.cache_get().isnumeric():
                self.handle_end_word()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == "\"":
                if self.cache_get() in {"b", "B", "x", "X"}:  # 位值字面值和十六进制字面值
                    self.cache_add()
                    self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
                else:
                    self.handle_end_word()
                    self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == "'":
                if self.cache_get() in {"b", "B", "x", "X"}:  # 位值字面值和十六进制字面值
                    self.cache_add()
                    self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
                else:
                    self.handle_end_word()
                    self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == "(":
                self.handle_end_word()
                self.start_parenthesis()  # 【移动指针】处理当前指针位置的左括号
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == ")":
                self.handle_end_word()
                self.end_parenthesis()  # 【移动指针】处理当前指针位置的右括号
                self.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                self.cache_add()
        else:
            self.cache_add()

    def handle_last(self):
        """处理字符串扫描后的情况"""
        if self.status == AstParseStatus.IN_WORD:
            self.handle_end_word()
            self.set_status(AstParseStatus.WAIT_TOKEN)

    def result(self):
        """获取自动机运行结果"""
        return self.stack[0]
