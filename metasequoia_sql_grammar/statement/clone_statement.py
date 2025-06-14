"""
CLONE 语句（clone statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CLONE_STATEMENT",
    "OPT_DATADIR_SSL",
]

# `CLONE` 语句
CLONE_STATEMENT = ms_parser.create_group(
    name="clone_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CLONE,  # 0
                TType.KEYWORD_LOCAL,  # 1
                TType.KEYWORD_DATA,  # 2
                TType.KEYWORD_DIRECTORY,  # 3
                "opt_equal",  # 4
                "text_literal_sys"  # 5
            ],
            action=lambda x: ast.CloneLocalStatement(data_directory=x[5])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CLONE,  # 0
                TType.KEYWORD_INSTANCE,  # 1
                TType.KEYWORD_FROM,  # 2
                "user_name",  # 3
                TType.OPERATOR_COLON,  # 4
                "num_literal_or_hex",  # 5
                TType.KEYWORD_IDENTIFIED,  # 6
                TType.KEYWORD_BY,  # 7
                "text_literal_sys",  # 8
                "opt_datadir_ssl"  # 9
            ],
            action=lambda x: ast.CloneInstanceStatement(user=x[3], port=x[5], password=x[8],
                                                        data_directory=x[9].data_directory, open_ssl=x[9].open_ssl)
        )
    ]
)

# `CLONE` 语句的临时数据目录和 SSL 选项信息
OPT_DATADIR_SSL = ms_parser.create_group(
    name="opt_datadir_ssl",
    rules=[
        ms_parser.create_rule(
            symbols=["open_ssl_type"],
            action=lambda x: ast.TempDatadirSsl(data_directory=None, open_ssl=x[0])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_DATA,  # 0
                TType.KEYWORD_DIRECTORY,  # 1
                "equal",  # 2
                "text_literal_sys",  # 3
                "open_ssl_type"  # 4
            ],
            action=lambda x: ast.TempDatadirSsl(data_directory=x[3], open_ssl=x[4])
        )
    ]
)
