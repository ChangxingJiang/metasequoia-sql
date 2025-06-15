"""
XA 事务语句（XA statement）
"""

from enum import IntEnum
from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumXaJoinOrResume, EnumXaSuspend

__all__ = [
    "EnumXaCommandType",
    "XaId",
    "XaStatement",
    "XaStartStatement",
    "XaEndStatement",
    "XaPrepareStatement",
    "XaCommitStatement",
    "XaRollbackStatement",
    "XaRecoverStatement",
]


class EnumXaCommandType(IntEnum):
    """XA 命令类型的枚举值"""

    START = 1  # XA START/BEGIN
    END = 2  # XA END
    PREPARE = 3  # XA PREPARE
    COMMIT = 4  # XA COMMIT
    ROLLBACK = 5  # XA ROLLBACK
    RECOVER = 6  # XA RECOVER


class XaId(Node):
    """
    XA 事务标识符的抽象语法树节点。
    
    语法规则：
        text_string [, text_string [, ulong_num]]
    """

    __slots__ = (
        "_gtrid",
        "_bqual",
        "_format_id",
    )

    def __init__(self, gtrid: str, bqual: Optional[str] = None,
                 format_id: Optional[int] = None):
        """
        初始化XA事务标识符节点。

        Parameters
        ----------
        gtrid : str
            全局事务标识符
        bqual : Optional[str]
            分支限定符，默认为None
        format_id : Optional[int]
            格式标识符，默认为None
        """
        self._gtrid = gtrid
        self._bqual = bqual
        self._format_id = format_id

    @property
    def gtrid(self) -> str:
        """
        获取全局事务标识符。

        Returns
        -------
        str
            全局事务标识符
        """
        return self._gtrid

    @property
    def bqual(self) -> Optional[str]:
        """
        获取分支限定符。

        Returns
        -------
        Optional[str]
            分支限定符
        """
        return self._bqual

    @property
    def format_id(self) -> Optional[int]:
        """
        获取格式标识符。

        Returns
        -------
        Optional[int]
            格式标识符
        """
        return self._format_id


class XaStatement(Statement):
    """XA 命令的抽象语法树节点基类"""

    __slots__ = (
        "_command_type",
    )

    def __init__(self, command_type: EnumXaCommandType):
        """
        初始化XA命令节点。

        Parameters
        ----------
        command_type : EnumXaCommandType
            XA命令类型
        """
        self._command_type = command_type

    @property
    def command_type(self) -> EnumXaCommandType:
        """
        获取XA命令类型。

        Returns
        -------
        EnumXaCommandType
            XA命令类型
        """
        return self._command_type


class XaStartStatement(XaStatement):
    """
    XA START/BEGIN 命令的抽象语法树节点。
    
    语法规则：
        XA {START|BEGIN} xid [JOIN|RESUME]
    """

    __slots__ = (
        "_xid",
        "_join_or_resume",
    )

    def __init__(self, xid: XaId, join_or_resume: "EnumXaJoinOrResume"):
        """
        初始化XA START命令节点。

        Parameters
        ----------
        xid : XaId
            XA事务标识符
        join_or_resume : EnumXaJoinOrResume
            JOIN或RESUME选项
        """
        super().__init__(EnumXaCommandType.START)
        self._xid = xid
        self._join_or_resume = join_or_resume

    @property
    def xid(self) -> XaId:
        """
        获取XA事务标识符。

        Returns
        -------
        XaId
            XA事务标识符
        """
        return self._xid

    @property
    def join_or_resume(self) -> "EnumXaJoinOrResume":
        """
        获取JOIN或RESUME选项。

        Returns
        -------
        EnumXaJoinOrResume
            JOIN或RESUME选项
        """
        return self._join_or_resume


class XaEndStatement(XaStatement):
    """
    XA END 命令的抽象语法树节点。
    
    语法规则：
        XA END xid [SUSPEND [FOR MIGRATE]]
    """

    __slots__ = (
        "_xid",
        "_suspend",
    )

    def __init__(self, xid: XaId, suspend: "EnumXaSuspend"):
        """
        初始化XA END命令节点。

        Parameters
        ----------
        xid : XaId
            XA事务标识符
        suspend : EnumXaSuspend
            SUSPEND选项
        """
        super().__init__(EnumXaCommandType.END)
        self._xid = xid
        self._suspend = suspend

    @property
    def xid(self) -> XaId:
        """
        获取XA事务标识符。

        Returns
        -------
        XaId
            XA事务标识符
        """
        return self._xid

    @property
    def suspend(self) -> "EnumXaSuspend":
        """
        获取SUSPEND选项。

        Returns
        -------
        EnumXaSuspend
            SUSPEND选项
        """
        return self._suspend


class XaPrepareStatement(XaStatement):
    """
    XA PREPARE 命令的抽象语法树节点。
    
    语法规则：
        XA PREPARE xid
    """

    __slots__ = (
        "_xid",
    )

    def __init__(self, xid: XaId):
        """
        初始化XA PREPARE命令节点。

        Parameters
        ----------
        xid : XaId
            XA事务标识符
        """
        super().__init__(EnumXaCommandType.PREPARE)
        self._xid = xid

    @property
    def xid(self) -> XaId:
        """
        获取XA事务标识符。

        Returns
        -------
        XaId
            XA事务标识符
        """
        return self._xid


class XaCommitStatement(XaStatement):
    """
    XA COMMIT 命令的抽象语法树节点。
    
    语法规则：
        XA COMMIT xid [ONE PHASE]
    """

    __slots__ = (
        "_xid",
        "_one_phase",
    )

    def __init__(self, xid: XaId, one_phase: bool):
        """
        初始化XA COMMIT命令节点。

        Parameters
        ----------
        xid : XaId
            XA事务标识符
        one_phase : bool
            是否为ONE PHASE提交
        """
        super().__init__(EnumXaCommandType.COMMIT)
        self._xid = xid
        self._one_phase = one_phase

    @property
    def xid(self) -> XaId:
        """
        获取XA事务标识符。

        Returns
        -------
        XaId
            XA事务标识符
        """
        return self._xid

    @property
    def one_phase(self) -> bool:
        """
        获取是否为ONE PHASE提交。

        Returns
        -------
        bool
            是否为ONE PHASE提交
        """
        return self._one_phase


class XaRollbackStatement(XaStatement):
    """
    XA ROLLBACK 命令的抽象语法树节点。
    
    语法规则：
        XA ROLLBACK xid
    """

    __slots__ = (
        "_xid",
    )

    def __init__(self, xid: XaId):
        """
        初始化XA ROLLBACK命令节点。

        Parameters
        ----------
        xid : XaId
            XA事务标识符
        """
        super().__init__(EnumXaCommandType.ROLLBACK)
        self._xid = xid

    @property
    def xid(self) -> XaId:
        """
        获取XA事务标识符。

        Returns
        -------
        XaId
            XA事务标识符
        """
        return self._xid


class XaRecoverStatement(XaStatement):
    """
    XA RECOVER 命令的抽象语法树节点。
    
    语法规则：
        XA RECOVER [CONVERT XID]
    """

    __slots__ = (
        "_convert_xid",
    )

    def __init__(self, convert_xid: bool):
        """
        初始化XA RECOVER命令节点。

        Parameters
        ----------
        convert_xid : bool
            是否转换XID
        """
        super().__init__(EnumXaCommandType.RECOVER)
        self._convert_xid = convert_xid

    @property
    def convert_xid(self) -> bool:
        """
        获取是否转换XID。

        Returns
        -------
        bool
            是否转换XID
        """
        return self._convert_xid
