"""
语义组：标识符


"""

import metasequoia_parser as ms_parser
from metasequoia_sql.terminal import SqlTerminalType as TType
from metasequoia_sql_grammar import top_level_node
from metasequoia_sql_grammar.basic import charset_name
from metasequoia_sql_grammar.basic import fixed_enum
from metasequoia_sql_grammar.basic import fixed_word
from metasequoia_sql_grammar.basic import ident
from metasequoia_sql_grammar.basic import ident_mysql
from metasequoia_sql_grammar.basic import literal
from metasequoia_sql_grammar.basic import param
from metasequoia_sql_grammar.basic import time_unit
from metasequoia_sql_grammar.basic import variable
from metasequoia_sql_grammar.clause import ddl_partition_by_clause
from metasequoia_sql_grammar.clause import from_clause
from metasequoia_sql_grammar.clause import group_by_clause
from metasequoia_sql_grammar.clause import having_clause
from metasequoia_sql_grammar.clause import index_hint_clause
from metasequoia_sql_grammar.clause import into_clause
from metasequoia_sql_grammar.clause import limit_clause
from metasequoia_sql_grammar.clause import locking_clause
from metasequoia_sql_grammar.clause import order_by_clause
from metasequoia_sql_grammar.clause import over_clause
from metasequoia_sql_grammar.clause import partition_clause
from metasequoia_sql_grammar.clause import qualify_clause
from metasequoia_sql_grammar.clause import where_clause
from metasequoia_sql_grammar.clause import window_clause
from metasequoia_sql_grammar.clause import window_partition_by_clause
from metasequoia_sql_grammar.clause import with_clause
from metasequoia_sql_grammar.expression import function_expression
from metasequoia_sql_grammar.expression import general_expression
from metasequoia_sql_grammar.expression import sum_function_expression
from metasequoia_sql_grammar.expression import window_function_expression
from metasequoia_sql_grammar.phrase import alias
from metasequoia_sql_grammar.phrase import cpu_range
from metasequoia_sql_grammar.phrase import ddl_alter_option
from metasequoia_sql_grammar.phrase import ddl_column_attribute
from metasequoia_sql_grammar.phrase import ddl_index_attribute
from metasequoia_sql_grammar.phrase import ddl_option
from metasequoia_sql_grammar.phrase import ddl_table_element
from metasequoia_sql_grammar.phrase import dml_option
from metasequoia_sql_grammar.phrase import field_type
from metasequoia_sql_grammar.phrase import function_option
from metasequoia_sql_grammar.phrase import json_table_option
from metasequoia_sql_grammar.phrase import on_duplicate
from metasequoia_sql_grammar.phrase import sql_state
from metasequoia_sql_grammar.phrase import thread_priority
from metasequoia_sql_grammar.phrase import time_interval
from metasequoia_sql_grammar.statement import alter_database_statement
from metasequoia_sql_grammar.statement import alter_function_statement
from metasequoia_sql_grammar.statement import alter_instance_statement
from metasequoia_sql_grammar.statement import alter_procedure_statement
from metasequoia_sql_grammar.statement import alter_resource_group_statement
from metasequoia_sql_grammar.statement import alter_table_statement
from metasequoia_sql_grammar.statement import analyze_statement
from metasequoia_sql_grammar.statement import begin_statement
from metasequoia_sql_grammar.statement import binlog_statement
from metasequoia_sql_grammar.statement import call_statement
from metasequoia_sql_grammar.statement import check_table_statement
from metasequoia_sql_grammar.statement import checksum_statement
from metasequoia_sql_grammar.statement import clone_statement
from metasequoia_sql_grammar.statement import commit_statement
from metasequoia_sql_grammar.statement import create_index_statement
from metasequoia_sql_grammar.statement import create_resource_group_statement
from metasequoia_sql_grammar.statement import create_role_statement
from metasequoia_sql_grammar.statement import create_table_statement
from metasequoia_sql_grammar.statement import deallocate_statement
from metasequoia_sql_grammar.statement import delete_statement
from metasequoia_sql_grammar.statement import describe_statement
from metasequoia_sql_grammar.statement import do_statement
from metasequoia_sql_grammar.statement import drop_statement
from metasequoia_sql_grammar.statement import execute_statement
from metasequoia_sql_grammar.statement import explain_statement
from metasequoia_sql_grammar.statement import flush_statement
from metasequoia_sql_grammar.statement import grant_and_revoke_statement
from metasequoia_sql_grammar.statement import help_statement
from metasequoia_sql_grammar.statement import import_statement
from metasequoia_sql_grammar.statement import insert_or_replace_statement
from metasequoia_sql_grammar.statement import install_or_uninstall_statement
from metasequoia_sql_grammar.statement import kill_statement
from metasequoia_sql_grammar.statement import lock_or_unlock_statement
from metasequoia_sql_grammar.statement import optimize_table_statement
from metasequoia_sql_grammar.statement import prepare_statement
from metasequoia_sql_grammar.statement import purge_statement
from metasequoia_sql_grammar.statement import release_statement
from metasequoia_sql_grammar.statement import rename_statement
from metasequoia_sql_grammar.statement import repair_table_statement
from metasequoia_sql_grammar.statement import reset_statement
from metasequoia_sql_grammar.statement import restart_statement
from metasequoia_sql_grammar.statement import rollback_statement
from metasequoia_sql_grammar.statement import savepoint_statement
from metasequoia_sql_grammar.statement import select_statement
from metasequoia_sql_grammar.statement import show_statement
from metasequoia_sql_grammar.statement import shutdown_statement
from metasequoia_sql_grammar.statement import signal_and_resignal_statement
from metasequoia_sql_grammar.statement import start_transaction_statement
from metasequoia_sql_grammar.statement import truncate_statement
from metasequoia_sql_grammar.statement import update_statement
from metasequoia_sql_grammar.statement import use_statement
from metasequoia_sql_grammar.statement import xa_statement
from metasequoia_sql_grammar.table import derived_table
from metasequoia_sql_grammar.table import general_table
from metasequoia_sql_grammar.table import joined_table
from metasequoia_sql_grammar.table import single_table
from metasequoia_sql_grammar.table import table_function


def build_grammar():
    grammar_builder = ms_parser.create_grammar(
        groups=[],
        terminal_type_enum=TType,
        start="start_entry",
        sr_priority=[
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_INTO],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.EMPTY_FROM_CLAUSE],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.SUBQUERY_AS_EXPR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_INTERVAL],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_BINARY, TType.KEYWORD_COLLATE],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_NOT],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.NEG, TType.OPERATOR_TILDE],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_BAR_BAR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_CARET],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_STAR, TType.OPERATOR_SLASH, TType.OPERATOR_PERCENT, TType.KEYWORD_DIV,
                         TType.KEYWORD_MOD],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_SUB, TType.OPERATOR_PLUS],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_LT_LT, TType.OPERATOR_GT_GT],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_AMP],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_BAR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_EQ, TType.OPERATOR_LT_EQ_GT, TType.OPERATOR_GT_EQ, TType.OPERATOR_GT,
                         TType.OPERATOR_LT_EQ, TType.OPERATOR_LT, TType.OPERATOR_BANG_EQ, TType.KEYWORD_IS,
                         TType.KEYWORD_LIKE, TType.KEYWORD_REGEXP, TType.KEYWORD_IN],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_BETWEEN, TType.KEYWORD_CASE, TType.KEYWORD_WHEN, TType.KEYWORD_THEN,
                         TType.KEYWORD_ELSE],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_AND, TType.OPERATOR_AMP_AMP],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_XOR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_OR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_COLON_EQ],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_JOIN, TType.KEYWORD_INNER, TType.KEYWORD_STRAIGHT_JOIN, TType.KEYWORD_NATURAL,
                         TType.KEYWORD_LEFT, TType.KEYWORD_RIGHT, TType.KEYWORD_ON, TType.KEYWORD_USING],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.CONDITIONLESS_JOIN],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_INTERSECT],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_UNION, TType.KEYWORD_EXCEPT],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_UNIQUE, TType.KEYWORD_KEY],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_USED_AS_KEYWORD],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.LITERAL_TEXT_STRING],
                combine_type=ms_parser.COMBINE_NONASSOC
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_USED_AS_IDENT],
                combine_type=ms_parser.COMBINE_LEFT
            )
        ]
    )

    for module in [
        fixed_word,  # 基础元素 - 固定的词语组合
        ident,  # 基础元素 - 标识符
        ident_mysql,  # 基础元素 - 标识符（MySQL 专有）
        literal,  # 基础元素 - 字面值
        charset_name,  # 基础元素 - 字符集名称
        param,  # 基础元素 - 参数
        variable,  # 基础元素 - 变量
        time_unit,  # 基础元素 - 时间单位类型
        fixed_enum,  # 固定的枚举类型

        # 短语
        field_type,  # 短语 - 字段类型
        function_option,  # 短语 - 函数选项
        json_table_option,  # 短语 - JSON 表选项
        alias,  # 短语 - 别名
        sql_state,  # 短语 - SQL状态
        time_interval,  # 短语 - 时间间隔
        thread_priority,  # 短语 - 线程优先级
        dml_option,  # DML 选项
        ddl_column_attribute,  # DDL 字段属性
        ddl_table_element,  # DDL 表元素
        ddl_index_attribute,  # DDL 索引属性
        ddl_option,  # DDL 选项
        on_duplicate,  # 重复值处理规则
        ddl_alter_option,  # DDL 修改表选项
        cpu_range,

        # 表达式
        general_expression,  # 表达式 - 通用表达式
        sum_function_expression,  # 表达式 - 聚集函数表达式
        window_function_expression,  # 表达式 - 窗口函数表达式
        function_expression,  # 表达式 - 普通函数表达式

        # 表
        general_table,  # 通用表逻辑
        single_table,  # 单表
        joined_table,  # 关联表
        derived_table,  # 派生表
        table_function,  # 生成表函数

        # 子句层级
        from_clause,  # FROM 子句
        group_by_clause,  # GROUP BY 子句
        having_clause,  # HAVING 子句
        index_hint_clause,  # 索引指定子句
        into_clause,  # INTO 子句
        limit_clause,  # LIMIT 子句
        locking_clause,  # 锁指定子句
        order_by_clause,  # ORDER BY 子句
        over_clause,  # OVER 子句
        partition_clause,  # PARTITION 子句
        window_partition_by_clause,  # PARTITION BY 子句
        qualify_clause,  # QUALIFY 子句
        where_clause,  # WHERE 子句
        window_clause,  # WINDOW 子句
        with_clause,  # WITH 子句
        ddl_partition_by_clause,  # DDL 分区子句

        # 语句
        alter_database_statement,  # ALTER DATABASE 语句
        alter_function_statement,  # ALTER FUNCTION 语句
        alter_instance_statement,  # ALTER INSTANCE 语句
        alter_procedure_statement,  # ALTER PROCEDURE 语句
        alter_resource_group_statement,  # ALTER RESOURCE GROUP 语句
        analyze_statement,  # ANALYZE TABLE 语句
        alter_table_statement,  # ALTER TABLE 语句
        begin_statement,  # BEGIN 语句
        binlog_statement,  # BINLOG 语句
        call_statement,  # ALTER TABLE 语句
        check_table_statement,  # CHECK TABLE 语句
        checksum_statement,  # CHECKSUM 语句
        clone_statement,  # CLONE 语句
        commit_statement,  # COMMIT 语句
        create_index_statement,  # CREATE INDEX 语句
        create_resource_group_statement,  # CREATE RESOURCE GROUP 语句
        create_role_statement,  # CREATE ROLE 语句
        create_table_statement,  # CREATE TABLE 语句
        deallocate_statement,  # DEALLOCATE 语句
        delete_statement,  # DELETE 语句
        describe_statement,  # DESCRIBE 语句
        do_statement,  # DO 语句
        drop_statement,  # DROP 语句
        execute_statement,  # EXECUTE 语句
        explain_statement,  # EXPLAIN 语句
        flush_statement,  # FLUSH 语句
        grant_and_revoke_statement,  # GRANT 和 REVOKE 语句
        help_statement,  # HELP 语句
        import_statement,  # IMPORT TABLE 语句
        insert_or_replace_statement,  # INSERT 语句或 UPDATE 语句
        install_or_uninstall_statement,  # INSTALL/UNINSTALL 语句
        kill_statement,  # KILL 语句
        lock_or_unlock_statement,  # LOCK/UNLOCK 语句
        optimize_table_statement,  # OPTIMIZE TABLE 语句
        prepare_statement,  # PREPARE 语句
        purge_statement,  # PURGE 语句
        release_statement,  # RELEASE 语句
        rename_statement,
        repair_table_statement,  # REPAIR TABLE 语句
        reset_statement,  # RESET 语句
        restart_statement,  # RESTART 语句
        rollback_statement,  # ROLLBACK 语句
        savepoint_statement,  # SAVEPOINT 语句
        select_statement,  # SELECT 语句
        show_statement,  # SHOW 语句
        shutdown_statement,  # SHUTDOWN 语句
        signal_and_resignal_statement,  # SIGNAL/RESIGNAL 语句
        start_transaction_statement,  # START TRANSACTION 语句
        truncate_statement,  # TRUNCATE 语句
        update_statement,  # UPDATE 语句
        use_statement,  # USE 语句
        xa_statement,  # XA 语句

        # 顶层节点
        top_level_node
    ]:
        for group_name in module.__all__:
            grammar_builder.group_append(getattr(module, group_name))

    return grammar_builder.build()


if __name__ == "__main__":
    import os
    import time

    repository_path = os.path.dirname(os.path.dirname(__file__))
    parser_path = os.path.join(repository_path, "metasequoia_sql", "syntax", "parser.py")

    start_time = time.time()
    parser = ms_parser.parser.ParserLALR1(build_grammar(), debug=True)
    source_code = ms_parser.compiler.compile_lalr1(parser, import_list=[
        "from metasequoia_sql import ast"
    ])
    end_time = time.time()
    print(f"编译完成，耗时：{end_time - start_time:.3f} 秒")
    with open(parser_path, "w+", encoding="UTF-8") as file:
        for row in source_code:
            file.write(f"{row}\n")
