"""
词法分析的有限状态机的行为描述类
"""

import abc

from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTMark, AMTSingle, AMTParenthesis, AMTSlice
from metasequoia_sql.lexical.fsm_memory import FSMMemory
from metasequoia_sql.lexical.fsm_status import FSMStatus

__all__ = ["FSMOperate", "FSMOperate"]

END = "<end>"  # 结束标识符


class FSMOperate(abc.ABC):
    """词法分析的有限状态机的行为描述类"""

    @staticmethod
    def do_nothing_to(status: FSMStatus):
        """实例化 SET_STATUS 类型的行为"""
        return FSMOperateSetStatus(status=status)

    @staticmethod
    def add_cache_to(status: FSMStatus):
        """实例化 ADD_CACHE 类型的行为"""
        return FSMOperateAddCache(status=status)

    @staticmethod
    def handle_cache_to_wait(marks: int):
        """实例化 HANDLE_CACHE 类型的行为，并将状态置为 WAIT"""
        return FSMOperateHandleCacheToWait(marks=marks)

    @staticmethod
    def handle_cache_to_end(marks: int):
        """实例化 HANDLE_CACHE 类型的行为，并将状态置为 END"""
        return FSMOperateHandleCacheToEnd(marks=marks)

    @staticmethod
    def handle_cache_word_to_wait():
        """实例化 HANDLE_CACHE_WORD 类型的行为，并将状态置为 WAIT"""
        return FSMOperateHandleCacheWordToWait()

    @staticmethod
    def handle_cache_word_to_end():
        """实例化 HANDLE_CACHE_WORD 类型的行为，并将状态置为 END"""
        return FSMOperateHandleCacheWordToEnd()

    @staticmethod
    def add_and_handle_cache(marks: int):
        """实例化 ADD_AND_HANDLE_CACHE 类型的行为，并不更改状态"""
        return FSMOperateAddAndHandleCache(marks=marks)

    @staticmethod
    def add_and_handle_cache_to_wait(marks: int):
        """实例化 ADD_AND_HANDLE_CACHE 类型的行为，并将状态置为 WAIT"""
        return FSMOperateAddAndHandleCacheToWait(marks=marks)

    @staticmethod
    def start_parenthesis():
        """实例化 START_PARENTHESIS 类型的行为"""
        return FSMOperateStartParenthesis()

    @staticmethod
    def end_parenthesis():
        """实例化 END_PARENTHESIS 类型的行为"""
        return FSMOperateEndParenthesis()

    @staticmethod
    def start_slice():
        """实例化 START_SLICE 类型的行为"""
        return FSMOperateStartSlice()

    @staticmethod
    def end_slice():
        """实例化 END_SLICE 类型的行为"""
        return FSMOperateEndSlice()

    @staticmethod
    def raise_error():
        """实例化 RAISE 类型的行为"""
        return FSMOperateRaise()

    @abc.abstractmethod
    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""


class FSMOperateAddCache(FSMOperate):
    """【状态机操作】将当前字符添加到的缓冲区"""

    def __init__(self, status: FSMStatus):
        self.status = status  # 需要切换到状态机状态（仅抛出异常时不需要默认值）

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.cache.append(ch)
        memory.status = self.status
        return True


class FSMOperateSetStatus(FSMOperate):
    """【状态机操作】仅设置当前状态"""

    def __init__(self, status: FSMStatus):
        self.status = status  # 需要切换到状态机状态（仅抛出异常时不需要默认值）

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.status = self.status
        return False


class FSMOperateHandleCacheToWait(FSMOperate):
    """【状态机操作】根据缓冲区中的字符构造词法树节点，并指定词法树节点的标记，并将状态转换为 FSMStatus.WAIT"""

    def __init__(self, marks: int):
        self.marks = marks

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.stack[-1].append(AMTSingle(memory.cache_get_and_reset(), self.marks))
        memory.status = FSMStatus.WAIT
        return False


class FSMOperateHandleCacheToEnd(FSMOperate):
    """【状态机操作】根据缓冲区中的字符构造词法树节点，并指定词法树节点的标记，并将状态转换为 FSMStatus.END"""

    def __init__(self, marks: int):
        self.marks = marks

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.stack[-1].append(AMTSingle(memory.cache_get_and_reset(), self.marks))
        memory.status = FSMStatus.END
        return False


class FSMOperateHandleCacheWordToWait(FSMOperate):
    """【状态机操作】根据缓冲区中的字符构造词法树节点，并分析词法树节点中的标记（用于分析普通词语是否可能为名称或字面值），而后将状态置为 FSMStatus.WAIT"""

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.cache_reset_and_handle()
        memory.status = FSMStatus.WAIT
        return False


class FSMOperateHandleCacheWordToEnd(FSMOperate):
    """【状态机操作】根据缓冲区中的字符构造词法树节点，并分析词法树节点中的标记（用于分析普通词语是否可能为名称或字面值），而后将状态置为 FSMStatus.END"""

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.cache_reset_and_handle()
        memory.status = FSMStatus.END
        return False


class FSMOperateAddAndHandleCacheToWait(FSMOperate):
    """【状态机操作】将当前字符添加到的缓冲区，然后根据缓冲区中的字符构造词法树节点，然后将状态置为 FSMStatus.WAIT"""

    def __init__(self, marks: int):
        self.marks = marks

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.cache.append(ch)
        memory.stack[-1].append(AMTSingle(memory.cache_get_and_reset(), self.marks))
        memory.status = FSMStatus.WAIT
        return True


class FSMOperateAddAndHandleCache(FSMOperate):
    """【状态机操作】将当前字符添加到的缓冲区，然后根据缓冲区中的字符构造词法树节点，不更改状态"""

    def __init__(self, marks: int):
        self.marks = marks

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.cache.append(ch)
        memory.stack[-1].append(AMTSingle(memory.cache_get_and_reset(), self.marks))
        return True


class FSMOperateStartParenthesis(FSMOperate):
    """【状态机操作】处理当前字符位置的开括号"""

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.stack.append([])
        return True


class FSMOperateEndParenthesis(FSMOperate):
    """【状态机操作】处理当前字符位置的闭括号"""

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        if len(memory.stack) <= 1:
            raise AMTParseError("插入语结束标记数量大于开始标记数量")
        tokens = memory.stack.pop()
        memory.stack[-1].append(AMTParenthesis(tokens, AMTMark.PARENTHESIS))
        return True


class FSMOperateStartSlice(FSMOperate):
    """【状态机操作】处理当前字符位置的 [ 括号"""

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        memory.stack.append([])
        return True


class FSMOperateEndSlice(FSMOperate):
    """【状态机操作】处理当前字符位置的 [ 括号"""

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        if len(memory.stack) <= 1:
            raise AMTParseError("结束语结束标记数量大于开始标记数量")
        tokens = memory.stack.pop()
        memory.stack[-1].append(AMTSlice(tokens, AMTMark.ARRAY_INDEX))
        return True


class FSMOperateRaise(FSMOperate):
    """【状态机操作】抛出异常"""

    def execute(self, memory: FSMMemory, ch: str):
        """执行操作"""
        if ch == END:
            raise AMTParseError(f"当前状态={memory.status.name}({memory.status.value}) 出现非法结束符")
        raise AMTParseError(f"当前状态={memory.status.name}({memory.status.value}) 出现非法字符: {ch}")
