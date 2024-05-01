"""
在 metasequoia_sql 中年可能抛出的异常
"""

__all__ = ["SqlParseError", "AMTParseError", "UnSupportDataSourceError", "ScannerError", "AnalyzerError"]


class SqlParseError(Exception):
    """SQL解析失败的异常"""

    def __init__(self, reason: str):
        self.reason = reason


class AMTParseError(SqlParseError):
    """抽象词法树 AMT 解析失败"""


class UnSupportDataSourceError(Exception):
    """数据源不支持的语法异常"""

    def __init__(self, reason: str):
        self.reason = reason


class ScannerError(Exception):
    """文本扫描异常"""


class AnalyzerError(Exception):
    """分析器异常"""
