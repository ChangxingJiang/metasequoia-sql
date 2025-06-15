"""
GRANT 和 REVOKE 语句（grant and revoke statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "GRANT_STATEMENT",
    "REVOKE_STATEMENT",
    "ROLE_OR_PRIVILEGE_LIST",
    "ROLE_OR_PRIVILEGE",
    "OPT_WITH_ROLES",
    "OPT_EXCEPT_ROLE_LIST",
    "OPT_GRANT_AS",
    "GRANT_IDENTIFIER",
]

# `GRANT` 语句
GRANT_STATEMENT = ms_parser.create_group(
    name="grant_statement",
    rules=[
        # GRANT role_or_privilege_list TO user_list opt_with_admin_option
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GRANT, "role_or_privilege_list", TType.KEYWORD_TO, "user_name_list",
                     "opt_keyword_with_admin_option"],
            action=lambda x: ast.GrantRolesStatement(roles=x[1], users=x[3], with_admin_option=x[4])
        ),
        # GRANT role_or_privilege_list ON opt_acl_type grant_ident TO user_list grant_options opt_grant_as
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GRANT, "role_or_privilege_list", TType.KEYWORD_ON, "opt_acl_type",
                     "grant_identifier", TType.KEYWORD_TO, "user_name_list", "opt_keyword_grant_option",
                     "opt_grant_as"],
            action=lambda x: ast.GrantPrivilegesStatement(privileges=x[1], acl_type=x[3], grant_identifier=x[4],
                                                          users=x[6], with_grant_option=x[7], grant_as=x[8])
        ),
        # GRANT ALL [PRIVILEGES] ON opt_acl_type grant_ident TO user_list grant_options opt_grant_as
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GRANT, TType.KEYWORD_ALL, "opt_keyword_privileges", TType.KEYWORD_ON, "opt_acl_type",
                     "grant_identifier", TType.KEYWORD_TO, "user_name_list", "opt_keyword_grant_option",
                     "opt_grant_as"],
            action=lambda x: ast.GrantAllPrivilegesStatement(acl_type=x[4], grant_identifier=x[5], users=x[7],
                                                             with_grant_option=x[8], grant_as=x[9])
        ),
        # GRANT PROXY ON user TO user_list opt_grant_option
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GRANT, TType.KEYWORD_PROXY, TType.KEYWORD_ON, "user_name", TType.KEYWORD_TO,
                     "user_name_list", "opt_keyword_grant_option"],
            action=lambda x: ast.GrantProxyStatement(proxy_user=x[3], users=x[5], with_grant_option=x[6])
        )
    ]
)

# `REVOKE` 语句
REVOKE_STATEMENT = ms_parser.create_group(
    name="revoke_statement",
    rules=[
        # REVOKE [IF EXISTS] role_or_privilege_list FROM user_list opt_ignore_unknown_user
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REVOKE, "opt_keyword_if_exists", "role_or_privilege_list", TType.KEYWORD_FROM,
                     "user_name_list", "opt_keyword_ignore_unknown_user"],
            action=lambda x: ast.RevokeRolesStatement(if_exists=x[1], roles=x[2], users=x[4], ignore_unknown_user=x[5])
        ),
        # REVOKE [IF EXISTS] role_or_privilege_list ON opt_acl_type grant_ident FROM user_list opt_ignore_unknown_user
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REVOKE, "opt_keyword_if_exists", "role_or_privilege_list", TType.KEYWORD_ON,
                     "opt_acl_type", "grant_identifier", TType.KEYWORD_FROM, "user_name_list",
                     "opt_keyword_ignore_unknown_user"],
            action=lambda x: ast.RevokePrivilegesStatement(if_exists=x[1], privileges=x[2], acl_type=x[4],
                                                           grant_identifier=x[5], users=x[7], ignore_unknown_user=x[8])
        ),
        # REVOKE [IF EXISTS] ALL [PRIVILEGES] ON opt_acl_type grant_ident FROM user_list opt_ignore_unknown_user
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REVOKE, "opt_keyword_if_exists", TType.KEYWORD_ALL, "opt_keyword_privileges",
                     TType.KEYWORD_ON, "opt_acl_type", "grant_identifier", TType.KEYWORD_FROM, "user_name_list",
                     "opt_keyword_ignore_unknown_user"],
            action=lambda x: ast.RevokeAllPrivilegesStatement(if_exists=x[1], acl_type=x[5], grant_identifier=x[6],
                                                              users=x[8], ignore_unknown_user=x[9])
        ),
        # REVOKE [IF EXISTS] ALL [PRIVILEGES], GRANT OPTION FROM user_list opt_ignore_unknown_user
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REVOKE, "opt_keyword_if_exists", TType.KEYWORD_ALL, "opt_keyword_privileges",
                     TType.OPERATOR_COMMA, TType.KEYWORD_GRANT, TType.KEYWORD_OPTION, TType.KEYWORD_FROM,
                     "user_name_list", "opt_keyword_ignore_unknown_user"],
            action=lambda x: ast.RevokeAllPrivilegesStatement(if_exists=x[1], acl_type=ast.EnumAclType.TABLE,
                                                              grant_identifier=ast.GrantIdentifierGlobal(), users=x[8],
                                                              ignore_unknown_user=x[9])
        ),
        # REVOKE [IF EXISTS] PROXY ON user FROM user_list opt_ignore_unknown_user
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REVOKE, "opt_keyword_if_exists", TType.KEYWORD_PROXY, TType.KEYWORD_ON, "user_name",
                     TType.KEYWORD_FROM, "user_name_list", "opt_keyword_ignore_unknown_user"],
            action=lambda x: ast.RevokeProxyStatement(if_exists=x[1], proxy_user=x[4], users=x[6],
                                                      ignore_unknown_user=x[7])
        )
    ]
)

# 角色或权限列表
ROLE_OR_PRIVILEGE_LIST = ms_parser.create_group(
    name="role_or_privilege_list",
    rules=[
        ms_parser.create_rule(
            symbols=["role_or_privilege"],
            action=ms_parser.template.action.LIST_INIT_0
        ),
        ms_parser.create_rule(
            symbols=["role_or_privilege_list", TType.OPERATOR_COMMA, "role_or_privilege"],
            action=ms_parser.template.action.LIST_APPEND_2
        )
    ]
)

# 角色或权限
ROLE_OR_PRIVILEGE = ms_parser.create_group(
    name="role_or_privilege",
    rules=[
        # role_ident_or_text opt_column_list - 对应 RoleOrDynamicPrivilege 或 DynamicPrivilege
        ms_parser.create_rule(
            symbols=["role_ident_or_text", "opt_ident_list_parens"],
            action=lambda x: ast.RoleOrDynamicPrivilege(privilege_name=x[0], column_list=x[1])
        ),
        # role_ident_or_text @ ident_or_text - 对应 RoleAtHost
        ms_parser.create_rule(
            symbols=["role_ident_or_text", TType.OPERATOR_AT, "ident_or_text"],
            action=lambda x: ast.RoleAtHost(role_name=x[0], host_name=x[2].get_str_value())
        ),
        # 静态权限
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SELECT, "opt_ident_list_parens"],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.SELECT, column_list=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INSERT, "opt_ident_list_parens"],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.INSERT, column_list=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UPDATE, "opt_ident_list_parens"],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.UPDATE, column_list=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REFERENCES, "opt_ident_list_parens"],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.REFERENCES,
                                                 column_list=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DELETE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.DELETE, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USAGE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.USAGE, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEX],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.INDEX, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.ALTER, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.CREATE, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.DROP, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXECUTE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.EXECUTE, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELOAD],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.RELOAD, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHUTDOWN],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.SHUTDOWN, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PROCESS],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.PROCESS, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FILE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.FILE, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GRANT, TType.KEYWORD_OPTION],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.GRANT, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_DATABASES],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.SHOW_DB, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUPER],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.SUPER, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_TEMPORARY, TType.KEYWORD_TABLES],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.CREATE_TMP,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCK, TType.KEYWORD_TABLES],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.LOCK_TABLES,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATION, TType.KEYWORD_SLAVE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.REPL_SLAVE,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATION, TType.KEYWORD_CLIENT],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.REPL_CLIENT,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_VIEW],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.CREATE_VIEW,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_VIEW],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.SHOW_VIEW, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_ROUTINE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.CREATE_ROUTINE,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_ROUTINE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.ALTER_ROUTINE,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_USER],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.CREATE_USER,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EVENT],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.EVENT, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TRIGGER],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.TRIGGER, column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_TABLESPACE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.CREATE_TABLESPACE,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_ROLE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.CREATE_ROLE,
                                                 column_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_ROLE],
            action=lambda x: ast.StaticPrivilege(privilege_type=ast.EnumStaticPrivilegeType.DROP_ROLE, column_list=None)
        )
    ]
)

# 可选的 `WITH ROLES` 子句
OPT_WITH_ROLES = ms_parser.create_group(
    name="opt_with_roles",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.WithRoleNone()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_ROLE, "user_name_list"],
            action=lambda x: ast.WithRoleList(role_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_ROLE, TType.KEYWORD_ALL, "opt_except_role_list"],
            action=lambda x: ast.WithRoleAll(except_role_list=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_ROLE, TType.KEYWORD_NONE],
            action=lambda x: ast.WithRoleNone()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_ROLE, TType.KEYWORD_DEFAULT],
            action=lambda x: ast.WithRoleDefault()
        )
    ]
)

# 可选的排除角色列表
OPT_EXCEPT_ROLE_LIST = ms_parser.create_group(
    name="opt_except_role_list",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXCEPT, "user_name_list"],
            action=lambda x: x[1]
        )
    ]
)

# 可选的 `GRANT AS` 子句
OPT_GRANT_AS = ms_parser.create_group(
    name="opt_grant_as",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS, "user_name", "opt_with_roles"],
            action=lambda x: x[1]  # TODO MySQL 后半部分没有意义，后续可以考虑补充
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# `GRANT` 语句中的标识符
GRANT_IDENTIFIER = ms_parser.create_group(
    name="grant_identifier",
    rules=[
        # * - 当前数据库的所有表
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_STAR],
            action=lambda x: ast.GrantIdentifierDatabase(database_name=None)
        ),
        # ident.* - 指定数据库的所有表
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, TType.OPERATOR_STAR],
            action=lambda x: ast.GrantIdentifierDatabase(database_name=x[0].get_str_value())
        ),
        # *.* - 全局权限
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_STAR, TType.OPERATOR_DOT, TType.OPERATOR_STAR],
            action=lambda x: ast.GrantIdentifierGlobal()
        ),
        # table_ident - 表权限
        ms_parser.create_rule(
            symbols=["identifier"],
            action=lambda x: ast.GrantIdentifierTable(table_identifier=x[0])
        )
    ]
)
