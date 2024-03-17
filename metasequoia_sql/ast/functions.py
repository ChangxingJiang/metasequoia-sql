"""
AST 对外暴露的辅助函数
"""

import enum
from typing import Union

from metasequoia_sql.ast.nodes import *
from metasequoia_sql.ast.old_nodes import ASTParenthesis, ASTLeaf, ASTStatement
from metasequoia_sql.ast.parser import ASTBuilder
from metasequoia_sql.common.text_scanner import TextScanner
from metasequoia_sql.errors import AstParseError


class ParseStatus(enum.Enum):
    """SQL 源码的解析状态"""
    WAIT_TOKEN = enum.auto()  # 前一个字符是开头、空白字符或上一个 token 的结尾，正等待新的 token
    IS_IN_NORMAL = enum.auto()  # 当前正在正常词语中
    IS_IN_DOUBLE_QUOTE = enum.auto()  # 当前正在双引号 " 中
    IS_IN_SINGLE_QUOTE = enum.auto()  # 当前正在单引号 ' 中
    IS_IN_BACK_QUOTE = enum.auto()  # 当前正在反引号 ` 中
    IS_IN_EXPLAIN_1 = enum.auto()  # 当前在 # 标记的注释中
    IS_IN_EXPLAIN_2 = enum.auto()  # 当前在 /* 和 */ 标注的注释中
    FAIL = enum.auto()  # 无法解析的 SQL 格式


def parse(text: str) -> List[AST]:
    """把源码解析为 AST 节点"""
    stack: List[List[Union[AST]]] = [[]]
    scanner = TextScanner(text.replace("\r\n", "\n"))
    status: ParseStatus = ParseStatus.WAIT_TOKEN
    while not scanner.is_finish:
        if status == ParseStatus.WAIT_TOKEN:  # 前一个字符是空白字符
            if scanner.get() == " ":
                stack[-1].append(ASTSpace(scanner.pop()))
            elif scanner.get() == "\n":
                stack[-1].append(ASTLineBreak(scanner.pop()))
            elif scanner.get() == "\"":
                stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_DOUBLE_QUOTE
            elif scanner.get() == "'":
                stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_SINGLE_QUOTE
            elif scanner.get() == "`":
                stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_BACK_QUOTE
            elif scanner.get() == "#":
                stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_EXPLAIN_1
            elif scanner.get() == "/":
                if scanner.get() == "*":
                    stack[-1].append(ASTBuilder([scanner.pop()]))
                    status = ParseStatus.IS_IN_EXPLAIN_2
                else:
                    stack[-1].append(ASTBuilder([scanner.pop()]))
                    status = ParseStatus.IS_IN_NORMAL
            elif scanner.get() == "(":
                stack[-1].append(ASTBuilder())  # 插入语的语法树
                stack.append([])
                scanner.pop()
                status = ParseStatus.WAIT_TOKEN
            elif scanner.get() == ")":
                if len(stack) > 1:
                    tokens = stack.pop()
                    stack[-1].append(ASTParenthesis(tokens, "(", ")"))
                    status = ParseStatus.WAIT_TOKEN
                    scanner.pop()
                else:
                    raise AstParseError("')' 数量大于 '('")
            else:
                stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_NORMAL
        elif status == ParseStatus.IS_IN_DOUBLE_QUOTE:
            if scanner.last != "\\" and scanner.now == "\"" and not scanner.next == "\"":
                builder = stack[-1].pop()
                builder.append(scanner.pop())
                stack[-1].append(ASTLiteralString(builder.source))
                status = ParseStatus.WAIT_TOKEN
            else:
                stack[-1][-1].append(scanner.pop())
        elif status == ParseStatus.IS_IN_SINGLE_QUOTE:
            if scanner.last != "\\" and scanner.now == "'" and not scanner.next == "'":
                builder = stack[-1].pop()
                builder.append(scanner.pop())
                stack[-1].append(ASTLiteralString(builder.source))
                status = ParseStatus.WAIT_TOKEN
            else:
                stack[-1][-1].append(scanner.pop())
        elif status == ParseStatus.IS_IN_BACK_QUOTE:
            if scanner.now == "`":
                builder = stack[-1].pop()
                builder.append(scanner.pop())
                stack[-1].append(ASTIdentifier(builder.source))
                status = ParseStatus.WAIT_TOKEN
            else:
                stack[-1][-1].append(scanner.pop())
        elif status == ParseStatus.IS_IN_EXPLAIN_1:
            if scanner.now == "\n":
                builder = stack[-1].pop()
                builder.append(scanner.pop())
                stack[-1].append(ASTLeaf(builder.source))
                status = ParseStatus.WAIT_TOKEN
            else:
                stack[-1][-1].append(scanner.pop())
        elif status == ParseStatus.IS_IN_EXPLAIN_2:
            if scanner.now == "/" and scanner.last == "*":
                builder = stack[-1].pop()
                builder.append(scanner.pop())
                stack[-1].append(ASTLeaf(builder.source))
                status = ParseStatus.WAIT_TOKEN
            else:
                stack[-1][-1].append(scanner.pop())
        elif status == ParseStatus.IS_IN_NORMAL:
            if scanner.now in {" ", "\n", ",", ";", "+", "-", "*", "/", "="}:
                builder = stack[-1].pop()
                stack[-1].append(ASTLeaf(builder.source))
                stack[-1].append(ASTLeaf(scanner.pop()))
                status = ParseStatus.WAIT_TOKEN
            elif scanner.now == "\"":
                if stack[-1][-1].source == "b":  # 兼容类似字符串 b'0'
                    stack[-1][-1].append(scanner.pop())
                else:
                    builder = stack[-1].pop()
                    stack[-1].append(ASTLeaf(builder.source))
                    stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_DOUBLE_QUOTE
            elif scanner.now == "'":
                if stack[-1][-1].source == "b":  # 兼容类似字符串 b'0'
                    stack[-1][-1].append(scanner.pop())
                else:
                    builder = stack[-1].pop()
                    stack[-1].append(ASTLeaf(builder.source))
                    stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_SINGLE_QUOTE
            elif scanner.now == "`":
                stack[-1].append(ASTLeaf(stack[-1].pop().source))
                stack[-1].append(ASTBuilder([scanner.pop()]))
                status = ParseStatus.IS_IN_BACK_QUOTE
            elif scanner.now == "(":
                stack[-1].append(ASTLeaf(stack[-1].pop().source))
                stack[-1].append(ASTBuilder())  # 插入语的语法树
                stack.append([])
                scanner.pop()
                status = ParseStatus.WAIT_TOKEN
            elif scanner.now == ")":
                stack[-1].append(ASTLeaf(stack[-1].pop().source))
                if len(stack) > 1:
                    tokens = stack.pop()
                    stack[-1].append(ASTParenthesis(tokens, "(", ")"))
                    status = ParseStatus.WAIT_TOKEN
                    scanner.pop()
                else:
                    raise AstParseError("')' 数量大于 '('")
            else:
                stack[-1][-1].append(scanner.pop())
                status = ParseStatus.IS_IN_NORMAL
        else:
            stack[-1][-1].append(scanner.pop())

    if len(stack) > 1:
        raise AstParseError("'(' 数量大于 ')'")
    else:
        if status == ParseStatus.IS_IN_NORMAL:  # 末尾没有分号的情况
            stack[-1].append(ASTLeaf(stack[-1].pop().source))
        return [ASTStatement(stack[0])]


def iter_child_nodes(node: AST) -> List[AST]:
    """有序地产生 node 所有的直接子节点的列表"""
    return node.children


def dump(node: AST) -> str:
    """返回 node 中树结构的格式化转储。这主要适用于调试目的"""
    return node.source
