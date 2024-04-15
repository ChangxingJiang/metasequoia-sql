"""文本扫描器"""

from metasequoia_sql.common.base_scanner import BaseScanner


class TextScanner(BaseScanner):
    """文本扫描器"""

    def __init__(self, text: str):
        super().__init__(list(text))
