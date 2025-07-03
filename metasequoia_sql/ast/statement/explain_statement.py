"""
EXPLAIN 语句（explain statement）
"""

from typing import Optional

from metasequoia_sql.ast.base import Node, Statement

__all__ = [
    "ExplainOptions",
    "ExplainStatement",
    "ExplainStatementForStatement",
    "ExplainStatementForConnection",
]


class ExplainOptions(Node):
    """【临时】EXPLAIN 语句选项"""

    __slots__ = (
        "_explain_format",
        "_is_analysis",
        "_explain_into"
    )

    def __init__(self,
                 explain_format: Optional[str] = None,
                 is_analysis: bool = False,
                 explain_into: Optional[str] = None
                 ):
        self._explain_format = explain_format
        self._is_analysis = is_analysis
        self._explain_into = explain_into

    @property
    def explain_format(self) -> Optional[str]:
        """
        解释格式

        Returns
        -------
        Optional[str]
            解释格式
        """
        return self._explain_format

    @property
    def is_analysis(self) -> bool:
        """
        是否进行分析

        Returns
        -------
        bool
            是否进行分析
        """
        return self._is_analysis

    @property
    def explain_into(self) -> Optional[str]:
        """
        解释结果输出位置

        Returns
        -------
        Optional[str]
            解释结果输出位置
        """
        return self._explain_into


class ExplainStatement(Statement):
    """EXPLAIN 语句"""

    __slots__ = (
        "_options",
    )

    def __init__(self, options: ExplainOptions):
        self._options = options

    @property
    def options(self) -> ExplainOptions:
        """
        解释选项

        Returns
        -------
        ExplainOptions
            解释选项
        """
        return self._options


class ExplainStatementForStatement(ExplainStatement):
    """用于解释语句的 EXPLAIN 语句"""

    __slots__ = (
        "_schema_name",
        "_statement"
    )

    def __init__(self, options: ExplainOptions, schema_name: Optional[str], statement: Statement):
        super().__init__(options)
        self._schema_name = schema_name
        self._statement = statement

    @property
    def schema_name(self) -> Optional[str]:
        """
        数据库名称

        Returns
        -------
        Optional[str]
            数据库名称
        """
        return self._schema_name

    @property
    def statement(self) -> Statement:
        """
        要解释的语句

        Returns
        -------
        Statement
            要解释的语句
        """
        return self._statement


class ExplainStatementForConnection(ExplainStatement):
    """用于解释连接的 EXPLAIN 语句"""

    __slots__ = (
        "_thread_id",
    )

    def __init__(self, options: ExplainOptions, thread_id: int):
        super().__init__(options)
        self._thread_id = thread_id

    @property
    def thread_id(self) -> int:
        """
        线程 ID

        Returns
        -------
        int
            线程 ID
        """
        return self._thread_id
