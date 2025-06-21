"""
处理命令（process command）

`EVENT` 语句和 `TRIGGER` 语句中使用的处理命令。
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.sql_state import SqlState
    from metasequoia_sql.ast.phrase.field_type import FieldType
    from metasequoia_sql.ast.basic.fixed_enum import EnumHandlerType
    from metasequoia_sql.ast.basic.charset_name import Charset

__all__ = [
    "ProcessCommand",
    "ProcessCommandStatement",
    "ProcessCommandReturn",
    "ProcessCommandConditionTuple",
    "ProcessCommandIf",
    "ProcessCommandCase",
    "ProcessCommandConditionValue",
    "ProcessCommandConditionValueNumber",
    "ProcessCommandConditionValueSqlState",
    "ProcessCommandConditionValueIdent",
    "ProcessCommandConditionValueSqlWarning",
    "ProcessCommandConditionValueNotFound",
    "ProcessCommandConditionValueSqlException",
    "ProcessCommandDeclare",
    "ProcessCommandDeclareVariable",
    "ProcessCommandDeclareCondition",
    "ProcessCommandDeclareHandler",
    "ProcessCommandDeclareCursor",
    "ProcessCommandBlock",
    "ProcessCommandLabeledBlock",
    "ProcessCommandUnlabeledBlock",
    "ProcessCommandLabeledControl",
    "ProcessCommandLoop",
    "ProcessCommandWhile",
    "ProcessCommandRepeat",
    "ProcessCommandLeave",
    "ProcessCommandIterate",
    "ProcessCommandOpen",
    "ProcessCommandFetch",
    "ProcessCommandClose",
    "ProcessCommandByString",
]


class ProcessCommand(Node):
    """处理命令"""


class ProcessCommandStatement(ProcessCommand):
    """处理命令：执行语句"""

    __slots__ = (
        "_statement"
    )

    def __init__(self, statement: Statement):
        self._statement = statement

    @property
    def statement(self) -> Statement:
        return self._statement


class ProcessCommandReturn(ProcessCommand):
    """处理命令：返回表达式结果"""

    __slots__ = (
        "_expression"
    )

    def __init__(self, expression: Expression):
        self._expression = expression

    @property
    def expression(self) -> Expression:
        return self._expression


class ProcessCommandConditionTuple(ProcessCommand):
    """处理命令中的条件表达式与对应的处理命令元组"""

    __slots__ = (
        "_condition",
        "_statements"
    )

    def __init__(self, condition: Expression, statements: List[ProcessCommand]):
        self._condition = condition
        self._statements = statements

    @property
    def condition(self) -> Expression:
        return self._condition

    @property
    def statements(self) -> List[ProcessCommand]:
        return self._statements


class ProcessCommandIf(ProcessCommand):
    """处理命令：`IF` 语句"""

    __slots__ = (
        "_condition_tuple_list",
        "_else_statements"
    )

    def __init__(self,
                 condition_tuple_list: List[ProcessCommandConditionTuple],
                 else_statements: Optional[list[ProcessCommand]]):
        self._condition_tuple_list = condition_tuple_list
        self._else_statements = else_statements

    @property
    def condition_tuple_list(self) -> List[ProcessCommandConditionTuple]:
        return self._condition_tuple_list

    @property
    def else_statements(self) -> list[ProcessCommand]:
        return self._else_statements


class ProcessCommandCase(ProcessCommand):
    """处理命令：`CASE` 语句"""

    __slots__ = (
        "_expression",
        "_condition_tuple_list",
        "_else_statements"
    )

    def __init__(self,
                 expression: Optional[Expression],
                 condition_tuple_list: List[ProcessCommandConditionTuple],
                 else_statements: Optional[list[ProcessCommand]]):
        self._expression = expression
        self._condition_tuple_list = condition_tuple_list
        self._else_statements = else_statements

    @property
    def expression(self) -> Optional[Expression]:
        return self._expression

    @property
    def condition_tuple_list(self) -> List[ProcessCommandConditionTuple]:
        return self._condition_tuple_list

    @property
    def else_statements(self) -> list[ProcessCommand]:
        return self._else_statements


class ProcessCommandConditionValue(Node):
    """处理命令中的条件值基类"""


class ProcessCommandConditionValueNumber(ProcessCommandConditionValue):
    """处理命令中的条件值：错误号"""

    __slots__ = (
        "_error_number",
    )

    def __init__(self, error_number: int):
        self._error_number = error_number

    @property
    def error_number(self) -> int:
        return self._error_number


class ProcessCommandConditionValueSqlState(ProcessCommandConditionValue):
    """处理命令中的条件值：SQL状态"""

    __slots__ = (
        "_sql_state",
    )

    def __init__(self, sql_state: "SqlState"):
        self._sql_state = sql_state

    @property
    def sql_state(self) -> "SqlState":
        return self._sql_state


class ProcessCommandConditionValueIdent(ProcessCommandConditionValue):
    """处理命令中的条件值：标识符"""

    __slots__ = (
        "_identifier",
    )

    def __init__(self, identifier: str):
        self._identifier = identifier

    @property
    def identifier(self) -> str:
        return self._identifier


class ProcessCommandConditionValueSqlWarning(ProcessCommandConditionValue):
    """处理命令中的条件值：SQL警告"""


class ProcessCommandConditionValueNotFound(ProcessCommandConditionValue):
    """处理命令中的条件值：未找到"""


class ProcessCommandConditionValueSqlException(ProcessCommandConditionValue):
    """处理命令中的条件值：SQL异常"""


class ProcessCommandDeclare(ProcessCommand):
    """处理命令中的声明表达式基类"""


class ProcessCommandDeclareVariable(ProcessCommandDeclare):
    """处理命令：声明变量"""

    __slots__ = (
        "_identifier_list",
        "_field_type",
        "_collate_name",
        "_default_expression",
    )

    def __init__(self,
                 identifier_list: List[str],
                 field_type: "FieldType",
                 collate_name: Optional["Charset"],
                 default_expression: Optional[Expression]):
        self._identifier_list = identifier_list
        self._field_type = field_type
        self._collate_name = collate_name
        self._default_expression = default_expression

    @property
    def identifier_list(self) -> List[str]:
        return self._identifier_list

    @property
    def field_type(self) -> "FieldType":
        return self._field_type

    @property
    def collate_name(self) -> Optional["Charset"]:
        return self._collate_name

    @property
    def default_expression(self) -> Optional[Expression]:
        return self._default_expression


class ProcessCommandDeclareCondition(ProcessCommandDeclare):
    """处理命令：声明条件"""

    __slots__ = (
        "_condition_name",
        "_condition_value",
    )

    def __init__(self, condition_name: str, condition_value: ProcessCommandConditionValue):
        self._condition_name = condition_name
        self._condition_value = condition_value

    @property
    def condition_name(self) -> str:
        return self._condition_name

    @property
    def condition_value(self) -> ProcessCommandConditionValue:
        return self._condition_value


class ProcessCommandDeclareHandler(ProcessCommandDeclare):
    """处理命令：声明处理器"""

    __slots__ = (
        "_handler_type",
        "_condition_list",
        "_statement",
    )

    def __init__(self,
                 handler_type: "EnumHandlerType",
                 condition_list: List[ProcessCommandConditionValue],
                 statement: ProcessCommand):
        self._handler_type = handler_type
        self._condition_list = condition_list
        self._statement = statement

    @property
    def handler_type(self) -> "EnumHandlerType":
        return self._handler_type

    @property
    def condition_list(self) -> List[ProcessCommandConditionValue]:
        return self._condition_list

    @property
    def statement(self) -> ProcessCommand:
        return self._statement


class ProcessCommandDeclareCursor(ProcessCommandDeclare):
    """处理命令：声明游标"""

    __slots__ = (
        "_cursor_name",
        "_select_statement",
    )

    def __init__(self, cursor_name: str, select_statement: Statement):
        self._cursor_name = cursor_name
        self._select_statement = select_statement

    @property
    def cursor_name(self) -> str:
        return self._cursor_name

    @property
    def select_statement(self) -> Statement:
        return self._select_statement


class ProcessCommandBlock(ProcessCommand):
    """处理命令：代码块（BEGIN...END）"""

    __slots__ = (
        "_declare_list",
        "_statement_list"
    )

    def __init__(self,
                 declare_list: List[ProcessCommandDeclare],
                 statement_list: List[ProcessCommand]):
        self._declare_list = declare_list
        self._statement_list = statement_list

    @property
    def declare_list(self) -> List[ProcessCommandDeclare]:
        return self._declare_list

    @property
    def statement_list(self) -> List[ProcessCommand]:
        return self._statement_list


class ProcessCommandLabeledBlock(ProcessCommand):
    """处理命令：带标签的代码块"""

    __slots__ = (
        "_begin_label",
        "_block_content",
        "_end_label"
    )

    def __init__(self,
                 begin_label: str,
                 block_content: ProcessCommandBlock,
                 end_label: Optional[str]):
        self._begin_label = begin_label
        self._block_content = block_content
        self._end_label = end_label

    @property
    def begin_label(self) -> str:
        return self._begin_label

    @property
    def block_content(self) -> ProcessCommandBlock:
        return self._block_content

    @property
    def end_label(self) -> Optional[str]:
        return self._end_label


class ProcessCommandUnlabeledBlock(ProcessCommand):
    """处理命令：不带标签的代码块"""

    __slots__ = (
        "_block_content",
    )

    def __init__(self, block_content: ProcessCommandBlock):
        self._block_content = block_content

    @property
    def block_content(self) -> ProcessCommandBlock:
        return self._block_content


class ProcessCommandLabeledControl(ProcessCommand):
    """处理命令：带标签的控制语句"""

    __slots__ = (
        "_begin_label",
        "_control_statement",
        "_end_label"
    )

    def __init__(self,
                 begin_label: str,
                 control_statement: ProcessCommand,
                 end_label: Optional[str]):
        self._begin_label = begin_label
        self._control_statement = control_statement
        self._end_label = end_label

    @property
    def begin_label(self) -> str:
        return self._begin_label

    @property
    def control_statement(self) -> ProcessCommand:
        return self._control_statement

    @property
    def end_label(self) -> Optional[str]:
        return self._end_label


class ProcessCommandLoop(ProcessCommand):
    """处理命令：LOOP 循环语句"""

    __slots__ = (
        "_statement_list",
    )

    def __init__(self, statement_list: List[ProcessCommand]):
        self._statement_list = statement_list

    @property
    def statement_list(self) -> List[ProcessCommand]:
        return self._statement_list


class ProcessCommandWhile(ProcessCommand):
    """处理命令：WHILE 循环语句"""

    __slots__ = (
        "_condition",
        "_statement_list"
    )

    def __init__(self, condition: Expression, statement_list: List[ProcessCommand]):
        self._condition = condition
        self._statement_list = statement_list

    @property
    def condition(self) -> Expression:
        return self._condition

    @property
    def statement_list(self) -> List[ProcessCommand]:
        return self._statement_list


class ProcessCommandRepeat(ProcessCommand):
    """处理命令：REPEAT...UNTIL 循环语句"""

    __slots__ = (
        "_statement_list",
        "_condition"
    )

    def __init__(self, statement_list: List[ProcessCommand], condition: Expression):
        self._statement_list = statement_list
        self._condition = condition

    @property
    def statement_list(self) -> List[ProcessCommand]:
        return self._statement_list

    @property
    def condition(self) -> Expression:
        return self._condition


class ProcessCommandLeave(ProcessCommand):
    """处理命令：LEAVE 语句"""

    __slots__ = (
        "_label_name",
    )

    def __init__(self, label_name: str):
        self._label_name = label_name

    @property
    def label_name(self) -> str:
        return self._label_name


class ProcessCommandIterate(ProcessCommand):
    """处理命令：ITERATE 语句"""

    __slots__ = (
        "_label_name",
    )

    def __init__(self, label_name: str):
        self._label_name = label_name

    @property
    def label_name(self) -> str:
        return self._label_name


class ProcessCommandOpen(ProcessCommand):
    """处理命令：OPEN 游标语句"""

    __slots__ = (
        "_cursor_name",
    )

    def __init__(self, cursor_name: str):
        self._cursor_name = cursor_name

    @property
    def cursor_name(self) -> str:
        return self._cursor_name


class ProcessCommandFetch(ProcessCommand):
    """处理命令：FETCH 游标语句"""

    __slots__ = (
        "_cursor_name",
        "_variable_list"
    )

    def __init__(self, cursor_name: str, variable_list: List[str]):
        self._cursor_name = cursor_name
        self._variable_list = variable_list

    @property
    def cursor_name(self) -> str:
        return self._cursor_name

    @property
    def variable_list(self) -> List[str]:
        return self._variable_list


class ProcessCommandClose(ProcessCommand):
    """处理命令：CLOSE 游标语句"""

    __slots__ = (
        "_cursor_name",
    )

    def __init__(self, cursor_name: str):
        self._cursor_name = cursor_name

    @property
    def cursor_name(self) -> str:
        return self._cursor_name


class ProcessCommandByString(ProcessCommand):
    """通过字符串定义的处理命令"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value
