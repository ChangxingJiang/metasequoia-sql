"""
抽象语法树（AST）节点的抽象基类
"""

import abc
import dataclasses

from metasequoia_sql.core.sql_type import SQLType

__all__ = ["ASTBase", "ASTExpressionBase"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBase(abc.ABC):
    """抽象语法树（AST）节点的抽象基类"""

    @abc.abstractmethod
    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} source={self.source()}>"

    def get_params_dict(self):
        """获取当前节点的所有参数（用于复制）"""
        return {field.name: getattr(self, field.name) for field in dataclasses.fields(self)}


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTExpressionBase(ASTBase, abc.ABC):
    """抽象语法树（AST）一般表达式节点的抽象基类"""
