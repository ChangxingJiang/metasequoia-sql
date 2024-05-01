"""
抽象词法树（AMT）的解析方法
"""

import enum
from typing import List, Union

from metasequoia_sql.common.basic import is_literal
from metasequoia_sql.common.text_scanner import TextScanner
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTBase, AMTMark, AMTBaseSingle, AMTBaseParenthesis


class AstParseStatus(enum.Enum):
    """SQL 源码的解析状态"""
    WAIT_TOKEN = enum.auto()  # 前一个字符是开头、空白字符或上一个 token 的结尾，正等待新的 token
    AFTER_2D = enum.auto()  # 在 - 符号之后
    AFTER_2F = enum.auto()  # 在 / 符号之后
    IN_WORD = enum.auto()  # 当前正在正常词语中
    IN_DOUBLE_QUOTE = enum.auto()  # 双引号中
    IN_DOUBLE_QUOTE_AFTER_5C = enum.auto()  # 双引号中：在 \ 之后
    IN_SINGLE_QUOTE = enum.auto()  # 单引号中
    IN_SINGLE_QUOTE_AFTER_5C = enum.auto()  # 单引号中：在 \ 之后
    IN_BACK_QUOTE = enum.auto()  # 当前正在反引号 ` 中
    IN_EXPLAIN_1 = enum.auto()  # 当前在 # 或 -- 标记的单行注释中
    IN_EXPLAIN_2 = enum.auto()  # 在多行注释中（用 /* 和 */ 标注）
    IN_EXPLAIN_2_AFTER_2A = enum.auto()  # 在多行注释中（用 /* 和 */ 标注），且在 * 符号之后


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
        self._cache.append(self.scanner.pop())

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

    def cache_reset_and_handle(self) -> None:
        """【不移动指针】处理在当前指针位置的前一个字符结束的缓存词语（即当前指针位置是下一个词语的第一个字符）

        1. 获取并重置缓存词语
        2. 解析缓存词语并更新到节点树中
        3. 将状态更新为等待下一个节点
        """
        origin = self.cache_get_and_reset()
        # 逗号、分号、点号、等号、计算运算符（含通配符）、比较运算符、子句核心关键词、逻辑运算符
        if origin.upper() in {",", ";", ".", "=", "+", "-", "/", "%", "||", "<>", "!=", "<", "<=", ">", ">=",
                              "SELECT", "FROM", "LATERAL", "VIEW", "LEFT", "RIGHT", "INNER", "OUTER", "FULL", "JOIN",
                              "ON", "WHERE", "GROUP", "BY", "HAVING", "ORDER", "LIMIT", "UNION", "EXCEPT", "MINUS",
                              "INTERSECT", "AND", "NOT", "OR"}:
            self.stack[-1].append(AMTBaseSingle(origin))
        # 下标
        elif origin.startswith("[") and origin.endswith("]"):
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.ARRAY_INDEX}))
        # 整数字面值、小数字面值、浮点数字面值、十六进制字面值、布尔值字面值、位值字面值、空值字面值
        elif is_literal(origin):
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.LITERAL}))
        # 其他字符、显式标识符
        else:
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.NAME}))

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
            if self.scanner.now == "/":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_2F)
            elif self.scanner.now == "-":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_2D)
            elif self.scanner.now in {" ", "\n"}:
                self.stack[-1].append(AMTBaseSingle(self.scanner.pop(), {AMTMark.SPACE}))
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now in {",", ";", "=", "+", "*", ".", "%"}:
                self.cache_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.cache_reset_and_handle()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == "\"":
                self.cache_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif self.scanner.now == "'":
                self.cache_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
            elif self.scanner.now == "`":
                self.cache_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_BACK_QUOTE)
            elif self.scanner.now == "#":
                self.cache_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_EXPLAIN_1)
            elif self.scanner.now == "(":
                self.start_parenthesis()  # 【移动指针】处理当前指针位置的左括号
            elif self.scanner.now == ")":
                self.end_parenthesis()  # 【移动指针】处理当前指针位置的右括号
            else:
                self.cache_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                self.set_status(AstParseStatus.IN_WORD)
        elif self.status == AstParseStatus.AFTER_2D:
            if self.scanner.now == "-":
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_1)
            else:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset()))
                self.set_status(AstParseStatus.WAIT_TOKEN)
        elif self.status == AstParseStatus.AFTER_2F:
            if self.scanner.now == "*":
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2)
            else:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset()))
                self.set_status(AstParseStatus.WAIT_TOKEN)
        elif self.status == AstParseStatus.IN_DOUBLE_QUOTE:
            if self.scanner.now == "\\":
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE_AFTER_5C)
            elif self.scanner.now == "\"" and self.scanner.next == "\"":
                # 当前指针位置字符为双引号字符串中的 "" 转义中的第 1 个字符
                self.cache_add()
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif self.scanner.now == "\"" and not self.scanner.next == "\"":
                # 字面值字符串（包含字面值日期和时间）
                self.cache_add()
                origin = self.cache_get_and_reset()
                self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.LITERAL, AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
        elif self.status == AstParseStatus.IN_DOUBLE_QUOTE_AFTER_5C:
            self.cache_add()
            self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
        elif self.status == AstParseStatus.IN_SINGLE_QUOTE:
            if self.scanner.now == "\\":
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE_AFTER_5C)
            elif self.scanner.now == "'" and self.scanner.next == "'":
                # 当前指针位置字符为单引号字符串中的 '' 转义中的第 1 个字符
                self.cache_add()
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
            elif self.scanner.now == "'" and not self.scanner.next == "'":
                # 字面值字符串（包含字面值日期和时间）
                self.cache_add()
                origin = self.cache_get_and_reset()
                self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.LITERAL, AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
        elif self.status == AstParseStatus.IN_SINGLE_QUOTE_AFTER_5C:
            self.cache_add()
            self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
        elif self.status == AstParseStatus.IN_BACK_QUOTE:
            if self.scanner.now == "`":
                # 显式标识符
                self.cache_add()
                origin = self.cache_get_and_reset()
                self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_BACK_QUOTE)
        elif self.status == AstParseStatus.IN_EXPLAIN_1:
            if self.scanner.now == "\n":
                # 单行注释
                origin = self.cache_get_and_reset()
                self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.COMMENT}))
                self.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_1)
        elif self.status == AstParseStatus.IN_EXPLAIN_2:
            if self.scanner.now == "*":
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2_AFTER_2A)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2)
        elif self.status == AstParseStatus.IN_EXPLAIN_2_AFTER_2A:
            if self.scanner.now == "/":
                # 多行注释
                self.cache_add()
                origin = self.cache_get_and_reset()
                self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.COMMENT}))
                self.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2)
        elif self.status == AstParseStatus.IN_WORD:
            if (self.scanner.now in {" ", "\n", ",", ";", "+", "-", "*", "/", "`", "<", "!", "%", "(", ")"} or
                    (self.scanner.now == "|" and self.scanner.last != "|") or
                    (self.scanner.now == "=" and self.scanner.last not in {"!", "<", ">"}) or
                    (self.scanner.now == ">" and self.scanner.last != "<") or
                    (self.scanner.now == "." and not self.cache_get().isnumeric()) or
                    (self.scanner.now in {"\"", "'"} and self.cache_get() not in {"b", "B", "x", "X"})
            ):
                self.cache_reset_and_handle()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            elif self.scanner.now == "\"" and self.cache_get() in {"b", "B", "x", "X"}:  # 位值字面值和十六进制字面值
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif self.scanner.now == "'" and self.cache_get() in {"b", "B", "x", "X"}:  # 位值字面值和十六进制字面值
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
            else:
                self.cache_add()
        else:
            self.cache_add()

    def handle_last(self):
        """处理字符串扫描后的情况"""
        if self.status == AstParseStatus.IN_WORD:
            self.cache_reset_and_handle()
            self.set_status(AstParseStatus.WAIT_TOKEN)

    def result(self):
        """获取自动机运行结果"""
        return self.stack[0]
