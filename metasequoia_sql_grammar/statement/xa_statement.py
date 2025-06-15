"""
XA 事务语句（XA statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "XA_STATEMENT",
    "XID",
]

# XA 事务语句
XA_STATEMENT = ms_parser.create_group(
    name="xa_statement",
    rules=[
        # XA {BEGIN|START} xid [JOIN|RESUME]
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_XA, "keyword_begin_or_start", "xid", "opt_xa_join_or_resume"],
            action=lambda x: ast.XaStartStatement(xid=x[2], join_or_resume=x[3])
        ),
        # XA END xid [SUSPEND [FOR MIGRATE]]
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_XA, TType.KEYWORD_END, "xid", "opt_xa_suspend"],
            action=lambda x: ast.XaEndStatement(xid=x[2], suspend=x[3])
        ),
        # XA PREPARE xid
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_XA, TType.KEYWORD_PREPARE, "xid"],
            action=lambda x: ast.XaPrepareStatement(xid=x[2])
        ),
        # XA COMMIT xid [ONE PHASE]
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_XA, TType.KEYWORD_COMMIT, "xid", "opt_keyword_one_phase"],
            action=lambda x: ast.XaCommitStatement(xid=x[2], one_phase=x[3])
        ),
        # XA ROLLBACK xid
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_XA, TType.KEYWORD_ROLLBACK, "xid"],
            action=lambda x: ast.XaRollbackStatement(xid=x[2])
        ),
        # XA RECOVER [CONVERT XID]
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_XA, TType.KEYWORD_RECOVER, "opt_keyword_convert_xid"],
            action=lambda x: ast.XaRecoverStatement(convert_xid=x[2])
        )
    ]
)

# XA 事务标识符
XID = ms_parser.create_group(
    name="xid",
    rules=[
        # text_string
        ms_parser.create_rule(
            symbols=["text_string"],
            action=lambda x: ast.XaId(gtrid=x[0].get_str_value())
        ),
        # text_string ',' text_string  
        ms_parser.create_rule(
            symbols=["text_string", TType.OPERATOR_COMMA, "text_string"],
            action=lambda x: ast.XaId(gtrid=x[0].get_str_value(), bqual=x[2].get_str_value())
        ),
        # text_string ',' text_string ',' ulong_num
        ms_parser.create_rule(
            symbols=["text_string", TType.OPERATOR_COMMA, "text_string", TType.OPERATOR_COMMA, "num_literal"],
            action=lambda x: ast.XaId(gtrid=x[0].get_str_value(), bqual=x[2].get_str_value(), format_id=x[4].value)
        )
    ]
)
