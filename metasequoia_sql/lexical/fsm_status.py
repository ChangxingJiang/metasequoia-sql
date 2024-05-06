"""
词法分析的有限状态机的状态枚举类
"""

import enum

__all__ = ["FSMStatus"]


class FSMStatus(enum.Enum):
    """词法分析的有限状态机的状态枚举类

    其中，FSMStatus.value 为枚举类的含义，用于在抛出异常时显示
    """
    WAIT = "等待下一个词语"

    # 能够组成多字符组合的单字符之后
    AFTER_21 = "在 ! 符号之后"
    AFTER_2D = "在 - 符号之后"
    AFTER_2F = "在 / 符号之后"
    AFTER_3C = "在 < 符号之后"
    AFTER_3C_3D = "在 <= 符号之后"
    AFTER_3E = "在 > 符号之后"
    AFTER_7C = "在 | 符号之后"
    AFTER_0 = "在 0 之后"
    AFTER_B = "在 b 或 B 之后"
    AFTER_X = "在 x 或 X 之后"

    # 正在匹配特定类型的字符
    IN_HEX_LITERAL_OF_DOUBLE_QUOTE = "在十六机制字面值的双引号中"
    IN_HEX_LITERAL_OF_SINGLE_QUOTE = "在十六进制字面值的单引号中"
    IN_HEX_LITERAL_AFTER_0X = "在0x开头的十六进制字面值中"
    IN_BIT_LITERAL_OF_DOUBLE_QUOTE = "在二进制字面值的双引号中"
    IN_BIT_LITERAL_OF_SINGLE_QUOTE = "在二进制字面值的单引号中"
    IN_BIT_LITERAL_AFTER_0B = "在0b开头的位值字面值中"
    IN_INT = "在整型中"
    IN_FLOAT = "在浮点数中"
    IN_DOUBLE_QUOTE = "在双引号中"
    IN_DOUBLE_QUOTE_AFTER_22 = "在双引号中的、的 \" 符号之后"
    IN_DOUBLE_QUOTE_AFTER_5C = "在双引号中的 \\ 符号之后"
    IN_SINGLE_QUOTE = "在单引号中"
    IN_SINGLE_QUOTE_AFTER_27 = "在单引号中的、的 ' 符号之后"
    IN_SINGLE_QUOTE_AFTER_5C = "在单引号中的 \\ 符号之后"
    IN_BACK_QUOTE = "在反引号中"
    IN_EXPLAIN_1 = "在 # 或 -- 标记的单行注释中"
    IN_EXPLAIN_2 = "在多行注释中"
    IN_EXPLAIN_2_AFTER_2A = "在多行注释中的 * 符号之后"
    IN_WORD = "在普通词语中"

    # 匹配状态已结束
    END = "已结束"

    # 自定义状态，用于插件开发
    CUSTOM_1 = "自定义状态1"
    CUSTOM_2 = "自定义状态2"
    CUSTOM_3 = "自定义状态3"
    CUSTOM_4 = "自定义状态4"
    CUSTOM_5 = "自定义状态5"
    CUSTOM_6 = "自定义状态6"
    CUSTOM_7 = "自定义状态7"
    CUSTOM_8 = "自定义状态8"
    CUSTOM_9 = "自定义状态9"
    CUSTOM_10 = "自定义状态10"
