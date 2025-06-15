"""
RESET 语句（reset statement）
"""

from typing import Optional, TYPE_CHECKING, List

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "ResetOption",
    "ResetSlaveOption",
    "ResetReplicaOption",
    "ResetMasterOption",
    "ResetStatement",
    "ResetOptionsStatement",
    "ResetPersistStatement",
]


class ResetOption(Statement):
    """RESET 选项的抽象语法树节点基类"""


class ResetSlaveOption(ResetOption):
    """
    RESET SLAVE 选项的抽象语法树节点。
    
    语法规则：
        SLAVE [ALL] [FOR CHANNEL channel_name]
    """

    __slots__ = (
        "_all",
        "_channel_name",
    )

    def __init__(self, all_flag: bool, channel_name: Optional[str]):
        """
        初始化 RESET SLAVE 选项节点。

        Parameters
        ----------
        all_flag : bool
            是否包含 ALL 选项
        channel_name : Optional[str]
            可选的通道名称
        """
        self._all = all_flag
        self._channel_name = channel_name

    @property
    def all_flag(self) -> bool:
        """
        获取是否包含 ALL 选项。

        Returns
        -------
        bool
            是否包含 ALL 选项
        """
        return self._all

    @property
    def channel_name(self) -> Optional[str]:
        """
        获取通道名称。

        Returns
        -------
        Optional[str]
            通道名称
        """
        return self._channel_name


class ResetReplicaOption(ResetOption):
    """
    RESET REPLICA 选项的抽象语法树节点。
    
    语法规则：
        REPLICA [ALL] [FOR CHANNEL channel_name]
    """

    __slots__ = (
        "_all",
        "_channel_name",
    )

    def __init__(self, all_flag: bool, channel_name: Optional[str]):
        """
        初始化 RESET REPLICA 选项节点。

        Parameters
        ----------
        all_flag : bool
            是否包含 ALL 选项
        channel_name : Optional[str]
            可选的通道名称
        """
        self._all = all_flag
        self._channel_name = channel_name

    @property
    def all_flag(self) -> bool:
        """
        获取是否包含 ALL 选项。

        Returns
        -------
        bool
            是否包含 ALL 选项
        """
        return self._all

    @property
    def channel_name(self) -> Optional[str]:
        """
        获取通道名称。

        Returns
        -------
        Optional[str]
            通道名称
        """
        return self._channel_name


class ResetMasterOption(ResetOption):
    """
    RESET MASTER/BINARY LOGS AND GTIDS 选项的抽象语法树节点。
    
    语法规则：
        (MASTER | BINARY LOGS AND GTIDS) [TO binlog_file_number]
    """

    __slots__ = (
        "_binlog_file_number",
    )

    def __init__(self, binlog_file_number: Optional[int]):
        """
        初始化 RESET MASTER 选项节点。

        Parameters
        ----------
        binlog_file_number : Optional[int]
            可选的二进制日志文件编号
        """
        self._binlog_file_number = binlog_file_number

    @property
    def binlog_file_number(self) -> Optional[int]:
        """
        获取二进制日志文件编号。

        Returns
        -------
        Optional[int]
            二进制日志文件编号
        """
        return self._binlog_file_number


class ResetStatement(Statement):
    """RESET 语句的抽象语法树节点基类"""


class ResetOptionsStatement(ResetStatement):
    """
    RESET 选项语句的抽象语法树节点。

    语法规则：
        RESET reset_options
    """

    __slots__ = (
        "_options",
    )

    def __init__(self, options: List[ResetOption]):
        """
        初始化 RESET 选项语句节点。

        Parameters
        ----------
        options : List[ResetOption]
            RESET 选项列表
        """
        self._options = options

    @property
    def options(self) -> List[ResetOption]:
        """
        获取 RESET 选项列表。

        Returns
        -------
        List[ResetOption]
            RESET 选项列表
        """
        return self._options


class ResetPersistStatement(ResetStatement):
    """
    RESET PERSIST 语句的抽象语法树节点。

    语法规则：
        RESET PERSIST [IF EXISTS] [identifier]
    """

    __slots__ = (
        "_if_exists",
        "_identifier",
    )

    def __init__(self, if_exists: bool, identifier: Optional["Identifier"]):
        """
        初始化 RESET PERSIST 语句节点。

        Parameters
        ----------
        if_exists : bool
            是否包含 IF EXISTS 子句
        identifier : Optional[Identifier]
            可选的持久化变量标识符
        """
        self._if_exists = if_exists
        self._identifier = identifier

    @property
    def if_exists(self) -> bool:
        """
        获取是否包含 IF EXISTS 子句。

        Returns
        -------
        bool
            是否包含 IF EXISTS 子句
        """
        return self._if_exists

    @property
    def identifier(self) -> Optional["Identifier"]:
        """
        获取持久化变量标识符。

        Returns
        -------
        Optional[Identifier]
            持久化变量标识符
        """
        return self._identifier
