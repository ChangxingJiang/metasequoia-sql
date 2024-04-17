"""
获取使用的字段列表
"""

from typing import Optional, List, Dict

from metasequoia_sql.analyzer.base import (AnalyzerRecursionListBase, AnalyzerSelectDictBase, AnalyzerSelectListBase)
from metasequoia_sql.analyzer.tool import QuoteNameColumn, QuoteIndexColumn, QuoteColumn
from metasequoia_sql.core import (SQLBase, SQLColumnNameExpression, DataSource, GLOBAL_VARIABLE_NAME_SET,
                                  SQLSubQueryExpression,
                                  SQLSingleSelectStatement)

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
]


class CurrentUsedQuoteWithAliasIndexColumns(AnalyzerRecursionListBase):
    """获取当前层级（不递归分析子查询）中，直接使用的字段名称（包含字段名、别名、列序号 3 种类型）"""

    @classmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[List[QuoteColumn]]:
        """自定义的处理规则"""
        if (isinstance(node, SQLColumnNameExpression)
                and node.source(DataSource.DEFAULT) not in GLOBAL_VARIABLE_NAME_SET):
            return [QuoteNameColumn(table_name=node.table, column_name=node.column)]
        # if isinstance(node, SQLNormalGroupByClause):  # TODO 处理 GROUP BY 和 ORDER BY 语句
        #     result = []
        #     for column in node.columns:
        #         if isinstance(column, SQLLiteralExpression):
        #             result.append(QuoteIndexColumn(column_index=column.as_int()))
        #         else:
        #             result.extend(cls.handle_node(column))
        #     return result
        if isinstance(node, SQLSubQueryExpression):
            return []
        return None


class CurrentColumnAliasToQuoteHash(AnalyzerSelectDictBase):
    """获取当前层级（不递归分析子查询）中，别名到引用字段的映射关系"""

    @classmethod
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteNameColumn]:
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteNameColumn]:
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteNameColumn]:
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteNameColumn]:
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteNameColumn]:
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteNameColumn]:
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
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteNameColumn]:
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
