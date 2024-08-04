"""
水杉 SQL 抛出的异常包括如下两个基类：

- SQL 解析器异常
- SQL 分析器异常
"""

__all__ = [
    # SQL 解析器异常
    "SqlParseError",
    "LexicalParseError",
    "UnSupportSqlTypeError",
    "ScannerError",
    "ScannerNotMatchError",

    # SQL 分析器异常
    "AnalyzerError",
]


class SqlParseError(Exception):
    """SQL解析失败的异常"""

    def __init__(self, reason: str):
        self.reason = reason


class LexicalParseError(SqlParseError):
    """词法解析异常"""


class UnSupportSqlTypeError(SqlParseError):
    """不支持的数据源异常"""


class ScannerError(SqlParseError):
    """文本扫描异常"""


class ScannerNotMatchError(ScannerError):
    """执行 scanner.match 方法时无法匹配的异常"""

    def __init__(self, token, tokens, scanner):
        self._token = token
        self._tokens = tokens
        self._scanner = scanner

    def guess_reason(self):
        """推测 match 匹配异常原因"""
        if self._token == "ON":
            return "尝试匹配 ON 关联表达式，但没有匹配到关键字 ON"
        return "其他原因"

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (f"没有匹配到目标词语: 尝试匹配短语:{self._tokens}, 匹配失败短语:{self._token}, "
                f"当前位置:{self._scanner.get_recent_source()}, "
                f"推测原因:{self.guess_reason()}")


class AnalyzerError(Exception):
    """分析器异常"""
