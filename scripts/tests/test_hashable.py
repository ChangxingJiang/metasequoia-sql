import dataclasses
import enum
import inspect
from types import GenericAlias

from metasequoia_sql import *


def instantiate(cls: type):
    """实例化类"""
    print(cls, type(cls), isinstance(cls, GenericAlias))
    if issubclass(cls, bool):
        # 实例化布尔值
        return True
    if issubclass(cls, enum.Enum):
        # 实例化枚举类：使用枚举类中年的第一个枚举值
        return cls._member_map_[cls._member_names_[0]]
    if dataclasses.is_dataclass(cls):
        # 实例化 dataclasses
        cls: dataclasses.dataclass
        param_dict = {}
        for field in dataclasses.fields(cls):
            param_dict[field.name] = instantiate(field.type)
        return cls(**param_dict)
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
        ast_obj = instantiate(ast_class)
