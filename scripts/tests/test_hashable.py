import dataclasses
import enum
import inspect
import typing

from metasequoia_sql import *


def check_hashable(cls: type, visited: typing.Optional[typing.Set[type]] = None) -> bool:
    """检查类 cls 是否是可哈希的

    Parameters
    ----------
    cls : type
        需要实例化的类
    visited : typing.Optional[typing.Set[type]], default = None
        当前路径上已经遍历过的类

    Returns
    -------
    is_hashable : bool
        如果可哈希则返回 True，否则返回 False
    """
    if visited is None:
        visited = set()
    if cls in visited:
        return True
    visited.add(cls)

    # 类型引用对象（该引用一定在 node 中）
    if isinstance(cls, typing.ForwardRef):
        return check_hashable(getattr(node, cls.__forward_arg__), visited=visited)

    # 使用字符串的类型引用对象（该引用一定在 node 中）
    if isinstance(cls, str):
        return check_hashable(getattr(node, cls), visited=visited)

    # 处理类型标注
    if cls.__name__ == "Optional" and cls.__dict__.get("__origin__") == typing.Union:  # typing.Optional
        return check_hashable(cls.__dict__["__args__"][0], visited=visited)
    if cls.__name__ == "Tuple" and cls.__dict__.get("__origin__") == tuple:  # typing.Tuple
        for arg in cls.__dict__["__args__"]:
            if hasattr(arg, "__class__") and arg.__class__.__name__ == "ellipsis":
                continue  # 忽略 Tuple[...] 中的省略号
            if check_hashable(arg, visited=visited) is False:
                return False
        return True
    if cls.__name__ == "Union" and cls.__dict__.get("__origin__") == typing.Union:  # typing.Union
        for arg in cls.__dict__["__args__"]:
            if check_hashable(arg, visited=visited) is False:
                return False
        return True

    # 处理可哈希的内置类型
    if issubclass(cls, bool):  # 布尔值
        return True
    if issubclass(cls, enum.Enum):  # 枚举类
        return True
    if issubclass(cls, str):  # 字符串
        return True
    if issubclass(cls, int):  # 整型
        return True

    # 处理不可哈希的内置类型
    if issubclass(cls, list):  # 列表
        return False
    if issubclass(cls, dict):  # 字典
        return False
    if issubclass(cls, dict):  # 集合
        return False

    # 处理 dataclasses 类型
    if dataclasses.is_dataclass(cls):
        cls: dataclasses.dataclass
        for field in dataclasses.fields(cls):
            if not check_hashable(field.type, visited=visited):
                return False
        return True

    visited.remove(cls)

    raise KeyError(f"未定义的实例化类型: {cls}")


if __name__ == "__main__":
    for class_name in node.__all__:
        # 跳过不是抽象语法树的节点
        if not class_name.startswith("AST"):
            continue

        # 获取抽象语法树节点
        ast_class = getattr(node, class_name)

        # 检查抽象语法树节点是否为 dataclasses 对象
        assert dataclasses.is_dataclass(ast_class)

        # 抽象类跳过后续对实例的检查
        if inspect.isabstract(ast_class):
            continue

        # 实例化抽象语法树节点
        ast_obj = check_hashable(ast_class)
