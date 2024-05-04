"""
解析 MySQL 建表语句
"""

from metasequoia_sql import SQLParser

if __name__ == "__main__":
    statement = SQLParser.parse_select_statement("""
    SELECT   d.pid
        ,d.human_gid
        ,d.human_cgid
        ,d.human_name
        ,d.group_name
        ,d.group_uuid
        ,d.group_gid
        ,d.company_name
        ,d.group_type
        ,d.group_num
        ,d.group_logo
        ,n.position_names positions
       ,row_number() OVER(PARTITION BY d.pid,d.group_gid ORDER BY d.human_cgid DESC) num

FROM    test.company_group_human_dimension_tmp d
    """)
