"""
SQL 语法解析器

将所有解析方法合并到这个类中，以支持插件开发。
如需替换词法解析器，重写 build_token_scanner 方法即可。

TODO 将 CURRENT_TIMESTAMP、CURRENT_DATE、CURRENT_TIME 改为单独节点处理
"""

from metasequoia_sql.core.parser.interface import SQLParser
