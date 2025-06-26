"""
ALTER INSTANCE 语句（alter instance statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    pass

__all__ = [
    "AlterInstanceAction",
    "AlterInstanceActionRotateInnodbMasterKey",
    "AlterInstanceActionRotateBinlogMasterKey",
    "AlterInstanceActionReloadTls",
    "AlterInstanceActionReloadTlsNoRollback",
    "AlterInstanceActionReloadTlsForChannel",
    "AlterInstanceActionReloadTlsForChannelNoRollback",
    "AlterInstanceActionEnableInnodbRedo",
    "AlterInstanceActionDisableInnodbRedo",
    "AlterInstanceActionReloadKeyring",
    "AlterInstanceStatement",
]


class AlterInstanceAction(Node):
    """ALTER INSTANCE 操作基类"""


class AlterInstanceActionRotateInnodbMasterKey(AlterInstanceAction):
    """ALTER INSTANCE 操作：ROTATE INNODB MASTER KEY"""


class AlterInstanceActionRotateBinlogMasterKey(AlterInstanceAction):
    """ALTER INSTANCE 操作：ROTATE BINLOG MASTER KEY"""


class AlterInstanceActionReloadTls(AlterInstanceAction):
    """ALTER INSTANCE 操作：RELOAD TLS"""


class AlterInstanceActionReloadTlsNoRollback(AlterInstanceAction):
    """ALTER INSTANCE 操作：RELOAD TLS NO ROLLBACK ON ERROR"""


class AlterInstanceActionReloadTlsForChannel(AlterInstanceAction):
    """ALTER INSTANCE 操作：RELOAD TLS FOR CHANNEL"""

    __slots__ = (
        "_channel_name",
    )

    def __init__(self, channel_name: str):
        """
        初始化 RELOAD TLS FOR CHANNEL 操作

        Parameters
        ----------
        channel_name : str
            通道名称
        """
        self._channel_name = channel_name

    @property
    def channel_name(self) -> str:
        """
        通道名称

        Returns
        -------
        str
            通道名称
        """
        return self._channel_name


class AlterInstanceActionReloadTlsForChannelNoRollback(AlterInstanceAction):
    """ALTER INSTANCE 操作：RELOAD TLS FOR CHANNEL NO ROLLBACK ON ERROR"""

    __slots__ = (
        "_channel_name",
    )

    def __init__(self, channel_name: str):
        """
        初始化 RELOAD TLS FOR CHANNEL NO ROLLBACK ON ERROR 操作

        Parameters
        ----------
        channel_name : str
            通道名称
        """
        self._channel_name = channel_name

    @property
    def channel_name(self) -> str:
        """
        通道名称

        Returns
        -------
        str
            通道名称
        """
        return self._channel_name


class AlterInstanceActionEnableInnodbRedo(AlterInstanceAction):
    """ALTER INSTANCE 操作：ENABLE INNODB REDO_LOG"""


class AlterInstanceActionDisableInnodbRedo(AlterInstanceAction):
    """ALTER INSTANCE 操作：DISABLE INNODB REDO_LOG"""


class AlterInstanceActionReloadKeyring(AlterInstanceAction):
    """ALTER INSTANCE 操作：RELOAD KEYRING"""


class AlterInstanceStatement(Statement):
    """ALTER INSTANCE 语句"""

    __slots__ = (
        "_action",
    )

    def __init__(self, action: AlterInstanceAction):
        """
        初始化 ALTER INSTANCE 语句

        Parameters
        ----------
        action : AlterInstanceAction
            ALTER INSTANCE 操作
        """
        self._action = action

    @property
    def action(self) -> AlterInstanceAction:
        """
        ALTER INSTANCE 操作

        Returns
        -------
        AlterInstanceAction
            ALTER INSTANCE 操作
        """
        return self._action
