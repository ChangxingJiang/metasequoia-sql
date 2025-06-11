"""
DROP 语句（drop statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOption
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOptionLock
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOptionAlgorithm
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOptionWithValidation
    from metasequoia_sql.ast.basic.literal import RoleName
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.basic.fixed_enum import EnumDropRestrict

__all__ = [
    "DropDatabaseStatement",
    "DropEventStatement",
    "DropFunctionStatement",
    "DropIndexStatement",
    "DropLogfileStatement",
    "DropProcedureStatement",
    "DropResourceGroupStatement",
    "DropRoleStatement",
    "DropServerStatement",
    "DropSrsStatement",
    "DropTablespaceStatement",
    "DropUndoTablespaceStatement",
    "DropTableStatement",
    "DropTriggerStatement",
    "DropUserStatement",
    "DropViewStatement",
]


class DropDatabaseStatement(Statement):
    """DROP DATABASE 语句"""

    __slots__ = (
        "_if_exists",
        "_database_name",
    )

    def __init__(self, if_exists: bool, schema_name: str):
        self._if_exists = if_exists
        self._schema_name = schema_name

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def schema_name(self) -> str:
        return self._schema_name


class DropEventStatement(Statement):
    """DROP EVENT 语句"""

    __slots__ = (
        "_if_exists",
        "_event_name",
    )

    def __init__(self, if_exists: bool, event_name: "Identifier"):
        self._if_exists = if_exists
        self._event_name = event_name

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def event_name(self) -> "Identifier":
        return self._event_name


class DropFunctionStatement(Statement):
    """DROP FUNCTION 语句"""

    __slots__ = (
        "_if_exists",
        "_function_name",
    )

    def __init__(self, if_exists: bool, function_name: "Identifier"):
        self._if_exists = if_exists
        self._function_name = function_name

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def function_name(self) -> "Identifier":
        return self._function_name


class DropIndexStatement(Statement):
    """DROP INDEX 语句"""

    __slots__ = (
        "_index_name",
        "_table_name",
        "_lock",
        "_algorithm",
        "_validation"
    )

    def __init__(self,
                 index_name: str,
                 table_name: str,
                 lock: Optional["AlterOptionLock"],
                 algorithm: Optional["AlterOptionAlgorithm"],
                 validation: Optional["AlterOptionWithValidation"]
                 ):
        self._index_name = index_name
        self._table_name = table_name
        self._lock = lock
        self._algorithm = algorithm
        self._validation = validation

    @property
    def index_name(self) -> str:
        return self._index_name

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def lock(self) -> Optional["AlterOptionLock"]:
        return self._lock

    @property
    def algorithm(self) -> Optional["AlterOptionAlgorithm"]:
        return self._algorithm

    @property
    def validation(self) -> Optional["AlterOptionWithValidation"]:
        return self._validation


class DropLogfileStatement(Statement):
    """DROP LOGFILE 语句"""

    __slots__ = (
        "_logfile_name",
        "_options",
    )

    def __init__(self, logfile_name: str, options: List["AlterOption"]):
        self._logfile_name = logfile_name
        self._options = options

    @property
    def logfile_name(self) -> str:
        return self._logfile_name

    @property
    def options(self) -> List["AlterOption"]:
        return self._options


class DropProcedureStatement(Statement):
    """DROP PROCEDURE 语句"""

    __slots__ = (
        "_if_exists",
        "_procedure_name",
    )

    def __init__(self, if_exists: bool, procedure_name: "Identifier"):
        self._if_exists = if_exists
        self._procedure_name = procedure_name

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def procedure_name(self) -> "Identifier":
        return self._procedure_name


class DropResourceGroupStatement(Statement):
    """DROP RESOURCE GROUP 语句"""

    __slots__ = (
        "_group_name",
        "_is_force",
    )

    def __init__(self, group_name: str, is_force: bool):
        self._group_name = group_name
        self._is_force = is_force

    @property
    def group_name(self) -> str:
        return self._group_name

    @property
    def is_force(self) -> bool:
        return self._is_force


class DropRoleStatement(Statement):
    """DROP ROLE 语句"""

    __slots__ = (
        "_if_exists",
        "_role_list",
    )

    def __init__(self, if_exists: bool, role_list: List["RoleName"]):
        self._if_exists = if_exists
        self._role_list = role_list

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def role_list(self) -> List["RoleName"]:
        return self._role_list


class DropServerStatement(Statement):
    """DROP SERVER 语句"""

    __slots__ = (
        "_if_exists",
        "_server_name",
    )

    def __init__(self, if_exists: bool, server_name: str):
        self._if_exists = if_exists
        self._server_name = server_name

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def server_name(self) -> str:
        return self._server_name


class DropSrsStatement(Statement):
    """DROP SPATIAL REFERENCE SYSTEM 语句（删除空间参考系统）"""

    __slots__ = (
        "_if_exists",
        "_srs_id"
    )

    def __init__(self, if_exists: bool, srs_id: int):
        self._if_exists = if_exists
        self._srs_id = srs_id

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def srs_id(self) -> int:
        return self._srs_id


class DropTablespaceStatement(Statement):
    """DROP TABLESPACE 语句"""

    __slots__ = (
        "_tablespace_name",
        "_options",
    )

    def __init__(self, tablespace_name: str, options: List["AlterOption"]):
        self._tablespace_name = tablespace_name
        self._options = options

    @property
    def tablespace_name(self) -> str:
        return self._tablespace_name

    @property
    def options(self) -> List["AlterOption"]:
        return self._options


class DropUndoTablespaceStatement(Statement):
    """DROP UNDO TABLESPACE 语句"""

    __slots__ = (
        "_tablespace_name",
        "_options",
    )

    def __init__(self, tablespace_name: str, options: List["AlterOption"]):
        self._tablespace_name = tablespace_name
        self._options = options

    @property
    def tablespace_name(self) -> str:
        return self._tablespace_name

    @property
    def options(self) -> List["AlterOption"]:
        return self._options


class DropTableStatement(Statement):
    """DROP TABLE 语句"""

    __slots__ = (
        "_temporary",
        "_if_exists",
        "_table_list",
        "_restrict"
    )

    def __init__(self,
                 temporary: bool,
                 if_exists: bool,
                 table_list: List["Identifier"],
                 restrict: "EnumDropRestrict"):
        self._temporary = temporary
        self._if_exists = if_exists
        self._table_list = table_list
        self._restrict = restrict

    @property
    def temporary(self) -> bool:
        return self._temporary

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def table_list(self) -> List["Identifier"]:
        return self._table_list

    @property
    def restrict(self) -> "EnumDropRestrict":
        return self._restrict


class DropTriggerStatement(Statement):
    """DROP TRIGGER 语句"""

    __slots__ = (
        "_if_exists",
        "_trigger_name",
    )

    def __init__(self, if_exists: bool, trigger_name: str):
        self._if_exists = if_exists
        self._trigger_name = trigger_name

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def trigger_name(self) -> str:
        return self._trigger_name


class DropUserStatement(Statement):
    """DROP USER 语句"""

    __slots__ = (
        "_if_exists",
        "_user_list"
    )

    def __init__(self, if_exists: bool, user_list: List["UserName"]):
        self._if_exists = if_exists
        self._user_list = user_list

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def user_list(self) -> List["UserName"]:
        return self._user_list


class DropViewStatement(Statement):
    """DROP VIEW 语句"""

    __slots__ = (
        "_if_exists",
        "_table_list",
        "_restrict"
    )

    def __init__(self, if_exists: bool, table_list: List["Identifier"], restrict: "EnumDropRestrict"):
        self._if_exists = if_exists
        self._table_list = table_list
        self._restrict = restrict

    @property
    def if_exists(self) -> bool:
        return self._if_exists

    @property
    def table_list(self) -> List["Identifier"]:
        return self._table_list

    @property
    def restrict(self) -> "EnumDropRestrict":
        return self._restrict
