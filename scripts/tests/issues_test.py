"""
Issue 问题测试用例
"""

import unittest

from metasequoia_sql import SQLParser


class TestIssueQuestion(unittest.TestCase):
    """Issue 问题测试用例"""

    def test_longtext(self):
        """测试含 longtext 建表语句解析"""
        SQLParser.parse_statements("""
CREATE TABLE `table_1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`field_1` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
CONSTRAINT `index_name_1` FOREIGN KEY (`field_1`) REFERENCES `table_2` (`field_2`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB;
""")
