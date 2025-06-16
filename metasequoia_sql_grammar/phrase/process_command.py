"""
处理命令（process command）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 处理命令的基类
    "PROCESS_COMMAND_LIST",
    "PROCESS_COMMAND",

    # 处理命令：执行语句
    "PROCESS_COMMAND_STATEMENT",

    # 处理命令：返回表达式结果
    "PROCESS_COMMAND_RETURN",

    # 处理命令：IF 语句
    "PROCESS_COMMAND_IF",
    "PROCESS_COMMAND_OPT_ELSEIF_LIST",
    "PROCESS_COMMAND_ELSEIF_LIST",
    "PROCESS_COMMAND_ELSEIF",
    "PROCESS_COMMAND_OPT_ELSE",

    # 处理命令：CASE 语句
    "PROCESS_COMMAND_CASE",
    "PROCESS_COMMAND_WHEN_CLAUSE_LIST",
    "PROCESS_COMMAND_WHEN_CLAUSE",

    # 处理命令的声明表达式
    "PROCESS_COMMAND_DECLARE_LIST",
    "PROCESS_COMMAND_DECLARE",
    "PROCESS_COMMAND_HANDLER_CONDITION_LIST",
    "PROCESS_COMMAND_HANDLER_CONDITION",
    "PROCESS_COMMAND_CONDITION",

    # 处理命令：代码块
    "PROCESS_COMMAND_LABELED_BLOCK",
    "PROCESS_COMMAND_UNLABELED_BLOCK",
    "PROCESS_COMMAND_BLOCK",

    # 处理命令：控制语句
    "PROCESS_COMMAND_LABELED_CONTROL",
    "PROCESS_COMMAND_UNLABELED_CONTROL",

    # 处理命令：游标操作
    "PROCESS_COMMAND_LEAVE",
    "PROCESS_COMMAND_ITERATE",
    "PROCESS_COMMAND_OPEN",
    "PROCESS_COMMAND_FETCH",
    "PROCESS_COMMAND_CLOSE",
]

# 分号分隔的处理命令的列表
PROCESS_COMMAND_LIST = ms_parser.create_group(
    name="process_command_list",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command", TType.OPERATOR_SEMICOLON],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=["process_command_list", "process_command", TType.OPERATOR_SEMICOLON],
            action=lambda x: x[0] + [x[1]]
        )
    ]
)

# 处理命令
PROCESS_COMMAND = ms_parser.create_group(
    name="process_command",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_statement"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_return"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_if"]
        ),
        ms_parser.create_rule(
            symbols=["process_command_case"]
        ),
        ms_parser.create_rule(
            symbols=["process_command_labeled_block"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_unlabeled_block"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_labeled_control"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_unlabeled_control"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_leave"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_iterate"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_open"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_fetch"],
        ),
        ms_parser.create_rule(
            symbols=["process_command_close"],
        )
    ]
)

# 处理命令：执行语句
PROCESS_COMMAND_STATEMENT = ms_parser.create_group(
    name="process_command_statement",
    rules=[
        ms_parser.create_rule(
            symbols=["sql_statement"],
            action=lambda x: ast.ProcessCommandStatement(
                statement=x[0]
            )
        )
    ]
)

# 处理命令：返回表达式结果
PROCESS_COMMAND_RETURN = ms_parser.create_group(
    name="process_command_return",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RETURN, "expr"],
            action=lambda x: ast.ProcessCommandReturn(expression=x[1])
        )
    ]
)

# 处理命令：IF 语句
PROCESS_COMMAND_IF = ms_parser.create_group(
    name="process_command_if",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_IF,  # 0
                "expr",  # 1
                TType.KEYWORD_THEN,  # 2
                "process_command_list",  # 3
                "process_command_opt_elseif_list",  # 4
                "process_command_opt_else",  # 5
                TType.KEYWORD_END,  # 6
                TType.KEYWORD_IF  # 7
            ],
            action=lambda x: ast.ProcessCommandIf(
                condition_tuple_list=[ast.ProcessCommandConditionTuple(condition=x[1], statements=x[3])] + x[4],
                else_statements=x[5]
            )
        )
    ]
)

# 处理命令中可选的 ELSEIF 子句的列表
PROCESS_COMMAND_OPT_ELSEIF_LIST = ms_parser.create_group(
    name="process_command_opt_elseif_list",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_elseif_list"],
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 处理命令中的 ELSEIF 子句的列表
PROCESS_COMMAND_ELSEIF_LIST = ms_parser.create_group(
    name="process_command_elseif_list",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_elseif_list", "process_command_elseif"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["process_command_elseif"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 处理命令中的 ELSEIF 子句
PROCESS_COMMAND_ELSEIF = ms_parser.create_group(
    name="process_command_elseif",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ELSEIF,
                "expr",
                TType.KEYWORD_THEN,
                "process_command_list",
            ],
            action=lambda x: ast.ProcessCommandConditionTuple(condition=x[1], statements=x[3])
        )
    ]
)

# 处理命令中可选的 ELSE 子句
PROCESS_COMMAND_OPT_ELSE = ms_parser.create_group(
    name="process_command_opt_else",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ELSE, "process_command_list"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 处理命令：`CASE` 语句
PROCESS_COMMAND_CASE = ms_parser.create_group(
    name="process_command_case",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CASE,  # 0
                "opt_expr",  # 1
                "process_command_when_clause_list",  # 2
                "process_command_opt_else",  # 3
                TType.KEYWORD_END,  # 4
                TType.KEYWORD_CASE  # 5
            ],
            action=lambda x: ast.ProcessCommandCase(
                expression=x[1],
                condition_tuple_list=x[2],
                else_statements=x[3]
            )
        )
    ]
)

# 处理命令中的 `WHEN` 子句的列表
PROCESS_COMMAND_WHEN_CLAUSE_LIST = ms_parser.create_group(
    name="process_command_when_clause_list",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_when_clause_list", "process_command_when_clause"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["process_command_when_clause"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 处理命令中的 `WHEN` 子句
PROCESS_COMMAND_WHEN_CLAUSE = ms_parser.create_group(
    name="process_command_when_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_WHEN,
                "expr",
                TType.KEYWORD_THEN,
                "process_command_list",
            ],
            action=lambda x: ast.ProcessCommandConditionTuple(condition=x[1], statements=x[3])
        )
    ]
)

# 处理命令的声明表达式的列表
PROCESS_COMMAND_DECLARE_LIST = ms_parser.create_group(
    name="process_command_declare_list",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_declare_list", "process_command_declare", TType.OPERATOR_SEMICOLON],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["process_command_declare", TType.OPERATOR_SEMICOLON],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 处理命令的声明表达式
PROCESS_COMMAND_DECLARE = ms_parser.create_group(
    name="process_command_declare",
    rules=[
        # 声明变量：DECLARE sp_decl_idents type opt_collate sp_opt_default
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_DECLARE,  # 0
                "ident_list",  # 1
                "field_type",  # 2
                "opt_collate",  # 3
                "opt_default_expr"  # 4
            ],
            action=lambda x: ast.ProcessCommandDeclareVariable(
                identifier_list=x[1],
                field_type=x[2],
                collate_name=x[3],
                default_expression=x[4]
            )
        ),
        # 声明条件：DECLARE ident CONDITION FOR sp_cond
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_DECLARE,  # 0
                "ident",  # 1
                TType.KEYWORD_CONDITION,  # 2
                TType.KEYWORD_FOR,  # 3
                "process_command_condition"  # 4
            ],
            action=lambda x: ast.ProcessCommandDeclareCondition(
                condition_name=x[1].get_str_value(),
                condition_value=x[4]
            )
        ),
        # 声明处理器：DECLARE sp_handler_type HANDLER FOR sp_hcond_list sp_proc_stmt
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_DECLARE,  # 0
                "handler_type",  # 1
                TType.KEYWORD_HANDLER,  # 2
                TType.KEYWORD_FOR,  # 3
                "process_command_handler_condition_list",  # 4
                "process_command"  # 5
            ],
            action=lambda x: ast.ProcessCommandDeclareHandler(
                handler_type=x[1],
                condition_list=x[4],
                statement=x[5]
            )
        ),
        # 声明游标：DECLARE ident CURSOR FOR select_stmt
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_DECLARE,  # 0
                "ident",  # 1
                TType.KEYWORD_CURSOR,  # 2
                TType.KEYWORD_FOR,  # 3
                "select_statement"  # 4
            ],
            action=lambda x: ast.ProcessCommandDeclareCursor(
                cursor_name=x[1].get_str_value(),
                select_statement=x[4]
            )
        )
    ]
)

# 处理命令中的处理器条件值的列表
PROCESS_COMMAND_HANDLER_CONDITION_LIST = ms_parser.create_group(
    name="process_command_handler_condition_list",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_handler_condition_list", TType.OPERATOR_COMMA,
                     "process_command_handler_condition"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["process_command_handler_condition"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 处理命令中的处理器条件值
PROCESS_COMMAND_HANDLER_CONDITION = ms_parser.create_group(
    name="process_command_handler_condition",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_condition"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: ast.ProcessCommandConditionValueIdent(identifier=x[0].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQLWARNING],
            action=lambda x: ast.ProcessCommandConditionValueSqlWarning()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, TType.KEYWORD_FOUND],
            action=lambda x: ast.ProcessCommandConditionValueNotFound()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQLEXCEPTION],
            action=lambda x: ast.ProcessCommandConditionValueSqlException()
        )
    ]
)

# 处理命令中的条件值
PROCESS_COMMAND_CONDITION = ms_parser.create_group(
    name="process_command_condition",
    rules=[
        ms_parser.create_rule(
            symbols=["num_literal_or_hex"],
            action=lambda x: ast.ProcessCommandConditionValueNumber(error_number=x[0].value)
        ),
        ms_parser.create_rule(
            symbols=["sql_state"],
            action=lambda x: ast.ProcessCommandConditionValueSqlState(sql_state=x[0])
        )
    ]
)

# 处理命令：带标签的代码块
PROCESS_COMMAND_LABELED_BLOCK = ms_parser.create_group(
    name="process_command_labeled_block",
    rules=[
        ms_parser.create_rule(
            symbols=[
                "label_ident",
                TType.OPERATOR_COLON,
                "process_command_block",
                "opt_label_ident"
            ],
            action=lambda x: ast.ProcessCommandLabeledBlock(
                begin_label=x[0].get_str_value(),
                block_content=x[2],
                end_label=x[3]
            )
        )
    ]
)

# 处理命令：不带标签的代码块
PROCESS_COMMAND_UNLABELED_BLOCK = ms_parser.create_group(
    name="process_command_unlabeled_block",
    rules=[
        ms_parser.create_rule(
            symbols=["process_command_block"],
            action=lambda x: ast.ProcessCommandUnlabeledBlock(block_content=x[0])
        )
    ]
)

# 处理命令中的代码块内容
PROCESS_COMMAND_BLOCK = ms_parser.create_group(
    name="process_command_block",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_BEGIN,
                "process_command_declare_list",
                "process_command_list",
                TType.KEYWORD_END
            ],
            action=lambda x: ast.ProcessCommandBlock(
                declare_list=x[1],
                statement_list=x[2]
            )
        )
    ]
)

# 处理命令：带标签的控制语句
PROCESS_COMMAND_LABELED_CONTROL = ms_parser.create_group(
    name="process_command_labeled_control",
    rules=[
        ms_parser.create_rule(
            symbols=[
                "label_ident",
                TType.OPERATOR_COLON,
                "process_command_unlabeled_control",
                "opt_label_ident"
            ],
            action=lambda x: ast.ProcessCommandLabeledControl(
                begin_label=x[0].get_str_value(),
                control_statement=x[2],
                end_label=x[3]
            )
        )
    ]
)

# 处理命令：不带标签的控制语句
PROCESS_COMMAND_UNLABELED_CONTROL = ms_parser.create_group(
    name="process_command_unlabeled_control",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_LOOP,
                "process_command_list",
                TType.KEYWORD_END,
                TType.KEYWORD_LOOP
            ],
            action=lambda x: ast.ProcessCommandLoop(statement_list=x[1])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_WHILE,
                "expr",
                TType.KEYWORD_DO,
                "process_command_list",
                TType.KEYWORD_END,
                TType.KEYWORD_WHILE
            ],
            action=lambda x: ast.ProcessCommandWhile(condition=x[1], statement_list=x[3])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_REPEAT,
                "process_command_list",
                TType.KEYWORD_UNTIL,
                "expr",
                TType.KEYWORD_END,
                TType.KEYWORD_REPEAT
            ],
            action=lambda x: ast.ProcessCommandRepeat(statement_list=x[1], condition=x[3])
        )
    ]
)

# 处理命令：`LEAVE` 语句
PROCESS_COMMAND_LEAVE = ms_parser.create_group(
    name="process_command_leave",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LEAVE, "label_ident"],
            action=lambda x: ast.ProcessCommandLeave(label_name=x[1].get_str_value())
        )
    ]
)

# 处理命令：`ITERATE` 语句
PROCESS_COMMAND_ITERATE = ms_parser.create_group(
    name="process_command_iterate",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ITERATE, "label_ident"],
            action=lambda x: ast.ProcessCommandIterate(label_name=x[1].get_str_value())
        )
    ]
)

# 处理命令：`OPEN` 游标语句
PROCESS_COMMAND_OPEN = ms_parser.create_group(
    name="process_command_open",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OPEN, "ident"],
            action=lambda x: ast.ProcessCommandOpen(cursor_name=x[1].get_str_value())
        )
    ]
)

# 处理命令：`FETCH` 游标语句
PROCESS_COMMAND_FETCH = ms_parser.create_group(
    name="process_command_fetch",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_FETCH,
                "keyword_next_from_or_from",
                "ident",
                TType.KEYWORD_INTO,
                "ident_list"
            ],
            action=lambda x: ast.ProcessCommandFetch(
                cursor_name=x[2].get_str_value(),
                variable_list=x[4]
            )
        )
    ]
)

# 处理命令：`CLOSE` 游标语句
PROCESS_COMMAND_CLOSE = ms_parser.create_group(
    name="process_command_close",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CLOSE, "ident"],
            action=lambda x: ast.ProcessCommandClose(cursor_name=x[1].get_str_value())
        )
    ]
)
