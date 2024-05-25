"""
词法分析优先状态机的存储器
"""

from typing import List, Union

from metasequoia_sql.lexical.amt_node import AMTBase, AMTMark, AMTSingle
from metasequoia_sql.lexical.fsm_status import FSMStatus

__all__ = ["FSMMemory"]


class FSMMemory:
    """词法分析优先状态机的存储器

    Attributes
    ----------
    text : str
        源代码字符串
    pos : int, default = 0
        当前词语的开始位置
    stack : List[List[AMTBase]]
        当前已解析的节点树。使用多层栈维护，每一层栈表示一层插入语。
    status : FSMStatus
        状态机状态
    """

    def __init__(self, text: str):
        self.text: str = text
        self.pos: int = 0
        self.stack: List[List[AMTBase]] = [[]]
        self.status: Union[FSMStatus, object] = FSMStatus.WAIT

    def cache_get_and_reset(self, idx: int) -> str:
        """获取当前正在缓存的词语，并重置词语缓存"""
        result = self.text[self.pos: idx]
        self.pos = idx
        return result
