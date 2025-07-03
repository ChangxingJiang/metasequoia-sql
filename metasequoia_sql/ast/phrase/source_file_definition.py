"""
源文件定义（source file definition）
"""

from metasequoia_sql.ast.base import Node

__all__ = [
    "SourceFileDefinition",
    "SourceLogFileDefinition",
    "SourceLogPositionDefinition",
    "RelayLogFileDefinition",
    "RelayLogPositionDefinition",
]


class SourceFileDefinition(Node):
    """源文件定义"""


class SourceLogFileDefinition(SourceFileDefinition):
    """指定日志文件名称的源文件定义"""

    __slots__ = (
        "_file_name",
    )

    def __init__(self, file_name: str):
        self._file_name = file_name

    @property
    def file_name(self) -> str:
        """
        日志文件名称

        Returns
        -------
        str
            日志文件名称
        """
        return self._file_name


class SourceLogPositionDefinition(SourceFileDefinition):
    """指定日志文件位置的源文件定义"""

    __slots__ = (
        "_position",
    )

    def __init__(self, position: int):
        self._position = position

    @property
    def position(self) -> int:
        """
        日志文件位置

        Returns
        -------
        int
            日志文件位置
        """
        return self._position


class RelayLogFileDefinition(SourceFileDefinition):
    """指定日志文件名称的源文件定义"""

    __slots__ = (
        "_file_name",
    )

    def __init__(self, file_name: str):
        self._file_name = file_name

    @property
    def file_name(self) -> str:
        """
        中继日志文件名称

        Returns
        -------
        str
            中继日志文件名称
        """
        return self._file_name


class RelayLogPositionDefinition(SourceFileDefinition):
    """指定日志文件位置的源文件定义"""

    __slots__ = (
        "_position",
    )

    def __init__(self, position: int):
        self._position = position

    @property
    def position(self) -> int:
        """
        中继日志文件位置

        Returns
        -------
        int
            中继日志文件位置
        """
        return self._position
