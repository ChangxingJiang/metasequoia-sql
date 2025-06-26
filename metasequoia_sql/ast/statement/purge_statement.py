"""
PURGE 语句（purge statement）
"""

from metasequoia_sql.ast.base import Expression, Node, Statement

__all__ = [
    "PurgeOption",
    "PurgeToOption",
    "PurgeBeforeOption",
    "PurgeStatement",
]


class PurgeOption(Node):
    """PURGE 选项基类"""


class PurgeToOption(PurgeOption):
    """PURGE TO 选项"""

    __slots__ = (
        "_log_file",
    )

    def __init__(self, log_file: str):
        self._log_file = log_file

    @property
    def log_file(self) -> str:
        """
        日志文件

        Returns
        -------
        str
            日志文件
        """
        return self._log_file


class PurgeBeforeOption(PurgeOption):
    """PURGE BEFORE 选项"""

    __slots__ = (
        "_before_expression",
    )

    def __init__(self, before_expression: Expression):
        self._before_expression = before_expression

    @property
    def before_expression(self) -> Expression:
        """
        BEFORE 表达式

        Returns
        -------
        Expression
            BEFORE 表达式
        """
        return self._before_expression


class PurgeStatement(Statement):
    """PURGE 语句"""

    __slots__ = (
        "_purge_option",
    )

    def __init__(self, purge_option: PurgeOption):
        self._purge_option = purge_option

    @property
    def purge_option(self) -> PurgeOption:
        """
        清除选项

        Returns
        -------
        PurgeOption
            清除选项
        """
        return self._purge_option
