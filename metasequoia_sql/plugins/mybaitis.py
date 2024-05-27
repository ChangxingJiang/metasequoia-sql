"""
MyBatis 语法处理插件

重写词法分析逻辑：
1. 增加自动机状态类型类（ASTParseStatusMyBatis）
2. 继承并重写支持 MaBatis 语法的状态机处理方法（ASTParserMyBatis）

重写句法分析逻辑：
1. 增加 MyBatis 元素节点作为一般表达式的子类（SQLMyBatisExpression）
2. 继承并重写解析器以支持 MyBatis 元素解析（SQLParserMyBatis）
"""

import dataclasses
from typing import Union, List

from metasequoia_sql import SQLType, ASTBase
from metasequoia_sql.analyzer import AnalyzerRecursionASTToListBase, CurrentUsedQuoteColumn
from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import SQLParser, ASTSingleSelectStatement
from metasequoia_sql.lexical import FSMMachine, FSMStatus, AMTMark, FSMMemory, FSMOperate


class FSMMachineMyBatis(FSMMachine):
    """继承并重写支持 MaBatis 语法的状态机处理方法"""

    def handle(self, memory: FSMMemory, ch: str) -> bool:
        """处理单个变化"""
        if memory.status == FSMStatus.WAIT and ch == "#":
            return FSMOperate.add_cache_to(FSMStatus.CUSTOM_1).execute(memory, ch)
        if memory.status == FSMStatus.CUSTOM_1:  # 在 # 之后
            if ch == "{":
                return FSMOperate.add_cache_to(FSMStatus.CUSTOM_2).execute(memory, ch)
            elif ch == "<END>":
                return FSMOperate.handle_cache_to_end(marks=AMTMark.NAME | AMTMark.COMMENT).execute(memory, ch)
            else:
                return FSMOperate.add_cache_to(FSMStatus.IN_EXPLAIN_1).execute(memory, ch)
        if memory.status == FSMStatus.CUSTOM_2:  # MyBatis 匹配状态
            if ch == "}":
                return FSMOperate.add_and_handle_cache_to_wait(marks=AMTMark.NAME | AMTMark.CUSTOM_1
                                                               ).execute(memory, ch)
            elif ch == "<END>":
                return FSMOperate.handle_cache_to_end(marks=AMTMark.NAME | AMTMark.COMMENT).execute(memory, ch)
            else:
                return FSMOperate.add_cache_to(FSMStatus.CUSTOM_2).execute(memory, ch)
        return super().handle(memory, ch)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SQLMyBatisExpression(ASTBase):
    """增加 MyBatis 元素节点作为一般表达式的子类"""

    mybatis_source: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        return self.mybatis_source


class SQLParserMyBatis(SQLParser):
    """继承并重写解析器以支持 MyBatis 元素解析"""

    @classmethod
    def _build_token_scanner(cls, string: str) -> TokenScanner:
        """构造词法扫描器"""
        return TokenScanner(FSMMachineMyBatis.parse(string))

    @classmethod
    def parse_unary_level_expression(cls, scanner_or_string: Union[TokenScanner, str],
                                     sql_type: SQLType = SQLType.DEFAULT
                                     ) -> ASTBase:
        """重写一般表达式元素解析逻辑"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search(AMTMark.CUSTOM_1):
            return SQLMyBatisExpression(mybatis_source=scanner.pop_as_source())
        return super()._parse_unary_level_expression(scanner, sql_type)


class GetAllMybatisParams(AnalyzerRecursionASTToListBase):
    """获取使用的 MyBatis 参数"""

    @classmethod
    def handle(cls, node: ASTBase) -> List[str]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source()[2:-1]]
        return cls.default_handle_node(node)


class GetMybatisParamInWhereClause(AnalyzerRecursionASTToListBase):
    """获取 WHERE 子句中的 Mybatis 参数"""

    @classmethod
    def handle(cls, node: ASTBase) -> List[str]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source()[2:-1]]
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle(node.where_clause)
        return cls.default_handle_node(node)


class GetMybatisParamInGroupByClause(AnalyzerRecursionASTToListBase):
    """获取 GROUP BY 子句中的 Mybatis 参数"""

    @classmethod
    def handle(cls, node: ASTBase) -> List[str]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source()[2:-1]]
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle(node.group_by_clause)
        return cls.default_handle_node(node)


if __name__ == "__main__":
    def test_main():
        """测试主逻辑"""
        test_sql = "SELECT shohin_mei FROM Shohin WHERE #{hanbai_tanka} > 500 GROUP BY #{tanka};"

        statements = SQLParserMyBatis.parse_statements(test_sql)
        for statement in statements:
            if isinstance(statement, ASTSingleSelectStatement):
                print(statement)
                print(statement.source(SQLType.MYSQL))
                print(CurrentUsedQuoteColumn.handle(statement))
                print(GetAllMybatisParams().handle(statement))
                print(GetMybatisParamInWhereClause().handle(statement))
                print(GetMybatisParamInGroupByClause().handle(statement))


    test_main()
