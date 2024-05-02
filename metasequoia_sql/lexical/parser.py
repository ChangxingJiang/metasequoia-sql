"""
抽象词法树（AMT）的解析方法

TODO 增加各种元素在末尾的单元测试
"""

from typing import List, Union

from metasequoia_sql.common.text_scanner import TextScanner
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTBase, AMTMark, AMTBaseSingle, AMTBaseParenthesis
from metasequoia_sql.lexical.fsm_operate import FSMOperate, FSMOperateType
from metasequoia_sql.lexical.fsm_operation_map import END, DEFAULT, FSM_OPERATION_MAP
from metasequoia_sql.lexical.fsm_status import FSMStatus

__all__ = ["FSMMachine"]


class FSMMachine:
    """词法分析的有限状态机

    Attributes
    ----------
    _stack : List[List[AMTBase]]
        当前已解析的节点树。使用多层栈维护，每一层栈表示一层插入语。
    _scanner : TextScanner
        源代码遍历器
    _status : FSMStatus
        状态机状态
    _cache : List[str]
        当前正在缓存的词语
    """

    def __init__(self, text: str):
        self._stack: List[List[AMTBase]] = [[]]
        self._scanner: TextScanner = TextScanner(text)
        self._status: Union[FSMStatus, object] = FSMStatus.WAIT
        self._cache: List[str] = []

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
    def status(self) -> FSMStatus:
        """获取当前自动机状态"""
        return self._status

    # ------------------------------ 当前缓存词语的相关方法 ------------------------------

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
            raise AMTParseError(f"当前 ')' 数量大于 '(': {self.scanner}")

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
        elif origin.upper() in {"TRUE", "FALSE", "NULL"}:
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.LITERAL}))
        else:
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.NAME}))

    # ------------------------------ 私有处理方法 ------------------------------

    def set_status(self, status: FSMStatus) -> None:
        """设置状态"""
        self._status = status

    # ------------------------------ 自动机执行方法 ------------------------------
    def parse(self):
        """执行文本解析自动机"""
        while not self.scanner.is_finish:
            self.handle_change(self.scanner.now)
        self.handle_change(END)  # 处理结束标记

        if self.status != FSMStatus.END:
            raise AMTParseError(f"词法分析有限状态机，结束时状态异常: {self.status}")

        if len(self.stack) > 1:
            for item in self.stack:
                print(item)
            raise AMTParseError(f"在解析过程中，`(` 数量大于 `)`，相差数量 = {len(self.stack) - 1}")

    def handle_change(self, ch: str):
        """处理一次的变化"""
        if self.status not in FSM_OPERATION_MAP:
            raise AMTParseError(f"未定义处理规则的状态: {self.status}")

        # 获取需要执行的行为
        operations = FSM_OPERATION_MAP[self.status]
        operate: FSMOperate = operations.get(ch, operations[DEFAULT])

        # 执行行为
        if operate.type == FSMOperateType.ADD_CACHE:
            self._cache.append(self.scanner.pop())
            self.set_status(operate.new_status)
        elif operate.type == FSMOperateType.HANDLE_CACHE:
            self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), operate.marks))
            self.set_status(operate.new_status)
        elif operate.type == FSMOperateType.HANDLE_CACHE_WORD:
            self.cache_reset_and_handle()
            self.set_status(operate.new_status)
        elif operate.type == FSMOperateType.ADD_AND_HANDLE_CACHE:
            self._cache.append(self.scanner.pop())
            self.stack[-1].append(AMTBaseSingle(self.cache_get_and_reset(), operate.marks))
            self.set_status(operate.new_status)
        elif operate.type == FSMOperateType.START_PARENTHESIS:
            self.start_parenthesis()
        elif operate.type == FSMOperateType.END_PARENTHESIS:
            self.end_parenthesis()
        elif operate.type == FSMOperateType.SET_STATUS:
            self.set_status(operate.new_status)
        elif operate.type == FSMOperateType.RAISE:
            if ch == END:
                raise AMTParseError(f"当前状态={self.status.name}({self.status.value}) 出现非法结束符")
            raise AMTParseError(f"当前状态={self.status.name}({self.status.value}) 出现非法字符: {ch}")
        else:
            raise AMTParseError(f"未知状态行为: {operate.type}")

    def result(self):
        """获取自动机运行结果"""
        return self.stack[0]
