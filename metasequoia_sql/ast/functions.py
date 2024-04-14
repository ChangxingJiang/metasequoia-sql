"""
AST 对外暴露的辅助函数
"""

from typing import List

from metasequoia_sql.ast.nodes import AST
from metasequoia_sql.ast.parser import AstParseContext, AstParseStatus
from metasequoia_sql.errors import AstParseError

__all__ = ["parse_as_tokens"]


def parse_as_tokens(text: str) -> List[AST]:
    """把源码解析为 AST 节点列表"""
    context = AstParseContext(format_sql_text(text))
    while not context.is_finish:
        if context.status == AstParseStatus.WAIT_TOKEN:  # 前一个字符是空白字符
            if context.now_ch == "/" and context.next_ch == "*":
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.cache_add()
                context.set_status(AstParseStatus.IN_EXPLAIN_2)
            elif context.now_ch in {" ", "\n", ",", ";", "=", "+", "*", "/", ".", "%"}:
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.handle_end_word()
            elif context.now_ch == "-" and not (context.last_ch == "-" or context.next_ch == "-"):
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.handle_end_word()
            elif context.now_ch == "\"":
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
            elif context.now_ch == "'":
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.set_status(AstParseStatus.IN_SINGLE_QUOTE)
            elif context.now_ch == "`":
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.set_status(AstParseStatus.IN_BACK_QUOTE)
            elif context.now_ch == "#" or (context.now_ch == "-" and context.next_ch == "-"):
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.set_status(AstParseStatus.IN_EXPLAIN_1)
            elif context.now_ch == "(":
                context.handle_left_parenthesis()  # 【移动指针】处理当前指针位置的左括号
            elif context.now_ch == ")":
                context.handle_right_parenthesis()  # 【移动指针】处理当前指针位置的右括号
            else:
                context.cache_reset_and_add()  # 【移动指针】重置当前缓存词语，并将当前指针位置字符添加到缓存
                context.set_status(AstParseStatus.IN_WORD)
        elif (context.status == AstParseStatus.IN_DOUBLE_QUOTE and
              context.last_ch != "\\" and context.now_ch == "\"" and not context.next_ch == "\""):
            context.cache_add_and_handle_end_word()
            context.set_status(AstParseStatus.WAIT_TOKEN)
        # 当前指针位置字符为双引号字符串中的 "" 转义中的第 1 个字符
        elif (context.status == AstParseStatus.IN_DOUBLE_QUOTE and
              context.last_ch != "\\" and context.now_ch == "\"" and context.next_ch == "\""):
            context.cache_add()
            context.cache_add()
        elif (context.status == AstParseStatus.IN_SINGLE_QUOTE and
              context.last_ch != "\\" and context.now_ch == "'" and not context.next_ch == "'"):
            context.cache_add_and_handle_end_word()
            context.set_status(AstParseStatus.WAIT_TOKEN)
        # 当前指针位置字符为单引号字符串中的 '' 转义中的第 1 个字符
        elif (context.status == AstParseStatus.IN_SINGLE_QUOTE and
              context.last_ch != "\\" and context.now_ch == "'" and context.next_ch == "'"):
            context.cache_add()
            context.cache_add()
        elif context.status == AstParseStatus.IN_BACK_QUOTE and context.now_ch == "`":
            context.cache_add_and_handle_end_word()
            context.set_status(AstParseStatus.WAIT_TOKEN)
        elif context.status == AstParseStatus.IN_EXPLAIN_1 and context.now_ch == "\n":
            context.handle_end_word()
            context.set_status(AstParseStatus.WAIT_TOKEN)
        elif context.status == AstParseStatus.IN_EXPLAIN_2 and context.last_ch == "*" and context.now_ch == "/":
            context.cache_add_and_handle_end_word()
            context.set_status(AstParseStatus.WAIT_TOKEN)
        elif context.status == AstParseStatus.IN_WORD:
            if context.now_ch in {" ", "\n", ",", ";", "+", "-", "*", "/", "`", "<", "!", "%", ""}:
                context.handle_end_word()
                context.set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == "|" and context.last_ch != "|":
                context.handle_end_word()
                context.set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == "=" and context.last_ch not in {"!", "<", ">"}:
                context.handle_end_word()
                context.set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == ">" and context.last_ch != "<":
                context.handle_end_word()
                context.set_status(AstParseStatus.WAIT_TOKEN)
            # 前面不完全为数字时，出现点号
            elif context.now_ch == "." and not context.cache_get().isnumeric():
                context.handle_end_word()
                context.set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == "\"":
                if context.cache_get() in {"b", "B", "x", "X"}:  # 位值字面值和十六进制字面值
                    context.cache_add()
                    context.set_status(AstParseStatus.IN_DOUBLE_QUOTE)
                else:
                    context.handle_end_word()
                    context.set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == "'":
                if context.cache_get() in {"b", "B", "x", "X"}:  # 位值字面值和十六进制字面值
                    context.cache_add()
                    context.set_status(AstParseStatus.IN_SINGLE_QUOTE)
                else:
                    context.handle_end_word()
                    context.set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == "(":
                context.handle_end_word()
                context.handle_left_parenthesis()  # 【移动指针】处理当前指针位置的左括号
                context.set_status(AstParseStatus.WAIT_TOKEN)
            elif context.now_ch == ")":
                context.handle_end_word()
                context.handle_right_parenthesis()  # 【移动指针】处理当前指针位置的右括号
                context.set_status(AstParseStatus.WAIT_TOKEN)
            else:
                context.cache_add()
        else:
            context.cache_add()

    # 处理最后一个词语
    if context.status == AstParseStatus.IN_WORD:
        context.handle_end_word()
        context.set_status(AstParseStatus.WAIT_TOKEN)

    if len(context.stack) > 1:
        raise AstParseError("'(' 数量大于 ')'")

    return context.stack[0]


def format_sql_text(text: str) -> str:
    """格式化 SQL 字符串

    将制表符和全角空格替换为半角空格
    """
    return text.replace("\t", " ").replace("　", " ")
