"""
Issue 问题测试用例
"""

import unittest

from metasequoia_sql import SQLParser


class TestIssueQuestion(unittest.TestCase):
    """Issue 问题测试用例"""

    def test_constraint(self):
        """测试含 constraint 建表语句解析"""
        SQLParser.parse_statements("""
CREATE TABLE `table_1` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`field_1` int(11) DEFAULT NULL,
PRIMARY KEY (`id`),
CONSTRAINT `index_name_1` FOREIGN KEY (`field_1`) REFERENCES `table_2` (`field_2`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB""")

    def test_generated_column(self):
        """测试包含计算字段的建表语句解析"""
        SQLParser.parse_statements("""
CREATE TABLE `table_1` (
`id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'xxx',
`field_1` int(11) NOT NULL DEFAULT '0' COMMENT 'xxx',
`field_2` int(11) NOT NULL DEFAULT '0' COMMENT 'xxx',
`field_3` int(11) GENERATED ALWAYS AS (field_1 + field_2) VIRTUAL NOT NULL COMMENT 'xxx',
`field_4` decimal(6, 2) GENERATED ALWAYS AS (field_1 / field_2) STORED NOT NULL COMMENT 'xxx',
PRIMARY KEY (`id`)
) ENGINE = InnoDB""")
