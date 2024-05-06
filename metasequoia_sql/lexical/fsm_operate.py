"""
词法分析的有限状态机的行为描述类
"""

import dataclasses
import enum
from typing import Set, Optional

from metasequoia_sql.lexical.amt_node import AMTMark
from metasequoia_sql.lexical.fsm_status import FSMStatus

__all__ = ["FSMOperateType", "FSMOperate"]


class FSMOperateType(enum.Enum):
    """词法分析的有限状态机的行为描述类的行为类型"""

    SET_STATUS = enum.auto()  # 仅设置当前状态
    ADD_CACHE = enum.auto()  # 将当前字符添加到的缓冲区
    HANDLE_CACHE = enum.auto()  # 根据缓冲区中的字符构造词法树节点，并指定词法树节点的标记
    HANDLE_CACHE_WORD = enum.auto()  # 根据缓冲区中的字符构造词法树节点，并分析词法树节点中的标记（用于分析普通词语是否可能为名称或字面值）
    ADD_AND_HANDLE_CACHE = enum.auto()  # 将当前字符添加到的缓冲区，然后根据缓冲区中的字符构造词法树节点
    START_PARENTHESIS = enum.auto()  # 处理当前字符位置的开括号
    END_PARENTHESIS = enum.auto()  # 处理当前字符位置的闭括号
    START_SLICE = enum.auto()  # 处理当前位置的 [ 符号
    END_SLICE = enum.auto()  # 处理当前位置的 ] 符号
    RAISE = enum.auto()  # 抛出异常


@dataclasses.dataclass(slots=True, frozen=True)
class FSMOperate:
    """词法分析的有限状态机的行为描述类"""

    type: FSMOperateType = dataclasses.field(kw_only=True)  # 有限状态机的行为类型
    marks: Optional[Set[AMTMark]] = dataclasses.field(kw_only=True, default=None)  # 构造的词法树节点的标记
    new_status: FSMStatus = dataclasses.field(kw_only=True, default=None)  # 需要切换到状态机状态（仅抛出异常时不需要默认值）

    @staticmethod
    def set_status(new_status: FSMStatus):
        """实例化 SET_STATUS 类型的行为"""
        return FSMOperate(type=FSMOperateType.SET_STATUS, new_status=new_status)

    @staticmethod
    def add_cache(new_status: FSMStatus):
        """实例化 ADD_CACHE 类型的行为"""
        return FSMOperate(type=FSMOperateType.ADD_CACHE, new_status=new_status)

    @staticmethod
    def handle_cache_to_wait(marks: Set[AMTMark]):
        """实例化 HANDLE_CACHE 类型的行为，并将状态置为 WAIT"""
        return FSMOperate(type=FSMOperateType.HANDLE_CACHE, marks=marks, new_status=FSMStatus.WAIT)

    @staticmethod
    def handle_cache_to_end(marks: Set[AMTMark]):
        """实例化 HANDLE_CACHE 类型的行为，并将状态置为 END"""
        return FSMOperate(type=FSMOperateType.HANDLE_CACHE, marks=marks, new_status=FSMStatus.END)

    @staticmethod
    def handle_cache_word_to_wait():
        """实例化 HANDLE_CACHE_WORD 类型的行为，并将状态置为 WAIT"""
        return FSMOperate(type=FSMOperateType.HANDLE_CACHE_WORD, new_status=FSMStatus.WAIT)

    @staticmethod
    def handle_cache_word_to_end():
        """实例化 HANDLE_CACHE_WORD 类型的行为，并将状态置为 END"""
        return FSMOperate(type=FSMOperateType.HANDLE_CACHE_WORD, new_status=FSMStatus.END)

    @staticmethod
    def add_and_handle_cache_to_wait(marks: Set[AMTMark]):
        """实例化 ADD_AND_HANDLE_CACHE 类型的行为，并将状态置为 WAIT"""
        return FSMOperate(type=FSMOperateType.ADD_AND_HANDLE_CACHE, marks=marks, new_status=FSMStatus.WAIT)

    @staticmethod
    def raise_error():
        """实例化 RAISE 类型的行为"""
        return FSMOperate(type=FSMOperateType.RAISE)

    @staticmethod
    def start_parenthesis():
        """实例化 START_PARENTHESIS 类型的行为"""
        return FSMOperate(type=FSMOperateType.START_PARENTHESIS)

    @staticmethod
    def end_parenthesis():
        """实例化 END_PARENTHESIS 类型的行为"""
        return FSMOperate(type=FSMOperateType.END_PARENTHESIS)

    @staticmethod
    def start_slice():
        """实例化 START_SLICE 类型的行为"""
        return FSMOperate(type=FSMOperateType.START_SLICE)

    @staticmethod
    def end_slice():
        """实例化 END_SLICE 类型的行为"""
        return FSMOperate(type=FSMOperateType.END_SLICE)
