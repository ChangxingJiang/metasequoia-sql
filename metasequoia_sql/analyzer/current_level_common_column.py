"""
当前层级，基于 SQL 语句的字段相关分析器
"""

from typing import List, Dict, Any

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerSelectASTToListBase, AnalyzerSelectASTToDictBase
from metasequoia_sql.analyzer.node import StandardColumn, QuoteColumn
from metasequoia_sql.analyzer.tool import QuoteIndexColumn
from metasequoia_sql.analyzer.toolkit import CurrentNodeUsedQuoteColumn

__all__ = [
    "CurrentColumnAliasToQuoteHash",
    "CurrentColumnIndexToQuoteHash",
    "CurrentUsedQuoteColumn",
    "CurrentSelectClauseUsedQuoteColumn",
    "CurrentJoinClauseUsedQuoteColumn",
    "CurrentWhereClauseUsedQuoteColumn",
    "CurrentGroupByClauseUsedQuoteColumn",
    "CurrentHavingClauseUsedQuoteColumn",
    "CurrentOrderByClauseUsedQuoteColumn",
    "CurrentColumnSelectToDirectQuoteHash",
]


class CurrentColumnAliasToQuoteHash(AnalyzerSelectASTToDictBase):
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
                result[alias_name] = CurrentNodeUsedQuoteColumn.handle(column.column_value)
        return result


class CurrentColumnIndexToQuoteHash(AnalyzerSelectASTToDictBase):
    """获取当前层级（不递归分析子查询）中，列序号到引用字段的映射关系"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> Dict[QuoteIndexColumn, List[QuoteColumn]]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement
                                       ) -> Dict[QuoteIndexColumn, List[QuoteColumn]]:
        """处理逻辑"""
        result = {}
        for column_index, column in enumerate(node.select_clause.columns):
            alias_name = QuoteIndexColumn(column_index=column_index)
            result[alias_name] = CurrentNodeUsedQuoteColumn.handle(column.column_value)
        return result


class CurrentUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取当前层级（不递归分析子查询）中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        origin_columns = CurrentNodeUsedQuoteColumn.handle(node)
        column_alias_to_quote_hash = CurrentColumnAliasToQuoteHash.handle(node)
        column_index_to_quote_hash = CurrentColumnIndexToQuoteHash.handle(node)
        result = []
        for origin_column in origin_columns:
            if origin_column in column_alias_to_quote_hash:
                result.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                result.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                result.append(origin_column)  # 引用是字段名的情况
        return result


class CurrentSelectClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取当前层级（不递归分析子查询）的 SELECT 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        origin_columns = CurrentNodeUsedQuoteColumn.handle(node.select_clause)
        column_alias_to_quote_hash = CurrentColumnAliasToQuoteHash.handle(node)
        column_index_to_quote_hash = CurrentColumnIndexToQuoteHash.handle(node)
        result = []
        for origin_column in origin_columns:
            if origin_column in column_alias_to_quote_hash:
                result.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                result.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                result.append(origin_column)  # 引用是字段名的情况
        return result


class CurrentJoinClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取当前层级（不递归分析子查询）的 JOIN 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        origin_columns = CurrentNodeUsedQuoteColumn.handle(node.join_clauses)
        column_alias_to_quote_hash = CurrentColumnAliasToQuoteHash.handle(node)
        column_index_to_quote_hash = CurrentColumnIndexToQuoteHash.handle(node)
        result = []
        for origin_column in origin_columns:
            if origin_column in column_alias_to_quote_hash:
                result.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                result.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                result.append(origin_column)  # 引用是字段名的情况
        return result


class CurrentWhereClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取当前层级（不递归分析子查询）的 WHERE 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        origin_columns = CurrentNodeUsedQuoteColumn.handle(node.where_clause)
        column_alias_to_quote_hash = CurrentColumnAliasToQuoteHash.handle(node)
        column_index_to_quote_hash = CurrentColumnIndexToQuoteHash.handle(node)
        result = []
        for origin_column in origin_columns:
            if origin_column in column_alias_to_quote_hash:
                result.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                result.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                result.append(origin_column)  # 引用是字段名的情况
        return result


class CurrentGroupByClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取当前层级（不递归分析子查询）的 GROUP BY 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        origin_columns = CurrentNodeUsedQuoteColumn.handle(node.group_by_clause)
        column_alias_to_quote_hash = CurrentColumnAliasToQuoteHash.handle(node)
        column_index_to_quote_hash = CurrentColumnIndexToQuoteHash.handle(node)
        result = []
        for origin_column in origin_columns:
            if origin_column in column_alias_to_quote_hash:
                result.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                result.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                result.append(origin_column)  # 引用是字段名的情况
        return result


class CurrentHavingClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取当前层级（不递归分析子查询）的 HAVING 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        origin_columns = CurrentNodeUsedQuoteColumn.handle(node.having_clause)
        column_alias_to_quote_hash = CurrentColumnAliasToQuoteHash.handle(node)
        column_index_to_quote_hash = CurrentColumnIndexToQuoteHash.handle(node)
        result = []
        for origin_column in origin_columns:
            if origin_column in column_alias_to_quote_hash:
                result.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                result.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                result.append(origin_column)  # 引用是字段名的情况
        return result


class CurrentOrderByClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取当前层级（不递归分析子查询）的 GROUP BY 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[QuoteColumn]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[QuoteColumn]:
        """处理逻辑"""
        origin_columns = CurrentNodeUsedQuoteColumn.handle(node.order_by_clause)
        column_alias_to_quote_hash = CurrentColumnAliasToQuoteHash.handle(node)
        column_index_to_quote_hash = CurrentColumnIndexToQuoteHash.handle(node)
        result = []
        for origin_column in origin_columns:
            if origin_column in column_alias_to_quote_hash:
                result.extend(column_alias_to_quote_hash[origin_column])  # 引用是别名的情况
            elif origin_column in column_index_to_quote_hash:
                result.extend(column_index_to_quote_hash[origin_column])  # 引用是列序号的情况
            else:
                result.append(origin_column)  # 引用是字段名的情况
        return result


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
            elif isinstance(column_expression.column_value, core.ASTColumnNameExpression):
                select_column = StandardColumn(column_name=column_expression.column_value.column_name,
                                               column_idx=column_idx)
            else:
                select_column = StandardColumn(column_name=column_expression.column_value.source(),
                                               column_idx=column_idx)
            result[select_column] = CurrentNodeUsedQuoteColumn.handle(column_expression.column_value)
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
