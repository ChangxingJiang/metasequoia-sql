"""
AST 对外暴露的辅助函数
"""

from metasequoia_sql.ast.nodes import *
from metasequoia_sql.ast.parser import AstParseContext, AstParseStatus
from metasequoia_sql.errors import AstParseError


def parse(text: str) -> List[AST]:
    """把源码解析为 AST 节点"""
    context = AstParseContext(text)
    scanner = context.scanner
    while not scanner.is_finish:
        if context.status == AstParseStatus.WAIT_TOKEN:  # 前一个字符是空白字符
            if context.now_ch == " ":
                context.move_handle_space()
            elif context.now_ch == "\n":
                context.move_handle_line_break()
            elif context.now_ch == "\"":
                context.move_cache_reset_and_add()
                context._stand_set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif context.now_ch == "'":
                context.move_cache_reset_and_add()
                context._stand_set_status(AstParseStatus.IN_SINGLE_QUOTE)
            elif context.now_ch == "`":
                context.move_cache_reset_and_add()
                context._stand_set_status(AstParseStatus.IN_BACK_QUOTE)
            elif context.now_ch == "#":
                context.move_cache_reset_and_add()
                context._stand_set_status(AstParseStatus.IN_EXPLAIN_1)
            elif context.now_ch == "/":
                if context.next_ch == "*":
                    context.move_cache_reset_and_add()
                    context._stand_set_status(AstParseStatus.IN_EXPLAIN_2)
                else:
                    context.move_cache_reset_and_add()
                    context._stand_set_status(AstParseStatus.IN_WORD)
            elif context.now_ch == "(":
                context.stack.append([])
                scanner.move()
                context._stand_set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == ")":
                print(context.stack)
                if len(context.stack) > 1:
                    tokens = context.stack.pop()
                    context.stack[-1].append(ASTParenthesis(tokens, "(", ")"))
                    context._stand_set_status(AstParseStatus.WAIT_TOKEN)
                    scanner.move()
                else:
                    raise AstParseError("')' 数量大于 '('")
            else:
                context.move_cache_reset_and_add()
                context._stand_set_status(AstParseStatus.IN_WORD)
        elif context.status == AstParseStatus.IN_DOUBLE_QUOTE:
            if context.last_ch != "\\" and context.now_ch == "\"" and not context.next_ch == "\"":
                context.move_cache_add()
                context.handle_end_word()
            else:
                context.move_cache_add()
        elif context.status == AstParseStatus.IN_SINGLE_QUOTE:
            if context.last_ch != "\\" and context.now_ch == "'" and not context.next_ch == "'":
                context.move_cache_add()
                context.handle_end_word()
            else:
                context.move_cache_add()
        elif context.status == AstParseStatus.IN_BACK_QUOTE:
            if context.now_ch == "`":
                context.move_cache_add()
                context.handle_end_word()
            else:
                context.move_cache_add()
        elif context.status == AstParseStatus.IN_EXPLAIN_1 and context.now_ch == "\n":
            context.handle_end_word()
        elif context.status == AstParseStatus.IN_EXPLAIN_2:
            if context.now_ch == "/" and context.last_ch == "*":
                context.move_cache_add()
                context.handle_end_word()
            else:
                context.move_cache_add()
        elif context.status == AstParseStatus.IN_WORD:
            if context.now_ch in {" ", "\n", ",", ";", "+", "-", "*", "/", "="}:
                context.handle_end_word()
            elif context.now_ch == "\"":
                if context.stack[-1][-1].source == "b":  # 兼容类似字符串 b'0'
                    context.move_cache_add()
                    context._stand_set_status(AstParseStatus.IN_DOUBLE_QUOTE)
                else:
                    context.handle_end_word()
            elif context.now_ch == "'":
                if context.stack[-1][-1].source == "b":  # 兼容类似字符串 b'0'
                    context.move_cache_add()
                    context._stand_set_status(AstParseStatus.IN_SINGLE_QUOTE)
                else:
                    context.handle_end_word()
            elif context.now_ch == "`":
                context.handle_end_word()
            elif context.now_ch == "(":
                context.handle_end_word()
                context.stack.append([])
                scanner.move()
            elif context.now_ch == ")":
                context.handle_end_word()
                if len(context.stack) > 1:
                    tokens = context.stack.pop()
                    context.stack[-1].append(ASTParenthesis(tokens, "(", ")"))
                    scanner.move()
                else:
                    raise AstParseError("')' 数量大于 '('")
            else:
                context.move_cache_add()
        else:
            context.move_cache_add()

    if len(context.stack) > 1:
        raise AstParseError("'(' 数量大于 ')'")
    else:
        if context.status == AstParseStatus.IN_WORD:  # 末尾没有分号的情况
            context.handle_end_word()
        return [ASTStatement(context.stack[0])]


def iter_child_nodes(node: AST) -> List[AST]:
    """有序地产生 node 所有的直接子节点的列表"""
    return node.children


def dump(node: AST) -> str:
    """返回 node 中树结构的格式化转储。这主要适用于调试目的"""
    return node.source
