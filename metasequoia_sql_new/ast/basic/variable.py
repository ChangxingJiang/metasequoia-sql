"""
变量（variable）
"""

from typing import List

from metasequoia_sql_new.ast.base import Expression

__all__ = [
    "UserVariable"
]


class UserVariable(Expression):
    """用户变量"""

    def __init__(self, variable_name: str):
        self._variable_name = variable_name

    def attr_list(self) -> List[str]:
        return ["variable_name"]

    @property
    def variable_name(self) -> str:
        return self._variable_name
