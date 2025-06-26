"""
账户锁定和密码过期选项（account lock expire option）
"""

from metasequoia_sql.ast.base import Node

__all__ = [
    "AccountLockExpireOption",
    "AccountUnlock",
    "AccountLock",
    "PasswordExpire",
    "PasswordExpireInterval",
    "PasswordExpireNever",
    "PasswordExpireDefault",
    "PasswordHistory",
    "PasswordHistoryDefault",
    "PasswordReuseInterval",
    "PasswordReuseIntervalDefault",
    "PasswordRequireCurrent",
    "PasswordRequireCurrentDefault",
    "PasswordRequireCurrentOptional",
    "FailedLoginAttempts",
    "PasswordLockTime",
    "PasswordLockTimeUnbounded",
]


class AccountLockExpireOption(Node):
    """账户锁定和密码过期选项的抽象基类"""


class AccountUnlock(AccountLockExpireOption):
    """账户解锁选项"""


class AccountLock(AccountLockExpireOption):
    """账户锁定选项"""


class PasswordExpire(AccountLockExpireOption):
    """密码立即过期选项"""


class PasswordExpireInterval(AccountLockExpireOption):
    """密码间隔过期选项"""

    __slots__ = ["_days"]

    def __init__(self, days: int):
        """
        初始化密码间隔过期选项。

        Parameters
        ----------
        days : int
            密码过期的天数
        """
        self._days = days

    @property
    def days(self) -> int:
        """
        获取密码过期的天数。

        Returns
        -------
        int
            密码过期的天数
        """
        return self._days


class PasswordExpireNever(AccountLockExpireOption):
    """密码永不过期选项"""


class PasswordExpireDefault(AccountLockExpireOption):
    """密码使用默认过期设置选项"""


class PasswordHistory(AccountLockExpireOption):
    """密码历史长度选项"""

    __slots__ = ["_length"]

    def __init__(self, length: int):
        """
        初始化密码历史长度选项。

        Parameters
        ----------
        length : int
            密码历史记录长度
        """
        self._length = length

    @property
    def length(self) -> int:
        """
        获取密码历史记录长度。

        Returns
        -------
        int
            密码历史记录长度
        """
        return self._length


class PasswordHistoryDefault(AccountLockExpireOption):
    """密码历史使用默认设置选项"""


class PasswordReuseInterval(AccountLockExpireOption):
    """密码重用间隔选项"""

    __slots__ = ["_days"]

    def __init__(self, days: int):
        """
        初始化密码重用间隔选项。

        Parameters
        ----------
        days : int
            密码重用间隔天数
        """
        self._days = days

    @property
    def days(self) -> int:
        """
        获取密码重用间隔天数。

        Returns
        -------
        int
            密码重用间隔天数
        """
        return self._days


class PasswordReuseIntervalDefault(AccountLockExpireOption):
    """密码重用间隔使用默认设置选项"""


class PasswordRequireCurrent(AccountLockExpireOption):
    """需要当前密码选项"""


class PasswordRequireCurrentDefault(AccountLockExpireOption):
    """当前密码要求使用默认设置选项"""


class PasswordRequireCurrentOptional(AccountLockExpireOption):
    """当前密码可选选项"""


class FailedLoginAttempts(AccountLockExpireOption):
    """失败登录尝试次数限制选项"""

    __slots__ = ["_attempts"]

    def __init__(self, attempts: int):
        """
        初始化失败登录尝试次数限制选项。

        Parameters
        ----------
        attempts : int
            失败登录尝试次数限制
        """
        self._attempts = attempts

    @property
    def attempts(self) -> int:
        """
        获取失败登录尝试次数限制。

        Returns
        -------
        int
            失败登录尝试次数限制
        """
        return self._attempts


class PasswordLockTime(AccountLockExpireOption):
    """密码锁定时间选项"""

    __slots__ = ["_time"]

    def __init__(self, time: int):
        """
        初始化密码锁定时间选项。

        Parameters
        ----------
        time : int
            密码锁定时间
        """
        self._time = time

    @property
    def time(self) -> int:
        """
        获取密码锁定时间。

        Returns
        -------
        int
            密码锁定时间
        """
        return self._time


class PasswordLockTimeUnbounded(AccountLockExpireOption):
    """密码无限制锁定选项"""
