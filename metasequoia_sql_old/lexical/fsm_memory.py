"""
词法分析优先状态机的存储器
"""

import dataclasses
from typing import List, Union

from metasequoia_sql_old.lexical.amt_node import AMTBase
from metasequoia_sql_old.lexical.fsm_status import FSMStatus

__all__ = ["FSMMemory"]


@dataclasses.dataclass(slots=True)
class FSMMemory:
    """词法分析优先状态机的结构体"""

    text: str = dataclasses.field(init=True)  # 源代码字符串
    pos_start: int = dataclasses.field(init=False, default=0)  # 当前词语的开始位置
    pos_now: int = dataclasses.field(init=False, default=0)  # 当前位置
    stack: List[List[AMTBase]] = dataclasses.field(init=False, default_factory=lambda: [[]])  # 当前已解析的节点树：多层栈，每一层栈为一层插入语
    status: Union[FSMStatus, object] = dataclasses.field(init=False, default=FSMStatus.WAIT)  # 自动机状态
