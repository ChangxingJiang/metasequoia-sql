"""
解析器的通用函数
"""

from typing import Optional

__all__ = ["unify_name"]


def unify_name(text: Optional[str]) -> Optional[str]:
    """格式化名称标识符：统一剔除当前引号并添加引号"""
    return text.strip("`") if text is not None else None
