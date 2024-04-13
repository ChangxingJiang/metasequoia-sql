"""基础扫描器"""

from typing import TypeVar, Generic, List, Optional

from metasequoia_sql.errors import ScannerError

T = TypeVar('T')  # 兼容 Python 3.10 及以下版本的泛型


class BaseScanner(Generic[T]):
    """文本扫描器"""

    def __init__(self, elements: List[T], pos: int = 0):
        """

        指针允许到 len(elements) 长度的位置，但在该位置不允许 get()。

        Parameters
        ----------
        elements : Any
            扫描的文本
        pos : int, default = 0
            当前指针位置
        """
        if pos < 0:
            raise ScannerError(f"初始化的指针小于 0: pos={pos}")
        if pos > len(elements):
            raise ScannerError(f"初始化指针大于字符串长度: len(text)={len(elements)}, pos={pos}")

        self._elements = elements
        self._pos = pos
        self._len = len(elements)

        self._last = elements[pos - 1] if pos > 0 else None  # 上一个元素

    @property
    def elements(self) -> List[T]:
        """返回扫描器中的所有元素"""
        return self._elements

    @property
    def pos(self) -> int:
        """返回当前扫描指针"""
        return self._pos

    @property
    def last(self) -> Optional[T]:
        """当前指针位置的上一个字符"""
        return self._last

    @property
    def now(self) -> Optional[T]:
        """当前指针位置的字符"""
        return self.get()

    @property
    def next1(self) -> Optional[T]:
        """当前指针位置的下一个字符"""
        return self._get_by_offset(1)

    @property
    def next2(self) -> Optional[T]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self._get_by_offset(2)

    @property
    def next3(self) -> Optional[T]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self._get_by_offset(3)

    @property
    def next4(self) -> Optional[T]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self._get_by_offset(4)

    def get(self) -> Optional[T]:
        """获取当前指针位置元素，但不移动指针

        - 如果指针已到达字符串末尾，则返回 None
        - 如果指针超出字符串长度，则抛出异常
        """
        if self.pos > self._len:
            raise ScannerError(f"要获取的指针大于等于字符串长度: len={self._len}, pos={self.pos}")
        if self.pos == self._len:
            return None
        return self._elements[self._pos]

    def pop(self) -> T:
        """获取当前指针位置元素，并移动指针

        - 如果要移动到的指针位置超出字符串长度，则抛出异常
        """
        if self.pos >= self._len:
            raise ScannerError(f"要移动到的指针下标大于字符串长度: len={self._len}, pos={self.pos + 1} {self}")

        self._last = self.get()  # 更新上一个元素
        result = self._elements[self.pos]
        self._pos += 1  # 移动指针
        return result

    def _get_by_offset(self, idx: int) -> Optional[T]:
        """获取当前指针位置 + idx 位置的元素，但不一定指针
        """
        if self.pos + idx >= self._len:
            return None
        return self._elements[self.pos + idx]

    @property
    def is_finish(self) -> bool:
        """返回当前是否已匹配结束"""
        return self.pos == self._len

    def __repr__(self):
        return f"<{self.__class__.__name__} tokens={self.elements[self.pos:]}, pos={self.pos}>"
