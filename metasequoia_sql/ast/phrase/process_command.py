# pylint: disable=C0302

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
        "_statement",
    )

    def __init__(self, statement: Statement):
        """
        初始化处理命令：执行语句

        Parameters
        ----------
        statement : Statement
            要执行的SQL语句
        """
        self._statement = statement

    @property
    def statement(self) -> Statement:
        """
        获取要执行的SQL语句

        Returns
        -------
        Statement
            要执行的SQL语句
        """
        return self._statement


class ProcessCommandReturn(ProcessCommand):
    """处理命令：返回表达式结果"""

    __slots__ = (
        "_expression",
    )

    def __init__(self, expression: Expression):
        """
        初始化处理命令：返回表达式结果

        Parameters
        ----------
        expression : Expression
            要返回的表达式
        """
        self._expression = expression

    @property
    def expression(self) -> Expression:
        """
        获取要返回的表达式

        Returns
        -------
        Expression
            要返回的表达式
        """
        return self._expression


class ProcessCommandConditionTuple(ProcessCommand):
    """处理命令中的条件表达式与对应的处理命令元组"""

    __slots__ = (
        "_condition",
        "_statements",
    )

    def __init__(self, condition: Expression, statements: List[ProcessCommand]):
        """
        初始化条件表达式与对应的处理命令元组

        Parameters
        ----------
        condition : Expression
            条件表达式
        statements : List[ProcessCommand]
            当条件满足时执行的处理命令列表
        """
        self._condition = condition
        self._statements = statements

    @property
    def condition(self) -> Expression:
        """
        获取条件表达式

        Returns
        -------
        Expression
            条件表达式
        """
        return self._condition

    @property
    def statements(self) -> List[ProcessCommand]:
        """
        获取当条件满足时执行的处理命令列表

        Returns
        -------
        List[ProcessCommand]
            处理命令列表
        """
        return self._statements


class ProcessCommandIf(ProcessCommand):
    """处理命令：`IF` 语句"""

    __slots__ = (
        "_condition_tuple_list",
        "_else_statements",
    )

    def __init__(self,
                 condition_tuple_list: List[ProcessCommandConditionTuple],
                 else_statements: Optional[list[ProcessCommand]]):
        """
        初始化 IF 语句

        Parameters
        ----------
        condition_tuple_list : List[ProcessCommandConditionTuple]
            条件表达式与对应处理命令的元组列表
        else_statements : Optional[list[ProcessCommand]]
            ELSE 分支的处理命令列表
        """
        self._condition_tuple_list = condition_tuple_list
        self._else_statements = else_statements

    @property
    def condition_tuple_list(self) -> List[ProcessCommandConditionTuple]:
        """
        获取条件表达式与对应处理命令的元组列表

        Returns
        -------
        List[ProcessCommandConditionTuple]
            条件表达式与对应处理命令的元组列表
        """
        return self._condition_tuple_list

    @property
    def else_statements(self) -> list[ProcessCommand]:
        """
        获取 ELSE 分支的处理命令列表

        Returns
        -------
        list[ProcessCommand]
            ELSE 分支的处理命令列表
        """
        return self._else_statements


class ProcessCommandCase(ProcessCommand):
    """处理命令：`CASE` 语句"""

    __slots__ = (
        "_expression",
        "_condition_tuple_list",
        "_else_statements",
    )

    def __init__(self,
                 expression: Optional[Expression],
                 condition_tuple_list: List[ProcessCommandConditionTuple],
                 else_statements: Optional[list[ProcessCommand]]):
        """
        初始化 CASE 语句

        Parameters
        ----------
        expression : Optional[Expression]
            CASE 表达式，可选
        condition_tuple_list : List[ProcessCommandConditionTuple]
            条件表达式与对应处理命令的元组列表
        else_statements : Optional[list[ProcessCommand]]
            ELSE 分支的处理命令列表
        """
        self._expression = expression
        self._condition_tuple_list = condition_tuple_list
        self._else_statements = else_statements

    @property
    def expression(self) -> Optional[Expression]:
        """
        获取 CASE 表达式

        Returns
        -------
        Optional[Expression]
            CASE 表达式，可能为空
        """
        return self._expression

    @property
    def condition_tuple_list(self) -> List[ProcessCommandConditionTuple]:
        """
        获取条件表达式与对应处理命令的元组列表

        Returns
        -------
        List[ProcessCommandConditionTuple]
            条件表达式与对应处理命令的元组列表
        """
        return self._condition_tuple_list

    @property
    def else_statements(self) -> list[ProcessCommand]:
        """
        获取 ELSE 分支的处理命令列表

        Returns
        -------
        list[ProcessCommand]
            ELSE 分支的处理命令列表
        """
        return self._else_statements


class ProcessCommandConditionValue(Node):
    """处理命令中的条件值基类"""


class ProcessCommandConditionValueNumber(ProcessCommandConditionValue):
    """处理命令中的条件值：错误号"""

    __slots__ = (
        "_error_number",
    )

    def __init__(self, error_number: int):
        """
        初始化错误号条件值

        Parameters
        ----------
        error_number : int
            错误号
        """
        self._error_number = error_number

    @property
    def error_number(self) -> int:
        """
        获取错误号

        Returns
        -------
        int
            错误号
        """
        return self._error_number


class ProcessCommandConditionValueSqlState(ProcessCommandConditionValue):
    """处理命令中的条件值：SQL状态"""

    __slots__ = (
        "_sql_state",
    )

    def __init__(self, sql_state: "SqlState"):
        """
        初始化 SQL 状态条件值

        Parameters
        ----------
        sql_state : SqlState
            SQL 状态
        """
        self._sql_state = sql_state

    @property
    def sql_state(self) -> "SqlState":
        """
        获取 SQL 状态

        Returns
        -------
        SqlState
            SQL 状态
        """
        return self._sql_state


class ProcessCommandConditionValueIdent(ProcessCommandConditionValue):
    """处理命令中的条件值：标识符"""

    __slots__ = (
        "_identifier",
    )

    def __init__(self, identifier: str):
        """
        初始化标识符条件值

        Parameters
        ----------
        identifier : str
            标识符名称
        """
        self._identifier = identifier

    @property
    def identifier(self) -> str:
        """
        获取标识符名称

        Returns
        -------
        str
            标识符名称
        """
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
        """
        初始化声明变量命令

        Parameters
        ----------
        identifier_list : List[str]
            变量标识符列表
        field_type : FieldType
            变量的字段类型
        collate_name : Optional[Charset]
            排序规则名称，可选
        default_expression : Optional[Expression]
            默认值表达式，可选
        """
        self._identifier_list = identifier_list
        self._field_type = field_type
        self._collate_name = collate_name
        self._default_expression = default_expression

    @property
    def identifier_list(self) -> List[str]:
        """
        获取变量标识符列表

        Returns
        -------
        List[str]
            变量标识符列表
        """
        return self._identifier_list

    @property
    def field_type(self) -> "FieldType":
        """
        获取变量的字段类型

        Returns
        -------
        FieldType
            变量的字段类型
        """
        return self._field_type

    @property
    def collate_name(self) -> Optional["Charset"]:
        """
        获取排序规则名称

        Returns
        -------
        Optional[Charset]
            排序规则名称，可能为空
        """
        return self._collate_name

    @property
    def default_expression(self) -> Optional[Expression]:
        """
        获取默认值表达式

        Returns
        -------
        Optional[Expression]
            默认值表达式，可能为空
        """
        return self._default_expression


class ProcessCommandDeclareCondition(ProcessCommandDeclare):
    """处理命令：声明条件"""

    __slots__ = (
        "_condition_name",
        "_condition_value",
    )

    def __init__(self, condition_name: str, condition_value: ProcessCommandConditionValue):
        """
        初始化声明条件命令

        Parameters
        ----------
        condition_name : str
            条件名称
        condition_value : ProcessCommandConditionValue
            条件值
        """
        self._condition_name = condition_name
        self._condition_value = condition_value

    @property
    def condition_name(self) -> str:
        """
        获取条件名称

        Returns
        -------
        str
            条件名称
        """
        return self._condition_name

    @property
    def condition_value(self) -> ProcessCommandConditionValue:
        """
        获取条件值

        Returns
        -------
        ProcessCommandConditionValue
            条件值
        """
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
        """
        初始化声明处理器命令

        Parameters
        ----------
        handler_type : EnumHandlerType
            处理器类型
        condition_list : List[ProcessCommandConditionValue]
            条件值列表
        statement : ProcessCommand
            要执行的处理命令
        """
        self._handler_type = handler_type
        self._condition_list = condition_list
        self._statement = statement

    @property
    def handler_type(self) -> "EnumHandlerType":
        """
        获取处理器类型

        Returns
        -------
        EnumHandlerType
            处理器类型
        """
        return self._handler_type

    @property
    def condition_list(self) -> List[ProcessCommandConditionValue]:
        """
        获取条件值列表

        Returns
        -------
        List[ProcessCommandConditionValue]
            条件值列表
        """
        return self._condition_list

    @property
    def statement(self) -> ProcessCommand:
        """
        获取要执行的处理命令

        Returns
        -------
        ProcessCommand
            要执行的处理命令
        """
        return self._statement


class ProcessCommandDeclareCursor(ProcessCommandDeclare):
    """处理命令：声明游标"""

    __slots__ = (
        "_cursor_name",
        "_select_statement",
    )

    def __init__(self, cursor_name: str, select_statement: Statement):
        """
        初始化声明游标命令

        Parameters
        ----------
        cursor_name : str
            游标名称
        select_statement : Statement
            SELECT 语句
        """
        self._cursor_name = cursor_name
        self._select_statement = select_statement

    @property
    def cursor_name(self) -> str:
        """
        获取游标名称

        Returns
        -------
        str
            游标名称
        """
        return self._cursor_name

    @property
    def select_statement(self) -> Statement:
        """
        获取 SELECT 语句

        Returns
        -------
        Statement
            SELECT 语句
        """
        return self._select_statement


class ProcessCommandBlock(ProcessCommand):
    """处理命令：代码块（BEGIN...END）"""

    __slots__ = (
        "_declare_list",
        "_statement_list",
    )

    def __init__(self,
                 declare_list: List[ProcessCommandDeclare],
                 statement_list: List[ProcessCommand]):
        """
        初始化代码块命令

        Parameters
        ----------
        declare_list : List[ProcessCommandDeclare]
            声明列表
        statement_list : List[ProcessCommand]
            语句列表
        """
        self._declare_list = declare_list
        self._statement_list = statement_list

    @property
    def declare_list(self) -> List[ProcessCommandDeclare]:
        """
        获取声明列表

        Returns
        -------
        List[ProcessCommandDeclare]
            声明列表
        """
        return self._declare_list

    @property
    def statement_list(self) -> List[ProcessCommand]:
        """
        获取语句列表

        Returns
        -------
        List[ProcessCommand]
            语句列表
        """
        return self._statement_list


class ProcessCommandLabeledBlock(ProcessCommand):
    """处理命令：带标签的代码块"""

    __slots__ = (
        "_begin_label",
        "_block_content",
        "_end_label",
    )

    def __init__(self,
                 begin_label: str,
                 block_content: ProcessCommandBlock,
                 end_label: Optional[str]):
        """
        初始化带标签的代码块命令

        Parameters
        ----------
        begin_label : str
            开始标签
        block_content : ProcessCommandBlock
            代码块内容
        end_label : Optional[str]
            结束标签，可选
        """
        self._begin_label = begin_label
        self._block_content = block_content
        self._end_label = end_label

    @property
    def begin_label(self) -> str:
        """
        获取开始标签

        Returns
        -------
        str
            开始标签
        """
        return self._begin_label

    @property
    def block_content(self) -> ProcessCommandBlock:
        """
        获取代码块内容

        Returns
        -------
        ProcessCommandBlock
            代码块内容
        """
        return self._block_content

    @property
    def end_label(self) -> Optional[str]:
        """
        获取结束标签

        Returns
        -------
        Optional[str]
            结束标签，可能为空
        """
        return self._end_label


class ProcessCommandUnlabeledBlock(ProcessCommand):
    """处理命令：不带标签的代码块"""

    __slots__ = (
        "_block_content",
    )

    def __init__(self, block_content: ProcessCommandBlock):
        """
        初始化不带标签的代码块命令

        Parameters
        ----------
        block_content : ProcessCommandBlock
            代码块内容
        """
        self._block_content = block_content

    @property
    def block_content(self) -> ProcessCommandBlock:
        """
        获取代码块内容

        Returns
        -------
        ProcessCommandBlock
            代码块内容
        """
        return self._block_content


class ProcessCommandLabeledControl(ProcessCommand):
    """处理命令：带标签的控制语句"""

    __slots__ = (
        "_begin_label",
        "_control_statement",
        "_end_label",
    )

    def __init__(self,
                 begin_label: str,
                 control_statement: ProcessCommand,
                 end_label: Optional[str]):
        """
        初始化带标签的控制语句命令

        Parameters
        ----------
        begin_label : str
            开始标签
        control_statement : ProcessCommand
            控制语句
        end_label : Optional[str]
            结束标签，可选
        """
        self._begin_label = begin_label
        self._control_statement = control_statement
        self._end_label = end_label

    @property
    def begin_label(self) -> str:
        """
        获取开始标签

        Returns
        -------
        str
            开始标签
        """
        return self._begin_label

    @property
    def control_statement(self) -> ProcessCommand:
        """
        获取控制语句

        Returns
        -------
        ProcessCommand
            控制语句
        """
        return self._control_statement

    @property
    def end_label(self) -> Optional[str]:
        """
        获取结束标签

        Returns
        -------
        Optional[str]
            结束标签，可能为空
        """
        return self._end_label


class ProcessCommandLoop(ProcessCommand):
    """处理命令：LOOP 循环语句"""

    __slots__ = (
        "_statement_list",
    )

    def __init__(self, statement_list: List[ProcessCommand]):
        """
        初始化 LOOP 循环语句命令

        Parameters
        ----------
        statement_list : List[ProcessCommand]
            循环体语句列表
        """
        self._statement_list = statement_list

    @property
    def statement_list(self) -> List[ProcessCommand]:
        """
        获取循环体语句列表

        Returns
        -------
        List[ProcessCommand]
            循环体语句列表
        """
        return self._statement_list


class ProcessCommandWhile(ProcessCommand):
    """处理命令：WHILE 循环语句"""

    __slots__ = (
        "_condition",
        "_statement_list",
    )

    def __init__(self, condition: Expression, statement_list: List[ProcessCommand]):
        """
        初始化 WHILE 循环语句命令

        Parameters
        ----------
        condition : Expression
            循环条件表达式
        statement_list : List[ProcessCommand]
            循环体语句列表
        """
        self._condition = condition
        self._statement_list = statement_list

    @property
    def condition(self) -> Expression:
        """
        获取循环条件表达式

        Returns
        -------
        Expression
            循环条件表达式
        """
        return self._condition

    @property
    def statement_list(self) -> List[ProcessCommand]:
        """
        获取循环体语句列表

        Returns
        -------
        List[ProcessCommand]
            循环体语句列表
        """
        return self._statement_list


class ProcessCommandRepeat(ProcessCommand):
    """处理命令：REPEAT...UNTIL 循环语句"""

    __slots__ = (
        "_statement_list",
        "_condition",
    )

    def __init__(self, statement_list: List[ProcessCommand], condition: Expression):
        """
        初始化 REPEAT...UNTIL 循环语句命令

        Parameters
        ----------
        statement_list : List[ProcessCommand]
            循环体语句列表
        condition : Expression
            终止条件表达式
        """
        self._statement_list = statement_list
        self._condition = condition

    @property
    def statement_list(self) -> List[ProcessCommand]:
        """
        获取循环体语句列表

        Returns
        -------
        List[ProcessCommand]
            循环体语句列表
        """
        return self._statement_list

    @property
    def condition(self) -> Expression:
        """
        获取终止条件表达式

        Returns
        -------
        Expression
            终止条件表达式
        """
        return self._condition


class ProcessCommandLeave(ProcessCommand):
    """处理命令：LEAVE 语句"""

    __slots__ = (
        "_label_name",
    )

    def __init__(self, label_name: str):
        """
        初始化 LEAVE 语句命令

        Parameters
        ----------
        label_name : str
            要离开的标签名称
        """
        self._label_name = label_name

    @property
    def label_name(self) -> str:
        """
        获取要离开的标签名称

        Returns
        -------
        str
            要离开的标签名称
        """
        return self._label_name


class ProcessCommandIterate(ProcessCommand):
    """处理命令：ITERATE 语句"""

    __slots__ = (
        "_label_name",
    )

    def __init__(self, label_name: str):
        """
        初始化 ITERATE 语句命令

        Parameters
        ----------
        label_name : str
            要迭代的标签名称
        """
        self._label_name = label_name

    @property
    def label_name(self) -> str:
        """
        获取要迭代的标签名称

        Returns
        -------
        str
            要迭代的标签名称
        """
        return self._label_name


class ProcessCommandOpen(ProcessCommand):
    """处理命令：OPEN 游标语句"""

    __slots__ = (
        "_cursor_name",
    )

    def __init__(self, cursor_name: str):
        """
        初始化 OPEN 游标语句命令

        Parameters
        ----------
        cursor_name : str
            要打开的游标名称
        """
        self._cursor_name = cursor_name

    @property
    def cursor_name(self) -> str:
        """
        获取要打开的游标名称

        Returns
        -------
        str
            要打开的游标名称
        """
        return self._cursor_name


class ProcessCommandFetch(ProcessCommand):
    """处理命令：FETCH 游标语句"""

    __slots__ = (
        "_cursor_name",
        "_variable_list",
    )

    def __init__(self, cursor_name: str, variable_list: List[str]):
        """
        初始化 FETCH 游标语句命令

        Parameters
        ----------
        cursor_name : str
            要获取数据的游标名称
        variable_list : List[str]
            用于存储获取数据的变量列表
        """
        self._cursor_name = cursor_name
        self._variable_list = variable_list

    @property
    def cursor_name(self) -> str:
        """
        获取要获取数据的游标名称

        Returns
        -------
        str
            要获取数据的游标名称
        """
        return self._cursor_name

    @property
    def variable_list(self) -> List[str]:
        """
        获取用于存储获取数据的变量列表

        Returns
        -------
        List[str]
            用于存储获取数据的变量列表
        """
        return self._variable_list


class ProcessCommandClose(ProcessCommand):
    """处理命令：CLOSE 游标语句"""

    __slots__ = (
        "_cursor_name",
    )

    def __init__(self, cursor_name: str):
        """
        初始化 CLOSE 游标语句命令

        Parameters
        ----------
        cursor_name : str
            要关闭的游标名称
        """
        self._cursor_name = cursor_name

    @property
    def cursor_name(self) -> str:
        """
        获取要关闭的游标名称

        Returns
        -------
        str
            要关闭的游标名称
        """
        return self._cursor_name


class ProcessCommandByString(ProcessCommand):
    """通过字符串定义的处理命令"""

    __slots__ = (
        "_value",
    )

    def __init__(self, value: str):
        """
        初始化通过字符串定义的处理命令

        Parameters
        ----------
        value : str
            字符串形式的命令内容
        """
        self._value = value

    @property
    def value(self) -> str:
        """
        获取字符串形式的命令内容

        Returns
        -------
        str
            字符串形式的命令内容
        """
        return self._value
