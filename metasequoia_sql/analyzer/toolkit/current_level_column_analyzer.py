"""
当前层级字段相关分析器
"""

import abc
from typing import List, Dict, Any

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerSelectASTToListBase, AnalyzerSelectASTToDictBase
from metasequoia_sql.analyzer.node import StandardColumn, QuoteColumn
from metasequoia_sql.analyzer.toolkit import CurrentNodeUsedQuoteColumn

__all__ = [
    "CurrentLevelColumnAliasToQuoteHash",
    "CurrentLevelColumnIndexToQuoteHash",
    "CurrentUsedQuoteColumn",
    "CurrentSelectClauseUsedQuoteColumn",
    "CurrentJoinClauseUsedQuoteColumn",
    "CurrentWhereClauseUsedQuoteColumn",
    "CurrentGroupByClauseUsedQuoteColumn",
    "CurrentHavingClauseUsedQuoteColumn",
    "CurrentOrderByClauseUsedQuoteColumn",
    "CurrentColumnSelectToDirectQuoteHash",
]


class CurrentLevelColumnAliasToQuoteHash(AnalyzerSelectASTToDictBase):
    """获取当前层级（不递归分析子查询）中，别名到引用字段的映射关系"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> Dict[QuoteColumn, List[QuoteColumn]]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement
                                       ) -> Dict[QuoteColumn, List[QuoteColumn]]:
        """处理 SQLSingleSelectStatement 类型节点"""
        result = {}
        for column in node.select_clause.columns:
            if column.alias is not None:
                alias_name = QuoteColumn(column_name=column.alias.name)
                result[alias_name] = CurrentNodeUsedQuoteColumn.handle(column.value)
        return result


class CurrentLevelColumnIndexToQuoteHash(AnalyzerSelectASTToDictBase):
    """获取当前层级（不递归分析子查询）中，列序号到引用字段的映射关系"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> Dict[QuoteColumn, List[QuoteColumn]]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement
                                       ) -> Dict[QuoteColumn, List[QuoteColumn]]:
        """处理逻辑"""
        result = {}
        for column_index, column in enumerate(node.select_clause.columns):
            quote_column = QuoteColumn(column_name=None, column_idx=column_index + 1)
            result[quote_column] = CurrentNodeUsedQuoteColumn.handle(column.value)
        return result


class CurrentQuoteColumnAnalyzerBase(AnalyzerSelectASTToListBase, abc.ABC):
    """当前层级引用字段对象分析器的抽象基类"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def _format_quote_columns(cls, quote_columns: List[QuoteColumn],
                              select_statement: core.ASTSingleSelectStatement
                              ) -> List[QuoteColumn]:
        """规范化引用字段对象列表"""
        column_alias_to_quote_hash = CurrentLevelColumnAliasToQuoteHash.handle(select_statement)
        column_index_to_quote_hash = CurrentLevelColumnIndexToQuoteHash.handle(select_statement)
        formatted_quote_columns = []
        for origin_column in quote_columns:
            if origin_column in column_alias_to_quote_hash:
                formatted_quote_columns.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                formatted_quote_columns.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                formatted_quote_columns.append(origin_column)  # 引用是字段名的情况
        return formatted_quote_columns


class CurrentUsedQuoteColumn(CurrentQuoteColumnAnalyzerBase):
    """获取当前层级（不递归分析子查询）中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        return cls._format_quote_columns(CurrentNodeUsedQuoteColumn.handle(node), node)


class CurrentSelectClauseUsedQuoteColumn(CurrentQuoteColumnAnalyzerBase):
    """获取当前层级（不递归分析子查询）的 SELECT 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        return cls._format_quote_columns(CurrentNodeUsedQuoteColumn.handle(node.select_clause), node)


class CurrentJoinClauseUsedQuoteColumn(CurrentQuoteColumnAnalyzerBase):
    """获取当前层级（不递归分析子查询）的 JOIN 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        return cls._format_quote_columns(CurrentNodeUsedQuoteColumn.handle(node.join_clauses), node)


class CurrentWhereClauseUsedQuoteColumn(CurrentQuoteColumnAnalyzerBase):
    """获取当前层级（不递归分析子查询）的 WHERE 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        return cls._format_quote_columns(CurrentNodeUsedQuoteColumn.handle(node.where_clause), node)


class CurrentGroupByClauseUsedQuoteColumn(CurrentQuoteColumnAnalyzerBase):
    """获取当前层级（不递归分析子查询）的 GROUP BY 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        return cls._format_quote_columns(CurrentNodeUsedQuoteColumn.handle(node.group_by_clause), node)


class CurrentHavingClauseUsedQuoteColumn(CurrentQuoteColumnAnalyzerBase):
    """获取当前层级（不递归分析子查询）的 HAVING 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        return cls._format_quote_columns(CurrentNodeUsedQuoteColumn.handle(node.having_clause), node)


class CurrentOrderByClauseUsedQuoteColumn(CurrentQuoteColumnAnalyzerBase):
    """获取当前层级（不递归分析子查询）的 GROUP BY 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        return cls._format_quote_columns(CurrentNodeUsedQuoteColumn.handle(node.order_by_clause), node)


class CurrentColumnSelectToDirectQuoteHash(AnalyzerSelectASTToDictBase):
    """获取当前层级（不递归分析子查询）中，生成字段与直接引用的引用字段信息

    生成字段信息：字段名、字段序号

    TODO 聚集函数的结果需要修复（可以从单元测试中拿 Case）
    """

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement
                                       ) -> Dict[StandardColumn, List[QuoteColumn]]:
        result = {}
        for column_idx, column_expression in enumerate(node.select_clause.columns):
            if column_expression.alias is not None:
                select_column = StandardColumn(column_name=column_expression.alias.name, column_idx=column_idx)
            elif isinstance(column_expression.value, core.ASTColumnName):
                select_column = StandardColumn(column_name=column_expression.value.column_name,
                                               column_idx=column_idx)
            else:
                select_column = StandardColumn(column_name=column_expression.value.source(),
                                               column_idx=column_idx)
            result[select_column] = CurrentNodeUsedQuoteColumn.handle(column_expression.value)
        return result

    @classmethod
    def _collector_init(cls) -> Any:
        return {}

    @classmethod
    def _collector_merge(cls, collector1: Any, collector2: Any) -> Any:
        for key, value in collector2.items():
            if key not in collector1:
                collector1[key] = []
            collector1[key].extend(value)

    @classmethod
    def _collector_get(cls, collector: Any) -> Any:
        return collector
