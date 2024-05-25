"""
在 metasequoia_sql 中年可能抛出的异常
"""

__all__ = ["SqlParseError", "AMTParseError", "UnSupportSqlTypeError", "ScannerError", "AnalyzerError",
           "ScannerNotMatchError"]


class SqlParseError(Exception):
    """SQL解析失败的异常"""

    def __init__(self, reason: str):
        self.reason = reason


class AMTParseError(SqlParseError):
    """抽象词法树 AMT 解析失败"""


class UnSupportSqlTypeError(Exception):
    """数据源不支持的语法异常"""

    def __init__(self, reason: str):
        self.reason = reason


class ScannerError(Exception):
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
