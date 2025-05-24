"""
词法分析的有限状态机的状态枚举类
"""

import enum

__all__ = ["FSMStatus"]


class FSMStatus(enum.IntEnum):
    """词法分析的有限状态机的状态枚举类

    其中，FSMStatus.value 为枚举类的含义，用于在抛出异常时显示
    """
    WAIT = 0  # 等待下一个词语

    # 能够组成多字符组合的单字符之后
    AFTER_21 = 11  # 在 ! 符号之后
    AFTER_26 = 12  # 在 & 符号之后
    AFTER_2D = 13  # 在 - 符号之后
    AFTER_2F = 14  # 在 / 符号之后
    AFTER_3C = 15  # 在 < 符号之后
    AFTER_3C_3D = 16  # 在 <= 符号之后
    AFTER_3E = 17  # 在 > 符号之后
    AFTER_7C = 18  # 在 | 符号之后
    AFTER_0 = 19  # 在 0 之后
    AFTER_B = 20  # 在 b 或 B 之后
    AFTER_X = 21  # 在 x 或 X 之后

    # 正在匹配特定类型的字符
    IN_HEX_LITERAL_OF_DOUBLE_QUOTE = 41  # 在十六机制字面值的双引号中
    IN_HEX_LITERAL_OF_SINGLE_QUOTE = 42  # 在十六进制字面值的单引号中
    IN_HEX_LITERAL_AFTER_0X = 43  # 在0x开头的十六进制字面值中
    IN_BIT_LITERAL_OF_DOUBLE_QUOTE = 44  # 在二进制字面值的双引号中
    IN_BIT_LITERAL_OF_SINGLE_QUOTE = 45  # 在二进制字面值的单引号中
    IN_BIT_LITERAL_AFTER_0B = 46  # 在0b开头的位值字面值中
    IN_INT = 47  # 在整型中
    IN_FLOAT = 48  # 在浮点数中
    IN_DOUBLE_QUOTE = 49  # 在双引号中
    IN_DOUBLE_QUOTE_AFTER_22 = 50  # 在双引号中的、的 \ 符号之后
    IN_DOUBLE_QUOTE_AFTER_5C = 51  # 在双引号中的 \\ 符号之后
    IN_SINGLE_QUOTE = 52  # 在单引号中
    IN_SINGLE_QUOTE_AFTER_27 = 53  # 在单引号中的、的 ' 符号之后
    IN_SINGLE_QUOTE_AFTER_5C = 54  # 在单引号中的 \\ 符号之后
    IN_BACK_QUOTE = 55  # 在反引号中
    IN_EXPLAIN_1 = 56  # 在 # 或 -- 标记的单行注释中
    IN_EXPLAIN_2 = 57  # 在多行注释中
    IN_EXPLAIN_2_AFTER_2A = 58  # 在多行注释中的 * 符号之后
    IN_WORD = 59  # 在普通词语中

    # 匹配状态已结束
    END = 255  # 已结束

    # 自定义状态，用于插件开发
    CUSTOM_1 = 201  # 自定义状态 1
    CUSTOM_2 = 202  # 自定义状态 2
    CUSTOM_3 = 203  # 自定义状态 3
    CUSTOM_4 = 204  # 自定义状态 4
    CUSTOM_5 = 205  # 自定义状态 5
    CUSTOM_6 = 206  # 自定义状态 6
    CUSTOM_7 = 207  # 自定义状态 7
    CUSTOM_8 = 208  # 自定义状态 8
    CUSTOM_9 = 209  # 自定义状态 9
    CUSTOM_10 = 210  # 自定义状态 10
