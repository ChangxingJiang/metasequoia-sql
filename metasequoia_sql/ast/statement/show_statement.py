# pylint: disable=C0302

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
        """
        初始化 SHOW 语句基类

        Parameters
        ----------
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._wild = wild
        self._where = where

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
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
        """
        初始化 SHOW BINLOG EVENTS 语句

        Parameters
        ----------
        in_file : Optional[str]
            日志文件名
        from_event : Optional[int]
            起始事件位置
        limit_clause : Optional[LimitClause]
            LIMIT 子句
        """
        self._in_file = in_file
        self._from_event = from_event
        self._limit_clause = limit_clause

    @property
    def in_file(self) -> Optional[str]:
        """
        日志文件名

        Returns
        -------
        Optional[str]
            日志文件名
        """
        return self._in_file

    @property
    def from_event(self) -> Optional[int]:
        """
        起始事件位置

        Returns
        -------
        Optional[int]
            起始事件位置
        """
        return self._from_event

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        """
        LIMIT 子句

        Returns
        -------
        Optional[LimitClause]
            LIMIT 子句
        """
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
        # pylint: disable=R0913
        self._command_type = command_type
        self._table_ident = table_ident
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def command_type(self) -> "EnumShowCommandType":
        """
        显示命令类型

        Returns
        -------
        EnumShowCommandType
            显示命令类型
        """
        return self._command_type

    @property
    def table_ident(self) -> "Identifier":
        """
        表标识符

        Returns
        -------
        Identifier
            表标识符
        """
        return self._table_ident

    @property
    def schema_name(self) -> Optional[str]:
        """
        模式名称

        Returns
        -------
        Optional[str]
            模式名称
        """
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
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
        """
        初始化 SHOW CREATE DATABASE 语句

        Parameters
        ----------
        if_not_exists : bool
            是否包含 IF NOT EXISTS 子句
        database_name : str
            数据库名称
        """
        self._if_not_exists = if_not_exists
        self._database_name = database_name

    @property
    def if_not_exists(self) -> bool:
        """
        是否包含 IF NOT EXISTS 子句

        Returns
        -------
        bool
            是否包含 IF NOT EXISTS 子句
        """
        return self._if_not_exists

    @property
    def database_name(self) -> str:
        """
        数据库名称

        Returns
        -------
        str
            数据库名称
        """
        return self._database_name


class ShowCreateEventStatement(Statement):
    """SHOW CREATE EVENT 语句"""

    __slots__ = (
        "_event_name",
    )

    def __init__(self, event_name: "Identifier"):
        """
        初始化 SHOW CREATE EVENT 语句

        Parameters
        ----------
        event_name : Identifier
            事件名称
        """
        self._event_name = event_name

    @property
    def event_name(self) -> "Identifier":
        """
        事件名称

        Returns
        -------
        Identifier
            事件名称
        """
        return self._event_name


class ShowCreateFunctionStatement(Statement):
    """SHOW CREATE FUNCTION 语句"""

    __slots__ = (
        "_function_name",
    )

    def __init__(self, function_name: "Identifier"):
        """
        初始化 SHOW CREATE FUNCTION 语句

        Parameters
        ----------
        function_name : Identifier
            函数名称
        """
        self._function_name = function_name

    @property
    def function_name(self) -> "Identifier":
        """
        函数名称

        Returns
        -------
        Identifier
            函数名称
        """
        return self._function_name


class ShowCreateProcedureStatement(Statement):
    """SHOW CREATE PROCEDURE 语句"""

    __slots__ = (
        "_procedure_name",
    )

    def __init__(self, procedure_name: "Identifier"):
        """
        初始化 SHOW CREATE PROCEDURE 语句

        Parameters
        ----------
        procedure_name : Identifier
            存储过程名称
        """
        self._procedure_name = procedure_name

    @property
    def procedure_name(self) -> "Identifier":
        """
        存储过程名称

        Returns
        -------
        Identifier
            存储过程名称
        """
        return self._procedure_name


class ShowCreateTableStatement(Statement):
    """SHOW CREATE TABLE 语句"""

    __slots__ = (
        "_table_ident",
    )

    def __init__(self, table_ident: "Identifier"):
        """
        初始化 SHOW CREATE TABLE 语句

        Parameters
        ----------
        table_ident : Identifier
            表标识符
        """
        self._table_ident = table_ident

    @property
    def table_ident(self) -> "Identifier":
        """
        表标识符

        Returns
        -------
        Identifier
            表标识符
        """
        return self._table_ident


class ShowCreateTriggerStatement(Statement):
    """SHOW CREATE TRIGGER 语句"""

    __slots__ = (
        "_trigger_name",
    )

    def __init__(self, trigger_name: "Identifier"):
        """
        初始化 SHOW CREATE TRIGGER 语句

        Parameters
        ----------
        trigger_name : Identifier
            触发器名称
        """
        self._trigger_name = trigger_name

    @property
    def trigger_name(self) -> "Identifier":
        """
        触发器名称

        Returns
        -------
        Identifier
            触发器名称
        """
        return self._trigger_name


class ShowCreateUserStatement(Statement):
    """SHOW CREATE USER 语句"""

    __slots__ = (
        "_user_name",
    )

    def __init__(self, user_name: "UserName"):
        """
        初始化 SHOW CREATE USER 语句

        Parameters
        ----------
        user_name : UserName
            用户名
        """
        self._user_name = user_name

    @property
    def user_name(self) -> "UserName":
        """
        用户名

        Returns
        -------
        UserName
            用户名
        """
        return self._user_name


class ShowCreateViewStatement(Statement):
    """SHOW CREATE VIEW 语句"""

    __slots__ = (
        "_view_name",
    )

    def __init__(self, view_name: "Identifier"):
        """
        初始化 SHOW CREATE VIEW 语句

        Parameters
        ----------
        view_name : Identifier
            视图名称
        """
        self._view_name = view_name

    @property
    def view_name(self) -> "Identifier":
        """
        视图名称

        Returns
        -------
        Identifier
            视图名称
        """
        return self._view_name


class ShowDatabasesStatement(ShowWildOrWhereBaseStatement):
    """SHOW DATABASES 语句"""


class ShowEngineLogsStatement(Statement):
    """SHOW ENGINE LOGS 语句"""

    __slots__ = (
        "_engine_name",
    )

    def __init__(self, engine_name: Optional[str]):
        """
        初始化 SHOW ENGINE LOGS 语句

        Parameters
        ----------
        engine_name : Optional[str]
            引擎名称
        """
        self._engine_name = engine_name

    @property
    def engine_name(self) -> Optional[str]:
        """
        引擎名称

        Returns
        -------
        Optional[str]
            引擎名称
        """
        return self._engine_name


class ShowEngineMutexStatement(Statement):
    """SHOW ENGINE MUTEX 语句"""

    __slots__ = (
        "_engine_name",
    )

    def __init__(self, engine_name: Optional[str]):
        """
        初始化 SHOW ENGINE MUTEX 语句

        Parameters
        ----------
        engine_name : Optional[str]
            引擎名称
        """
        self._engine_name = engine_name

    @property
    def engine_name(self) -> Optional[str]:
        """
        引擎名称

        Returns
        -------
        Optional[str]
            引擎名称
        """
        return self._engine_name


class ShowEngineStatusStatement(Statement):
    """SHOW ENGINE STATUS 语句"""

    __slots__ = (
        "_engine_name",
    )

    def __init__(self, engine_name: Optional[str]):
        """
        初始化 SHOW ENGINE STATUS 语句

        Parameters
        ----------
        engine_name : Optional[str]
            引擎名称
        """
        self._engine_name = engine_name

    @property
    def engine_name(self) -> Optional[str]:
        """
        引擎名称

        Returns
        -------
        Optional[str]
            引擎名称
        """
        return self._engine_name


class ShowEnginesStatement(Statement):
    """SHOW ENGINES 语句"""


class ShowErrorsStatement(Statement):
    """SHOW ERRORS 语句"""

    __slots__ = (
        "_limit_clause",
    )

    def __init__(self, limit_clause: Optional["LimitClause"]):
        """
        初始化 SHOW ERRORS 语句

        Parameters
        ----------
        limit_clause : Optional[LimitClause]
            LIMIT 子句
        """
        self._limit_clause = limit_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        """
        LIMIT 子句

        Returns
        -------
        Optional[LimitClause]
            LIMIT 子句
        """
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
        """
        初始化 SHOW EVENTS 语句

        Parameters
        ----------
        schema_name : Optional[str], optional
            模式名称，默认为 None
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def schema_name(self) -> Optional[str]:
        """
        模式名称

        Returns
        -------
        Optional[str]
            模式名称
        """
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
        return self._where


class ShowFunctionCodeStatement(Statement):
    """SHOW FUNCTION CODE 语句"""

    __slots__ = (
        "_function_name",
    )

    def __init__(self, function_name: "Identifier"):
        """
        初始化 SHOW FUNCTION CODE 语句

        Parameters
        ----------
        function_name : Identifier
            函数名称
        """
        self._function_name = function_name

    @property
    def function_name(self) -> "Identifier":
        """
        函数名称

        Returns
        -------
        Identifier
            函数名称
        """
        return self._function_name


class ShowFunctionStatusStatement(ShowWildOrWhereBaseStatement):
    """SHOW FUNCTION STATUS 语句"""


class ShowGrantsStatement(Statement):
    """SHOW GRANTS 语句"""

    __slots__ = (
        "_for_user",
        "_using_user_list"
    )

    def __init__(self, for_user: Optional["UserName"] = None, using_user_list: Optional[List["UserName"]] = None):
        """
        初始化 SHOW GRANTS 语句

        Parameters
        ----------
        for_user : Optional[UserName], optional
            用户名，默认为 None
        using_user_list : Optional[List[UserName]], optional
            使用的用户列表，默认为 None
        """
        self._for_user = for_user
        self._using_user_list = using_user_list or []

    @property
    def for_user(self) -> Optional["UserName"]:
        """
        用户名

        Returns
        -------
        Optional[UserName]
            用户名
        """
        return self._for_user

    @property
    def using_user_list(self) -> List["UserName"]:
        """
        使用的用户列表

        Returns
        -------
        List[UserName]
            使用的用户列表
        """
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
        """
        初始化 SHOW KEYS 语句

        Parameters
        ----------
        is_extended : bool
            是否扩展显示
        table_ident : Identifier
            表标识符
        schema_name : Optional[str]
            模式名称
        where_clause : Optional[Expression]
            WHERE 子句表达式
        """
        self._is_extended = is_extended
        self._table_ident = table_ident
        self._schema_name = schema_name
        self._where_clause = where_clause

    @property
    def is_extended(self) -> bool:
        """
        是否扩展显示

        Returns
        -------
        bool
            是否扩展显示
        """
        return self._is_extended

    @property
    def table_ident(self) -> "Identifier":
        """
        表标识符

        Returns
        -------
        Identifier
            表标识符
        """
        return self._table_ident

    @property
    def schema_name(self) -> Optional[str]:
        """
        模式名称

        Returns
        -------
        Optional[str]
            模式名称
        """
        return self._schema_name

    @property
    def where_clause(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
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
        """
        初始化 SHOW OPEN TABLES 语句

        Parameters
        ----------
        schema_name : Optional[str]
            模式名称
        wild : Optional[str]
            通配符模式
        where : Optional[Expression]
            WHERE 子句表达式
        """
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def schema_name(self) -> Optional[str]:
        """
        模式名称

        Returns
        -------
        Optional[str]
            模式名称
        """
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
        return self._where


class ShowParseTreeStatement(Statement):
    """SHOW PARSE TREE 语句"""

    __slots__ = (
        "_statement",
    )

    def __init__(self, statement: Statement):
        """
        初始化 SHOW PARSE TREE 语句

        Parameters
        ----------
        statement : Statement
            要显示解析树的语句
        """
        self._statement = statement

    @property
    def statement(self) -> Statement:
        """
        要显示解析树的语句

        Returns
        -------
        Statement
            要显示解析树的语句
        """
        return self._statement


class ShowPluginsStatement(Statement):
    """SHOW PLUGINS 语句"""


class ShowPrivilegesStatement(Statement):
    """SHOW PRIVILEGES 语句"""


class ShowProcedureCodeStatement(Statement):
    """SHOW PROCEDURE CODE 语句"""

    __slots__ = (
        "_procedure_name",
    )

    def __init__(self, procedure_name: "Identifier"):
        """
        初始化 SHOW PROCEDURE CODE 语句

        Parameters
        ----------
        procedure_name : Identifier
            存储过程名称
        """
        self._procedure_name = procedure_name

    @property
    def procedure_name(self) -> "Identifier":
        """
        存储过程名称

        Returns
        -------
        Identifier
            存储过程名称
        """
        return self._procedure_name


class ShowProcedureStatusStatement(ShowWildOrWhereBaseStatement):
    """SHOW PROCEDURE STATUS 语句"""


class ShowProcesslistStatement(Statement):
    """SHOW PROCESSLIST 语句"""

    __slots__ = (
        "_is_full",
    )

    def __init__(self, is_full: bool):
        """
        初始化 SHOW PROCESSLIST 语句

        Parameters
        ----------
        is_full : bool
            是否显示完整信息
        """
        self._is_full = is_full

    @property
    def is_full(self) -> bool:
        """
        是否显示完整信息

        Returns
        -------
        bool
            是否显示完整信息
        """
        return self._is_full


class ShowProfileStatement(Statement):
    """SHOW PROFILE 语句"""

    __slots__ = (
        "_profile_type",
        "_thread_id",
        "_limit_clause",
    )

    def __init__(self, profile_type: "EnumProfileType", thread_id: Optional[int], limit_clause: "LimitClause"):
        """
        初始化 SHOW PROFILE 语句

        Parameters
        ----------
        profile_type : EnumProfileType
            性能分析类型
        thread_id : Optional[int]
            线程 ID
        limit_clause : LimitClause
            LIMIT 子句
        """
        self._profile_type = profile_type
        self._thread_id = thread_id
        self._limit_clause = limit_clause

    @property
    def profile_type(self) -> "EnumProfileType":
        """
        性能分析类型

        Returns
        -------
        EnumProfileType
            性能分析类型
        """
        return self._profile_type

    @property
    def thread_id(self) -> Optional[int]:
        """
        线程 ID

        Returns
        -------
        Optional[int]
            线程 ID
        """
        return self._thread_id

    @property
    def limit_clause(self) -> "LimitClause":
        """
        LIMIT 子句

        Returns
        -------
        LimitClause
            LIMIT 子句
        """
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
        """
        初始化 SHOW RELAYLOG EVENTS 语句

        Parameters
        ----------
        binlog_in : Optional[str]
            二进制日志文件
        binlog_from : Optional[int]
            起始位置
        limit_clause : Optional[LimitClause]
            LIMIT 子句
        channel_name : Optional[str]
            通道名称
        """
        self._binlog_in = binlog_in
        self._binlog_from = binlog_from
        self._limit_clause = limit_clause
        self._channel_name = channel_name

    @property
    def binlog_in(self) -> Optional[str]:
        """
        二进制日志文件

        Returns
        -------
        Optional[str]
            二进制日志文件
        """
        return self._binlog_in

    @property
    def binlog_from(self) -> Optional[int]:
        """
        起始位置

        Returns
        -------
        Optional[int]
            起始位置
        """
        return self._binlog_from

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        """
        LIMIT 子句

        Returns
        -------
        Optional[LimitClause]
            LIMIT 子句
        """
        return self._limit_clause

    @property
    def channel_name(self) -> Optional[str]:
        """
        通道名称

        Returns
        -------
        Optional[str]
            通道名称
        """
        return self._channel_name


class ShowReplicaStatusStatement(Statement):
    """SHOW REPLICA STATUS 语句"""

    __slots__ = (
        "_channel_name",
    )

    def __init__(self, channel_name: Optional[str]):
        """
        初始化 SHOW REPLICA STATUS 语句

        Parameters
        ----------
        channel_name : Optional[str]
            通道名称
        """
        self._channel_name = channel_name

    @property
    def channel_name(self) -> Optional[str]:
        """
        通道名称

        Returns
        -------
        Optional[str]
            通道名称
        """
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
        """
        初始化 SHOW STATUS 语句

        Parameters
        ----------
        variable_type : EnumVariableType
            变量类型
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._variable_type = variable_type
        self._wild = wild
        self._where = where

    @property
    def variable_type(self) -> "EnumVariableType":
        """
        变量类型

        Returns
        -------
        EnumVariableType
            变量类型
        """
        return self._variable_type

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
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
        """
        初始化 SHOW TABLE STATUS 语句

        Parameters
        ----------
        schema_name : Optional[str], optional
            模式名称，默认为 None
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def schema_name(self) -> Optional[str]:
        """
        模式名称

        Returns
        -------
        Optional[str]
            模式名称
        """
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
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
        """
        初始化 SHOW TABLES 语句

        Parameters
        ----------
        command_type : EnumShowCommandType
            显示命令类型
        schema_name : Optional[str], optional
            模式名称，默认为 None
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._command_type = command_type
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def command_type(self) -> "EnumShowCommandType":
        """
        显示命令类型

        Returns
        -------
        EnumShowCommandType
            显示命令类型
        """
        return self._command_type

    @property
    def schema_name(self) -> Optional[str]:
        """
        模式名称

        Returns
        -------
        Optional[str]
            模式名称
        """
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
        return self._where


class ShowTriggersStatement(Statement):
    """SHOW TRIGGERS 语句"""

    __slots__ = (
        "_is_full",
        "_schema_name",
        "_wild",
        "_where"
    )

    def __init__(self,
                 is_full: bool,
                 schema_name: Optional[str],
                 wild: Optional[str] = None,
                 where: Optional[Expression] = None):
        """
        初始化 SHOW TRIGGERS 语句

        Parameters
        ----------
        is_full : bool
            是否显示完整信息
        schema_name : Optional[str]
            模式名称
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._is_full = is_full
        self._schema_name = schema_name
        self._wild = wild
        self._where = where

    @property
    def is_full(self) -> bool:
        """
        是否显示完整信息

        Returns
        -------
        bool
            是否显示完整信息
        """
        return self._is_full

    @property
    def schema_name(self) -> Optional[str]:
        """
        模式名称

        Returns
        -------
        Optional[str]
            模式名称
        """
        return self._schema_name

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
        return self._where


class ShowWarningsStatement(Statement):
    """SHOW WARNINGS 语句"""

    __slots__ = (
        "_limit_clause",
    )

    def __init__(self, limit_clause: Optional["LimitClause"]):
        """
        初始化 SHOW WARNINGS 语句

        Parameters
        ----------
        limit_clause : Optional[LimitClause]
            LIMIT 子句
        """
        self._limit_clause = limit_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        """
        LIMIT 子句

        Returns
        -------
        Optional[LimitClause]
            LIMIT 子句
        """
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
        """
        初始化 SHOW VARIABLES 语句

        Parameters
        ----------
        variable_type : EnumVariableType
            变量类型
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._variable_type = variable_type
        self._wild = wild
        self._where = where

    @property
    def variable_type(self) -> "EnumVariableType":
        """
        变量类型

        Returns
        -------
        EnumVariableType
            变量类型
        """
        return self._variable_type

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
        return self._where


class TempWildOrWhere(Node):
    """【临时】通配符或 WHERE 子句"""

    __slots__ = (
        "_wild",
        "_where"
    )

    def __init__(self, wild: Optional[str] = None, where: Optional[Expression] = None):
        """
        初始化临时通配符或 WHERE 子句

        Parameters
        ----------
        wild : Optional[str], optional
            通配符模式，默认为 None
        where : Optional[Expression], optional
            WHERE 子句表达式，默认为 None
        """
        self._wild = wild
        self._where = where

    @property
    def wild(self) -> Optional[str]:
        """
        通配符模式

        Returns
        -------
        Optional[str]
            通配符模式
        """
        return self._wild

    @property
    def where(self) -> Optional[Expression]:
        """
        WHERE 子句表达式

        Returns
        -------
        Optional[Expression]
            WHERE 子句表达式
        """
        return self._where
