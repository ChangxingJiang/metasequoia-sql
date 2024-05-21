"""
词法分析有限状态机，针对不同状态、不同输入值的行为映射表
"""

from typing import Dict

from metasequoia_sql.common import char_set
from metasequoia_sql.errors import AMTParseError
from metasequoia_sql.lexical.amt_node import AMTMark
from metasequoia_sql.lexical.fsm_operate import FSMOperate, FSMOperateBase
from metasequoia_sql.lexical.fsm_status import FSMStatus

__all__ = ["END", "DEFAULT", "FSM_OPERATION_MAP"]

END = "<end>"  # 结束标识符
DEFAULT = "<default>"  # 默认标识符

# 行为映射表设置表（用于设置配置信息，输入参数允许是一个不可变集合）
FSM_OPERATION_MAP_SOURCE = {
    # 等待下一个词语
    FSMStatus.WAIT: {
        "!": FSMOperate.add_cache(new_status=FSMStatus.AFTER_21),
        "&": FSMOperate.add_cache(new_status=FSMStatus.AFTER_26),
        "-": FSMOperate.add_cache(new_status=FSMStatus.AFTER_2D),
        "/": FSMOperate.add_cache(new_status=FSMStatus.AFTER_2F),
        "<": FSMOperate.add_cache(new_status=FSMStatus.AFTER_3C),
        ">": FSMOperate.add_cache(new_status=FSMStatus.AFTER_3E),
        "|": FSMOperate.add_cache(new_status=FSMStatus.AFTER_7C),
        "0": FSMOperate.add_cache(new_status=FSMStatus.AFTER_0),
        frozenset({" ", "\n"}): FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.SPACE),
        "~": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),
        "*": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),
        "^": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),
        frozenset({",", ";", "=", "+", ".", "%"}): FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),
        "\"": FSMOperate.add_cache(new_status=FSMStatus.IN_DOUBLE_QUOTE),
        "'": FSMOperate.add_cache(new_status=FSMStatus.IN_SINGLE_QUOTE),
        "`": FSMOperate.add_cache(new_status=FSMStatus.IN_BACK_QUOTE),
        "#": FSMOperate.add_cache(new_status=FSMStatus.IN_EXPLAIN_1),
        frozenset({"b", "B"}): FSMOperate.add_cache(new_status=FSMStatus.AFTER_B),
        frozenset({"x", "X"}): FSMOperate.add_cache(new_status=FSMStatus.AFTER_X),
        char_set.NUMBER: FSMOperate.add_cache(new_status=FSMStatus.IN_INT),
        "(": FSMOperate.start_parenthesis(),
        ")": FSMOperate.end_parenthesis(),
        "[": FSMOperate.start_slice(),
        "]": FSMOperate.end_slice(),
        END: FSMOperate.set_status(FSMStatus.END),
        DEFAULT: FSMOperate.add_cache(FSMStatus.IN_WORD)
    },

    # 在 ! 符号之后
    FSMStatus.AFTER_21: {
        "=": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：!=
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：!
    },

    # 在 & 符号之后
    FSMStatus.AFTER_26: {
        "&": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：&&
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：&
    },

    # 在 - 符号之后
    FSMStatus.AFTER_2D: {
        "-": FSMOperate.add_cache(new_status=FSMStatus.IN_EXPLAIN_1),  # 符号：--
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE)
    },

    # 在 / 符号之后
    FSMStatus.AFTER_2F: {
        "*": FSMOperate.add_cache(new_status=FSMStatus.IN_EXPLAIN_2),  # 符号：/*
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE)
    },

    # 在 < 符号之后
    FSMStatus.AFTER_3C: {
        "=": FSMOperate.add_cache(new_status=FSMStatus.AFTER_3C_3D),  # 符号：<=
        ">": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：<>
        "<": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：<<
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE)  # 符号：<
    },

    # 在 < 符号之后
    FSMStatus.AFTER_3C_3D: {
        ">": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：<=>
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE)  # 符号：<=
    },

    # 在 > 符号之后
    FSMStatus.AFTER_3E: {
        "=": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：>=
        ">": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：>>
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE)  # 符号：>
    },

    # 在 | 符号之后
    FSMStatus.AFTER_7C: {
        "|": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：||
        char_set.END_TOKEN: FSMOperate.handle_cache_to_wait(marks=AMTMark.NONE),  # 符号：|
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在 0 之后
    FSMStatus.AFTER_0: {
        "x": FSMOperate.add_cache(new_status=FSMStatus.IN_HEX_LITERAL_AFTER_0X),  # "0x" 开头的十六进制字面值
        "b": FSMOperate.add_cache(new_status=FSMStatus.IN_BIT_LITERAL_AFTER_0B),  # "0b" 开头的位值字面值
        ".": FSMOperate.add_cache(new_status=FSMStatus.IN_FLOAT),  # "0." 开头的浮点数
        char_set.NUMBER: FSMOperate.add_cache(new_status=FSMStatus.IN_INT),  # "0+整数" 开头的整数
        char_set.END_TOKEN: FSMOperate.handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_INT),  # 0
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.LITERAL | AMTMark.LITERAL_INT),  # 0
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_WORD)
    },

    # 在 b 或 B 之后
    FSMStatus.AFTER_B: {
        "\"": FSMOperate.add_cache(new_status=FSMStatus.IN_BIT_LITERAL_OF_DOUBLE_QUOTE),  # 位值字面值
        "'": FSMOperate.add_cache(new_status=FSMStatus.IN_BIT_LITERAL_OF_SINGLE_QUOTE),  # 位值字面值
        ".": FSMOperate.handle_cache_word_to_wait(),
        char_set.END_TOKEN_WITHOUT_QUOTE: FSMOperate.handle_cache_to_wait(marks=AMTMark.NAME),  # b 或 B
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.NAME),  # b 或 B
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_WORD)
    },

    # 在 x 或 X 之后
    FSMStatus.AFTER_X: {
        "\"": FSMOperate.add_cache(new_status=FSMStatus.IN_HEX_LITERAL_OF_DOUBLE_QUOTE),  # 十六进制字面值
        "'": FSMOperate.add_cache(new_status=FSMStatus.IN_HEX_LITERAL_OF_SINGLE_QUOTE),  # 十六进制字面值
        ".": FSMOperate.handle_cache_word_to_wait(),
        char_set.END_TOKEN_WITHOUT_QUOTE: FSMOperate.handle_cache_to_wait(marks=AMTMark.NAME),  # x 或 X
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.NAME),  # x 或 X
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_WORD)
    },

    # 在十六机制字面值的双引号中
    FSMStatus.IN_HEX_LITERAL_OF_DOUBLE_QUOTE: {
        "\"": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_HEX),
        char_set.HEX_LITERAL: FSMOperate.add_cache(new_status=FSMStatus.IN_HEX_LITERAL_OF_DOUBLE_QUOTE),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在十六进制字面值的单引号中
    FSMStatus.IN_HEX_LITERAL_OF_SINGLE_QUOTE: {
        "'": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_HEX),
        char_set.HEX_LITERAL: FSMOperate.add_cache(new_status=FSMStatus.IN_HEX_LITERAL_OF_SINGLE_QUOTE),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在 0x 开头的十六进制字面值中，例如：0x2F
    FSMStatus.IN_HEX_LITERAL_AFTER_0X: {
        char_set.HEX_LITERAL: FSMOperate.add_cache(new_status=FSMStatus.IN_HEX_LITERAL_AFTER_0X),
        char_set.END_TOKEN: FSMOperate.handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_HEX),
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.LITERAL | AMTMark.LITERAL_HEX),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在二进制字面值的双引号中
    FSMStatus.IN_BIT_LITERAL_OF_DOUBLE_QUOTE: {
        "\"": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_BIT),
        char_set.BIT_LITERAL: FSMOperate.add_cache(new_status=FSMStatus.IN_BIT_LITERAL_OF_DOUBLE_QUOTE),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在二进制字面值的单引号中
    FSMStatus.IN_BIT_LITERAL_OF_SINGLE_QUOTE: {
        "'": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_BIT),
        char_set.BIT_LITERAL: FSMOperate.add_cache(new_status=FSMStatus.IN_BIT_LITERAL_OF_SINGLE_QUOTE),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在 0b 开头的位值字面值中，例如：0b01
    FSMStatus.IN_BIT_LITERAL_AFTER_0B: {
        char_set.BIT_LITERAL: FSMOperate.add_cache(new_status=FSMStatus.IN_BIT_LITERAL_AFTER_0B),
        char_set.END_TOKEN: FSMOperate.handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_BIT),
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.LITERAL | AMTMark.LITERAL_BIT),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在整型中，例如：25
    FSMStatus.IN_INT: {
        ".": FSMOperate.add_cache(new_status=FSMStatus.IN_FLOAT),
        char_set.NUMBER: FSMOperate.add_cache(new_status=FSMStatus.IN_INT),
        char_set.END_TOKEN: FSMOperate.handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_INT),
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.LITERAL | AMTMark.LITERAL_INT),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_WORD),
    },

    # 在浮点数中
    FSMStatus.IN_FLOAT: {
        char_set.NUMBER: FSMOperate.add_cache(new_status=FSMStatus.IN_FLOAT),
        char_set.END_TOKEN: FSMOperate.handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.LITERAL_FLOAT),
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.LITERAL | AMTMark.LITERAL_FLOAT),
        DEFAULT: FSMOperate.raise_error()
    },

    # 在双引号中
    FSMStatus.IN_DOUBLE_QUOTE: {
        "\\": FSMOperate.add_cache(new_status=FSMStatus.IN_DOUBLE_QUOTE_AFTER_5C),
        "\"": FSMOperate.add_cache(new_status=FSMStatus.IN_DOUBLE_QUOTE_AFTER_22),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_DOUBLE_QUOTE)
    },

    # 在双引号中的、的 \" 符号之后
    FSMStatus.IN_DOUBLE_QUOTE_AFTER_22: {
        "\"": FSMOperate.add_cache(new_status=FSMStatus.IN_DOUBLE_QUOTE),
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.LITERAL | AMTMark.NAME),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.NAME)
    },

    # 在双引号中的 \\ 符号之后
    FSMStatus.IN_DOUBLE_QUOTE_AFTER_5C: {
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.add_cache(FSMStatus.IN_DOUBLE_QUOTE)
    },

    # 在单引号中
    FSMStatus.IN_SINGLE_QUOTE: {
        "\\": FSMOperate.add_cache(new_status=FSMStatus.IN_SINGLE_QUOTE_AFTER_5C),
        "'": FSMOperate.add_cache(new_status=FSMStatus.IN_SINGLE_QUOTE_AFTER_27),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_SINGLE_QUOTE)
    },

    # 在单引号中的、的 ' 符号之后
    FSMStatus.IN_SINGLE_QUOTE_AFTER_27: {
        "'": FSMOperate.add_cache(new_status=FSMStatus.IN_SINGLE_QUOTE),
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.LITERAL | AMTMark.NAME),
        DEFAULT: FSMOperate.handle_cache_to_wait(marks=AMTMark.LITERAL | AMTMark.NAME)
    },

    # 在单引号中的 \\ 符号之后
    FSMStatus.IN_SINGLE_QUOTE_AFTER_5C: {
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_SINGLE_QUOTE)
    },

    # 在反引号中
    FSMStatus.IN_BACK_QUOTE: {
        "`": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NAME),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_BACK_QUOTE)
    },

    # 在 # 或 -- 标记的单行注释中
    FSMStatus.IN_EXPLAIN_1: {
        "\n": FSMOperate.handle_cache_to_wait(marks=AMTMark.COMMENT),
        END: FSMOperate.handle_cache_to_end(marks=AMTMark.COMMENT),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_EXPLAIN_1)
    },

    # 在多行注释中
    FSMStatus.IN_EXPLAIN_2: {
        "*": FSMOperate.add_cache(FSMStatus.IN_EXPLAIN_2_AFTER_2A),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.add_cache(FSMStatus.IN_EXPLAIN_2)
    },

    # 在多行注释中的 * 符号之后
    FSMStatus.IN_EXPLAIN_2_AFTER_2A: {
        "/": FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.COMMENT),
        END: FSMOperate.raise_error(),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_EXPLAIN_2)
    },

    # 在普通词语中
    FSMStatus.IN_WORD: {
        ".": FSMOperate.handle_cache_word_to_wait(),
        char_set.END_TOKEN: FSMOperate.handle_cache_word_to_wait(),
        END: FSMOperate.handle_cache_word_to_end(),
        DEFAULT: FSMOperate.add_cache(new_status=FSMStatus.IN_WORD)
    }
}

# 状态行为映射表（用于用时行为映射信息，输入参数必须是一个字符）
FSM_OPERATION_MAP: Dict[FSMStatus, Dict[str, FSMOperateBase]] = {}
for status, operation_map in FSM_OPERATION_MAP_SOURCE.items():
    FSM_OPERATION_MAP[status] = {}
    for ch_or_set, fsm_operation in operation_map.items():
        if isinstance(ch_or_set, str):
            FSM_OPERATION_MAP[status][ch_or_set] = fsm_operation
        elif isinstance(ch_or_set, frozenset):
            for ch in ch_or_set:
                FSM_OPERATION_MAP[status][ch] = fsm_operation
        else:
            raise AMTParseError("非法的行为映射表设置表")
