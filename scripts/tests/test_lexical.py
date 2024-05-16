"""
测试词法解析器
"""

import unittest
from typing import List

from metasequoia_sql import lexical


def get_amt_source(amt_list: List[lexical.AMTBase]):
    """获取抽象词法树节点的源代码"""
    return "".join(amt.source for amt in amt_list)


class TestLexical(unittest.TestCase):
    """测试词法解析器"""

    def test_bitwise_inversion(self):
        """测试按位取反符号"""
        for sql in ["~1", "~ 1", "~~ 1"]:
            self.assertEqual(get_amt_source(lexical.FSMMachine.parse(sql)), sql)
