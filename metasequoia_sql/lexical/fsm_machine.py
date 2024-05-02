"""
词法分析的有限状态机

TODO 增加各种元素在末尾的单元测试
"""

from typing import List, Union

from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTBase, AMTMark, AMTSingle, AMTParenthesis
from metasequoia_sql.lexical.fsm_operate import FSMOperate, FSMOperateType
from metasequoia_sql.lexical.fsm_operation_map import END, DEFAULT, FSM_OPERATION_MAP
from metasequoia_sql.lexical.fsm_status import FSMStatus

__all__ = ["FSMMachine"]


class FSMMachine:
    """词法分析的有限状态机

    Attributes
    ----------
    stack : List[List[AMTBase]]
        当前已解析的节点树。使用多层栈维护，每一层栈表示一层插入语。
    text : str
        源代码遍历器
    status : FSMStatus
        状态机状态
    cache : List[str]
        当前正在缓存的词语
    """

    def __init__(self, text: str):
        self.stack: List[List[AMTBase]] = [[]]
        self.text: str = text
        self.status: Union[FSMStatus, object] = FSMStatus.WAIT
        self.cache: List[str] = []

    # ------------------------------ 当前缓存词语的相关方法 ------------------------------

    def _cache_get_and_reset(self) -> str:
        """获取当前正在缓存的词语，并重置词语缓存"""
        result = "".join(self.cache)
        self.cache = []
        return result

    def cache_reset_and_handle(self) -> None:
        """【不移动指针】处理在当前指针位置的前一个字符结束的缓存词语（即当前指针位置是下一个词语的第一个字符）

        1. 获取并重置缓存词语
        2. 解析缓存词语并更新到节点树中
        3. 将状态更新为等待下一个节点
        """
        origin = self._cache_get_and_reset()
        # 逗号、分号、点号、等号、计算运算符（含通配符）、比较运算符、子句核心关键词、逻辑运算符
        if origin.upper() in {"SELECT", "FROM", "LATERAL", "VIEW", "LEFT", "RIGHT", "INNER", "OUTER", "FULL", "JOIN",
                              "ON", "WHERE", "GROUP", "BY", "HAVING", "ORDER", "LIMIT", "UNION", "EXCEPT", "MINUS",
                              "INTERSECT", "AND", "NOT", "OR"}:
            self.stack[-1].append(AMTSingle(origin))
        elif origin.upper() in {"TRUE", "FALSE", "NULL"}:
            self.stack[-1].append(AMTSingle(origin, {AMTMark.LITERAL}))
        else:
            self.stack[-1].append(AMTSingle(origin, {AMTMark.NAME}))

    # ------------------------------ 自动机执行方法 ------------------------------
    def parse(self):
        """执行文本解析自动机"""
        idx = 0
        while idx < len(self.text):
            if self.handle_ch(self.text[idx]):
                idx += 1
        self.handle_ch(END)  # 处理结束标记

        if self.status != FSMStatus.END:
            raise AMTParseError(f"词法分析有限状态机，结束时状态异常: {self.status}")

        if len(self.stack) > 1:
            raise AMTParseError("词法分析有限状态机，解析到的 `(` 数量大于 `)`")

    def handle_ch(self, ch: str) -> bool:
        """处理一个字符；如果指针需要移动则返回 True，否则返回 False"""
        if self.status not in FSM_OPERATION_MAP:
            raise AMTParseError(f"未定义处理规则的状态: {self.status}")

        # 获取需要执行的行为
        operations = FSM_OPERATION_MAP[self.status]
        operate: FSMOperate = operations.get(ch, operations[DEFAULT])

        # 执行行为
        if operate.type == FSMOperateType.ADD_CACHE:
            self.cache.append(ch)
            self.status = operate.new_status
            return True
        if operate.type == FSMOperateType.HANDLE_CACHE:
            self.stack[-1].append(AMTSingle(self._cache_get_and_reset(), operate.marks))
            self.status = operate.new_status
            return False
        if operate.type == FSMOperateType.HANDLE_CACHE_WORD:
            self.cache_reset_and_handle()
            self.status = operate.new_status
            return False
        if operate.type == FSMOperateType.ADD_AND_HANDLE_CACHE:
            self.cache.append(ch)
            self.stack[-1].append(AMTSingle(self._cache_get_and_reset(), operate.marks))
            self.status = operate.new_status
            return True
        if operate.type == FSMOperateType.START_PARENTHESIS:
            self.stack.append([])
            return True
        if operate.type == FSMOperateType.END_PARENTHESIS:
            if len(self.stack) <= 1:
                raise AMTParseError("当前 ')' 数量大于 '('")
            tokens = self.stack.pop()
            self.stack[-1].append(AMTParenthesis(tokens, {AMTMark.PARENTHESIS}))
            return True
        if operate.type == FSMOperateType.SET_STATUS:
            self.status = operate.new_status
            return False
        if operate.type == FSMOperateType.RAISE:
            if ch == END:
                raise AMTParseError(f"当前状态={self.status.name}({self.status.value}) 出现非法结束符")
            raise AMTParseError(f"当前状态={self.status.name}({self.status.value}) 出现非法字符: {ch}")
        raise AMTParseError(f"未知状态行为: {operate.type}")

    def result(self):
        """获取自动机运行结果"""
        return self.stack[0]
