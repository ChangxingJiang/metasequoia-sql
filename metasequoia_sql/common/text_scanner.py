"""文本扫描器"""

from typing import Optional


class ScannerError(Exception):
    """文本扫描异常"""


class TextScanner:
    """文本扫描器"""

    def __init__(self, text: str, pos: int = 0):
        """

        指针允许到字符串长度的位置，但在该位置不允许获取。

        Parameters
        ----------
        text : str
            扫描的文本
        pos : int, default = 0
            当前指针位置
        """
        if pos < 0:
            raise ScannerError(f"初始化的指针小于 0: pos={pos}")
        if pos > len(text):
            raise ScannerError(f"初始化指针大于字符串长度: len(text)={len(text)}, pos={pos}")

        self._text = text
        self._pos = pos
        self._len = len(text)

        self._last = text[pos - 1] if pos > 0 else None  # 上一个元素

    @property
    def text(self) -> str:
        return self._text

    @property
    def pos(self) -> int:
        return self._pos

    @property
    def last(self) -> Optional[str]:
        """当前指针位置的上一个字符"""
        return self._last

    @property
    def now(self) -> Optional[str]:
        """当前指针位置的字符"""
        return self.top()

    @property
    def next(self) -> Optional[str]:
        """当前指针位置的下一个字符"""
        return self.top_next()

    def top(self) -> Optional[str]:
        """获取当前指针位置元素，但不移动指针

        - 如果指针已到达字符串末尾，则返回 None
        - 如果指针超出字符串长度，则抛出异常
        """
        if self._pos > self._len:
            raise ScannerError(f"要获取的指针大于等于字符串长度: len={self._len}, pos={self._pos}")
        if self._pos == self._len:
            return None
        return self._text[self._pos]

    def top_next(self) -> Optional[str]:
        """获取当前指针下一个位置的元素，但不一定指针

        Returns
        -------

        """
        if self._pos + 1 > self._len:
            raise ScannerError(f"要获取的指针大于等于字符串长度: len={self._len}, pos={self._pos + 1}")
        if self._pos + 1 == self._len:
            return None
        return self._text[self._pos + 1]

    def get(self) -> str:
        """获取当前指针位置元素，并移动指针

        - 如果要移动到的指针位置超出字符串长度，则抛出异常
        """
        if self._pos >= self._len:
            raise ScannerError(f"要移动到的指针下标大于字符串长度: len={self._len}, pos={self._pos + 1}")

        self._last = self.top()  # 更新上一个元素
        result = self._text[self._pos]
        self._pos += 1  # 移动指针
        return result

    def move(self) -> None:
        """移动指针"""
        self._pos += 1

    @property
    def is_finish(self) -> bool:
        """返回当前是否已匹配结束"""
        return self._pos == self._len
