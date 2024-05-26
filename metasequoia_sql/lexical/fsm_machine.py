"""
词法分析的有限状态机

TODO 增加各种元素在末尾的单元测试
TODO 将过滤空格字符的逻辑添加到自动机参数中
"""

from typing import List, Dict, Optional

from metasequoia_sql.common.basic import preproc_sql
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTBase
from metasequoia_sql.lexical.fsm_memory import FSMMemory
from metasequoia_sql.lexical.fsm_operate import FSMOperate
from metasequoia_sql.lexical.fsm_operation_map import END, FSM_OPERATION_MAP, FSM_OPERATION_MAP_DEFAULT
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

    @staticmethod
    def parse(text: str) -> List[AMTBase]:
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
        memory = FSMMemory(text)  # 初始化自动机的缓存器
        fsm_machine = FSMMachine()  # 初始化自动机的执行器

        for ch in text:
            if not fsm_machine.handle(memory, ch):
                fsm_machine.handle(memory, ch)  # 如果第一次操作不会移动指针，那么第二次操作一定会移动
        fsm_machine.handle(memory, END)  # 处理结束标记：处理结束标记后不需要考虑指针是否移动

        if memory.status != FSMStatus.END:
            raise AMTParseError(f"词法分析有限状态机，结束时状态异常: {memory.status}")

        if len(memory.stack) > 1:
            raise AMTParseError("词法分析有限状态机，解析到的 `(` 数量大于 `)`")

        return memory.stack[0]

    def handle(self, memory: FSMMemory, ch: str) -> bool:
        """处理一个字符；如果指针需要移动则返回 True，否则返回 False"""
        # 获取需要执行的行为
        operate: Optional[FSMOperate] = FSM_OPERATION_MAP.get((memory.status, ch))

        if operate is None:
            operate = FSM_OPERATION_MAP_DEFAULT[memory.status]  # 如果没有则使用当前状态的默认处理规则

        # 执行处理方法：
        return operate.execute(memory, ch)
