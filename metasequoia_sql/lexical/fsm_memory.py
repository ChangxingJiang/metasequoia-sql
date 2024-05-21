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
    stack : List[List[AMTBase]]
        当前已解析的节点树。使用多层栈维护，每一层栈表示一层插入语。
    status : FSMStatus
        状态机状态
    cache : List[str]
        当前正在缓存的词语
    """

    def __init__(self):
        self.stack: List[List[AMTBase]] = [[]]
        self.status: Union[FSMStatus, object] = FSMStatus.WAIT
        self.cache: List[str] = []

    def cache_get_and_reset(self) -> str:
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
        origin = self.cache_get_and_reset()
        # 逗号、分号、点号、等号、计算运算符（含通配符）、比较运算符、子句核心关键词、逻辑运算符
        if origin.upper() in {"SELECT", "FROM", "LATERAL", "VIEW", "LEFT", "RIGHT", "INNER", "OUTER", "FULL", "JOIN",
                              "ON", "WHERE", "GROUP", "BY", "HAVING", "ORDER", "LIMIT", "UNION", "EXCEPT", "MINUS",
                              "INTERSECT", "AND", "NOT", "OR"}:
            self.stack[-1].append(AMTSingle(origin))
        elif origin.upper() in {"TRUE", "FALSE", "NULL"}:
            self.stack[-1].append(AMTSingle(origin, AMTMark.LITERAL))
        else:
            self.stack[-1].append(AMTSingle(origin, AMTMark.NAME))
