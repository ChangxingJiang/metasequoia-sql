class SqlParseError(Exception):
    """SQL解析失败的异常"""

    def __init__(self, reason: str):
        self.reason = reason


class AstParseError(SqlParseError):
    """AST 解析失败"""


class TokenIdxOutOfRangeError(SqlParseError):
    """尝试获取超过 Tokens 长度的抽象语法树节点的异常"""


class FullStatementCalledSource(Exception):
    """调用了 FullStatement 的 source 方法"""


class UnSupportDataSourceError(Exception):
    """数据源不支持的语法异常"""

    def __init__(self, reason: str):
        self.reason = reason


class ScannerError(Exception):
    """文本扫描异常"""