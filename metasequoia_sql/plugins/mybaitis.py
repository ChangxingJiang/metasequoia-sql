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
import enum
from typing import Union, List, Optional, Any

from metasequoia_sql import SQLType, ASTBase
from metasequoia_sql.analyzer import AnalyzerRecursionListBase, CurrentUsedQuoteColumn
from metasequoia_sql.lexical import ASTParser, AstParseStatus, AMTBaseSingle, AMTMark
from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import SQLParser, ASTGeneralExpression, ASTSingleSelectStatement


class ASTParseStatusMyBatis(enum.Enum):
    """新增的 MyBaits 匹配状态"""
    IN_MYBATIS = enum.auto()


class ASTParserMyBatis(ASTParser):
    """继承并重写支持 MaBatis 语法的状态机处理方法"""

    def handle_change(self):
        """处理单个变化"""
        # 进入 MyBatis 匹配状态
        if self.status == AstParseStatus.WAIT_TOKEN and self.scanner.now == "#" and self.scanner.next1 == "{":
            self.set_status(ASTParseStatusMyBatis.IN_MYBATIS)
            self.cache_add()
            self.cache_add()
            return

        # 处理 MyBatis 匹配状态
        if self.status == ASTParseStatusMyBatis.IN_MYBATIS:
            if self.scanner.now == "}":
                self.cache_add_and_handle_end_word()
                self.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                self.cache_add()
            return

        super().handle_change()

    def handle_end_word(self):
        """处理词语"""
        origin = self.cache_get()
        if origin.startswith("#{") and origin.endswith("}"):
            self.cache_reset()
            self.stack[-1].append(AMTBaseSingle(origin, {AMTMark.NAME, AMTMark.CUSTOM}))
            return
        super().handle_end_word()

    def handle_last(self):
        """处理最后一个词语是 MyBatis 参数的情况"""
        if self.status == ASTParseStatusMyBatis.IN_MYBATIS:
            self.handle_end_word()
            self.set_status(AstParseStatus.WAIT_TOKEN)
            return
        super().handle_last()


@dataclasses.dataclass(slots=True)
class SQLMyBatisExpression(ASTGeneralExpression):
    """增加 MyBatis 元素节点作为一般表达式的子类"""

    mybatis_source: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        return self.mybatis_source


class SQLParserMyBatis(SQLParser):
    """继承并重写解析器以支持 MyBatis 元素解析"""

    @classmethod
    def build_token_scanner(cls, string: str) -> TokenScanner:
        """构造词法扫描器"""
        context_automaton = ASTParserMyBatis(string)
        context_automaton.parse()
        return TokenScanner(context_automaton.result(), ignore_space=True, ignore_comment=True)

    @classmethod
    def parse_general_expression_element(cls, scanner_or_string: Union[TokenScanner, str],
                                         maybe_window: bool) -> ASTGeneralExpression:
        """重写一般表达式元素解析逻辑"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search(AMTMark.CUSTOM):
            return SQLMyBatisExpression(mybatis_source=scanner.pop_as_source())
        return super().parse_general_expression_element(scanner, maybe_window)


class GetAllMybatisParams(AnalyzerRecursionListBase):
    """获取使用的 MyBatis 参数"""

    @classmethod
    def custom_handle_node(cls, node: ASTBase) -> Optional[List[Any]]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source(SQLType.DEFAULT)[2:-1]]
        return None


class GetMybatisParamInWhereClause(AnalyzerRecursionListBase):
    """获取 WHERE 子句中的 Mybatis 参数"""

    @classmethod
    def custom_handle_node(cls, node: ASTBase) -> Optional[List[Any]]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source(SQLType.DEFAULT)[2:-1]]
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle_node(node.where_clause)
        return None


class GetMybatisParamInGroupByClause(AnalyzerRecursionListBase):
    """获取 GROUP BY 子句中的 Mybatis 参数"""

    @classmethod
    def custom_handle_node(cls, node: ASTBase) -> Optional[List[Any]]:
        """自定义的处理规则"""
        if isinstance(node, SQLMyBatisExpression):
            return [node.source(SQLType.DEFAULT)[2:-1]]
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle_node(node.group_by_clause)
        return None


if __name__ == "__main__":
    def test_main():
        """测试主逻辑"""
        test_sql = "SELECT shohin_mei FROM Shohin WHERE #{hanbai_tanka} > 500 GROUP BY #{tanka};"

        statements = SQLParserMyBatis.parse_statements(test_sql)
        for statement in statements:
            print(statement)
            print(statement.source(SQLType.MYSQL))
            print(CurrentUsedQuoteColumn.handle(statement))
            print(GetAllMybatisParams().handle(statement))
            print(GetMybatisParamInWhereClause().handle(statement))
            print(GetMybatisParamInGroupByClause().handle(statement))


    test_main()
