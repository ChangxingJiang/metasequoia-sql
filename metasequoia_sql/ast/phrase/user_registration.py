"""
用户注册相关的 AST 节点类
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    pass

__all__ = [
    "UserRegistration",
    "UserRegistrationInitiate",
    "UserRegistrationUnregister",
    "UserRegistrationFinish",
]


class UserRegistration(Node):
    """
    用户注册操作的基类
    
    Parameters
    ----------
    factor : int
        因子编号（2 或 3）
    """

    __slots__ = ("_factor",)

    def __init__(self, factor: int):
        self._factor = factor

    @property
    def factor(self) -> int:
        """因子编号"""
        return self._factor


class UserRegistrationInitiate(UserRegistration):
    """
    初始化注册：factor INITIATE REGISTRATION
    
    Parameters
    ----------
    factor : int
        因子编号（2 或 3）
    """

    __slots__ = ()

    def __init__(self, factor: int):
        super().__init__(factor)


class UserRegistrationUnregister(UserRegistration):
    """
    取消注册：factor UNREGISTER
    
    Parameters
    ----------
    factor : int
        因子编号（2 或 3）
    """

    __slots__ = ()

    def __init__(self, factor: int):
        super().__init__(factor)


class UserRegistrationFinish(UserRegistration):
    """
    完成注册：factor FINISH REGISTRATION SET CHALLENGE_RESPONSE AS TEXT_STRING_hash
    
    Parameters
    ----------
    factor : int
        因子编号（2 或 3）
    challenge_response : str
        挑战响应字符串
    """

    __slots__ = ("_challenge_response",)

    def __init__(self, factor: int, challenge_response: str):
        super().__init__(factor)
        self._challenge_response = challenge_response

    @property
    def challenge_response(self) -> str:
        """挑战响应字符串"""
        return self._challenge_response
