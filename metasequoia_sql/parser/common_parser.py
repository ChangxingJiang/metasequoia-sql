from typing import List

from metasequoia_sql import ast
from metasequoia_sql.parser.token_scanner import TokenScanner


class SqlParser:
    @staticmethod
    def create_token_scanner(tokens: List[ast.AST], pos: int = 0):
        return TokenScanner(tokens, pos)
