"""
水杉 SQL 抛出的异常包括如下两个基类：

- SQL 解析器异常
- SQL 分析器异常
"""

__all__ = [
    # SQL 解析器异常
    "SqlParseError",  # SQL 解析异常
    "LexicalParseError",  # 词法解析异常
    "NotSupportError",  # 不支持的 SQL 类型异常

    # SQL 分析器异常
    "AnalyzerError",
]


class SqlParseError(Exception):
    """SQL 解析异常"""


class LexicalParseError(SqlParseError):
    """词法解析异常"""


class NotSupportError(SqlParseError):
    """不支持的 SQL 类型异常"""


class AnalyzerError(Exception):
    """分析器异常"""
