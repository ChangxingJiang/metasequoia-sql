"""
SHOW 语句（show statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.clause.limit_clause import LimitClause
    from metasequoia_sql.ast.basic.fixed_enum import EnumShowCommandType, EnumProfileType, EnumVariableType
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.literal import UserName

__all__ = [
    # SHOW 语句基类
    "ShowWildOrWhereBaseStatement",

    # SHOW 语句
    "ShowBinaryLogStatusStatement",
    "ShowBinaryLogsStatement",
    "ShowBinlogEventsStatement",
    "ShowCharSetStatement",
    "ShowCollationStatement",
    "ShowColumnsStatement",
    "ShowCountErrorsStatement",
    "ShowCountWarningsStatement",
    "ShowCreateDatabaseStatement",
    "ShowCreateEventStatement",
    "ShowCreateFunctionStatement",
    "ShowCreateProcedureStatement",
    "ShowCreateTableStatement",
    "ShowCreateTriggerStatement",
    "ShowCreateUserStatement",
    "ShowCreateViewStatement",
    "ShowDatabasesStatement",
    "ShowEngineLogsStatement",
    "ShowEngineMutexStatement",
    "ShowEngineStatusStatement",
    "ShowEnginesStatement",
    "ShowErrorsStatement",
    "ShowEventsStatement",
    "ShowFunctionCodeStatement",
    "ShowFunctionStatusStatement",
    "ShowGrantsStatement",
    "ShowKeysStatement",
    "ShowMasterStatusStatement",
    "ShowOpenTablesStatement",
    "ShowParseTreeStatement",
    "ShowPluginsStatement",
    "ShowPrivilegesStatement",
    "ShowProcedureCodeStatement",
    "ShowProcedureStatusStatement",
    "ShowProcesslistStatement",
    "ShowProfileStatement",
    "ShowProfilesStatement",
    "ShowRelaylogEventsStatement",
    "ShowReplicaStatusStatement",
    "ShowReplicasStatement",
    "ShowStatusStatement",
    "ShowTableStatusStatement",
    "ShowTablesStatement",
    "ShowTriggersStatement",
    "ShowWarningsStatement",
    "ShowVariablesStatement",

    # 临时对象
    "TempWildOrWhere",
]


class ShowWildOrWhereBaseStatement(Statement):
    """仅包含可选的通配符或 WHERE 子句的 SHOW 语句基类"""

    __slots__ = (
        "_wild",
        "_where"
    )

    def __init__(self, wild: Optional[str] = None, where: Optional[Expression] = None):
        self._wild = wild
        self._where = where

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowBinaryLogStatusStatement(Statement):
    """SHOW BINARY LOG STATUS 语句"""


class ShowBinaryLogsStatement(Statement):
    """SHOW BINARY LOGS 语句"""


class ShowBinlogEventsStatement(Statement):
    """SHOW BINLOG EVENTS 语句"""

    __slots__ = (
        "_in_file",
        "_from_event",
        "_limit_clause"
    )

    def __init__(self,
                 in_file: Optional[str],
                 from_event: Optional[int],
                 limit_clause: Optional["LimitClause"]):
        self._in_file = in_file
        self._from_event = from_event
        self._limit_clause = limit_clause

    @property
    def in_file(self) -> Optional[str]:
        return self._in_file

    @property
    def from_event(self) -> Optional[int]:
        return self._from_event

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause


class ShowCharSetStatement(ShowWildOrWhereBaseStatement):
    """SHOW CHARACTER SET 语句"""


class ShowCollationStatement(ShowWildOrWhereBaseStatement):
    """SHOW COLLATION 语句"""


class ShowColumnsStatement(Statement):
    """SHOW COLUMNS 语句"""

    __slots__ = (
        "_command_type",
        "_table_ident",
        "_schema_name",
        "_wild",
        "_where"
    )

    def __init__(self,
                 command_type: "EnumShowCommandType",
                 table_ident: "Identifier",
                 schema_name: Optional[str],
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        self._command_type = command_type
        self._table_ident = table_ident
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def command_type(self) -> "EnumShowCommandType":
        return self._command_type

    @property
    def table_ident(self) -> "Identifier":
        return self._table_ident

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowCountErrorsStatement(Statement):
    """SHOW COUNT ERRORS 语句"""


class ShowCountWarningsStatement(Statement):
    """SHOW COUNT WARNINGS 语句"""


class ShowCreateDatabaseStatement(Statement):
    """SHOW CREATE DATABASE 语句"""

    __slots__ = (
        "_if_not_exists",
        "_database_name"
    )

    def __init__(self, if_not_exists: bool, database_name: str):
        self._if_not_exists = if_not_exists
        self._database_name = database_name

    @property
    def if_not_exists(self) -> bool:
        return self._if_not_exists

    @property
    def database_name(self) -> str:
        return self._database_name


class ShowCreateEventStatement(Statement):
    """SHOW CREATE EVENT 语句"""

    __slots__ = (
        "_event_name"
    )

    def __init__(self, event_name: "Identifier"):
        self._event_name = event_name

    @property
    def event_name(self) -> "Identifier":
        return self._event_name


class ShowCreateFunctionStatement(Statement):
    """SHOW CREATE FUNCTION 语句"""

    __slots__ = (
        "_function_name"
    )

    def __init__(self, function_name: "Identifier"):
        self._function_name = function_name

    @property
    def function_name(self) -> "Identifier":
        return self._function_name


class ShowCreateProcedureStatement(Statement):
    """SHOW CREATE PROCEDURE 语句"""

    __slots__ = (
        "_procedure_name"
    )

    def __init__(self, procedure_name: "Identifier"):
        self._procedure_name = procedure_name

    @property
    def procedure_name(self) -> "Identifier":
        return self._procedure_name


class ShowCreateTableStatement(Statement):
    """SHOW CREATE TABLE 语句"""

    __slots__ = (
        "_table_ident"
    )

    def __init__(self, table_ident: "Identifier"):
        self._table_ident = table_ident

    @property
    def table_ident(self) -> "Identifier":
        return self._table_ident


class ShowCreateTriggerStatement(Statement):
    """SHOW CREATE TRIGGER 语句"""

    __slots__ = (
        "_trigger_name"
    )

    def __init__(self, trigger_name: "Identifier"):
        self._trigger_name = trigger_name

    @property
    def trigger_name(self) -> "Identifier":
        return self._trigger_name


class ShowCreateUserStatement(Statement):
    """SHOW CREATE USER 语句"""

    __slots__ = (
        "_user_name"
    )

    def __init__(self, user_name: "UserName"):
        self._user_name = user_name

    @property
    def user_name(self) -> "UserName":
        return self._user_name


class ShowCreateViewStatement(Statement):
    """SHOW CREATE VIEW 语句"""

    __slots__ = (
        "_view_name"
    )

    def __init__(self, view_name: "Identifier"):
        self._view_name = view_name

    @property
    def view_name(self) -> "Identifier":
        return self._view_name


class ShowDatabasesStatement(ShowWildOrWhereBaseStatement):
    """SHOW DATABASES 语句"""


class ShowEngineLogsStatement(Statement):
    """SHOW ENGINE LOGS 语句"""

    __slots__ = (
        "_engine_name"
    )

    def __init__(self, engine_name: Optional[str]):
        self._engine_name = engine_name

    @property
    def engine_name(self) -> Optional[str]:
        return self._engine_name


class ShowEngineMutexStatement(Statement):
    """SHOW ENGINE MUTEX 语句"""

    __slots__ = (
        "_engine_name"
    )

    def __init__(self, engine_name: Optional[str]):
        self._engine_name = engine_name

    @property
    def engine_name(self) -> Optional[str]:
        return self._engine_name


class ShowEngineStatusStatement(Statement):
    """SHOW ENGINE STATUS 语句"""

    __slots__ = (
        "_engine_name"
    )

    def __init__(self, engine_name: Optional[str]):
        self._engine_name = engine_name

    @property
    def engine_name(self) -> Optional[str]:
        return self._engine_name


class ShowEnginesStatement(Statement):
    """SHOW ENGINES 语句"""


class ShowErrorsStatement(Statement):
    """SHOW ERRORS 语句"""

    __slots__ = (
        "_limit_clause"
    )

    def __init__(self, limit_clause: Optional["LimitClause"]):
        self._limit_clause = limit_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause


class ShowEventsStatement(Statement):
    """SHOW EVENTS 语句"""

    __slots__ = (
        "_schema_name",
        "_wild",
        "_where"
    )

    def __init__(self,
                 schema_name: Optional[str] = None,
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowFunctionCodeStatement(Statement):
    """SHOW FUNCTION CODE 语句"""

    __slots__ = (
        "_function_name"
    )

    def __init__(self, function_name: "Identifier"):
        self._function_name = function_name

    @property
    def function_name(self) -> "Identifier":
        return self._function_name


class ShowFunctionStatusStatement(ShowWildOrWhereBaseStatement):
    """SHOW FUNCTION STATUS 语句"""


class ShowGrantsStatement(Statement):
    """SHOW GRANTS 语句"""

    __slots__ = (
        "_for_user",
        "_using_user_list"
    )

    def __init__(self, for_user: Optional["UserName"] = None, using_user_list: List["UserName"] = None):
        self._for_user = for_user
        self._using_user_list = using_user_list

    @property
    def for_user(self) -> Optional["UserName"]:
        return self._for_user

    @property
    def using_user_list(self) -> List["UserName"]:
        return self._using_user_list


class ShowKeysStatement(Statement):
    """SHOW KEYS 语句"""

    __slots__ = (
        "_is_extended",
        "_table_ident",
        "_schema_name",
        "_where_clause"
    )

    def __init__(self,
                 is_extended: bool,
                 table_ident: "Identifier",
                 schema_name: Optional[str],
                 where_clause: Optional[Expression]):
        self._is_extended = is_extended
        self._table_ident = table_ident
        self._schema_name = schema_name
        self._where_clause = where_clause

    @property
    def is_extended(self) -> bool:
        return self._is_extended

    @property
    def table_ident(self) -> "Identifier":
        return self._table_ident

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def where_clause(self) -> Optional[Expression]:
        return self._where_clause


class ShowMasterStatusStatement(Statement):
    """SHOW MASTER STATUS 语句"""


class ShowOpenTablesStatement(Statement):
    """SHOW OPEN TABLES 语句"""

    __slots__ = (
        "_schema_name",
        "_wild",
        "_where"
    )

    def __init__(self, schema_name: Optional[str], wild: Optional[str], where: Optional[Expression]):
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowParseTreeStatement(Statement):
    """SHOW PARSE TREE 语句"""

    __slots__ = (
        "_statement"
    )

    def __init__(self, statement: Statement):
        self._statement = statement

    @property
    def statement(self) -> Statement:
        return self._statement


class ShowPluginsStatement(Statement):
    """SHOW PLUGINS 语句"""


class ShowPrivilegesStatement(Statement):
    """SHOW PRIVILEGES 语句"""


class ShowProcedureCodeStatement(Statement):
    """SHOW PROCEDURE CODE 语句"""

    __slots__ = (
        "_procedure_name"
    )

    def __init__(self, procedure_name: "Identifier"):
        self._procedure_name = procedure_name

    @property
    def procedure_name(self) -> "Identifier":
        return self._procedure_name


class ShowProcedureStatusStatement(ShowWildOrWhereBaseStatement):
    """SHOW PROCEDURE STATUS 语句"""


class ShowProcesslistStatement(Statement):
    """SHOW PROCESSLIST 语句"""

    __slots__ = (
        "_is_full"
    )

    def __init__(self, is_full: bool):
        self._is_full = is_full

    @property
    def is_full(self) -> bool:
        return self._is_full


class ShowProfileStatement(Statement):
    """SHOW PROFILE 语句"""

    __slots__ = (
        "_profile_type",
        "_thread_id",
        "_limit_clause",
    )

    def __init__(self, profile_type: "EnumProfileType", thread_id: Optional[int], limit_clause: "LimitClause"):
        self._profile_type = profile_type
        self._thread_id = thread_id
        self._limit_clause = limit_clause

    @property
    def profile_type(self) -> "EnumProfileType":
        return self._profile_type

    @property
    def thread_id(self) -> Optional[int]:
        return self._thread_id

    @property
    def limit_clause(self) -> "LimitClause":
        return self._limit_clause


class ShowProfilesStatement(Statement):
    """SHOW PROFILES 语句"""


class ShowRelaylogEventsStatement(Statement):
    """SHOW RELAYLOG EVENTS 语句"""

    __slots__ = (
        "_binlog_in",
        "_binlog_from",
        "_limit_clause",
        "_channel_name"
    )

    def __init__(self,
                 binlog_in: Optional[str],
                 binlog_from: Optional[int],
                 limit_clause: Optional["LimitClause"],
                 channel_name: Optional[str]):
        self._binlog_in = binlog_in
        self._binlog_from = binlog_from
        self._limit_clause = limit_clause
        self._channel_name = channel_name

    @property
    def binlog_in(self) -> Optional[str]:
        return self._binlog_in

    @property
    def binlog_from(self) -> Optional[int]:
        return self._binlog_from

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause

    @property
    def channel_name(self) -> Optional[str]:
        return self._channel_name


class ShowReplicaStatusStatement(Statement):
    """SHOW REPLICA STATUS 语句"""

    __slots__ = (
        "_channel_name"
    )

    def __init__(self, channel_name: Optional[str]):
        self._channel_name = channel_name

    @property
    def channel_name(self) -> Optional[str]:
        return self._channel_name


class ShowReplicasStatement(Statement):
    """SHOW REPLICAS 语句"""


class ShowStatusStatement(Statement):
    """SHOW STATUS 语句"""

    __slots__ = (
        "_variable_type",
        "_wild",
        "_where"
    )

    def __init__(self,
                 variable_type: "EnumVariableType",
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        self._variable_type = variable_type
        self._wild = wild
        self._where = where

    @property
    def variable_type(self) -> "EnumVariableType":
        return self._variable_type

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowTableStatusStatement(Statement):
    """SHOW TABLE STATUS 语句"""

    __slots__ = (
        "_schema_name",
        "_wild",
        "_where"
    )

    def __init__(self,
                 schema_name: Optional[str] = None,
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowTablesStatement(Statement):
    """SHOW TABLES 语句"""

    __slots__ = (
        "_command_type",
        "_schema_name",
        "_wild",
        "_where"
    )

    def __init__(self,
                 command_type: "EnumShowCommandType",
                 schema_name: Optional[str] = None,
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        self._command_type = command_type
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def command_type(self) -> "EnumShowCommandType":
        return self._command_type

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowTriggersStatement(Statement):
    """SHOW TRIGGERS 语句"""

    def __init__(self,
                 is_full: bool,
                 schema_name: Optional[str],
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        self._is_full = is_full
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def is_full(self) -> bool:
        return self._is_full

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class ShowWarningsStatement(Statement):
    """SHOW WARNINGS 语句"""

    __slots__ = (
        "_limit_clause"
    )

    def __init__(self, limit_clause: Optional["LimitClause"]):
        self._limit_clause = limit_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause


class ShowVariablesStatement(Statement):
    """SHOW VARIABLES 语句"""

    __slots__ = (
        "_variable_type",
        "_wild",
        "_where"
    )

    def __init__(self,
                 variable_type: "EnumVariableType",
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        self._variable_type = variable_type
        self._wild = wild
        self._where = where

    @property
    def variable_type(self) -> "EnumVariableType":
        return self._variable_type

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where


class TempWildOrWhere(Node):
    """【临时】通配符或 WHERE 子句"""

    __slots__ = (
        "_wild",
        "_where"
    )

    def __init__(self, wild: Optional[str] = None, where: Optional[Expression] = None):
        self._wild = wild
        self._where = where

    @property
    def wild(self) -> Optional[str]:
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        return self._where
