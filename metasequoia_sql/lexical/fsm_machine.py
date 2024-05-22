"""
词法分析的有限状态机

TODO 增加各种元素在末尾的单元测试
TODO 将过滤空格字符的逻辑添加到自动机参数中
"""

from typing import List, Dict

from metasequoia_sql.common.basic import preproc_sql
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTBase
from metasequoia_sql.lexical.fsm_memory import FSMMemory
from metasequoia_sql.lexical.fsm_operate import FSMOperate
from metasequoia_sql.lexical.fsm_operation_map import END, DEFAULT, FSM_OPERATION_MAP
from metasequoia_sql.lexical.fsm_status import FSMStatus

__all__ = ["FSMMachine"]


class FSMMachine:
    """词法分析的有限状态机"""

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
        self.memory = FSMMemory()

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

        # 因为在 Python 中，遍历字符串的性能要远高于遍历下标后再用下标获取字符，所以优先使用遍历字符串的方法实现
        for ch in text:
            while not fsm_machine.handle(ch):
                pass  # 不断循环，直到处理方法返回需要移动指针为止
        fsm_machine.handle(END)  # 处理结束标记

        if fsm_machine.memory.status != FSMStatus.END:
            raise AMTParseError(f"词法分析有限状态机，结束时状态异常: {fsm_machine.memory.status}")

        if len(fsm_machine.memory.stack) > 1:
            raise AMTParseError("词法分析有限状态机，解析到的 `(` 数量大于 `)`")

        return fsm_machine.memory.stack[0]

    def handle(self, ch: str) -> bool:
        """处理一个字符；如果指针需要移动则返回 True，否则返回 False"""
        # 获取需要执行的行为
        operate: FSMOperate = FSM_OPERATION_MAP.get((self.memory.status, ch))

        if operate is None:
            operate = FSM_OPERATION_MAP[(self.memory.status, DEFAULT)]  # 如果没有则使用当前状态的默认处理规则

        # 执行行为
        return operate.execute(self.memory, ch)
