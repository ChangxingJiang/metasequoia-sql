"""
当前层级，基于 SQL 语句的字段相关分析器
"""

from typing import Optional, List, Dict, Any

from metasequoia_sql.analyzer.base import (AnalyzerRecursionListBase, AnalyzerSelectDictBase, AnalyzerSelectListBase,
                                           AnalyzerSelectASTToDictBase)
from metasequoia_sql.analyzer.tool import QuoteNameColumn, QuoteIndexColumn, SelectColumn
from metasequoia_sql.common import name_set
from metasequoia_sql.core import (ASTBase, ASTColumnNameExpression, SQLType,
                                  ASTSubQueryExpression,
                                  ASTSingleSelectStatement)

__all__ = [
    "CurrentUsedQuoteWithAliasIndexColumns",
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


class CurrentUsedQuoteWithAliasIndexColumns(AnalyzerRecursionListBase):
    """获取当前层级（不递归分析子查询）中，直接使用的字段名称（包含字段名、别名、列序号 3 种类型）"""

    @classmethod
    def custom_handle_node(cls, node: ASTBase) -> Optional[List[QuoteNameColumn]]:
        """自定义的处理规则"""
        if (isinstance(node, ASTColumnNameExpression)
                and node.source(SQLType.DEFAULT) not in name_set.GLOBAL_VARIABLE_NAME_SET):
            return [QuoteNameColumn(table_name=node.table, column_name=node.column)]
        if isinstance(node, ASTSubQueryExpression):
            return []
        return None


class CurrentColumnAliasToQuoteHash(AnalyzerSelectDictBase):
    """获取当前层级（不递归分析子查询）中，别名到引用字段的映射关系"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement
                                        ) -> Dict[QuoteNameColumn, List[QuoteNameColumn]]:
        """处理 SQLSingleSelectStatement 类型节点"""
        result = {}
        for column in node.select_clause.columns:
            if column.alias is not None:
                alias_name = QuoteNameColumn(column_name=column.alias.name)
                result[alias_name] = CurrentUsedQuoteWithAliasIndexColumns.handle(column.column)
        return result


class CurrentColumnIndexToQuoteHash(AnalyzerSelectDictBase):
    """获取当前层级（不递归分析子查询）中，列序号到引用字段的映射关系"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement
                                        ) -> Dict[QuoteIndexColumn, List[QuoteNameColumn]]:
        """处理逻辑"""
        result = {}
        for column_index, column in enumerate(node.select_clause.columns):
            alias_name = QuoteIndexColumn(column_index=column_index)
            result[alias_name] = CurrentUsedQuoteWithAliasIndexColumns.handle(column.column)
        return result


class CurrentUsedQuoteColumn(AnalyzerSelectListBase):
    """获取当前层级（不递归分析子查询）中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> List[QuoteNameColumn]:
        """处理逻辑"""
        origin_columns = CurrentUsedQuoteWithAliasIndexColumns.handle(node)
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


class CurrentSelectClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取当前层级（不递归分析子查询）的 SELECT 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> List[QuoteNameColumn]:
        """处理逻辑"""
        origin_columns = CurrentUsedQuoteWithAliasIndexColumns.handle(node.select_clause)
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


class CurrentJoinClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取当前层级（不递归分析子查询）的 JOIN 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> List[QuoteNameColumn]:
        """处理逻辑"""
        origin_columns = CurrentUsedQuoteWithAliasIndexColumns.handle(node.join_clauses)
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


class CurrentWhereClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取当前层级（不递归分析子查询）的 WHERE 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> List[QuoteNameColumn]:
        """处理逻辑"""
        origin_columns = CurrentUsedQuoteWithAliasIndexColumns.handle(node.where_clause)
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


class CurrentGroupByClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取当前层级（不递归分析子查询）的 GROUP BY 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> List[QuoteNameColumn]:
        """处理逻辑"""
        origin_columns = CurrentUsedQuoteWithAliasIndexColumns.handle(node.group_by_clause)
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


class CurrentHavingClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取当前层级（不递归分析子查询）的 HAVING 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> List[QuoteNameColumn]:
        """处理逻辑"""
        origin_columns = CurrentUsedQuoteWithAliasIndexColumns.handle(node.having_clause)
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


class CurrentOrderByClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取当前层级（不递归分析子查询）的 GROUP BY 子句中，直接使用的字段引用名称（仅包含字段名的格式，并将别名、列序号映射为字段名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> List[QuoteNameColumn]:
        """处理逻辑"""
        origin_columns = CurrentUsedQuoteWithAliasIndexColumns.handle(node.order_by_clause)
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
    def handle_single_select_statement(cls, node: ASTSingleSelectStatement
                                       ) -> Dict[SelectColumn, List[QuoteNameColumn]]:
        result = {}
        for column_idx, column_expression in enumerate(node.select_clause.columns):
            if column_expression.alias is not None:
                select_column = SelectColumn(column_name=column_expression.alias.name, column_idx=column_idx)
            elif isinstance(column_expression.column, ASTColumnNameExpression):
                select_column = SelectColumn(column_name=column_expression.column.column, column_idx=column_idx)
            else:
                select_column = SelectColumn(column_name=column_expression.column.source(SQLType.DEFAULT),
                                             column_idx=column_idx)
            result[select_column] = CurrentUsedQuoteWithAliasIndexColumns.handle(column_expression.column)
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
