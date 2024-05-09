"""
词法分析的有限状态机

TODO 增加各种元素在末尾的单元测试
"""

from typing import List, Union, Dict

from metasequoia_sql.common.basic import preproc_sql
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTBase, AMTMark, AMTSingle, AMTParenthesis, AMTSlice
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
    status : FSMStatus
        状态机状态
    cache : List[str]
        当前正在缓存的词语
    """

    def __init__(self, operation_map: Dict[FSMStatus, Dict[str, FSMOperate]] = None):
        """

        Parameters
        ----------
        operation_map : Dict[FSMStatus, Dict[str, FSMOperate]]
            状态行为映射表
        """
        if operation_map is None:
            operation_map = FSM_OPERATION_MAP
        self.operation_map = operation_map
        self.stack: List[List[AMTBase]] = [[]]
        self.status: Union[FSMStatus, object] = FSMStatus.WAIT
        self.cache: List[str] = []

    @classmethod
    def parse(cls, text: str) -> List[AMTBase]:
        """使用词法分析的有限状态机将 SQL 源代码解析为 AMT 抽象词法树

        Parameters
        ----------
        text : str
            SQL 源代码

        Returns
        -------
        amt_list : List[AMTBase]
            首层抽象词法树节点的列表
        """
        text = preproc_sql(text)
        fsm_machine = cls()

        idx = 0
        while idx < len(text):
            if fsm_machine.handle(text[idx]):
                idx += 1
        fsm_machine.handle(END)  # 处理结束标记

        if fsm_machine.status != FSMStatus.END:
            raise AMTParseError(f"词法分析有限状态机，结束时状态异常: {fsm_machine.status}")

        if len(fsm_machine.stack) > 1:
            raise AMTParseError("词法分析有限状态机，解析到的 `(` 数量大于 `)`")

        return fsm_machine.stack[0]

    # ------------------------------ 当前缓存词语的相关方法 ------------------------------

    def _cache_get_and_reset(self) -> str:
        """获取当前正在缓存的词语，并重置词语缓存"""
        result = "".join(self.cache)
        self.cache = []
        return result

    def _cache_reset_and_handle(self) -> None:
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

    def handle(self, ch: str) -> bool:
        # pylint: disable=R0912

        """处理一个字符；如果指针需要移动则返回 True，否则返回 False

        TODO 待增加两种插入语在栈中的标记
        TODO 待调整实现方法，优化 R0912
        """
        if self.status not in FSM_OPERATION_MAP:
            raise AMTParseError(f"未定义处理规则的状态: {self.status}")

        # 获取需要执行的行为
        operations = FSM_OPERATION_MAP[self.status]
        operate: FSMOperate = operations.get(ch, operations[DEFAULT])

        # 执行行为
        if operate.type == FSMOperateType.ADD_CACHE:
            self.cache.append(ch)
            self.status = operate.new_status
            need_move = True
        elif operate.type == FSMOperateType.HANDLE_CACHE:
            self.stack[-1].append(AMTSingle(self._cache_get_and_reset(), operate.marks))
            self.status = operate.new_status
            need_move = False
        elif operate.type == FSMOperateType.HANDLE_CACHE_WORD:
            self._cache_reset_and_handle()
            self.status = operate.new_status
            need_move = False
        elif operate.type == FSMOperateType.ADD_AND_HANDLE_CACHE:
            self.cache.append(ch)
            self.stack[-1].append(AMTSingle(self._cache_get_and_reset(), operate.marks))
            self.status = operate.new_status
            need_move = True
        elif operate.type == FSMOperateType.START_PARENTHESIS:
            self.stack.append([])
            need_move = True
        elif operate.type == FSMOperateType.END_PARENTHESIS:
            if len(self.stack) <= 1:
                raise AMTParseError("插入语结束标记数量大于开始标记数量")
            tokens = self.stack.pop()
            self.stack[-1].append(AMTParenthesis(tokens, {AMTMark.PARENTHESIS}))
            need_move = True
        elif operate.type == FSMOperateType.START_SLICE:
            self.stack.append([])
            need_move = True
        elif operate.type == FSMOperateType.END_SLICE:
            if len(self.stack) <= 1:
                raise AMTParseError("结束语结束标记数量大于开始标记数量")
            tokens = self.stack.pop()
            self.stack[-1].append(AMTSlice(tokens, {AMTMark.ARRAY_INDEX}))
            need_move = True
        elif operate.type == FSMOperateType.SET_STATUS:
            self.status = operate.new_status
            need_move = False
        elif operate.type == FSMOperateType.RAISE:
            if ch == END:
                raise AMTParseError(f"当前状态={self.status.name}({self.status.value}) 出现非法结束符")
            raise AMTParseError(f"当前状态={self.status.name}({self.status.value}) 出现非法字符: {ch}")
        else:
            raise AMTParseError(f"未知状态行为: {operate.type}")
        return need_move
