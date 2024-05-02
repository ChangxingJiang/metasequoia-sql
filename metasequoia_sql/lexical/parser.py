"""
抽象词法树（AMT）的解析方法

TODO 增加各种元素在末尾的单元测试
"""

import enum
from typing import List, Union

from metasequoia_sql.common import static
from metasequoia_sql.common.basic import is_bool_literal, is_null_literal
from metasequoia_sql.common.text_scanner import TextScanner
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTBase, AMTMark, AMTBaseSingle, AMTBaseParenthesis


class AstParseStatus(enum.Enum):
    """SQL 源码的解析状态"""
    WAIT = enum.auto()  # 前一个字符是开头、空白字符或上一个 token 的结尾，正等待新的 token
    AFTER_21 = enum.auto()  # 在 ! 符号之后
    AFTER_2D = enum.auto()  # 在 - 符号之后
    AFTER_2F = enum.auto()  # 在 / 符号之后
    AFTER_3C = enum.auto()  # 在 < 符号之后
    AFTER_3E = enum.auto()  # 在 > 符号之后
    AFTER_5B = enum.auto()  # 在 [ 符号之后
    AFTER_7C = enum.auto()  # 在 | 符号之后
    AFTER_0 = enum.auto()  # 在 0 之后
    AFTER_B = enum.auto()  # 在 b 或 B 之后
    AFTER_X = enum.auto()  # 在 x 或 X 之后
    IN_HEX_LITERAL_OF_DOUBLE_QUOTE = enum.auto()  # 在十六机制字面值的双引号中
    IN_HEX_LITERAL_OF_SINGLE_QUOTE = enum.auto()  # 在十六进制字面值的单引号中
    IN_HEX_LITERAL_AFTER_0X = enum.auto()  # 在 0x 格式的十六进制字面值中
    IN_BIT_LITERAL_OF_DOUBLE_QUOTE = enum.auto()  # 在二进制字面值的双引号中
    IN_BIT_LITERAL_OF_SINGLE_QUOTE = enum.auto()  # 在二进制字面值的单引号中
    IN_BIT_LITERAL_AFTER_0B = enum.auto()  # 在 0b 格式的十六进制字面值中
    IN_INT = enum.auto()  # 当前正在整数中
    IN_FLOAT = enum.auto()  # 当前正在浮点数中
    IN_INDEX = enum.auto()  # 当前正在匹配数组下标中
    IN_WORD = enum.auto()  # 当前正在普通词语中
    IN_DOUBLE_QUOTE = enum.auto()  # 双引号中
    IN_DOUBLE_QUOTE_AFTER_5C = enum.auto()  # 双引号中：在 \ 之后
    IN_DOUBLE_QUOTE_AFTER_22 = enum.auto()  # 双引号中：在非开头的 " 之后
    IN_SINGLE_QUOTE = enum.auto()  # 单引号中
    IN_SINGLE_QUOTE_AFTER_5C = enum.auto()  # 单引号中：在 \ 之后
    IN_SINGLE_QUOTE_AFTER_27 = enum.auto()  # 单引号中：在非开头的 ' 之后
    IN_BACK_QUOTE = enum.auto()  # 当前正在反引号 ` 中
    IN_EXPLAIN_1 = enum.auto()  # 当前在 # 或 -- 标记的单行注释中
    IN_EXPLAIN_2 = enum.auto()  # 在多行注释中（用 /* 和 */ 标注）
    IN_EXPLAIN_2_AFTER_2A = enum.auto()  # 在多行注释中（用 /* 和 */ 标注），且在 * 符号之后
    FINISH = enum.auto()  # 匹配正常完成

    CUSTOM_1 = "自定义状态1"  # 用于插件开发
    CUSTOM_2 = "自定义状态2"  # 用于插件开发
    CUSTOM_3 = "自定义状态3"  # 用于插件开发
    CUSTOM_4 = "自定义状态4"  # 用于插件开发
    CUSTOM_5 = "自定义状态5"  # 用于插件开发
    CUSTOM_6 = "自定义状态6"  # 用于插件开发
    CUSTOM_7 = "自定义状态7"  # 用于插件开发
    CUSTOM_8 = "自定义状态8"  # 用于插件开发
    CUSTOM_9 = "自定义状态9"  # 用于插件开发
    CUSTOM_10 = "自定义状态10"  # 用于插件开发


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
        self._status: Union[AstParseStatus, object] = AstParseStatus.WAIT
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

    def cache_add(self) -> None:
        """将当前指针位置的字符添加到缓存，并移动指针位置"""
        self._cache.append(self.scanner.pop())

    def cache_get_and_reset(self) -> str:
        """获取当前正在缓存的词语，并重置词语缓存"""
        result = "".join(self._cache)
        self._cache = []
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
        if origin.upper() in {"SELECT", "FROM", "LATERAL", "VIEW", "LEFT", "RIGHT", "INNER", "OUTER", "FULL", "JOIN",
                              "ON", "WHERE", "GROUP", "BY", "HAVING", "ORDER", "LIMIT", "UNION", "EXCEPT", "MINUS",
                              "INTERSECT", "AND", "NOT", "OR"}:
            self.stack[-1].append(AMTBaseSingle(origin))
        # 整数字面值、小数字面值、浮点数字面值、十六进制字面值、布尔值字面值、位值字面值、空值字面值
        elif is_bool_literal(origin) or is_null_literal(origin):
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.LITERAL}))
        # 其他字符、显式标识符
        else:
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.NAME}))

    # ------------------------------ 私有处理方法 ------------------------------

    def set_status(self, status: AstParseStatus) -> None:
        """设置状态"""
        self._status = status

    # ------------------------------ 自动机执行方法 ------------------------------
    def parse(self):
        """执行文本解析自动机"""
        while not self.scanner.is_finish:
            self.handle_change(self.scanner.now)

        # 处理结束标记
        self.handle_change("<END>")

        if len(self.stack) > 1:
            for item in self.stack:
                print(item)
            raise AMTParseError(f"在解析过程中，`(` 数量大于 `)`，相差数量 = {len(self.stack) - 1}")

    def handle_change(self, ch: str):
        """处理一次的变化"""
        if self.status == AstParseStatus.WAIT:  # 前一个字符是空白字符
            if ch == "!":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_21)
            elif ch == "/":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_2F)
            elif ch == "-":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_2D)
            elif ch == "|":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_7C)
            elif ch == "<":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_3C)
            elif ch == ">":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_3E)
            elif ch == "[":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_5B)
            elif ch == "0":
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_0)
            elif ch in {" ", "\n"}:
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.SPACE}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "*":
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.NAME}))  # 可能为通配符
                self.set_status(AstParseStatus.WAIT)
            elif ch in {",", ";", "=", "+", ".", "%"}:
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "\"":
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif ch == "'":
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
            elif ch == "`":
                self.cache_add()
                self.set_status(AstParseStatus.IN_BACK_QUOTE)
            elif ch == "#":
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_1)
            elif ch in {"b", "B"}:
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_B)
            elif ch in {"x", "X"}:
                self.cache_add()
                self.set_status(AstParseStatus.AFTER_X)
            elif ch in static.NUMBER_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_INT)
            elif ch == "(":
                self.start_parenthesis()
                self.set_status(AstParseStatus.WAIT)
            elif ch == ")":
                self.end_parenthesis()
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.set_status(AstParseStatus.FINISH)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_WORD)
        elif self.status == AstParseStatus.AFTER_2D:
            if ch == "-":
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_1)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset()))
                self.set_status(AstParseStatus.WAIT)
        elif self.status == AstParseStatus.AFTER_2F:
            if ch == "*":
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset()))
                self.set_status(AstParseStatus.WAIT)
        elif self.status == AstParseStatus.IN_DOUBLE_QUOTE:
            if ch == "\\":
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE_AFTER_5C)
            elif ch == "\"":
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE_AFTER_22)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
        elif self.status == AstParseStatus.IN_DOUBLE_QUOTE_AFTER_22:
            if ch == "\"":
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.NAME}))
                self.set_status(AstParseStatus.FINISH)
            else:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT)
        elif self.status == AstParseStatus.IN_DOUBLE_QUOTE_AFTER_5C:
            if ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
        elif self.status == AstParseStatus.IN_SINGLE_QUOTE:
            if ch == "\\":
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE_AFTER_5C)
            elif ch == "'":
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE_AFTER_27)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
        elif self.status == AstParseStatus.IN_SINGLE_QUOTE_AFTER_5C:
            if ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
        elif self.status == AstParseStatus.IN_SINGLE_QUOTE_AFTER_27:
            if ch == "'":
                self.cache_add()
                self.set_status(AstParseStatus.IN_SINGLE_QUOTE)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.NAME}))
                self.set_status(AstParseStatus.FINISH)
            else:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT)
        elif self.status == AstParseStatus.IN_BACK_QUOTE:
            if ch == "`":
                # 显式标识符
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_BACK_QUOTE)
        elif self.status == AstParseStatus.IN_EXPLAIN_1:
            if ch == "\n":
                # 单行注释
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.COMMENT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.COMMENT}))
                self.set_status(AstParseStatus.FINISH)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_1)
        elif self.status == AstParseStatus.IN_EXPLAIN_2:
            if ch == "*":
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2_AFTER_2A)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2)
        elif self.status == AstParseStatus.IN_EXPLAIN_2_AFTER_2A:
            if ch == "/":
                # 多行注释
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.COMMENT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_EXPLAIN_2)
        elif self.status == AstParseStatus.AFTER_B:
            if ch == "\"":
                # 位值字面值
                self.cache_add()
                self.set_status(AstParseStatus.IN_BIT_LITERAL_OF_DOUBLE_QUOTE)
            elif ch == "'":
                # 位值字面值
                self.cache_add()
                self.set_status(AstParseStatus.IN_BIT_LITERAL_OF_SINGLE_QUOTE)
            elif ch in static.END_TOKEN_CHARACTER_SET:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.NAME}))
                self.set_status(AstParseStatus.FINISH)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_WORD)
        elif self.status == AstParseStatus.IN_BIT_LITERAL_OF_DOUBLE_QUOTE:
            if ch == "\"":
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_BIT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch in static.BIT_LITERAL_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_BIT_LITERAL_OF_DOUBLE_QUOTE)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                raise AMTParseError(f"当前状态={self.status} 出现位值字面值中的非法字符: {ch}")
        elif self.status == AstParseStatus.IN_BIT_LITERAL_OF_SINGLE_QUOTE:
            if ch == "'":
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_BIT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch in static.BIT_LITERAL_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_BIT_LITERAL_OF_SINGLE_QUOTE)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                raise AMTParseError(f"当前状态={self.status} 出现位值字面值中的非法字符: {ch}")
        elif self.status == AstParseStatus.AFTER_X:
            if ch == "\"":
                # 位值字面值
                self.cache_add()
                self.set_status(AstParseStatus.IN_HEX_LITERAL_OF_DOUBLE_QUOTE)
            elif ch == "'":
                # 位值字面值
                self.cache_add()
                self.set_status(AstParseStatus.IN_HEX_LITERAL_OF_SINGLE_QUOTE)
            elif ch in static.END_TOKEN_CHARACTER_SET:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.NAME}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.NAME}))
                self.set_status(AstParseStatus.FINISH)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_WORD)
        elif self.status == AstParseStatus.IN_HEX_LITERAL_OF_DOUBLE_QUOTE:
            if ch == "\"":
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_HEX}))
                self.set_status(AstParseStatus.WAIT)
            elif ch in static.HEX_LITERAL_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_HEX_LITERAL_OF_DOUBLE_QUOTE)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                raise AMTParseError(f"当前状态={self.status} 出现十六进制字面值中的非法字符: {ch}")
        elif self.status == AstParseStatus.IN_HEX_LITERAL_OF_SINGLE_QUOTE:
            if ch == "'":
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_HEX}))
                self.set_status(AstParseStatus.WAIT)
            elif ch in static.HEX_LITERAL_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_HEX_LITERAL_OF_SINGLE_QUOTE)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                raise AMTParseError(f"当前状态={self.status} 出现十六进制字面值中的非法字符: {ch}")
        elif self.status == AstParseStatus.AFTER_7C:
            if ch == "|":
                # 符号：||
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                raise AMTParseError(f"当前状态={self.status} 在 | 字符后出现非法字符: {ch}")
        elif self.status == AstParseStatus.AFTER_3C:
            if ch == "=":
                # 符号：<=
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
            elif ch == ">":
                # 符号：<>
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                # 符号 <
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
        elif self.status == AstParseStatus.AFTER_3E:
            if ch == "=":
                # 符号：>=
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                # 符号 >
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
        elif self.status == AstParseStatus.AFTER_21:
            if ch == "=":
                # 符号：!=
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), set()))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法的结束标记")
            else:
                raise AMTParseError(f"当前状态={self.status} 在 ! 字符后出现非法字符: {ch}")
        elif self.status == AstParseStatus.IN_INT:
            if ch == ".":
                self.cache_add()
                self.set_status(AstParseStatus.IN_FLOAT)
            elif ch in static.NUMBER_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_INT)
            elif ch in static.END_TOKEN_CHARACTER_SET:
                # 整型字面值
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_INT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_INT}))
                self.set_status(AstParseStatus.FINISH)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_WORD)
        elif self.status == AstParseStatus.IN_FLOAT:
            if ch in static.NUMBER_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_FLOAT)
            elif ch in static.END_TOKEN_CHARACTER_SET:
                # 浮点数字面值
                self.stack[-1].append(
                    AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_FLOAT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(
                    AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_FLOAT}))
                self.set_status(AstParseStatus.FINISH)
            else:
                raise AMTParseError(f"当前状态={self.status} 在浮点数中出现非法字符: {ch}")
        elif self.status == AstParseStatus.AFTER_5B:
            if ch in static.NUMBER_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_INDEX)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法结束符")
            else:
                raise AMTParseError(f"当前状态={self.status} 出现非法字符: {ch}")
        elif self.status == AstParseStatus.IN_INDEX:
            if ch in static.NUMBER_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_INDEX)
            elif ch == "]":
                self.cache_add()
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.ARRAY_INDEX}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                raise AMTParseError(f"当前状态={self.status} 出现非法结束符")
            else:
                raise AMTParseError(f"当前状态={self.status} 出现非法字符: {ch}")
        elif self.status == AstParseStatus.AFTER_0:
            if ch == "x":
                self.cache_add()
                self.set_status(AstParseStatus.IN_HEX_LITERAL_AFTER_0X)
            elif ch == "b":
                self.cache_add()
                self.set_status(AstParseStatus.IN_BIT_LITERAL_AFTER_0B)
            elif ch == ".":
                self.cache_add()
                self.set_status(AstParseStatus.IN_FLOAT)
            elif ch in static.NUMBER_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_INT)
            elif ch in static.END_TOKEN_CHARACTER_SET:
                # 整型字面值
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_INT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_INT}))
                self.set_status(AstParseStatus.FINISH)
            else:
                self.cache_add()
                self.set_status(AstParseStatus.IN_WORD)
        elif self.status == AstParseStatus.IN_HEX_LITERAL_AFTER_0X:
            if ch in static.HEX_LITERAL_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_HEX_LITERAL_AFTER_0X)
            elif ch == static.END_TOKEN_CHARACTER_SET:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_HEX}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_HEX}))
                self.set_status(AstParseStatus.FINISH)
            else:
                raise AMTParseError(f"当前状态={self.status} 出现非法字符: {ch}")
        elif self.status == AstParseStatus.IN_BIT_LITERAL_AFTER_0B:
            if ch in static.BIT_LITERAL_CHARACTER_SET:
                self.cache_add()
                self.set_status(AstParseStatus.IN_BIT_LITERAL_AFTER_0B)
            elif ch == static.END_TOKEN_CHARACTER_SET:
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_BIT}))
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), {AMTMark.LITERAL, AMTMark.LITERAL_BIT}))
                self.set_status(AstParseStatus.FINISH)
            else:
                raise AMTParseError(f"当前状态={self.status} 出现非法字符: {ch}")
        elif self.status == AstParseStatus.IN_WORD:
            if ch in static.END_TOKEN_CHARACTER_SET or ch == ".":
                self.cache_reset_and_handle()
                self.set_status(AstParseStatus.WAIT)
            elif ch == "<END>":
                self.cache_reset_and_handle()
                self.set_status(AstParseStatus.FINISH)
            else:
                self.cache_add()
        else:
            raise AMTParseError(f"未定义处理规则的状态: {self.status}")

    def result(self):
        """获取自动机运行结果"""
        return self.stack[0]
