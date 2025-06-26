"""
INTO 子句（into clause）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.basic.variable import Variable

__all__ = [
    "FileFieldOption",
    "FileLineOption",
    "IntoClause",
    "IntoClauseOutfile",
    "IntoClauseDumpfile",
    "IntoClauseVariable",
]


class FileFieldOption(Node):
    """外部文件字段格式选项"""

    __slots__ = ["_terminated_by", "_optionally_enclosed_by", "_enclosed_by", "_escaped_by"]

    def __init__(self,
                 terminated_by: Optional[str] = None,
                 optionally_enclosed_by: Optional[str] = None,
                 enclosed_by: Optional[str] = None,
                 escaped_by: Optional[str] = None):
        """初始化外部文件字段格式选项
        
        Parameters
        ----------
        terminated_by : Optional[str], optional
            字段终止符, by default None
        optionally_enclosed_by : Optional[str], optional
            可选的字段包围符, by default None
        enclosed_by : Optional[str], optional
            字段包围符, by default None
        escaped_by : Optional[str], optional
            转义字符, by default None
        """
        self._terminated_by = terminated_by
        self._optionally_enclosed_by = optionally_enclosed_by
        self._enclosed_by = enclosed_by
        self._escaped_by = escaped_by

    @property
    def terminated_by(self) -> str:
        """获取字段终止符
        
        Returns
        -------
        str
            字段终止符
        """
        return self._terminated_by

    @property
    def optionally_enclosed_by(self) -> str:
        """获取可选的字段包围符
        
        Returns
        -------
        str
            可选的字段包围符
        """
        return self._optionally_enclosed_by

    @property
    def enclosed_by(self) -> str:
        """获取字段包围符
        
        Returns
        -------
        str
            字段包围符
        """
        return self._enclosed_by

    @property
    def escaped_by(self) -> str:
        """获取转义字符
        
        Returns
        -------
        str
            转义字符
        """
        return self._escaped_by

    def merge(self, other: "FileFieldOption") -> "FileFieldOption":
        """合并另一个文件字段选项
        
        Parameters
        ----------
        other : FileFieldOption
            要合并的文件字段选项
            
        Returns
        -------
        FileFieldOption
            合并后的文件字段选项
        """
        if not isinstance(other, FileFieldOption):
            raise TypeError("other must be a FileFieldOption")
        if other.terminated_by is not None:
            self._terminated_by = other.terminated_by
        if other.optionally_enclosed_by is not None:
            self._optionally_enclosed_by = other.optionally_enclosed_by
        if other.enclosed_by is not None:
            self._enclosed_by = other.enclosed_by
        if other.escaped_by is not None:
            self._escaped_by = other.escaped_by
        return self


class FileLineOption(Node):
    """外部文件行字段格式选项"""

    __slots__ = ["_terminated_by", "_starting_by"]

    def __init__(self,
                 terminated_by: Optional[str] = None,
                 starting_by: Optional[str] = None):
        """初始化外部文件行字段格式选项
        
        Parameters
        ----------
        terminated_by : Optional[str], optional
            行终止符, by default None
        starting_by : Optional[str], optional
            行起始符, by default None
        """
        self._terminated_by = terminated_by
        self._starting_by = starting_by

    @property
    def terminated_by(self) -> Optional[str]:
        """获取行终止符
        
        Returns
        -------
        Optional[str]
            行终止符
        """
        return self._terminated_by

    @property
    def starting_by(self) -> Optional[str]:
        """获取行起始符
        
        Returns
        -------
        Optional[str]
            行起始符
        """
        return self._starting_by

    def merge(self, other: "FileLineOption") -> "FileLineOption":
        """合并另一个文件行选项
        
        Parameters
        ----------
        other : FileLineOption
            要合并的文件行选项
            
        Returns
        -------
        FileLineOption
            合并后的文件行选项
        """
        if not isinstance(other, FileLineOption):
            raise TypeError("other must be a FileFieldOption")
        if other.terminated_by is not None:
            self._terminated_by = other.terminated_by
        if other.starting_by is not None:
            self._starting_by = other.starting_by
        return self


class IntoClause(Node):
    """INTO 子句的抽象类"""


class IntoClauseOutfile(IntoClause):
    """INTO 子句（导出结果集到外部格式化文件）"""

    __slots__ = ["_file_path", "_charset", "_field_option", "_line_option"]

    def __init__(self, file_path: str, charset: Optional["Charset"], field_option: FileFieldOption,
                 line_option: FileLineOption):
        """初始化 INTO OUTFILE 子句
        
        Parameters
        ----------
        file_path : str
            输出文件路径
        charset : Optional[Charset]
            字符集
        field_option : FileFieldOption
            字段选项
        line_option : FileLineOption
            行选项
        """
        self._file_path = file_path
        self._charset = charset
        self._field_option = field_option
        self._line_option = line_option

    @property
    def file_path(self) -> str:
        """获取输出文件路径
        
        Returns
        -------
        str
            输出文件路径
        """
        return self._file_path

    @property
    def charset(self) -> "Charset":
        """获取字符集
        
        Returns
        -------
        Charset
            字符集
        """
        return self._charset

    @property
    def field_option(self) -> FileFieldOption:
        """获取字段选项
        
        Returns
        -------
        FileFieldOption
            字段选项
        """
        return self._field_option

    @property
    def line_option(self) -> FileLineOption:
        """获取行选项
        
        Returns
        -------
        FileLineOption
            行选项
        """
        return self._line_option


class IntoClauseDumpfile(IntoClause):
    """INTO 子句（导出结果集到外部文件）"""

    __slots__ = ["_file_path"]

    def __init__(self, file_path: str):
        """初始化 INTO DUMPFILE 子句
        
        Parameters
        ----------
        file_path : str
            输出文件路径
        """
        self._file_path = file_path

    @property
    def file_path(self) -> str:
        """获取输出文件路径
        
        Returns
        -------
        str
            输出文件路径
        """
        return self._file_path


class IntoClauseVariable(IntoClause):
    """INTO 子句（导出结果集到变量）"""

    __slots__ = ["_variable_list"]

    def __init__(self, variable_list: List["Variable"]):
        """初始化 INTO 变量子句
        
        Parameters
        ----------
        variable_list : List[Variable]
            变量列表
        """
        self._variable_list = variable_list

    @property
    def variable_list(self) -> List["Variable"]:
        """获取变量列表
        
        Returns
        -------
        List[Variable]
            变量列表
        """
        return self._variable_list
