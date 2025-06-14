"""
二进制日志语句的抽象语法树节点。
"""

from metasequoia_sql.ast.base import Statement

__all__ = [
    "BinlogStatement"
]

class BinlogStatement(Statement):
    """
    二进制日志语句的抽象语法树节点。

    语法规则：
        BINLOG base64_event_string
    """

    __slots__ = (
        "_event_string"
    )

    def __init__(self, event_string: str) -> None:
        """
        初始化二进制日志语句节点。

        Parameters
        ----------
        event_string: str
            Base64 编码的二进制日志事件字符串
        """
        self._event_string = event_string

    @property
    def event_string(self) -> str:
        """
        获取二进制日志事件字符串。
        Returns
        -------
        str
            Base64 编码的二进制日志事件字符串
        """
        return self._event_string
