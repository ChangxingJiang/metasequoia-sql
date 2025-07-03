"""
KEYCACHE 和 PRELOAD 语句（keycache and preload statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "KEYCACHE_STATEMENT",
    "PRELOAD_STATEMENT",

    # 预加载键及列表
    "PRELOAD_LIST",
    "PRELOAD_KEYS",

    # 键缓存及列表
    "KEYCACHE_LIST",
    "ASSIGN_TO_KEYCACHE",

    # 管理分区
    "ADM_PARTITION",

    # 通用元素
    "OPT_CACHE_KEY_LIST",
]

# `CACHE INDEX` 语句
KEYCACHE_STATEMENT = ms_parser.create_group(
    name="keycache_statement",
    rules=[
        # CACHE INDEX keycache_list IN key_cache_name
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CACHE,  # 0
                TType.KEYWORD_INDEX,  # 1
                "keycache_list",  # 2
                TType.KEYWORD_IN,  # 3
                "ident_or_default",  # 4
            ],
            action=lambda x: ast.CacheIndexStatement(
                keycache_list=x[2],
                key_cache_name=x[4]
            )
        ),
        # CACHE INDEX table_ident adm_partition opt_cache_key_list IN key_cache_name
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CACHE,  # 0
                TType.KEYWORD_INDEX,  # 1
                "identifier",  # 2 (table_ident)
                "adm_partition",  # 3
                "opt_cache_key_list",  # 4
                TType.KEYWORD_IN,  # 5
                "ident_or_default",  # 6 (key_cache_name)
            ],
            action=lambda x: ast.CacheIndexPartitionsStatement(
                table_name=x[2],
                partition=x[3],
                cache_key_list=x[4],
                key_cache_name=x[6]
            )
        )
    ]
)

# `LOAD INDEX` 语句
PRELOAD_STATEMENT = ms_parser.create_group(
    name="preload_statement",
    rules=[
        # LOAD INDEX INTO CACHE table_ident adm_partition opt_cache_key_list opt_ignore_leaves
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_LOAD,  # 0
                TType.KEYWORD_INDEX,  # 1
                TType.KEYWORD_INTO,  # 2
                TType.KEYWORD_CACHE,  # 3
                "identifier",  # 4
                "adm_partition",  # 5
                "opt_cache_key_list",  # 6
                "opt_keyword_ignore_leaves",  # 7
            ],
            action=lambda x: ast.LoadIndexPartitionsStatement(
                table_name=x[4],
                partition=x[5],
                cache_key_list=x[6],
                ignore_leaves=x[7]
            )
        ),
        # LOAD INDEX INTO CACHE preload_list
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_LOAD,  # 0
                TType.KEYWORD_INDEX,  # 1
                TType.KEYWORD_INTO,  # 2
                TType.KEYWORD_CACHE,  # 3
                "preload_list",  # 4
            ],
            action=lambda x: ast.LoadIndexStatement(
                preload_list=x[4]
            )
        )
    ]
)

# 键缓存列表
KEYCACHE_LIST = ms_parser.create_group(
    name="keycache_list",
    rules=[
        ms_parser.create_rule(
            symbols=["assign_to_keycache"],
            action=ms_parser.template.action.LIST_INIT_0
        ),
        ms_parser.create_rule(
            symbols=["keycache_list", TType.OPERATOR_COMMA, "assign_to_keycache"],
            action=ms_parser.template.action.LIST_APPEND_2
        )
    ]
)

# 分配到键缓存
ASSIGN_TO_KEYCACHE = ms_parser.create_group(
    name="assign_to_keycache",
    rules=[
        ms_parser.create_rule(
            symbols=["identifier", "opt_cache_key_list"],
            action=lambda x: ast.AssignToKeycache(
                table_name=x[0],
                cache_key_list=x[1]
            )
        )
    ]
)

# 管理分区: PARTITION (all_or_alt_part_name_list)
ADM_PARTITION = ms_parser.create_group(
    name="adm_partition",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_PARTITION,  # 0
                TType.OPERATOR_LBRACE,  # 1
                "all_or_alt_part_name_list",  # 2
                TType.OPERATOR_RBRACE,  # 3
            ],
            action=lambda x: ast.AdmPartition(partition_list=x[2])
        )
    ]
)

# 预加载列表
PRELOAD_LIST = ms_parser.create_group(
    name="preload_list",
    rules=[
        ms_parser.create_rule(
            symbols=["preload_keys"],
            action=ms_parser.template.action.LIST_INIT_0
        ),
        ms_parser.create_rule(
            symbols=["preload_list", TType.OPERATOR_COMMA, "preload_keys"],
            action=ms_parser.template.action.LIST_APPEND_2
        )
    ]
)

# 预加载键
PRELOAD_KEYS = ms_parser.create_group(
    name="preload_keys",
    rules=[
        ms_parser.create_rule(
            symbols=["identifier", "opt_cache_key_list", "opt_keyword_ignore_leaves"],
            action=lambda x: ast.PreloadKeys(
                table_name=x[0],
                cache_key_list=x[1],
                ignore_leaves=x[2]
            )
        )
    ]
)

# 可选的缓存键列表
OPT_CACHE_KEY_LIST = ms_parser.create_group(
    name="opt_cache_key_list",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_keys_or_index", TType.OPERATOR_LBRACE, "opt_hint_key_name_list", TType.OPERATOR_RBRACE],
            action=lambda x: x[2]  # 返回 IndexHintClause
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)
