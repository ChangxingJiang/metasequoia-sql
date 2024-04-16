"""
在 metasequoia_sql 中年可能抛出的异常
"""

__all__ = ["SqlParseError", "AstParseError", "UnSupportDataSourceError", "ScannerError", "AnalyzerError"]


class SqlParseError(Exception):
    """SQL解析失败的异常"""

    def __init__(self, reason: str):
        self.reason = reason


class AstParseError(SqlParseError):
    """AST 解析失败"""


class UnSupportDataSourceError(Exception):
    """数据源不支持的语法异常"""

    def __init__(self, reason: str):
        self.reason = reason


class ScannerError(Exception):
    """文本扫描异常"""


class AnalyzerError(Exception):
    """分析器异常"""
