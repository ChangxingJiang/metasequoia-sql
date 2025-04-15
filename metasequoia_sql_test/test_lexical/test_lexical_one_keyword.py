"""
测试解析单个关键字类型的 Token
"""

import unittest

from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType
from metasequoia_sql_test.common import parse_one_token


class TestLexicalOneOperator(unittest.TestCase):
    """测试解析单个关键字类型的 Token"""

    def test_keyword_accessible(self):
        """测试解析 ACCESSIBLE 关键字"""
        terminal = parse_one_token("ACCESSIBLE")
        self.assertEqual(TType.KEYWORD_ACCESSIBLE, terminal.symbol_id)
        self.assertEqual("ACCESSIBLE", terminal.symbol_value)

        terminal = parse_one_token("accessible")
        self.assertEqual(TType.KEYWORD_ACCESSIBLE, terminal.symbol_id)
        self.assertEqual("accessible", terminal.symbol_value)

    def test_keyword_account(self):
        """测试解析 ACCOUNT 关键字"""
        terminal = parse_one_token("ACCOUNT")
        self.assertEqual(TType.KEYWORD_ACCOUNT, terminal.symbol_id)
        self.assertEqual("ACCOUNT", terminal.symbol_value)

        terminal = parse_one_token("account")
        self.assertEqual(TType.KEYWORD_ACCOUNT, terminal.symbol_id)
        self.assertEqual("account", terminal.symbol_value)

    def test_keyword_action(self):
        """测试解析 ACTION 关键字"""
        terminal = parse_one_token("ACTION")
        self.assertEqual(TType.KEYWORD_ACTION, terminal.symbol_id)
        self.assertEqual("ACTION", terminal.symbol_value)

        terminal = parse_one_token("action")
        self.assertEqual(TType.KEYWORD_ACTION, terminal.symbol_id)
        self.assertEqual("action", terminal.symbol_value)

    def test_keyword_active(self):
        """测试解析 ACTIVE 关键字"""
        terminal = parse_one_token("ACTIVE")
        self.assertEqual(TType.KEYWORD_ACTIVE, terminal.symbol_id)
        self.assertEqual("ACTIVE", terminal.symbol_value)

        terminal = parse_one_token("active")
        self.assertEqual(TType.KEYWORD_ACTIVE, terminal.symbol_id)
        self.assertEqual("active", terminal.symbol_value)

    def test_keyword_add(self):
        """测试解析 ADD 关键字"""
        terminal = parse_one_token("ADD")
        self.assertEqual(TType.KEYWORD_ADD, terminal.symbol_id)
        self.assertEqual("ADD", terminal.symbol_value)

        terminal = parse_one_token("add")
        self.assertEqual(TType.KEYWORD_ADD, terminal.symbol_id)
        self.assertEqual("add", terminal.symbol_value)

    def test_keyword_admin(self):
        """测试解析 ADMIN 关键字"""
        terminal = parse_one_token("ADMIN")
        self.assertEqual(TType.KEYWORD_ADMIN, terminal.symbol_id)
        self.assertEqual("ADMIN", terminal.symbol_value)

        terminal = parse_one_token("admin")
        self.assertEqual(TType.KEYWORD_ADMIN, terminal.symbol_id)
        self.assertEqual("admin", terminal.symbol_value)

    def test_keyword_after(self):
        """测试解析 AFTER 关键字"""
        terminal = parse_one_token("AFTER")
        self.assertEqual(TType.KEYWORD_AFTER, terminal.symbol_id)
        self.assertEqual("AFTER", terminal.symbol_value)

        terminal = parse_one_token("after")
        self.assertEqual(TType.KEYWORD_AFTER, terminal.symbol_id)
        self.assertEqual("after", terminal.symbol_value)

    def test_keyword_against(self):
        """测试解析 AGAINST 关键字"""
        terminal = parse_one_token("AGAINST")
        self.assertEqual(TType.KEYWORD_AGAINST, terminal.symbol_id)
        self.assertEqual("AGAINST", terminal.symbol_value)

        terminal = parse_one_token("against")
        self.assertEqual(TType.KEYWORD_AGAINST, terminal.symbol_id)
        self.assertEqual("against", terminal.symbol_value)

    def test_keyword_aggregate(self):
        """测试解析 AGGREGATE 关键字"""
        terminal = parse_one_token("AGGREGATE")
        self.assertEqual(TType.KEYWORD_AGGREGATE, terminal.symbol_id)
        self.assertEqual("AGGREGATE", terminal.symbol_value)

        terminal = parse_one_token("aggregate")
        self.assertEqual(TType.KEYWORD_AGGREGATE, terminal.symbol_id)
        self.assertEqual("aggregate", terminal.symbol_value)

    def test_keyword_algorithm(self):
        """测试解析 ALGORITHM 关键字"""
        terminal = parse_one_token("ALGORITHM")
        self.assertEqual(TType.KEYWORD_ALGORITHM, terminal.symbol_id)
        self.assertEqual("ALGORITHM", terminal.symbol_value)

        terminal = parse_one_token("algorithm")
        self.assertEqual(TType.KEYWORD_ALGORITHM, terminal.symbol_id)
        self.assertEqual("algorithm", terminal.symbol_value)

    def test_keyword_all(self):
        """测试解析 ALL 关键字"""
        terminal = parse_one_token("ALL")
        self.assertEqual(TType.KEYWORD_ALL, terminal.symbol_id)
        self.assertEqual("ALL", terminal.symbol_value)

        terminal = parse_one_token("all")
        self.assertEqual(TType.KEYWORD_ALL, terminal.symbol_id)
        self.assertEqual("all", terminal.symbol_value)

    def test_keyword_alter(self):
        """测试解析 ALTER 关键字"""
        terminal = parse_one_token("ALTER")
        self.assertEqual(TType.KEYWORD_ALTER, terminal.symbol_id)
        self.assertEqual("ALTER", terminal.symbol_value)

        terminal = parse_one_token("alter")
        self.assertEqual(TType.KEYWORD_ALTER, terminal.symbol_id)
        self.assertEqual("alter", terminal.symbol_value)

    def test_keyword_always(self):
        """测试解析 ALWAYS 关键字"""
        terminal = parse_one_token("ALWAYS")
        self.assertEqual(TType.KEYWORD_ALWAYS, terminal.symbol_id)
        self.assertEqual("ALWAYS", terminal.symbol_value)

        terminal = parse_one_token("always")
        self.assertEqual(TType.KEYWORD_ALWAYS, terminal.symbol_id)
        self.assertEqual("always", terminal.symbol_value)

    def test_keyword_analyze(self):
        """测试解析 ANALYZE 关键字"""
        terminal = parse_one_token("ANALYZE")
        self.assertEqual(TType.KEYWORD_ANALYZE, terminal.symbol_id)
        self.assertEqual("ANALYZE", terminal.symbol_value)

        terminal = parse_one_token("analyze")
        self.assertEqual(TType.KEYWORD_ANALYZE, terminal.symbol_id)
        self.assertEqual("analyze", terminal.symbol_value)

    def test_keyword_and(self):
        """测试解析 AND 关键字"""
        terminal = parse_one_token("AND")
        self.assertEqual(TType.KEYWORD_AND, terminal.symbol_id)
        self.assertEqual("AND", terminal.symbol_value)

        terminal = parse_one_token("and")
        self.assertEqual(TType.KEYWORD_AND, terminal.symbol_id)
        self.assertEqual("and", terminal.symbol_value)

    def test_keyword_any(self):
        """测试解析 ANY 关键字"""
        terminal = parse_one_token("ANY")
        self.assertEqual(TType.KEYWORD_ANY, terminal.symbol_id)
        self.assertEqual("ANY", terminal.symbol_value)

        terminal = parse_one_token("any")
        self.assertEqual(TType.KEYWORD_ANY, terminal.symbol_id)
        self.assertEqual("any", terminal.symbol_value)

    def test_keyword_array(self):
        """测试解析 ARRAY 关键字"""
        terminal = parse_one_token("ARRAY")
        self.assertEqual(TType.KEYWORD_ARRAY, terminal.symbol_id)
        self.assertEqual("ARRAY", terminal.symbol_value)

        terminal = parse_one_token("array")
        self.assertEqual(TType.KEYWORD_ARRAY, terminal.symbol_id)
        self.assertEqual("array", terminal.symbol_value)

    def test_keyword_as(self):
        """测试解析 AS 关键字"""
        terminal = parse_one_token("AS")
        self.assertEqual(TType.KEYWORD_AS, terminal.symbol_id)
        self.assertEqual("AS", terminal.symbol_value)

        terminal = parse_one_token("as")
        self.assertEqual(TType.KEYWORD_AS, terminal.symbol_id)
        self.assertEqual("as", terminal.symbol_value)

    def test_keyword_asc(self):
        """测试解析 ASC 关键字"""
        terminal = parse_one_token("ASC")
        self.assertEqual(TType.KEYWORD_ASC, terminal.symbol_id)
        self.assertEqual("ASC", terminal.symbol_value)

        terminal = parse_one_token("asc")
        self.assertEqual(TType.KEYWORD_ASC, terminal.symbol_id)
        self.assertEqual("asc", terminal.symbol_value)

    def test_keyword_ascii(self):
        """测试解析 ASCII 关键字"""
        terminal = parse_one_token("ASCII")
        self.assertEqual(TType.KEYWORD_ASCII, terminal.symbol_id)
        self.assertEqual("ASCII", terminal.symbol_value)

        terminal = parse_one_token("ascii")
        self.assertEqual(TType.KEYWORD_ASCII, terminal.symbol_id)
        self.assertEqual("ascii", terminal.symbol_value)

    def test_keyword_asensitive(self):
        """测试解析 ASENSITIVE 关键字"""
        terminal = parse_one_token("ASENSITIVE")
        self.assertEqual(TType.KEYWORD_ASENSITIVE, terminal.symbol_id)
        self.assertEqual("ASENSITIVE", terminal.symbol_value)

        terminal = parse_one_token("asensitive")
        self.assertEqual(TType.KEYWORD_ASENSITIVE, terminal.symbol_id)
        self.assertEqual("asensitive", terminal.symbol_value)

    def test_keyword_at(self):
        """测试解析 AT 关键字"""
        terminal = parse_one_token("AT")
        self.assertEqual(TType.KEYWORD_AT, terminal.symbol_id)
        self.assertEqual("AT", terminal.symbol_value)

        terminal = parse_one_token("at")
        self.assertEqual(TType.KEYWORD_AT, terminal.symbol_id)
        self.assertEqual("at", terminal.symbol_value)

    def test_keyword_attribute(self):
        """测试解析 ATTRIBUTE 关键字"""
        terminal = parse_one_token("ATTRIBUTE")
        self.assertEqual(TType.KEYWORD_ATTRIBUTE, terminal.symbol_id)
        self.assertEqual("ATTRIBUTE", terminal.symbol_value)

        terminal = parse_one_token("attribute")
        self.assertEqual(TType.KEYWORD_ATTRIBUTE, terminal.symbol_id)
        self.assertEqual("attribute", terminal.symbol_value)

    def test_keyword_authentication(self):
        """测试解析 AUTHENTICATION 关键字"""
        terminal = parse_one_token("AUTHENTICATION")
        self.assertEqual(TType.KEYWORD_AUTHENTICATION, terminal.symbol_id)
        self.assertEqual("AUTHENTICATION", terminal.symbol_value)

        terminal = parse_one_token("authentication")
        self.assertEqual(TType.KEYWORD_AUTHENTICATION, terminal.symbol_id)
        self.assertEqual("authentication", terminal.symbol_value)

    def test_keyword_auto_inc(self):
        """测试解析 AUTO_INC 关键字"""
        terminal = parse_one_token("AUTO_INC")
        self.assertEqual(TType.KEYWORD_AUTO_INC, terminal.symbol_id)
        self.assertEqual("AUTO_INC", terminal.symbol_value)

        terminal = parse_one_token("auto_inc")
        self.assertEqual(TType.KEYWORD_AUTO_INC, terminal.symbol_id)
        self.assertEqual("auto_inc", terminal.symbol_value)

    def test_keyword_autoextend_size(self):
        """测试解析 AUTOEXTEND_SIZE 关键字"""
        terminal = parse_one_token("AUTOEXTEND_SIZE")
        self.assertEqual(TType.KEYWORD_AUTOEXTEND_SIZE, terminal.symbol_id)
        self.assertEqual("AUTOEXTEND_SIZE", terminal.symbol_value)

        terminal = parse_one_token("autoextend_size")
        self.assertEqual(TType.KEYWORD_AUTOEXTEND_SIZE, terminal.symbol_id)
        self.assertEqual("autoextend_size", terminal.symbol_value)

    def test_keyword_auto_increment(self):
        """测试解析 AUTO_INCREMENT 关键字"""
        terminal = parse_one_token("AUTO_INCREMENT")
        self.assertEqual(TType.KEYWORD_AUTO_INCREMENT, terminal.symbol_id)
        self.assertEqual("AUTO_INCREMENT", terminal.symbol_value)

        terminal = parse_one_token("auto_increment")
        self.assertEqual(TType.KEYWORD_AUTO_INCREMENT, terminal.symbol_id)
        self.assertEqual("auto_increment", terminal.symbol_value)

    def test_keyword_avg(self):
        """测试解析 AVG 关键字"""
        terminal = parse_one_token("AVG")
        self.assertEqual(TType.KEYWORD_AVG, terminal.symbol_id)
        self.assertEqual("AVG", terminal.symbol_value)

        terminal = parse_one_token("avg")
        self.assertEqual(TType.KEYWORD_AVG, terminal.symbol_id)
        self.assertEqual("avg", terminal.symbol_value)

    def test_keyword_avg_row_length(self):
        """测试解析 AVG_ROW_LENGTH 关键字"""
        terminal = parse_one_token("AVG_ROW_LENGTH")
        self.assertEqual(TType.KEYWORD_AVG_ROW_LENGTH, terminal.symbol_id)
        self.assertEqual("AVG_ROW_LENGTH", terminal.symbol_value)

        terminal = parse_one_token("avg_row_length")
        self.assertEqual(TType.KEYWORD_AVG_ROW_LENGTH, terminal.symbol_id)
        self.assertEqual("avg_row_length", terminal.symbol_value)

    def test_keyword_backup(self):
        """测试解析 BACKUP 关键字"""
        terminal = parse_one_token("BACKUP")
        self.assertEqual(TType.KEYWORD_BACKUP, terminal.symbol_id)
        self.assertEqual("BACKUP", terminal.symbol_value)

        terminal = parse_one_token("backup")
        self.assertEqual(TType.KEYWORD_BACKUP, terminal.symbol_id)
        self.assertEqual("backup", terminal.symbol_value)

    def test_keyword_before(self):
        """测试解析 BEFORE 关键字"""
        terminal = parse_one_token("BEFORE")
        self.assertEqual(TType.KEYWORD_BEFORE, terminal.symbol_id)
        self.assertEqual("BEFORE", terminal.symbol_value)

        terminal = parse_one_token("before")
        self.assertEqual(TType.KEYWORD_BEFORE, terminal.symbol_id)
        self.assertEqual("before", terminal.symbol_value)

    def test_keyword_begin(self):
        """测试解析 BEGIN 关键字"""
        terminal = parse_one_token("BEGIN")
        self.assertEqual(TType.KEYWORD_BEGIN, terminal.symbol_id)
        self.assertEqual("BEGIN", terminal.symbol_value)

        terminal = parse_one_token("begin")
        self.assertEqual(TType.KEYWORD_BEGIN, terminal.symbol_id)
        self.assertEqual("begin", terminal.symbol_value)

    def test_keyword_bernoulli(self):
        """测试解析 BERNOULLI 关键字"""
        terminal = parse_one_token("BERNOULLI")
        self.assertEqual(TType.KEYWORD_BERNOULLI, terminal.symbol_id)
        self.assertEqual("BERNOULLI", terminal.symbol_value)

        terminal = parse_one_token("bernoulli")
        self.assertEqual(TType.KEYWORD_BERNOULLI, terminal.symbol_id)
        self.assertEqual("bernoulli", terminal.symbol_value)

    def test_keyword_between(self):
        """测试解析 BETWEEN 关键字"""
        terminal = parse_one_token("BETWEEN")
        self.assertEqual(TType.KEYWORD_BETWEEN, terminal.symbol_id)
        self.assertEqual("BETWEEN", terminal.symbol_value)

        terminal = parse_one_token("between")
        self.assertEqual(TType.KEYWORD_BETWEEN, terminal.symbol_id)
        self.assertEqual("between", terminal.symbol_value)

    def test_keyword_bigint(self):
        """测试解析 BIGINT 关键字"""
        terminal = parse_one_token("BIGINT")
        self.assertEqual(TType.KEYWORD_BIGINT, terminal.symbol_id)
        self.assertEqual("BIGINT", terminal.symbol_value)

        terminal = parse_one_token("bigint")
        self.assertEqual(TType.KEYWORD_BIGINT, terminal.symbol_id)
        self.assertEqual("bigint", terminal.symbol_value)

    def test_keyword_binary(self):
        """测试解析 BINARY 关键字"""
        terminal = parse_one_token("BINARY")
        self.assertEqual(TType.KEYWORD_BINARY, terminal.symbol_id)
        self.assertEqual("BINARY", terminal.symbol_value)

        terminal = parse_one_token("binary")
        self.assertEqual(TType.KEYWORD_BINARY, terminal.symbol_id)
        self.assertEqual("binary", terminal.symbol_value)

    def test_keyword_binlog(self):
        """测试解析 BINLOG 关键字"""
        terminal = parse_one_token("BINLOG")
        self.assertEqual(TType.KEYWORD_BINLOG, terminal.symbol_id)
        self.assertEqual("BINLOG", terminal.symbol_value)

        terminal = parse_one_token("binlog")
        self.assertEqual(TType.KEYWORD_BINLOG, terminal.symbol_id)
        self.assertEqual("binlog", terminal.symbol_value)

    def test_keyword_bit(self):
        """测试解析 BIT 关键字"""
        terminal = parse_one_token("BIT")
        self.assertEqual(TType.KEYWORD_BIT, terminal.symbol_id)
        self.assertEqual("BIT", terminal.symbol_value)

        terminal = parse_one_token("bit")
        self.assertEqual(TType.KEYWORD_BIT, terminal.symbol_id)
        self.assertEqual("bit", terminal.symbol_value)

    def test_keyword_blob(self):
        """测试解析 BLOB 关键字"""
        terminal = parse_one_token("BLOB")
        self.assertEqual(TType.KEYWORD_BLOB, terminal.symbol_id)
        self.assertEqual("BLOB", terminal.symbol_value)

        terminal = parse_one_token("blob")
        self.assertEqual(TType.KEYWORD_BLOB, terminal.symbol_id)
        self.assertEqual("blob", terminal.symbol_value)

    def test_keyword_block(self):
        """测试解析 BLOCK 关键字"""
        terminal = parse_one_token("BLOCK")
        self.assertEqual(TType.KEYWORD_BLOCK, terminal.symbol_id)
        self.assertEqual("BLOCK", terminal.symbol_value)

        terminal = parse_one_token("block")
        self.assertEqual(TType.KEYWORD_BLOCK, terminal.symbol_id)
        self.assertEqual("block", terminal.symbol_value)

    def test_keyword_bool(self):
        """测试解析 BOOL 关键字"""
        terminal = parse_one_token("BOOL")
        self.assertEqual(TType.KEYWORD_BOOL, terminal.symbol_id)
        self.assertEqual("BOOL", terminal.symbol_value)

        terminal = parse_one_token("bool")
        self.assertEqual(TType.KEYWORD_BOOL, terminal.symbol_id)
        self.assertEqual("bool", terminal.symbol_value)

    def test_keyword_boolean(self):
        """测试解析 BOOLEAN 关键字"""
        terminal = parse_one_token("BOOLEAN")
        self.assertEqual(TType.KEYWORD_BOOLEAN, terminal.symbol_id)
        self.assertEqual("BOOLEAN", terminal.symbol_value)

        terminal = parse_one_token("boolean")
        self.assertEqual(TType.KEYWORD_BOOLEAN, terminal.symbol_id)
        self.assertEqual("boolean", terminal.symbol_value)

    def test_keyword_both(self):
        """测试解析 BOTH 关键字"""
        terminal = parse_one_token("BOTH")
        self.assertEqual(TType.KEYWORD_BOTH, terminal.symbol_id)
        self.assertEqual("BOTH", terminal.symbol_value)

        terminal = parse_one_token("both")
        self.assertEqual(TType.KEYWORD_BOTH, terminal.symbol_id)
        self.assertEqual("both", terminal.symbol_value)

    def test_keyword_btree(self):
        """测试解析 BTREE 关键字"""
        terminal = parse_one_token("BTREE")
        self.assertEqual(TType.KEYWORD_BTREE, terminal.symbol_id)
        self.assertEqual("BTREE", terminal.symbol_value)

        terminal = parse_one_token("btree")
        self.assertEqual(TType.KEYWORD_BTREE, terminal.symbol_id)
        self.assertEqual("btree", terminal.symbol_value)

    def test_keyword_buckets(self):
        """测试解析 BUCKETS 关键字"""
        terminal = parse_one_token("BUCKETS")
        self.assertEqual(TType.KEYWORD_BUCKETS, terminal.symbol_id)
        self.assertEqual("BUCKETS", terminal.symbol_value)

        terminal = parse_one_token("buckets")
        self.assertEqual(TType.KEYWORD_BUCKETS, terminal.symbol_id)
        self.assertEqual("buckets", terminal.symbol_value)

    def test_keyword_bulk(self):
        """测试解析 BULK 关键字"""
        terminal = parse_one_token("BULK")
        self.assertEqual(TType.KEYWORD_BULK, terminal.symbol_id)
        self.assertEqual("BULK", terminal.symbol_value)

        terminal = parse_one_token("bulk")
        self.assertEqual(TType.KEYWORD_BULK, terminal.symbol_id)
        self.assertEqual("bulk", terminal.symbol_value)

    def test_keyword_by(self):
        """测试解析 BY 关键字"""
        terminal = parse_one_token("BY")
        self.assertEqual(TType.KEYWORD_BY, terminal.symbol_id)
        self.assertEqual("BY", terminal.symbol_value)

        terminal = parse_one_token("by")
        self.assertEqual(TType.KEYWORD_BY, terminal.symbol_id)
        self.assertEqual("by", terminal.symbol_value)

    def test_keyword_byte(self):
        """测试解析 BYTE 关键字"""
        terminal = parse_one_token("BYTE")
        self.assertEqual(TType.KEYWORD_BYTE, terminal.symbol_id)
        self.assertEqual("BYTE", terminal.symbol_value)

        terminal = parse_one_token("byte")
        self.assertEqual(TType.KEYWORD_BYTE, terminal.symbol_id)
        self.assertEqual("byte", terminal.symbol_value)

    def test_keyword_cache(self):
        """测试解析 CACHE 关键字"""
        terminal = parse_one_token("CACHE")
        self.assertEqual(TType.KEYWORD_CACHE, terminal.symbol_id)
        self.assertEqual("CACHE", terminal.symbol_value)

        terminal = parse_one_token("cache")
        self.assertEqual(TType.KEYWORD_CACHE, terminal.symbol_id)
        self.assertEqual("cache", terminal.symbol_value)

    def test_keyword_call(self):
        """测试解析 CALL 关键字"""
        terminal = parse_one_token("CALL")
        self.assertEqual(TType.KEYWORD_CALL, terminal.symbol_id)
        self.assertEqual("CALL", terminal.symbol_value)

        terminal = parse_one_token("call")
        self.assertEqual(TType.KEYWORD_CALL, terminal.symbol_id)
        self.assertEqual("call", terminal.symbol_value)

    def test_keyword_cascade(self):
        """测试解析 CASCADE 关键字"""
        terminal = parse_one_token("CASCADE")
        self.assertEqual(TType.KEYWORD_CASCADE, terminal.symbol_id)
        self.assertEqual("CASCADE", terminal.symbol_value)

        terminal = parse_one_token("cascade")
        self.assertEqual(TType.KEYWORD_CASCADE, terminal.symbol_id)
        self.assertEqual("cascade", terminal.symbol_value)

    def test_keyword_cascaded(self):
        """测试解析 CASCADED 关键字"""
        terminal = parse_one_token("CASCADED")
        self.assertEqual(TType.KEYWORD_CASCADED, terminal.symbol_id)
        self.assertEqual("CASCADED", terminal.symbol_value)

        terminal = parse_one_token("cascaded")
        self.assertEqual(TType.KEYWORD_CASCADED, terminal.symbol_id)
        self.assertEqual("cascaded", terminal.symbol_value)

    def test_keyword_case(self):
        """测试解析 CASE 关键字"""
        terminal = parse_one_token("CASE")
        self.assertEqual(TType.KEYWORD_CASE, terminal.symbol_id)
        self.assertEqual("CASE", terminal.symbol_value)

        terminal = parse_one_token("case")
        self.assertEqual(TType.KEYWORD_CASE, terminal.symbol_id)
        self.assertEqual("case", terminal.symbol_value)

    def test_keyword_catalog_name(self):
        """测试解析 CATALOG_NAME 关键字"""
        terminal = parse_one_token("CATALOG_NAME")
        self.assertEqual(TType.KEYWORD_CATALOG_NAME, terminal.symbol_id)
        self.assertEqual("CATALOG_NAME", terminal.symbol_value)

        terminal = parse_one_token("catalog_name")
        self.assertEqual(TType.KEYWORD_CATALOG_NAME, terminal.symbol_id)
        self.assertEqual("catalog_name", terminal.symbol_value)

    def test_keyword_chain(self):
        """测试解析 CHAIN 关键字"""
        terminal = parse_one_token("CHAIN")
        self.assertEqual(TType.KEYWORD_CHAIN, terminal.symbol_id)
        self.assertEqual("CHAIN", terminal.symbol_value)

        terminal = parse_one_token("chain")
        self.assertEqual(TType.KEYWORD_CHAIN, terminal.symbol_id)
        self.assertEqual("chain", terminal.symbol_value)

    def test_keyword_challenge_response(self):
        """测试解析 CHALLENGE_RESPONSE 关键字"""
        terminal = parse_one_token("CHALLENGE_RESPONSE")
        self.assertEqual(TType.KEYWORD_CHALLENGE_RESPONSE, terminal.symbol_id)
        self.assertEqual("CHALLENGE_RESPONSE", terminal.symbol_value)

        terminal = parse_one_token("challenge_response")
        self.assertEqual(TType.KEYWORD_CHALLENGE_RESPONSE, terminal.symbol_id)
        self.assertEqual("challenge_response", terminal.symbol_value)

    def test_keyword_change(self):
        """测试解析 CHANGE 关键字"""
        terminal = parse_one_token("CHANGE")
        self.assertEqual(TType.KEYWORD_CHANGE, terminal.symbol_id)
        self.assertEqual("CHANGE", terminal.symbol_value)

        terminal = parse_one_token("change")
        self.assertEqual(TType.KEYWORD_CHANGE, terminal.symbol_id)
        self.assertEqual("change", terminal.symbol_value)

    def test_keyword_changed(self):
        """测试解析 CHANGED 关键字"""
        terminal = parse_one_token("CHANGED")
        self.assertEqual(TType.KEYWORD_CHANGED, terminal.symbol_id)
        self.assertEqual("CHANGED", terminal.symbol_value)

        terminal = parse_one_token("changed")
        self.assertEqual(TType.KEYWORD_CHANGED, terminal.symbol_id)
        self.assertEqual("changed", terminal.symbol_value)

    def test_keyword_channel(self):
        """测试解析 CHANNEL 关键字"""
        terminal = parse_one_token("CHANNEL")
        self.assertEqual(TType.KEYWORD_CHANNEL, terminal.symbol_id)
        self.assertEqual("CHANNEL", terminal.symbol_value)

        terminal = parse_one_token("channel")
        self.assertEqual(TType.KEYWORD_CHANNEL, terminal.symbol_id)
        self.assertEqual("channel", terminal.symbol_value)

    def test_keyword_char(self):
        """测试解析 CHAR 关键字"""
        terminal = parse_one_token("CHAR")
        self.assertEqual(TType.KEYWORD_CHAR, terminal.symbol_id)
        self.assertEqual("CHAR", terminal.symbol_value)

        terminal = parse_one_token("char")
        self.assertEqual(TType.KEYWORD_CHAR, terminal.symbol_id)
        self.assertEqual("char", terminal.symbol_value)

    def test_keyword_character(self):
        """测试解析 CHARACTER 关键字"""
        terminal = parse_one_token("CHARACTER")
        self.assertEqual(TType.KEYWORD_CHARACTER, terminal.symbol_id)
        self.assertEqual("CHARACTER", terminal.symbol_value)

        terminal = parse_one_token("character")
        self.assertEqual(TType.KEYWORD_CHARACTER, terminal.symbol_id)
        self.assertEqual("character", terminal.symbol_value)

    def test_keyword_charset(self):
        """测试解析 CHARSET 关键字"""
        terminal = parse_one_token("CHARSET")
        self.assertEqual(TType.KEYWORD_CHARSET, terminal.symbol_id)
        self.assertEqual("CHARSET", terminal.symbol_value)

        terminal = parse_one_token("charset")
        self.assertEqual(TType.KEYWORD_CHARSET, terminal.symbol_id)
        self.assertEqual("charset", terminal.symbol_value)

    def test_keyword_check(self):
        """测试解析 CHECK 关键字"""
        terminal = parse_one_token("CHECK")
        self.assertEqual(TType.KEYWORD_CHECK, terminal.symbol_id)
        self.assertEqual("CHECK", terminal.symbol_value)

        terminal = parse_one_token("check")
        self.assertEqual(TType.KEYWORD_CHECK, terminal.symbol_id)
        self.assertEqual("check", terminal.symbol_value)

    def test_keyword_checksum(self):
        """测试解析 CHECKSUM 关键字"""
        terminal = parse_one_token("CHECKSUM")
        self.assertEqual(TType.KEYWORD_CHECKSUM, terminal.symbol_id)
        self.assertEqual("CHECKSUM", terminal.symbol_value)

        terminal = parse_one_token("checksum")
        self.assertEqual(TType.KEYWORD_CHECKSUM, terminal.symbol_id)
        self.assertEqual("checksum", terminal.symbol_value)

    def test_keyword_cipher(self):
        """测试解析 CIPHER 关键字"""
        terminal = parse_one_token("CIPHER")
        self.assertEqual(TType.KEYWORD_CIPHER, terminal.symbol_id)
        self.assertEqual("CIPHER", terminal.symbol_value)

        terminal = parse_one_token("cipher")
        self.assertEqual(TType.KEYWORD_CIPHER, terminal.symbol_id)
        self.assertEqual("cipher", terminal.symbol_value)

    def test_keyword_class_origin(self):
        """测试解析 CLASS_ORIGIN 关键字"""
        terminal = parse_one_token("CLASS_ORIGIN")
        self.assertEqual(TType.KEYWORD_CLASS_ORIGIN, terminal.symbol_id)
        self.assertEqual("CLASS_ORIGIN", terminal.symbol_value)

        terminal = parse_one_token("class_origin")
        self.assertEqual(TType.KEYWORD_CLASS_ORIGIN, terminal.symbol_id)
        self.assertEqual("class_origin", terminal.symbol_value)

    def test_keyword_client(self):
        """测试解析 CLIENT 关键字"""
        terminal = parse_one_token("CLIENT")
        self.assertEqual(TType.KEYWORD_CLIENT, terminal.symbol_id)
        self.assertEqual("CLIENT", terminal.symbol_value)

        terminal = parse_one_token("client")
        self.assertEqual(TType.KEYWORD_CLIENT, terminal.symbol_id)
        self.assertEqual("client", terminal.symbol_value)

    def test_keyword_clone(self):
        """测试解析 CLONE 关键字"""
        terminal = parse_one_token("CLONE")
        self.assertEqual(TType.KEYWORD_CLONE, terminal.symbol_id)
        self.assertEqual("CLONE", terminal.symbol_value)

        terminal = parse_one_token("clone")
        self.assertEqual(TType.KEYWORD_CLONE, terminal.symbol_id)
        self.assertEqual("clone", terminal.symbol_value)

    def test_keyword_close(self):
        """测试解析 CLOSE 关键字"""
        terminal = parse_one_token("CLOSE")
        self.assertEqual(TType.KEYWORD_CLOSE, terminal.symbol_id)
        self.assertEqual("CLOSE", terminal.symbol_value)

        terminal = parse_one_token("close")
        self.assertEqual(TType.KEYWORD_CLOSE, terminal.symbol_id)
        self.assertEqual("close", terminal.symbol_value)

    def test_keyword_coalesce(self):
        """测试解析 COALESCE 关键字"""
        terminal = parse_one_token("COALESCE")
        self.assertEqual(TType.KEYWORD_COALESCE, terminal.symbol_id)
        self.assertEqual("COALESCE", terminal.symbol_value)

        terminal = parse_one_token("coalesce")
        self.assertEqual(TType.KEYWORD_COALESCE, terminal.symbol_id)
        self.assertEqual("coalesce", terminal.symbol_value)

    def test_keyword_code(self):
        """测试解析 CODE 关键字"""
        terminal = parse_one_token("CODE")
        self.assertEqual(TType.KEYWORD_CODE, terminal.symbol_id)
        self.assertEqual("CODE", terminal.symbol_value)

        terminal = parse_one_token("code")
        self.assertEqual(TType.KEYWORD_CODE, terminal.symbol_id)
        self.assertEqual("code", terminal.symbol_value)

    def test_keyword_collate(self):
        """测试解析 COLLATE 关键字"""
        terminal = parse_one_token("COLLATE")
        self.assertEqual(TType.KEYWORD_COLLATE, terminal.symbol_id)
        self.assertEqual("COLLATE", terminal.symbol_value)

        terminal = parse_one_token("collate")
        self.assertEqual(TType.KEYWORD_COLLATE, terminal.symbol_id)
        self.assertEqual("collate", terminal.symbol_value)

    def test_keyword_collation(self):
        """测试解析 COLLATION 关键字"""
        terminal = parse_one_token("COLLATION")
        self.assertEqual(TType.KEYWORD_COLLATION, terminal.symbol_id)
        self.assertEqual("COLLATION", terminal.symbol_value)

        terminal = parse_one_token("collation")
        self.assertEqual(TType.KEYWORD_COLLATION, terminal.symbol_id)
        self.assertEqual("collation", terminal.symbol_value)

    def test_keyword_column(self):
        """测试解析 COLUMN 关键字"""
        terminal = parse_one_token("COLUMN")
        self.assertEqual(TType.KEYWORD_COLUMN, terminal.symbol_id)
        self.assertEqual("COLUMN", terminal.symbol_value)

        terminal = parse_one_token("column")
        self.assertEqual(TType.KEYWORD_COLUMN, terminal.symbol_id)
        self.assertEqual("column", terminal.symbol_value)

    def test_keyword_columns(self):
        """测试解析 COLUMNS 关键字"""
        terminal = parse_one_token("COLUMNS")
        self.assertEqual(TType.KEYWORD_COLUMNS, terminal.symbol_id)
        self.assertEqual("COLUMNS", terminal.symbol_value)

        terminal = parse_one_token("columns")
        self.assertEqual(TType.KEYWORD_COLUMNS, terminal.symbol_id)
        self.assertEqual("columns", terminal.symbol_value)

    def test_keyword_column_format(self):
        """测试解析 COLUMN_FORMAT 关键字"""
        terminal = parse_one_token("COLUMN_FORMAT")
        self.assertEqual(TType.KEYWORD_COLUMN_FORMAT, terminal.symbol_id)
        self.assertEqual("COLUMN_FORMAT", terminal.symbol_value)

        terminal = parse_one_token("column_format")
        self.assertEqual(TType.KEYWORD_COLUMN_FORMAT, terminal.symbol_id)
        self.assertEqual("column_format", terminal.symbol_value)

    def test_keyword_column_name(self):
        """测试解析 COLUMN_NAME 关键字"""
        terminal = parse_one_token("COLUMN_NAME")
        self.assertEqual(TType.KEYWORD_COLUMN_NAME, terminal.symbol_id)
        self.assertEqual("COLUMN_NAME", terminal.symbol_value)

        terminal = parse_one_token("column_name")
        self.assertEqual(TType.KEYWORD_COLUMN_NAME, terminal.symbol_id)
        self.assertEqual("column_name", terminal.symbol_value)

    def test_keyword_comment(self):
        """测试解析 COMMENT 关键字"""
        terminal = parse_one_token("COMMENT")
        self.assertEqual(TType.KEYWORD_COMMENT, terminal.symbol_id)
        self.assertEqual("COMMENT", terminal.symbol_value)

        terminal = parse_one_token("comment")
        self.assertEqual(TType.KEYWORD_COMMENT, terminal.symbol_id)
        self.assertEqual("comment", terminal.symbol_value)

    def test_keyword_commit(self):
        """测试解析 COMMIT 关键字"""
        terminal = parse_one_token("COMMIT")
        self.assertEqual(TType.KEYWORD_COMMIT, terminal.symbol_id)
        self.assertEqual("COMMIT", terminal.symbol_value)

        terminal = parse_one_token("commit")
        self.assertEqual(TType.KEYWORD_COMMIT, terminal.symbol_id)
        self.assertEqual("commit", terminal.symbol_value)

    def test_keyword_committed(self):
        """测试解析 COMMITTED 关键字"""
        terminal = parse_one_token("COMMITTED")
        self.assertEqual(TType.KEYWORD_COMMITTED, terminal.symbol_id)
        self.assertEqual("COMMITTED", terminal.symbol_value)

        terminal = parse_one_token("committed")
        self.assertEqual(TType.KEYWORD_COMMITTED, terminal.symbol_id)
        self.assertEqual("committed", terminal.symbol_value)

    def test_keyword_compact(self):
        """测试解析 COMPACT 关键字"""
        terminal = parse_one_token("COMPACT")
        self.assertEqual(TType.KEYWORD_COMPACT, terminal.symbol_id)
        self.assertEqual("COMPACT", terminal.symbol_value)

        terminal = parse_one_token("compact")
        self.assertEqual(TType.KEYWORD_COMPACT, terminal.symbol_id)
        self.assertEqual("compact", terminal.symbol_value)

    def test_keyword_completion(self):
        """测试解析 COMPLETION 关键字"""
        terminal = parse_one_token("COMPLETION")
        self.assertEqual(TType.KEYWORD_COMPLETION, terminal.symbol_id)
        self.assertEqual("COMPLETION", terminal.symbol_value)

        terminal = parse_one_token("completion")
        self.assertEqual(TType.KEYWORD_COMPLETION, terminal.symbol_id)
        self.assertEqual("completion", terminal.symbol_value)

    def test_keyword_component(self):
        """测试解析 COMPONENT 关键字"""
        terminal = parse_one_token("COMPONENT")
        self.assertEqual(TType.KEYWORD_COMPONENT, terminal.symbol_id)
        self.assertEqual("COMPONENT", terminal.symbol_value)

        terminal = parse_one_token("component")
        self.assertEqual(TType.KEYWORD_COMPONENT, terminal.symbol_id)
        self.assertEqual("component", terminal.symbol_value)

    def test_keyword_compressed(self):
        """测试解析 COMPRESSED 关键字"""
        terminal = parse_one_token("COMPRESSED")
        self.assertEqual(TType.KEYWORD_COMPRESSED, terminal.symbol_id)
        self.assertEqual("COMPRESSED", terminal.symbol_value)

        terminal = parse_one_token("compressed")
        self.assertEqual(TType.KEYWORD_COMPRESSED, terminal.symbol_id)
        self.assertEqual("compressed", terminal.symbol_value)

    def test_keyword_compression(self):
        """测试解析 COMPRESSION 关键字"""
        terminal = parse_one_token("COMPRESSION")
        self.assertEqual(TType.KEYWORD_COMPRESSION, terminal.symbol_id)
        self.assertEqual("COMPRESSION", terminal.symbol_value)

        terminal = parse_one_token("compression")
        self.assertEqual(TType.KEYWORD_COMPRESSION, terminal.symbol_id)
        self.assertEqual("compression", terminal.symbol_value)

    def test_keyword_concurrent(self):
        """测试解析 CONCURRENT 关键字"""
        terminal = parse_one_token("CONCURRENT")
        self.assertEqual(TType.KEYWORD_CONCURRENT, terminal.symbol_id)
        self.assertEqual("CONCURRENT", terminal.symbol_value)

        terminal = parse_one_token("concurrent")
        self.assertEqual(TType.KEYWORD_CONCURRENT, terminal.symbol_id)
        self.assertEqual("concurrent", terminal.symbol_value)

    def test_keyword_condition(self):
        """测试解析 CONDITION 关键字"""
        terminal = parse_one_token("CONDITION")
        self.assertEqual(TType.KEYWORD_CONDITION, terminal.symbol_id)
        self.assertEqual("CONDITION", terminal.symbol_value)

        terminal = parse_one_token("condition")
        self.assertEqual(TType.KEYWORD_CONDITION, terminal.symbol_id)
        self.assertEqual("condition", terminal.symbol_value)

    def test_keyword_connection(self):
        """测试解析 CONNECTION 关键字"""
        terminal = parse_one_token("CONNECTION")
        self.assertEqual(TType.KEYWORD_CONNECTION, terminal.symbol_id)
        self.assertEqual("CONNECTION", terminal.symbol_value)

        terminal = parse_one_token("connection")
        self.assertEqual(TType.KEYWORD_CONNECTION, terminal.symbol_id)
        self.assertEqual("connection", terminal.symbol_value)

    def test_keyword_consistent(self):
        """测试解析 CONSISTENT 关键字"""
        terminal = parse_one_token("CONSISTENT")
        self.assertEqual(TType.KEYWORD_CONSISTENT, terminal.symbol_id)
        self.assertEqual("CONSISTENT", terminal.symbol_value)

        terminal = parse_one_token("consistent")
        self.assertEqual(TType.KEYWORD_CONSISTENT, terminal.symbol_id)
        self.assertEqual("consistent", terminal.symbol_value)

    def test_keyword_constraint(self):
        """测试解析 CONSTRAINT 关键字"""
        terminal = parse_one_token("CONSTRAINT")
        self.assertEqual(TType.KEYWORD_CONSTRAINT, terminal.symbol_id)
        self.assertEqual("CONSTRAINT", terminal.symbol_value)

        terminal = parse_one_token("constraint")
        self.assertEqual(TType.KEYWORD_CONSTRAINT, terminal.symbol_id)
        self.assertEqual("constraint", terminal.symbol_value)

    def test_keyword_constraint_catalog(self):
        """测试解析 CONSTRAINT_CATALOG 关键字"""
        terminal = parse_one_token("CONSTRAINT_CATALOG")
        self.assertEqual(TType.KEYWORD_CONSTRAINT_CATALOG, terminal.symbol_id)
        self.assertEqual("CONSTRAINT_CATALOG", terminal.symbol_value)

        terminal = parse_one_token("constraint_catalog")
        self.assertEqual(TType.KEYWORD_CONSTRAINT_CATALOG, terminal.symbol_id)
        self.assertEqual("constraint_catalog", terminal.symbol_value)

    def test_keyword_constraint_name(self):
        """测试解析 CONSTRAINT_NAME 关键字"""
        terminal = parse_one_token("CONSTRAINT_NAME")
        self.assertEqual(TType.KEYWORD_CONSTRAINT_NAME, terminal.symbol_id)
        self.assertEqual("CONSTRAINT_NAME", terminal.symbol_value)

        terminal = parse_one_token("constraint_name")
        self.assertEqual(TType.KEYWORD_CONSTRAINT_NAME, terminal.symbol_id)
        self.assertEqual("constraint_name", terminal.symbol_value)

    def test_keyword_constraint_schema(self):
        """测试解析 CONSTRAINT_SCHEMA 关键字"""
        terminal = parse_one_token("CONSTRAINT_SCHEMA")
        self.assertEqual(TType.KEYWORD_CONSTRAINT_SCHEMA, terminal.symbol_id)
        self.assertEqual("CONSTRAINT_SCHEMA", terminal.symbol_value)

        terminal = parse_one_token("constraint_schema")
        self.assertEqual(TType.KEYWORD_CONSTRAINT_SCHEMA, terminal.symbol_id)
        self.assertEqual("constraint_schema", terminal.symbol_value)

    def test_keyword_contains(self):
        """测试解析 CONTAINS 关键字"""
        terminal = parse_one_token("CONTAINS")
        self.assertEqual(TType.KEYWORD_CONTAINS, terminal.symbol_id)
        self.assertEqual("CONTAINS", terminal.symbol_value)

        terminal = parse_one_token("contains")
        self.assertEqual(TType.KEYWORD_CONTAINS, terminal.symbol_id)
        self.assertEqual("contains", terminal.symbol_value)

    def test_keyword_context(self):
        """测试解析 CONTEXT 关键字"""
        terminal = parse_one_token("CONTEXT")
        self.assertEqual(TType.KEYWORD_CONTEXT, terminal.symbol_id)
        self.assertEqual("CONTEXT", terminal.symbol_value)

        terminal = parse_one_token("context")
        self.assertEqual(TType.KEYWORD_CONTEXT, terminal.symbol_id)
        self.assertEqual("context", terminal.symbol_value)

    def test_keyword_continue(self):
        """测试解析 CONTINUE 关键字"""
        terminal = parse_one_token("CONTINUE")
        self.assertEqual(TType.KEYWORD_CONTINUE, terminal.symbol_id)
        self.assertEqual("CONTINUE", terminal.symbol_value)

        terminal = parse_one_token("continue")
        self.assertEqual(TType.KEYWORD_CONTINUE, terminal.symbol_id)
        self.assertEqual("continue", terminal.symbol_value)

    def test_keyword_convert(self):
        """测试解析 CONVERT 关键字"""
        terminal = parse_one_token("CONVERT")
        self.assertEqual(TType.KEYWORD_CONVERT, terminal.symbol_id)
        self.assertEqual("CONVERT", terminal.symbol_value)

        terminal = parse_one_token("convert")
        self.assertEqual(TType.KEYWORD_CONVERT, terminal.symbol_id)
        self.assertEqual("convert", terminal.symbol_value)

    def test_keyword_cpu(self):
        """测试解析 CPU 关键字"""
        terminal = parse_one_token("CPU")
        self.assertEqual(TType.KEYWORD_CPU, terminal.symbol_id)
        self.assertEqual("CPU", terminal.symbol_value)

        terminal = parse_one_token("cpu")
        self.assertEqual(TType.KEYWORD_CPU, terminal.symbol_id)
        self.assertEqual("cpu", terminal.symbol_value)

    def test_keyword_create(self):
        """测试解析 CREATE 关键字"""
        terminal = parse_one_token("CREATE")
        self.assertEqual(TType.KEYWORD_CREATE, terminal.symbol_id)
        self.assertEqual("CREATE", terminal.symbol_value)

        terminal = parse_one_token("create")
        self.assertEqual(TType.KEYWORD_CREATE, terminal.symbol_id)
        self.assertEqual("create", terminal.symbol_value)

    def test_keyword_cross(self):
        """测试解析 CROSS 关键字"""
        terminal = parse_one_token("CROSS")
        self.assertEqual(TType.KEYWORD_CROSS, terminal.symbol_id)
        self.assertEqual("CROSS", terminal.symbol_value)

        terminal = parse_one_token("cross")
        self.assertEqual(TType.KEYWORD_CROSS, terminal.symbol_id)
        self.assertEqual("cross", terminal.symbol_value)

    def test_keyword_cube(self):
        """测试解析 CUBE 关键字"""
        terminal = parse_one_token("CUBE")
        self.assertEqual(TType.KEYWORD_CUBE, terminal.symbol_id)
        self.assertEqual("CUBE", terminal.symbol_value)

        terminal = parse_one_token("cube")
        self.assertEqual(TType.KEYWORD_CUBE, terminal.symbol_id)
        self.assertEqual("cube", terminal.symbol_value)

    def test_keyword_cume_dist(self):
        """测试解析 CUME_DIST 关键字"""
        terminal = parse_one_token("CUME_DIST")
        self.assertEqual(TType.KEYWORD_CUME_DIST, terminal.symbol_id)
        self.assertEqual("CUME_DIST", terminal.symbol_value)

        terminal = parse_one_token("cume_dist")
        self.assertEqual(TType.KEYWORD_CUME_DIST, terminal.symbol_id)
        self.assertEqual("cume_dist", terminal.symbol_value)

    def test_keyword_current(self):
        """测试解析 CURRENT 关键字"""
        terminal = parse_one_token("CURRENT")
        self.assertEqual(TType.KEYWORD_CURRENT, terminal.symbol_id)
        self.assertEqual("CURRENT", terminal.symbol_value)

        terminal = parse_one_token("current")
        self.assertEqual(TType.KEYWORD_CURRENT, terminal.symbol_id)
        self.assertEqual("current", terminal.symbol_value)

    def test_keyword_current_date(self):
        """测试解析 CURRENT_DATE 关键字"""
        terminal = parse_one_token("CURRENT_DATE")
        self.assertEqual(TType.KEYWORD_CURRENT_DATE, terminal.symbol_id)
        self.assertEqual("CURRENT_DATE", terminal.symbol_value)

        terminal = parse_one_token("current_date")
        self.assertEqual(TType.KEYWORD_CURRENT_DATE, terminal.symbol_id)
        self.assertEqual("current_date", terminal.symbol_value)

    def test_keyword_current_time(self):
        """测试解析 CURRENT_TIME 关键字"""
        terminal = parse_one_token("CURRENT_TIME")
        self.assertEqual(TType.KEYWORD_CURRENT_TIME, terminal.symbol_id)
        self.assertEqual("CURRENT_TIME", terminal.symbol_value)

        terminal = parse_one_token("current_time")
        self.assertEqual(TType.KEYWORD_CURRENT_TIME, terminal.symbol_id)
        self.assertEqual("current_time", terminal.symbol_value)

    def test_keyword_current_timestamp(self):
        """测试解析 CURRENT_TIMESTAMP 关键字"""
        terminal = parse_one_token("CURRENT_TIMESTAMP")
        self.assertEqual(TType.KEYWORD_CURRENT_TIMESTAMP, terminal.symbol_id)
        self.assertEqual("CURRENT_TIMESTAMP", terminal.symbol_value)

        terminal = parse_one_token("current_timestamp")
        self.assertEqual(TType.KEYWORD_CURRENT_TIMESTAMP, terminal.symbol_id)
        self.assertEqual("current_timestamp", terminal.symbol_value)

    def test_keyword_current_user(self):
        """测试解析 CURRENT_USER 关键字"""
        terminal = parse_one_token("CURRENT_USER")
        self.assertEqual(TType.KEYWORD_CURRENT_USER, terminal.symbol_id)
        self.assertEqual("CURRENT_USER", terminal.symbol_value)

        terminal = parse_one_token("current_user")
        self.assertEqual(TType.KEYWORD_CURRENT_USER, terminal.symbol_id)
        self.assertEqual("current_user", terminal.symbol_value)

    def test_keyword_cursor(self):
        """测试解析 CURSOR 关键字"""
        terminal = parse_one_token("CURSOR")
        self.assertEqual(TType.KEYWORD_CURSOR, terminal.symbol_id)
        self.assertEqual("CURSOR", terminal.symbol_value)

        terminal = parse_one_token("cursor")
        self.assertEqual(TType.KEYWORD_CURSOR, terminal.symbol_id)
        self.assertEqual("cursor", terminal.symbol_value)

    def test_keyword_cursor_name(self):
        """测试解析 CURSOR_NAME 关键字"""
        terminal = parse_one_token("CURSOR_NAME")
        self.assertEqual(TType.KEYWORD_CURSOR_NAME, terminal.symbol_id)
        self.assertEqual("CURSOR_NAME", terminal.symbol_value)

        terminal = parse_one_token("cursor_name")
        self.assertEqual(TType.KEYWORD_CURSOR_NAME, terminal.symbol_id)
        self.assertEqual("cursor_name", terminal.symbol_value)

    def test_keyword_data(self):
        """测试解析 DATA 关键字"""
        terminal = parse_one_token("DATA")
        self.assertEqual(TType.KEYWORD_DATA, terminal.symbol_id)
        self.assertEqual("DATA", terminal.symbol_value)

        terminal = parse_one_token("data")
        self.assertEqual(TType.KEYWORD_DATA, terminal.symbol_id)
        self.assertEqual("data", terminal.symbol_value)

    def test_keyword_database(self):
        """测试解析 DATABASE 关键字"""
        terminal = parse_one_token("DATABASE")
        self.assertEqual(TType.KEYWORD_DATABASE, terminal.symbol_id)
        self.assertEqual("DATABASE", terminal.symbol_value)

        terminal = parse_one_token("database")
        self.assertEqual(TType.KEYWORD_DATABASE, terminal.symbol_id)
        self.assertEqual("database", terminal.symbol_value)

    def test_keyword_databases(self):
        """测试解析 DATABASES 关键字"""
        terminal = parse_one_token("DATABASES")
        self.assertEqual(TType.KEYWORD_DATABASES, terminal.symbol_id)
        self.assertEqual("DATABASES", terminal.symbol_value)

        terminal = parse_one_token("databases")
        self.assertEqual(TType.KEYWORD_DATABASES, terminal.symbol_id)
        self.assertEqual("databases", terminal.symbol_value)

    def test_keyword_datafile(self):
        """测试解析 DATAFILE 关键字"""
        terminal = parse_one_token("DATAFILE")
        self.assertEqual(TType.KEYWORD_DATAFILE, terminal.symbol_id)
        self.assertEqual("DATAFILE", terminal.symbol_value)

        terminal = parse_one_token("datafile")
        self.assertEqual(TType.KEYWORD_DATAFILE, terminal.symbol_id)
        self.assertEqual("datafile", terminal.symbol_value)

    def test_keyword_date(self):
        """测试解析 DATE 关键字"""
        terminal = parse_one_token("DATE")
        self.assertEqual(TType.KEYWORD_DATE, terminal.symbol_id)
        self.assertEqual("DATE", terminal.symbol_value)

        terminal = parse_one_token("date")
        self.assertEqual(TType.KEYWORD_DATE, terminal.symbol_id)
        self.assertEqual("date", terminal.symbol_value)

    def test_keyword_datetime(self):
        """测试解析 DATETIME 关键字"""
        terminal = parse_one_token("DATETIME")
        self.assertEqual(TType.KEYWORD_DATETIME, terminal.symbol_id)
        self.assertEqual("DATETIME", terminal.symbol_value)

        terminal = parse_one_token("datetime")
        self.assertEqual(TType.KEYWORD_DATETIME, terminal.symbol_id)
        self.assertEqual("datetime", terminal.symbol_value)

    def test_keyword_day(self):
        """测试解析 DAY 关键字"""
        terminal = parse_one_token("DAY")
        self.assertEqual(TType.KEYWORD_DAY, terminal.symbol_id)
        self.assertEqual("DAY", terminal.symbol_value)

        terminal = parse_one_token("day")
        self.assertEqual(TType.KEYWORD_DAY, terminal.symbol_id)
        self.assertEqual("day", terminal.symbol_value)

    def test_keyword_day_hour(self):
        """测试解析 DAY_HOUR 关键字"""
        terminal = parse_one_token("DAY_HOUR")
        self.assertEqual(TType.KEYWORD_DAY_HOUR, terminal.symbol_id)
        self.assertEqual("DAY_HOUR", terminal.symbol_value)

        terminal = parse_one_token("day_hour")
        self.assertEqual(TType.KEYWORD_DAY_HOUR, terminal.symbol_id)
        self.assertEqual("day_hour", terminal.symbol_value)

    def test_keyword_day_microsecond(self):
        """测试解析 DAY_MICROSECOND 关键字"""
        terminal = parse_one_token("DAY_MICROSECOND")
        self.assertEqual(TType.KEYWORD_DAY_MICROSECOND, terminal.symbol_id)
        self.assertEqual("DAY_MICROSECOND", terminal.symbol_value)

        terminal = parse_one_token("day_microsecond")
        self.assertEqual(TType.KEYWORD_DAY_MICROSECOND, terminal.symbol_id)
        self.assertEqual("day_microsecond", terminal.symbol_value)

    def test_keyword_day_minute(self):
        """测试解析 DAY_MINUTE 关键字"""
        terminal = parse_one_token("DAY_MINUTE")
        self.assertEqual(TType.KEYWORD_DAY_MINUTE, terminal.symbol_id)
        self.assertEqual("DAY_MINUTE", terminal.symbol_value)

        terminal = parse_one_token("day_minute")
        self.assertEqual(TType.KEYWORD_DAY_MINUTE, terminal.symbol_id)
        self.assertEqual("day_minute", terminal.symbol_value)

    def test_keyword_day_second(self):
        """测试解析 DAY_SECOND 关键字"""
        terminal = parse_one_token("DAY_SECOND")
        self.assertEqual(TType.KEYWORD_DAY_SECOND, terminal.symbol_id)
        self.assertEqual("DAY_SECOND", terminal.symbol_value)

        terminal = parse_one_token("day_second")
        self.assertEqual(TType.KEYWORD_DAY_SECOND, terminal.symbol_id)
        self.assertEqual("day_second", terminal.symbol_value)

    def test_keyword_deallocate(self):
        """测试解析 DEALLOCATE 关键字"""
        terminal = parse_one_token("DEALLOCATE")
        self.assertEqual(TType.KEYWORD_DEALLOCATE, terminal.symbol_id)
        self.assertEqual("DEALLOCATE", terminal.symbol_value)

        terminal = parse_one_token("deallocate")
        self.assertEqual(TType.KEYWORD_DEALLOCATE, terminal.symbol_id)
        self.assertEqual("deallocate", terminal.symbol_value)

    def test_keyword_dec(self):
        """测试解析 DEC 关键字"""
        terminal = parse_one_token("DEC")
        self.assertEqual(TType.KEYWORD_DEC, terminal.symbol_id)
        self.assertEqual("DEC", terminal.symbol_value)

        terminal = parse_one_token("dec")
        self.assertEqual(TType.KEYWORD_DEC, terminal.symbol_id)
        self.assertEqual("dec", terminal.symbol_value)

    def test_keyword_decimal(self):
        """测试解析 DECIMAL 关键字"""
        terminal = parse_one_token("DECIMAL")
        self.assertEqual(TType.KEYWORD_DECIMAL, terminal.symbol_id)
        self.assertEqual("DECIMAL", terminal.symbol_value)

        terminal = parse_one_token("decimal")
        self.assertEqual(TType.KEYWORD_DECIMAL, terminal.symbol_id)
        self.assertEqual("decimal", terminal.symbol_value)

    def test_keyword_declare(self):
        """测试解析 DECLARE 关键字"""
        terminal = parse_one_token("DECLARE")
        self.assertEqual(TType.KEYWORD_DECLARE, terminal.symbol_id)
        self.assertEqual("DECLARE", terminal.symbol_value)

        terminal = parse_one_token("declare")
        self.assertEqual(TType.KEYWORD_DECLARE, terminal.symbol_id)
        self.assertEqual("declare", terminal.symbol_value)

    def test_keyword_default(self):
        """测试解析 DEFAULT 关键字"""
        terminal = parse_one_token("DEFAULT")
        self.assertEqual(TType.KEYWORD_DEFAULT, terminal.symbol_id)
        self.assertEqual("DEFAULT", terminal.symbol_value)

        terminal = parse_one_token("default")
        self.assertEqual(TType.KEYWORD_DEFAULT, terminal.symbol_id)
        self.assertEqual("default", terminal.symbol_value)

    def test_keyword_default_auth(self):
        """测试解析 DEFAULT_AUTH 关键字"""
        terminal = parse_one_token("DEFAULT_AUTH")
        self.assertEqual(TType.KEYWORD_DEFAULT_AUTH, terminal.symbol_id)
        self.assertEqual("DEFAULT_AUTH", terminal.symbol_value)

        terminal = parse_one_token("default_auth")
        self.assertEqual(TType.KEYWORD_DEFAULT_AUTH, terminal.symbol_id)
        self.assertEqual("default_auth", terminal.symbol_value)

    def test_keyword_definer(self):
        """测试解析 DEFINER 关键字"""
        terminal = parse_one_token("DEFINER")
        self.assertEqual(TType.KEYWORD_DEFINER, terminal.symbol_id)
        self.assertEqual("DEFINER", terminal.symbol_value)

        terminal = parse_one_token("definer")
        self.assertEqual(TType.KEYWORD_DEFINER, terminal.symbol_id)
        self.assertEqual("definer", terminal.symbol_value)

    def test_keyword_definition(self):
        """测试解析 DEFINITION 关键字"""
        terminal = parse_one_token("DEFINITION")
        self.assertEqual(TType.KEYWORD_DEFINITION, terminal.symbol_id)
        self.assertEqual("DEFINITION", terminal.symbol_value)

        terminal = parse_one_token("definition")
        self.assertEqual(TType.KEYWORD_DEFINITION, terminal.symbol_id)
        self.assertEqual("definition", terminal.symbol_value)

    def test_keyword_delayed(self):
        """测试解析 DELAYED 关键字"""
        terminal = parse_one_token("DELAYED")
        self.assertEqual(TType.KEYWORD_DELAYED, terminal.symbol_id)
        self.assertEqual("DELAYED", terminal.symbol_value)

        terminal = parse_one_token("delayed")
        self.assertEqual(TType.KEYWORD_DELAYED, terminal.symbol_id)
        self.assertEqual("delayed", terminal.symbol_value)

    def test_keyword_delay_key_write(self):
        """测试解析 DELAY_KEY_WRITE 关键字"""
        terminal = parse_one_token("DELAY_KEY_WRITE")
        self.assertEqual(TType.KEYWORD_DELAY_KEY_WRITE, terminal.symbol_id)
        self.assertEqual("DELAY_KEY_WRITE", terminal.symbol_value)

        terminal = parse_one_token("delay_key_write")
        self.assertEqual(TType.KEYWORD_DELAY_KEY_WRITE, terminal.symbol_id)
        self.assertEqual("delay_key_write", terminal.symbol_value)

    def test_keyword_delete(self):
        """测试解析 DELETE 关键字"""
        terminal = parse_one_token("DELETE")
        self.assertEqual(TType.KEYWORD_DELETE, terminal.symbol_id)
        self.assertEqual("DELETE", terminal.symbol_value)

        terminal = parse_one_token("delete")
        self.assertEqual(TType.KEYWORD_DELETE, terminal.symbol_id)
        self.assertEqual("delete", terminal.symbol_value)

    def test_keyword_dense_rank(self):
        """测试解析 DENSE_RANK 关键字"""
        terminal = parse_one_token("DENSE_RANK")
        self.assertEqual(TType.KEYWORD_DENSE_RANK, terminal.symbol_id)
        self.assertEqual("DENSE_RANK", terminal.symbol_value)

        terminal = parse_one_token("dense_rank")
        self.assertEqual(TType.KEYWORD_DENSE_RANK, terminal.symbol_id)
        self.assertEqual("dense_rank", terminal.symbol_value)

    def test_keyword_desc(self):
        """测试解析 DESC 关键字"""
        terminal = parse_one_token("DESC")
        self.assertEqual(TType.KEYWORD_DESC, terminal.symbol_id)
        self.assertEqual("DESC", terminal.symbol_value)

        terminal = parse_one_token("desc")
        self.assertEqual(TType.KEYWORD_DESC, terminal.symbol_id)
        self.assertEqual("desc", terminal.symbol_value)

    def test_keyword_describe(self):
        """测试解析 DESCRIBE 关键字"""
        terminal = parse_one_token("DESCRIBE")
        self.assertEqual(TType.KEYWORD_DESCRIBE, terminal.symbol_id)
        self.assertEqual("DESCRIBE", terminal.symbol_value)

        terminal = parse_one_token("describe")
        self.assertEqual(TType.KEYWORD_DESCRIBE, terminal.symbol_id)
        self.assertEqual("describe", terminal.symbol_value)

    def test_keyword_description(self):
        """测试解析 DESCRIPTION 关键字"""
        terminal = parse_one_token("DESCRIPTION")
        self.assertEqual(TType.KEYWORD_DESCRIPTION, terminal.symbol_id)
        self.assertEqual("DESCRIPTION", terminal.symbol_value)

        terminal = parse_one_token("description")
        self.assertEqual(TType.KEYWORD_DESCRIPTION, terminal.symbol_id)
        self.assertEqual("description", terminal.symbol_value)

    def test_keyword_deterministic(self):
        """测试解析 DETERMINISTIC 关键字"""
        terminal = parse_one_token("DETERMINISTIC")
        self.assertEqual(TType.KEYWORD_DETERMINISTIC, terminal.symbol_id)
        self.assertEqual("DETERMINISTIC", terminal.symbol_value)

        terminal = parse_one_token("deterministic")
        self.assertEqual(TType.KEYWORD_DETERMINISTIC, terminal.symbol_id)
        self.assertEqual("deterministic", terminal.symbol_value)

    def test_keyword_diagnostics(self):
        """测试解析 DIAGNOSTICS 关键字"""
        terminal = parse_one_token("DIAGNOSTICS")
        self.assertEqual(TType.KEYWORD_DIAGNOSTICS, terminal.symbol_id)
        self.assertEqual("DIAGNOSTICS", terminal.symbol_value)

        terminal = parse_one_token("diagnostics")
        self.assertEqual(TType.KEYWORD_DIAGNOSTICS, terminal.symbol_id)
        self.assertEqual("diagnostics", terminal.symbol_value)

    def test_keyword_directory(self):
        """测试解析 DIRECTORY 关键字"""
        terminal = parse_one_token("DIRECTORY")
        self.assertEqual(TType.KEYWORD_DIRECTORY, terminal.symbol_id)
        self.assertEqual("DIRECTORY", terminal.symbol_value)

        terminal = parse_one_token("directory")
        self.assertEqual(TType.KEYWORD_DIRECTORY, terminal.symbol_id)
        self.assertEqual("directory", terminal.symbol_value)

    def test_keyword_disable(self):
        """测试解析 DISABLE 关键字"""
        terminal = parse_one_token("DISABLE")
        self.assertEqual(TType.KEYWORD_DISABLE, terminal.symbol_id)
        self.assertEqual("DISABLE", terminal.symbol_value)

        terminal = parse_one_token("disable")
        self.assertEqual(TType.KEYWORD_DISABLE, terminal.symbol_id)
        self.assertEqual("disable", terminal.symbol_value)

    def test_keyword_discard(self):
        """测试解析 DISCARD 关键字"""
        terminal = parse_one_token("DISCARD")
        self.assertEqual(TType.KEYWORD_DISCARD, terminal.symbol_id)
        self.assertEqual("DISCARD", terminal.symbol_value)

        terminal = parse_one_token("discard")
        self.assertEqual(TType.KEYWORD_DISCARD, terminal.symbol_id)
        self.assertEqual("discard", terminal.symbol_value)

    def test_keyword_disk(self):
        """测试解析 DISK 关键字"""
        terminal = parse_one_token("DISK")
        self.assertEqual(TType.KEYWORD_DISK, terminal.symbol_id)
        self.assertEqual("DISK", terminal.symbol_value)

        terminal = parse_one_token("disk")
        self.assertEqual(TType.KEYWORD_DISK, terminal.symbol_id)
        self.assertEqual("disk", terminal.symbol_value)

    def test_keyword_distinct(self):
        """测试解析 DISTINCT 关键字"""
        terminal = parse_one_token("DISTINCT")
        self.assertEqual(TType.KEYWORD_DISTINCT, terminal.symbol_id)
        self.assertEqual("DISTINCT", terminal.symbol_value)

        terminal = parse_one_token("distinct")
        self.assertEqual(TType.KEYWORD_DISTINCT, terminal.symbol_id)
        self.assertEqual("distinct", terminal.symbol_value)

    def test_keyword_distinctrow(self):
        """测试解析 DISTINCTROW 关键字"""
        terminal = parse_one_token("DISTINCTROW")
        self.assertEqual(TType.KEYWORD_DISTINCTROW, terminal.symbol_id)
        self.assertEqual("DISTINCTROW", terminal.symbol_value)

        terminal = parse_one_token("distinctrow")
        self.assertEqual(TType.KEYWORD_DISTINCTROW, terminal.symbol_id)
        self.assertEqual("distinctrow", terminal.symbol_value)

    def test_keyword_div(self):
        """测试解析 DIV 关键字"""
        terminal = parse_one_token("DIV")
        self.assertEqual(TType.KEYWORD_DIV, terminal.symbol_id)
        self.assertEqual("DIV", terminal.symbol_value)

        terminal = parse_one_token("div")
        self.assertEqual(TType.KEYWORD_DIV, terminal.symbol_id)
        self.assertEqual("div", terminal.symbol_value)

    def test_keyword_do(self):
        """测试解析 DO 关键字"""
        terminal = parse_one_token("DO")
        self.assertEqual(TType.KEYWORD_DO, terminal.symbol_id)
        self.assertEqual("DO", terminal.symbol_value)

        terminal = parse_one_token("do")
        self.assertEqual(TType.KEYWORD_DO, terminal.symbol_id)
        self.assertEqual("do", terminal.symbol_value)

    def test_keyword_double(self):
        """测试解析 DOUBLE 关键字"""
        terminal = parse_one_token("DOUBLE")
        self.assertEqual(TType.KEYWORD_DOUBLE, terminal.symbol_id)
        self.assertEqual("DOUBLE", terminal.symbol_value)

        terminal = parse_one_token("double")
        self.assertEqual(TType.KEYWORD_DOUBLE, terminal.symbol_id)
        self.assertEqual("double", terminal.symbol_value)

    def test_keyword_drop(self):
        """测试解析 DROP 关键字"""
        terminal = parse_one_token("DROP")
        self.assertEqual(TType.KEYWORD_DROP, terminal.symbol_id)
        self.assertEqual("DROP", terminal.symbol_value)

        terminal = parse_one_token("drop")
        self.assertEqual(TType.KEYWORD_DROP, terminal.symbol_id)
        self.assertEqual("drop", terminal.symbol_value)

    def test_keyword_dual(self):
        """测试解析 DUAL 关键字"""
        terminal = parse_one_token("DUAL")
        self.assertEqual(TType.KEYWORD_DUAL, terminal.symbol_id)
        self.assertEqual("DUAL", terminal.symbol_value)

        terminal = parse_one_token("dual")
        self.assertEqual(TType.KEYWORD_DUAL, terminal.symbol_id)
        self.assertEqual("dual", terminal.symbol_value)

    def test_keyword_dumpfile(self):
        """测试解析 DUMPFILE 关键字"""
        terminal = parse_one_token("DUMPFILE")
        self.assertEqual(TType.KEYWORD_DUMPFILE, terminal.symbol_id)
        self.assertEqual("DUMPFILE", terminal.symbol_value)

        terminal = parse_one_token("dumpfile")
        self.assertEqual(TType.KEYWORD_DUMPFILE, terminal.symbol_id)
        self.assertEqual("dumpfile", terminal.symbol_value)

    def test_keyword_duplicate(self):
        """测试解析 DUPLICATE 关键字"""
        terminal = parse_one_token("DUPLICATE")
        self.assertEqual(TType.KEYWORD_DUPLICATE, terminal.symbol_id)
        self.assertEqual("DUPLICATE", terminal.symbol_value)

        terminal = parse_one_token("duplicate")
        self.assertEqual(TType.KEYWORD_DUPLICATE, terminal.symbol_id)
        self.assertEqual("duplicate", terminal.symbol_value)

    def test_keyword_dynamic(self):
        """测试解析 DYNAMIC 关键字"""
        terminal = parse_one_token("DYNAMIC")
        self.assertEqual(TType.KEYWORD_DYNAMIC, terminal.symbol_id)
        self.assertEqual("DYNAMIC", terminal.symbol_value)

        terminal = parse_one_token("dynamic")
        self.assertEqual(TType.KEYWORD_DYNAMIC, terminal.symbol_id)
        self.assertEqual("dynamic", terminal.symbol_value)

    def test_keyword_each(self):
        """测试解析 EACH 关键字"""
        terminal = parse_one_token("EACH")
        self.assertEqual(TType.KEYWORD_EACH, terminal.symbol_id)
        self.assertEqual("EACH", terminal.symbol_value)

        terminal = parse_one_token("each")
        self.assertEqual(TType.KEYWORD_EACH, terminal.symbol_id)
        self.assertEqual("each", terminal.symbol_value)

    def test_keyword_else(self):
        """测试解析 ELSE 关键字"""
        terminal = parse_one_token("ELSE")
        self.assertEqual(TType.KEYWORD_ELSE, terminal.symbol_id)
        self.assertEqual("ELSE", terminal.symbol_value)

        terminal = parse_one_token("else")
        self.assertEqual(TType.KEYWORD_ELSE, terminal.symbol_id)
        self.assertEqual("else", terminal.symbol_value)

    def test_keyword_elseif(self):
        """测试解析 ELSEIF 关键字"""
        terminal = parse_one_token("ELSEIF")
        self.assertEqual(TType.KEYWORD_ELSEIF, terminal.symbol_id)
        self.assertEqual("ELSEIF", terminal.symbol_value)

        terminal = parse_one_token("elseif")
        self.assertEqual(TType.KEYWORD_ELSEIF, terminal.symbol_id)
        self.assertEqual("elseif", terminal.symbol_value)

    def test_keyword_empty(self):
        """测试解析 EMPTY 关键字"""
        terminal = parse_one_token("EMPTY")
        self.assertEqual(TType.KEYWORD_EMPTY, terminal.symbol_id)
        self.assertEqual("EMPTY", terminal.symbol_value)

        terminal = parse_one_token("empty")
        self.assertEqual(TType.KEYWORD_EMPTY, terminal.symbol_id)
        self.assertEqual("empty", terminal.symbol_value)

    def test_keyword_enable(self):
        """测试解析 ENABLE 关键字"""
        terminal = parse_one_token("ENABLE")
        self.assertEqual(TType.KEYWORD_ENABLE, terminal.symbol_id)
        self.assertEqual("ENABLE", terminal.symbol_value)

        terminal = parse_one_token("enable")
        self.assertEqual(TType.KEYWORD_ENABLE, terminal.symbol_id)
        self.assertEqual("enable", terminal.symbol_value)

    def test_keyword_enclosed(self):
        """测试解析 ENCLOSED 关键字"""
        terminal = parse_one_token("ENCLOSED")
        self.assertEqual(TType.KEYWORD_ENCLOSED, terminal.symbol_id)
        self.assertEqual("ENCLOSED", terminal.symbol_value)

        terminal = parse_one_token("enclosed")
        self.assertEqual(TType.KEYWORD_ENCLOSED, terminal.symbol_id)
        self.assertEqual("enclosed", terminal.symbol_value)

    def test_keyword_encryption(self):
        """测试解析 ENCRYPTION 关键字"""
        terminal = parse_one_token("ENCRYPTION")
        self.assertEqual(TType.KEYWORD_ENCRYPTION, terminal.symbol_id)
        self.assertEqual("ENCRYPTION", terminal.symbol_value)

        terminal = parse_one_token("encryption")
        self.assertEqual(TType.KEYWORD_ENCRYPTION, terminal.symbol_id)
        self.assertEqual("encryption", terminal.symbol_value)

    def test_keyword_end(self):
        """测试解析 END 关键字"""
        terminal = parse_one_token("END")
        self.assertEqual(TType.KEYWORD_END, terminal.symbol_id)
        self.assertEqual("END", terminal.symbol_value)

        terminal = parse_one_token("end")
        self.assertEqual(TType.KEYWORD_END, terminal.symbol_id)
        self.assertEqual("end", terminal.symbol_value)

    def test_keyword_ends(self):
        """测试解析 ENDS 关键字"""
        terminal = parse_one_token("ENDS")
        self.assertEqual(TType.KEYWORD_ENDS, terminal.symbol_id)
        self.assertEqual("ENDS", terminal.symbol_value)

        terminal = parse_one_token("ends")
        self.assertEqual(TType.KEYWORD_ENDS, terminal.symbol_id)
        self.assertEqual("ends", terminal.symbol_value)

    def test_keyword_enforced(self):
        """测试解析 ENFORCED 关键字"""
        terminal = parse_one_token("ENFORCED")
        self.assertEqual(TType.KEYWORD_ENFORCED, terminal.symbol_id)
        self.assertEqual("ENFORCED", terminal.symbol_value)

        terminal = parse_one_token("enforced")
        self.assertEqual(TType.KEYWORD_ENFORCED, terminal.symbol_id)
        self.assertEqual("enforced", terminal.symbol_value)

    def test_keyword_engine(self):
        """测试解析 ENGINE 关键字"""
        terminal = parse_one_token("ENGINE")
        self.assertEqual(TType.KEYWORD_ENGINE, terminal.symbol_id)
        self.assertEqual("ENGINE", terminal.symbol_value)

        terminal = parse_one_token("engine")
        self.assertEqual(TType.KEYWORD_ENGINE, terminal.symbol_id)
        self.assertEqual("engine", terminal.symbol_value)

    def test_keyword_engines(self):
        """测试解析 ENGINES 关键字"""
        terminal = parse_one_token("ENGINES")
        self.assertEqual(TType.KEYWORD_ENGINES, terminal.symbol_id)
        self.assertEqual("ENGINES", terminal.symbol_value)

        terminal = parse_one_token("engines")
        self.assertEqual(TType.KEYWORD_ENGINES, terminal.symbol_id)
        self.assertEqual("engines", terminal.symbol_value)

    def test_keyword_engine_attribute(self):
        """测试解析 ENGINE_ATTRIBUTE 关键字"""
        terminal = parse_one_token("ENGINE_ATTRIBUTE")
        self.assertEqual(TType.KEYWORD_ENGINE_ATTRIBUTE, terminal.symbol_id)
        self.assertEqual("ENGINE_ATTRIBUTE", terminal.symbol_value)

        terminal = parse_one_token("engine_attribute")
        self.assertEqual(TType.KEYWORD_ENGINE_ATTRIBUTE, terminal.symbol_id)
        self.assertEqual("engine_attribute", terminal.symbol_value)

    def test_keyword_enum(self):
        """测试解析 ENUM 关键字"""
        terminal = parse_one_token("ENUM")
        self.assertEqual(TType.KEYWORD_ENUM, terminal.symbol_id)
        self.assertEqual("ENUM", terminal.symbol_value)

        terminal = parse_one_token("enum")
        self.assertEqual(TType.KEYWORD_ENUM, terminal.symbol_id)
        self.assertEqual("enum", terminal.symbol_value)

    def test_keyword_error(self):
        """测试解析 ERROR 关键字"""
        terminal = parse_one_token("ERROR")
        self.assertEqual(TType.KEYWORD_ERROR, terminal.symbol_id)
        self.assertEqual("ERROR", terminal.symbol_value)

        terminal = parse_one_token("error")
        self.assertEqual(TType.KEYWORD_ERROR, terminal.symbol_id)
        self.assertEqual("error", terminal.symbol_value)

    def test_keyword_errors(self):
        """测试解析 ERRORS 关键字"""
        terminal = parse_one_token("ERRORS")
        self.assertEqual(TType.KEYWORD_ERRORS, terminal.symbol_id)
        self.assertEqual("ERRORS", terminal.symbol_value)

        terminal = parse_one_token("errors")
        self.assertEqual(TType.KEYWORD_ERRORS, terminal.symbol_id)
        self.assertEqual("errors", terminal.symbol_value)

    def test_keyword_escape(self):
        """测试解析 ESCAPE 关键字"""
        terminal = parse_one_token("ESCAPE")
        self.assertEqual(TType.KEYWORD_ESCAPE, terminal.symbol_id)
        self.assertEqual("ESCAPE", terminal.symbol_value)

        terminal = parse_one_token("escape")
        self.assertEqual(TType.KEYWORD_ESCAPE, terminal.symbol_id)
        self.assertEqual("escape", terminal.symbol_value)

    def test_keyword_escaped(self):
        """测试解析 ESCAPED 关键字"""
        terminal = parse_one_token("ESCAPED")
        self.assertEqual(TType.KEYWORD_ESCAPED, terminal.symbol_id)
        self.assertEqual("ESCAPED", terminal.symbol_value)

        terminal = parse_one_token("escaped")
        self.assertEqual(TType.KEYWORD_ESCAPED, terminal.symbol_id)
        self.assertEqual("escaped", terminal.symbol_value)

    def test_keyword_event(self):
        """测试解析 EVENT 关键字"""
        terminal = parse_one_token("EVENT")
        self.assertEqual(TType.KEYWORD_EVENT, terminal.symbol_id)
        self.assertEqual("EVENT", terminal.symbol_value)

        terminal = parse_one_token("event")
        self.assertEqual(TType.KEYWORD_EVENT, terminal.symbol_id)
        self.assertEqual("event", terminal.symbol_value)

    def test_keyword_events(self):
        """测试解析 EVENTS 关键字"""
        terminal = parse_one_token("EVENTS")
        self.assertEqual(TType.KEYWORD_EVENTS, terminal.symbol_id)
        self.assertEqual("EVENTS", terminal.symbol_value)

        terminal = parse_one_token("events")
        self.assertEqual(TType.KEYWORD_EVENTS, terminal.symbol_id)
        self.assertEqual("events", terminal.symbol_value)

    def test_keyword_every(self):
        """测试解析 EVERY 关键字"""
        terminal = parse_one_token("EVERY")
        self.assertEqual(TType.KEYWORD_EVERY, terminal.symbol_id)
        self.assertEqual("EVERY", terminal.symbol_value)

        terminal = parse_one_token("every")
        self.assertEqual(TType.KEYWORD_EVERY, terminal.symbol_id)
        self.assertEqual("every", terminal.symbol_value)

    def test_keyword_except(self):
        """测试解析 EXCEPT 关键字"""
        terminal = parse_one_token("EXCEPT")
        self.assertEqual(TType.KEYWORD_EXCEPT, terminal.symbol_id)
        self.assertEqual("EXCEPT", terminal.symbol_value)

        terminal = parse_one_token("except")
        self.assertEqual(TType.KEYWORD_EXCEPT, terminal.symbol_id)
        self.assertEqual("except", terminal.symbol_value)

    def test_keyword_exchange(self):
        """测试解析 EXCHANGE 关键字"""
        terminal = parse_one_token("EXCHANGE")
        self.assertEqual(TType.KEYWORD_EXCHANGE, terminal.symbol_id)
        self.assertEqual("EXCHANGE", terminal.symbol_value)

        terminal = parse_one_token("exchange")
        self.assertEqual(TType.KEYWORD_EXCHANGE, terminal.symbol_id)
        self.assertEqual("exchange", terminal.symbol_value)

    def test_keyword_exclude(self):
        """测试解析 EXCLUDE 关键字"""
        terminal = parse_one_token("EXCLUDE")
        self.assertEqual(TType.KEYWORD_EXCLUDE, terminal.symbol_id)
        self.assertEqual("EXCLUDE", terminal.symbol_value)

        terminal = parse_one_token("exclude")
        self.assertEqual(TType.KEYWORD_EXCLUDE, terminal.symbol_id)
        self.assertEqual("exclude", terminal.symbol_value)

    def test_keyword_execute(self):
        """测试解析 EXECUTE 关键字"""
        terminal = parse_one_token("EXECUTE")
        self.assertEqual(TType.KEYWORD_EXECUTE, terminal.symbol_id)
        self.assertEqual("EXECUTE", terminal.symbol_value)

        terminal = parse_one_token("execute")
        self.assertEqual(TType.KEYWORD_EXECUTE, terminal.symbol_id)
        self.assertEqual("execute", terminal.symbol_value)

    def test_keyword_exists(self):
        """测试解析 EXISTS 关键字"""
        terminal = parse_one_token("EXISTS")
        self.assertEqual(TType.KEYWORD_EXISTS, terminal.symbol_id)
        self.assertEqual("EXISTS", terminal.symbol_value)

        terminal = parse_one_token("exists")
        self.assertEqual(TType.KEYWORD_EXISTS, terminal.symbol_id)
        self.assertEqual("exists", terminal.symbol_value)

    def test_keyword_exit(self):
        """测试解析 EXIT 关键字"""
        terminal = parse_one_token("EXIT")
        self.assertEqual(TType.KEYWORD_EXIT, terminal.symbol_id)
        self.assertEqual("EXIT", terminal.symbol_value)

        terminal = parse_one_token("exit")
        self.assertEqual(TType.KEYWORD_EXIT, terminal.symbol_id)
        self.assertEqual("exit", terminal.symbol_value)

    def test_keyword_expansion(self):
        """测试解析 EXPANSION 关键字"""
        terminal = parse_one_token("EXPANSION")
        self.assertEqual(TType.KEYWORD_EXPANSION, terminal.symbol_id)
        self.assertEqual("EXPANSION", terminal.symbol_value)

        terminal = parse_one_token("expansion")
        self.assertEqual(TType.KEYWORD_EXPANSION, terminal.symbol_id)
        self.assertEqual("expansion", terminal.symbol_value)

    def test_keyword_expire(self):
        """测试解析 EXPIRE 关键字"""
        terminal = parse_one_token("EXPIRE")
        self.assertEqual(TType.KEYWORD_EXPIRE, terminal.symbol_id)
        self.assertEqual("EXPIRE", terminal.symbol_value)

        terminal = parse_one_token("expire")
        self.assertEqual(TType.KEYWORD_EXPIRE, terminal.symbol_id)
        self.assertEqual("expire", terminal.symbol_value)

    def test_keyword_explain(self):
        """测试解析 EXPLAIN 关键字"""
        terminal = parse_one_token("EXPLAIN")
        self.assertEqual(TType.KEYWORD_EXPLAIN, terminal.symbol_id)
        self.assertEqual("EXPLAIN", terminal.symbol_value)

        terminal = parse_one_token("explain")
        self.assertEqual(TType.KEYWORD_EXPLAIN, terminal.symbol_id)
        self.assertEqual("explain", terminal.symbol_value)

    def test_keyword_export(self):
        """测试解析 EXPORT 关键字"""
        terminal = parse_one_token("EXPORT")
        self.assertEqual(TType.KEYWORD_EXPORT, terminal.symbol_id)
        self.assertEqual("EXPORT", terminal.symbol_value)

        terminal = parse_one_token("export")
        self.assertEqual(TType.KEYWORD_EXPORT, terminal.symbol_id)
        self.assertEqual("export", terminal.symbol_value)

    def test_keyword_extended(self):
        """测试解析 EXTENDED 关键字"""
        terminal = parse_one_token("EXTENDED")
        self.assertEqual(TType.KEYWORD_EXTENDED, terminal.symbol_id)
        self.assertEqual("EXTENDED", terminal.symbol_value)

        terminal = parse_one_token("extended")
        self.assertEqual(TType.KEYWORD_EXTENDED, terminal.symbol_id)
        self.assertEqual("extended", terminal.symbol_value)

    def test_keyword_extent_size(self):
        """测试解析 EXTENT_SIZE 关键字"""
        terminal = parse_one_token("EXTENT_SIZE")
        self.assertEqual(TType.KEYWORD_EXTENT_SIZE, terminal.symbol_id)
        self.assertEqual("EXTENT_SIZE", terminal.symbol_value)

        terminal = parse_one_token("extent_size")
        self.assertEqual(TType.KEYWORD_EXTENT_SIZE, terminal.symbol_id)
        self.assertEqual("extent_size", terminal.symbol_value)

    def test_keyword_factor(self):
        """测试解析 FACTOR 关键字"""
        terminal = parse_one_token("FACTOR")
        self.assertEqual(TType.KEYWORD_FACTOR, terminal.symbol_id)
        self.assertEqual("FACTOR", terminal.symbol_value)

        terminal = parse_one_token("factor")
        self.assertEqual(TType.KEYWORD_FACTOR, terminal.symbol_id)
        self.assertEqual("factor", terminal.symbol_value)

    def test_keyword_failed_login_attempts(self):
        """测试解析 FAILED_LOGIN_ATTEMPTS 关键字"""
        terminal = parse_one_token("FAILED_LOGIN_ATTEMPTS")
        self.assertEqual(TType.KEYWORD_FAILED_LOGIN_ATTEMPTS, terminal.symbol_id)
        self.assertEqual("FAILED_LOGIN_ATTEMPTS", terminal.symbol_value)

        terminal = parse_one_token("failed_login_attempts")
        self.assertEqual(TType.KEYWORD_FAILED_LOGIN_ATTEMPTS, terminal.symbol_id)
        self.assertEqual("failed_login_attempts", terminal.symbol_value)

    def test_keyword_false(self):
        """测试解析 FALSE 关键字"""
        terminal = parse_one_token("FALSE")
        self.assertEqual(TType.KEYWORD_FALSE, terminal.symbol_id)
        self.assertEqual("FALSE", terminal.symbol_value)

        terminal = parse_one_token("false")
        self.assertEqual(TType.KEYWORD_FALSE, terminal.symbol_id)
        self.assertEqual("false", terminal.symbol_value)

    def test_keyword_fast(self):
        """测试解析 FAST 关键字"""
        terminal = parse_one_token("FAST")
        self.assertEqual(TType.KEYWORD_FAST, terminal.symbol_id)
        self.assertEqual("FAST", terminal.symbol_value)

        terminal = parse_one_token("fast")
        self.assertEqual(TType.KEYWORD_FAST, terminal.symbol_id)
        self.assertEqual("fast", terminal.symbol_value)

    def test_keyword_faults(self):
        """测试解析 FAULTS 关键字"""
        terminal = parse_one_token("FAULTS")
        self.assertEqual(TType.KEYWORD_FAULTS, terminal.symbol_id)
        self.assertEqual("FAULTS", terminal.symbol_value)

        terminal = parse_one_token("faults")
        self.assertEqual(TType.KEYWORD_FAULTS, terminal.symbol_id)
        self.assertEqual("faults", terminal.symbol_value)

    def test_keyword_fetch(self):
        """测试解析 FETCH 关键字"""
        terminal = parse_one_token("FETCH")
        self.assertEqual(TType.KEYWORD_FETCH, terminal.symbol_id)
        self.assertEqual("FETCH", terminal.symbol_value)

        terminal = parse_one_token("fetch")
        self.assertEqual(TType.KEYWORD_FETCH, terminal.symbol_id)
        self.assertEqual("fetch", terminal.symbol_value)

    def test_keyword_fields(self):
        """测试解析 FIELDS 关键字"""
        terminal = parse_one_token("FIELDS")
        self.assertEqual(TType.KEYWORD_FIELDS, terminal.symbol_id)
        self.assertEqual("FIELDS", terminal.symbol_value)

        terminal = parse_one_token("fields")
        self.assertEqual(TType.KEYWORD_FIELDS, terminal.symbol_id)
        self.assertEqual("fields", terminal.symbol_value)

    def test_keyword_file(self):
        """测试解析 FILE 关键字"""
        terminal = parse_one_token("FILE")
        self.assertEqual(TType.KEYWORD_FILE, terminal.symbol_id)
        self.assertEqual("FILE", terminal.symbol_value)

        terminal = parse_one_token("file")
        self.assertEqual(TType.KEYWORD_FILE, terminal.symbol_id)
        self.assertEqual("file", terminal.symbol_value)

    def test_keyword_file_block_size(self):
        """测试解析 FILE_BLOCK_SIZE 关键字"""
        terminal = parse_one_token("FILE_BLOCK_SIZE")
        self.assertEqual(TType.KEYWORD_FILE_BLOCK_SIZE, terminal.symbol_id)
        self.assertEqual("FILE_BLOCK_SIZE", terminal.symbol_value)

        terminal = parse_one_token("file_block_size")
        self.assertEqual(TType.KEYWORD_FILE_BLOCK_SIZE, terminal.symbol_id)
        self.assertEqual("file_block_size", terminal.symbol_value)

    def test_keyword_filter(self):
        """测试解析 FILTER 关键字"""
        terminal = parse_one_token("FILTER")
        self.assertEqual(TType.KEYWORD_FILTER, terminal.symbol_id)
        self.assertEqual("FILTER", terminal.symbol_value)

        terminal = parse_one_token("filter")
        self.assertEqual(TType.KEYWORD_FILTER, terminal.symbol_id)
        self.assertEqual("filter", terminal.symbol_value)

    def test_keyword_finish(self):
        """测试解析 FINISH 关键字"""
        terminal = parse_one_token("FINISH")
        self.assertEqual(TType.KEYWORD_FINISH, terminal.symbol_id)
        self.assertEqual("FINISH", terminal.symbol_value)

        terminal = parse_one_token("finish")
        self.assertEqual(TType.KEYWORD_FINISH, terminal.symbol_id)
        self.assertEqual("finish", terminal.symbol_value)

    def test_keyword_first(self):
        """测试解析 FIRST 关键字"""
        terminal = parse_one_token("FIRST")
        self.assertEqual(TType.KEYWORD_FIRST, terminal.symbol_id)
        self.assertEqual("FIRST", terminal.symbol_value)

        terminal = parse_one_token("first")
        self.assertEqual(TType.KEYWORD_FIRST, terminal.symbol_id)
        self.assertEqual("first", terminal.symbol_value)

    def test_keyword_first_value(self):
        """测试解析 FIRST_VALUE 关键字"""
        terminal = parse_one_token("FIRST_VALUE")
        self.assertEqual(TType.KEYWORD_FIRST_VALUE, terminal.symbol_id)
        self.assertEqual("FIRST_VALUE", terminal.symbol_value)

        terminal = parse_one_token("first_value")
        self.assertEqual(TType.KEYWORD_FIRST_VALUE, terminal.symbol_id)
        self.assertEqual("first_value", terminal.symbol_value)

    def test_keyword_fixed(self):
        """测试解析 FIXED 关键字"""
        terminal = parse_one_token("FIXED")
        self.assertEqual(TType.KEYWORD_FIXED, terminal.symbol_id)
        self.assertEqual("FIXED", terminal.symbol_value)

        terminal = parse_one_token("fixed")
        self.assertEqual(TType.KEYWORD_FIXED, terminal.symbol_id)
        self.assertEqual("fixed", terminal.symbol_value)

    def test_keyword_float(self):
        """测试解析 FLOAT 关键字"""
        terminal = parse_one_token("FLOAT")
        self.assertEqual(TType.KEYWORD_FLOAT, terminal.symbol_id)
        self.assertEqual("FLOAT", terminal.symbol_value)

        terminal = parse_one_token("float")
        self.assertEqual(TType.KEYWORD_FLOAT, terminal.symbol_id)
        self.assertEqual("float", terminal.symbol_value)

    def test_keyword_float4(self):
        """测试解析 FLOAT4 关键字"""
        terminal = parse_one_token("FLOAT4")
        self.assertEqual(TType.KEYWORD_FLOAT4, terminal.symbol_id)
        self.assertEqual("FLOAT4", terminal.symbol_value)

        terminal = parse_one_token("float4")
        self.assertEqual(TType.KEYWORD_FLOAT4, terminal.symbol_id)
        self.assertEqual("float4", terminal.symbol_value)

    def test_keyword_float8(self):
        """测试解析 FLOAT8 关键字"""
        terminal = parse_one_token("FLOAT8")
        self.assertEqual(TType.KEYWORD_FLOAT8, terminal.symbol_id)
        self.assertEqual("FLOAT8", terminal.symbol_value)

        terminal = parse_one_token("float8")
        self.assertEqual(TType.KEYWORD_FLOAT8, terminal.symbol_id)
        self.assertEqual("float8", terminal.symbol_value)

    def test_keyword_flush(self):
        """测试解析 FLUSH 关键字"""
        terminal = parse_one_token("FLUSH")
        self.assertEqual(TType.KEYWORD_FLUSH, terminal.symbol_id)
        self.assertEqual("FLUSH", terminal.symbol_value)

        terminal = parse_one_token("flush")
        self.assertEqual(TType.KEYWORD_FLUSH, terminal.symbol_id)
        self.assertEqual("flush", terminal.symbol_value)

    def test_keyword_following(self):
        """测试解析 FOLLOWING 关键字"""
        terminal = parse_one_token("FOLLOWING")
        self.assertEqual(TType.KEYWORD_FOLLOWING, terminal.symbol_id)
        self.assertEqual("FOLLOWING", terminal.symbol_value)

        terminal = parse_one_token("following")
        self.assertEqual(TType.KEYWORD_FOLLOWING, terminal.symbol_id)
        self.assertEqual("following", terminal.symbol_value)

    def test_keyword_follows(self):
        """测试解析 FOLLOWS 关键字"""
        terminal = parse_one_token("FOLLOWS")
        self.assertEqual(TType.KEYWORD_FOLLOWS, terminal.symbol_id)
        self.assertEqual("FOLLOWS", terminal.symbol_value)

        terminal = parse_one_token("follows")
        self.assertEqual(TType.KEYWORD_FOLLOWS, terminal.symbol_id)
        self.assertEqual("follows", terminal.symbol_value)

    def test_keyword_for(self):
        """测试解析 FOR 关键字"""
        terminal = parse_one_token("FOR")
        self.assertEqual(TType.KEYWORD_FOR, terminal.symbol_id)
        self.assertEqual("FOR", terminal.symbol_value)

        terminal = parse_one_token("for")
        self.assertEqual(TType.KEYWORD_FOR, terminal.symbol_id)
        self.assertEqual("for", terminal.symbol_value)

    def test_keyword_force(self):
        """测试解析 FORCE 关键字"""
        terminal = parse_one_token("FORCE")
        self.assertEqual(TType.KEYWORD_FORCE, terminal.symbol_id)
        self.assertEqual("FORCE", terminal.symbol_value)

        terminal = parse_one_token("force")
        self.assertEqual(TType.KEYWORD_FORCE, terminal.symbol_id)
        self.assertEqual("force", terminal.symbol_value)

    def test_keyword_foreign(self):
        """测试解析 FOREIGN 关键字"""
        terminal = parse_one_token("FOREIGN")
        self.assertEqual(TType.KEYWORD_FOREIGN, terminal.symbol_id)
        self.assertEqual("FOREIGN", terminal.symbol_value)

        terminal = parse_one_token("foreign")
        self.assertEqual(TType.KEYWORD_FOREIGN, terminal.symbol_id)
        self.assertEqual("foreign", terminal.symbol_value)

    def test_keyword_format(self):
        """测试解析 FORMAT 关键字"""
        terminal = parse_one_token("FORMAT")
        self.assertEqual(TType.KEYWORD_FORMAT, terminal.symbol_id)
        self.assertEqual("FORMAT", terminal.symbol_value)

        terminal = parse_one_token("format")
        self.assertEqual(TType.KEYWORD_FORMAT, terminal.symbol_id)
        self.assertEqual("format", terminal.symbol_value)

    def test_keyword_found(self):
        """测试解析 FOUND 关键字"""
        terminal = parse_one_token("FOUND")
        self.assertEqual(TType.KEYWORD_FOUND, terminal.symbol_id)
        self.assertEqual("FOUND", terminal.symbol_value)

        terminal = parse_one_token("found")
        self.assertEqual(TType.KEYWORD_FOUND, terminal.symbol_id)
        self.assertEqual("found", terminal.symbol_value)

    def test_keyword_from(self):
        """测试解析 FROM 关键字"""
        terminal = parse_one_token("FROM")
        self.assertEqual(TType.KEYWORD_FROM, terminal.symbol_id)
        self.assertEqual("FROM", terminal.symbol_value)

        terminal = parse_one_token("from")
        self.assertEqual(TType.KEYWORD_FROM, terminal.symbol_id)
        self.assertEqual("from", terminal.symbol_value)

    def test_keyword_full(self):
        """测试解析 FULL 关键字"""
        terminal = parse_one_token("FULL")
        self.assertEqual(TType.KEYWORD_FULL, terminal.symbol_id)
        self.assertEqual("FULL", terminal.symbol_value)

        terminal = parse_one_token("full")
        self.assertEqual(TType.KEYWORD_FULL, terminal.symbol_id)
        self.assertEqual("full", terminal.symbol_value)

    def test_keyword_fulltext(self):
        """测试解析 FULLTEXT 关键字"""
        terminal = parse_one_token("FULLTEXT")
        self.assertEqual(TType.KEYWORD_FULLTEXT, terminal.symbol_id)
        self.assertEqual("FULLTEXT", terminal.symbol_value)

        terminal = parse_one_token("fulltext")
        self.assertEqual(TType.KEYWORD_FULLTEXT, terminal.symbol_id)
        self.assertEqual("fulltext", terminal.symbol_value)

    def test_keyword_function(self):
        """测试解析 FUNCTION 关键字"""
        terminal = parse_one_token("FUNCTION")
        self.assertEqual(TType.KEYWORD_FUNCTION, terminal.symbol_id)
        self.assertEqual("FUNCTION", terminal.symbol_value)

        terminal = parse_one_token("function")
        self.assertEqual(TType.KEYWORD_FUNCTION, terminal.symbol_id)
        self.assertEqual("function", terminal.symbol_value)

    def test_keyword_general(self):
        """测试解析 GENERAL 关键字"""
        terminal = parse_one_token("GENERAL")
        self.assertEqual(TType.KEYWORD_GENERAL, terminal.symbol_id)
        self.assertEqual("GENERAL", terminal.symbol_value)

        terminal = parse_one_token("general")
        self.assertEqual(TType.KEYWORD_GENERAL, terminal.symbol_id)
        self.assertEqual("general", terminal.symbol_value)

    def test_keyword_generate(self):
        """测试解析 GENERATE 关键字"""
        terminal = parse_one_token("GENERATE")
        self.assertEqual(TType.KEYWORD_GENERATE, terminal.symbol_id)
        self.assertEqual("GENERATE", terminal.symbol_value)

        terminal = parse_one_token("generate")
        self.assertEqual(TType.KEYWORD_GENERATE, terminal.symbol_id)
        self.assertEqual("generate", terminal.symbol_value)

    def test_keyword_generated(self):
        """测试解析 GENERATED 关键字"""
        terminal = parse_one_token("GENERATED")
        self.assertEqual(TType.KEYWORD_GENERATED, terminal.symbol_id)
        self.assertEqual("GENERATED", terminal.symbol_value)

        terminal = parse_one_token("generated")
        self.assertEqual(TType.KEYWORD_GENERATED, terminal.symbol_id)
        self.assertEqual("generated", terminal.symbol_value)

    def test_keyword_geomcollection(self):
        """测试解析 GEOMCOLLECTION 关键字"""
        terminal = parse_one_token("GEOMCOLLECTION")
        self.assertEqual(TType.KEYWORD_GEOMCOLLECTION, terminal.symbol_id)
        self.assertEqual("GEOMCOLLECTION", terminal.symbol_value)

        terminal = parse_one_token("geomcollection")
        self.assertEqual(TType.KEYWORD_GEOMCOLLECTION, terminal.symbol_id)
        self.assertEqual("geomcollection", terminal.symbol_value)

    def test_keyword_geometry(self):
        """测试解析 GEOMETRY 关键字"""
        terminal = parse_one_token("GEOMETRY")
        self.assertEqual(TType.KEYWORD_GEOMETRY, terminal.symbol_id)
        self.assertEqual("GEOMETRY", terminal.symbol_value)

        terminal = parse_one_token("geometry")
        self.assertEqual(TType.KEYWORD_GEOMETRY, terminal.symbol_id)
        self.assertEqual("geometry", terminal.symbol_value)

    def test_keyword_geometrycollection(self):
        """测试解析 GEOMETRYCOLLECTION 关键字"""
        terminal = parse_one_token("GEOMETRYCOLLECTION")
        self.assertEqual(TType.KEYWORD_GEOMETRYCOLLECTION, terminal.symbol_id)
        self.assertEqual("GEOMETRYCOLLECTION", terminal.symbol_value)

        terminal = parse_one_token("geometrycollection")
        self.assertEqual(TType.KEYWORD_GEOMETRYCOLLECTION, terminal.symbol_id)
        self.assertEqual("geometrycollection", terminal.symbol_value)

    def test_keyword_get(self):
        """测试解析 GET 关键字"""
        terminal = parse_one_token("GET")
        self.assertEqual(TType.KEYWORD_GET, terminal.symbol_id)
        self.assertEqual("GET", terminal.symbol_value)

        terminal = parse_one_token("get")
        self.assertEqual(TType.KEYWORD_GET, terminal.symbol_id)
        self.assertEqual("get", terminal.symbol_value)

    def test_keyword_get_master_public_key(self):
        """测试解析 GET_MASTER_PUBLIC_KEY 关键字"""
        terminal = parse_one_token("GET_MASTER_PUBLIC_KEY")
        self.assertEqual(TType.KEYWORD_GET_MASTER_PUBLIC_KEY, terminal.symbol_id)
        self.assertEqual("GET_MASTER_PUBLIC_KEY", terminal.symbol_value)

        terminal = parse_one_token("get_master_public_key")
        self.assertEqual(TType.KEYWORD_GET_MASTER_PUBLIC_KEY, terminal.symbol_id)
        self.assertEqual("get_master_public_key", terminal.symbol_value)

    def test_keyword_get_format(self):
        """测试解析 GET_FORMAT 关键字"""
        terminal = parse_one_token("GET_FORMAT")
        self.assertEqual(TType.KEYWORD_GET_FORMAT, terminal.symbol_id)
        self.assertEqual("GET_FORMAT", terminal.symbol_value)

        terminal = parse_one_token("get_format")
        self.assertEqual(TType.KEYWORD_GET_FORMAT, terminal.symbol_id)
        self.assertEqual("get_format", terminal.symbol_value)

    def test_keyword_get_source_public_key(self):
        """测试解析 GET_SOURCE_PUBLIC_KEY 关键字"""
        terminal = parse_one_token("GET_SOURCE_PUBLIC_KEY")
        self.assertEqual(TType.KEYWORD_GET_SOURCE_PUBLIC_KEY, terminal.symbol_id)
        self.assertEqual("GET_SOURCE_PUBLIC_KEY", terminal.symbol_value)

        terminal = parse_one_token("get_source_public_key")
        self.assertEqual(TType.KEYWORD_GET_SOURCE_PUBLIC_KEY, terminal.symbol_id)
        self.assertEqual("get_source_public_key", terminal.symbol_value)

    def test_keyword_global(self):
        """测试解析 GLOBAL 关键字"""
        terminal = parse_one_token("GLOBAL")
        self.assertEqual(TType.KEYWORD_GLOBAL, terminal.symbol_id)
        self.assertEqual("GLOBAL", terminal.symbol_value)

        terminal = parse_one_token("global")
        self.assertEqual(TType.KEYWORD_GLOBAL, terminal.symbol_id)
        self.assertEqual("global", terminal.symbol_value)

    def test_keyword_grant(self):
        """测试解析 GRANT 关键字"""
        terminal = parse_one_token("GRANT")
        self.assertEqual(TType.KEYWORD_GRANT, terminal.symbol_id)
        self.assertEqual("GRANT", terminal.symbol_value)

        terminal = parse_one_token("grant")
        self.assertEqual(TType.KEYWORD_GRANT, terminal.symbol_id)
        self.assertEqual("grant", terminal.symbol_value)

    def test_keyword_grants(self):
        """测试解析 GRANTS 关键字"""
        terminal = parse_one_token("GRANTS")
        self.assertEqual(TType.KEYWORD_GRANTS, terminal.symbol_id)
        self.assertEqual("GRANTS", terminal.symbol_value)

        terminal = parse_one_token("grants")
        self.assertEqual(TType.KEYWORD_GRANTS, terminal.symbol_id)
        self.assertEqual("grants", terminal.symbol_value)

    def test_keyword_group(self):
        """测试解析 GROUP 关键字"""
        terminal = parse_one_token("GROUP")
        self.assertEqual(TType.KEYWORD_GROUP, terminal.symbol_id)
        self.assertEqual("GROUP", terminal.symbol_value)

        terminal = parse_one_token("group")
        self.assertEqual(TType.KEYWORD_GROUP, terminal.symbol_id)
        self.assertEqual("group", terminal.symbol_value)

    def test_keyword_grouping(self):
        """测试解析 GROUPING 关键字"""
        terminal = parse_one_token("GROUPING")
        self.assertEqual(TType.KEYWORD_GROUPING, terminal.symbol_id)
        self.assertEqual("GROUPING", terminal.symbol_value)

        terminal = parse_one_token("grouping")
        self.assertEqual(TType.KEYWORD_GROUPING, terminal.symbol_id)
        self.assertEqual("grouping", terminal.symbol_value)

    def test_keyword_groups(self):
        """测试解析 GROUPS 关键字"""
        terminal = parse_one_token("GROUPS")
        self.assertEqual(TType.KEYWORD_GROUPS, terminal.symbol_id)
        self.assertEqual("GROUPS", terminal.symbol_value)

        terminal = parse_one_token("groups")
        self.assertEqual(TType.KEYWORD_GROUPS, terminal.symbol_id)
        self.assertEqual("groups", terminal.symbol_value)

    def test_keyword_group_replication(self):
        """测试解析 GROUP_REPLICATION 关键字"""
        terminal = parse_one_token("GROUP_REPLICATION")
        self.assertEqual(TType.KEYWORD_GROUP_REPLICATION, terminal.symbol_id)
        self.assertEqual("GROUP_REPLICATION", terminal.symbol_value)

        terminal = parse_one_token("group_replication")
        self.assertEqual(TType.KEYWORD_GROUP_REPLICATION, terminal.symbol_id)
        self.assertEqual("group_replication", terminal.symbol_value)

    def test_keyword_gtids(self):
        """测试解析 GTIDS 关键字"""
        terminal = parse_one_token("GTIDS")
        self.assertEqual(TType.KEYWORD_GTIDS, terminal.symbol_id)
        self.assertEqual("GTIDS", terminal.symbol_value)

        terminal = parse_one_token("gtids")
        self.assertEqual(TType.KEYWORD_GTIDS, terminal.symbol_id)
        self.assertEqual("gtids", terminal.symbol_value)

    def test_keyword_gtid_only(self):
        """测试解析 GTID_ONLY 关键字"""
        terminal = parse_one_token("GTID_ONLY")
        self.assertEqual(TType.KEYWORD_GTID_ONLY, terminal.symbol_id)
        self.assertEqual("GTID_ONLY", terminal.symbol_value)

        terminal = parse_one_token("gtid_only")
        self.assertEqual(TType.KEYWORD_GTID_ONLY, terminal.symbol_id)
        self.assertEqual("gtid_only", terminal.symbol_value)

    def test_keyword_handler(self):
        """测试解析 HANDLER 关键字"""
        terminal = parse_one_token("HANDLER")
        self.assertEqual(TType.KEYWORD_HANDLER, terminal.symbol_id)
        self.assertEqual("HANDLER", terminal.symbol_value)

        terminal = parse_one_token("handler")
        self.assertEqual(TType.KEYWORD_HANDLER, terminal.symbol_id)
        self.assertEqual("handler", terminal.symbol_value)

    def test_keyword_hash(self):
        """测试解析 HASH 关键字"""
        terminal = parse_one_token("HASH")
        self.assertEqual(TType.KEYWORD_HASH, terminal.symbol_id)
        self.assertEqual("HASH", terminal.symbol_value)

        terminal = parse_one_token("hash")
        self.assertEqual(TType.KEYWORD_HASH, terminal.symbol_id)
        self.assertEqual("hash", terminal.symbol_value)

    def test_keyword_having(self):
        """测试解析 HAVING 关键字"""
        terminal = parse_one_token("HAVING")
        self.assertEqual(TType.KEYWORD_HAVING, terminal.symbol_id)
        self.assertEqual("HAVING", terminal.symbol_value)

        terminal = parse_one_token("having")
        self.assertEqual(TType.KEYWORD_HAVING, terminal.symbol_id)
        self.assertEqual("having", terminal.symbol_value)

    def test_keyword_help(self):
        """测试解析 HELP 关键字"""
        terminal = parse_one_token("HELP")
        self.assertEqual(TType.KEYWORD_HELP, terminal.symbol_id)
        self.assertEqual("HELP", terminal.symbol_value)

        terminal = parse_one_token("help")
        self.assertEqual(TType.KEYWORD_HELP, terminal.symbol_id)
        self.assertEqual("help", terminal.symbol_value)

    def test_keyword_high_priority(self):
        """测试解析 HIGH_PRIORITY 关键字"""
        terminal = parse_one_token("HIGH_PRIORITY")
        self.assertEqual(TType.KEYWORD_HIGH_PRIORITY, terminal.symbol_id)
        self.assertEqual("HIGH_PRIORITY", terminal.symbol_value)

        terminal = parse_one_token("high_priority")
        self.assertEqual(TType.KEYWORD_HIGH_PRIORITY, terminal.symbol_id)
        self.assertEqual("high_priority", terminal.symbol_value)

    def test_keyword_histogram(self):
        """测试解析 HISTOGRAM 关键字"""
        terminal = parse_one_token("HISTOGRAM")
        self.assertEqual(TType.KEYWORD_HISTOGRAM, terminal.symbol_id)
        self.assertEqual("HISTOGRAM", terminal.symbol_value)

        terminal = parse_one_token("histogram")
        self.assertEqual(TType.KEYWORD_HISTOGRAM, terminal.symbol_id)
        self.assertEqual("histogram", terminal.symbol_value)

    def test_keyword_history(self):
        """测试解析 HISTORY 关键字"""
        terminal = parse_one_token("HISTORY")
        self.assertEqual(TType.KEYWORD_HISTORY, terminal.symbol_id)
        self.assertEqual("HISTORY", terminal.symbol_value)

        terminal = parse_one_token("history")
        self.assertEqual(TType.KEYWORD_HISTORY, terminal.symbol_id)
        self.assertEqual("history", terminal.symbol_value)

    def test_keyword_host(self):
        """测试解析 HOST 关键字"""
        terminal = parse_one_token("HOST")
        self.assertEqual(TType.KEYWORD_HOST, terminal.symbol_id)
        self.assertEqual("HOST", terminal.symbol_value)

        terminal = parse_one_token("host")
        self.assertEqual(TType.KEYWORD_HOST, terminal.symbol_id)
        self.assertEqual("host", terminal.symbol_value)

    def test_keyword_hosts(self):
        """测试解析 HOSTS 关键字"""
        terminal = parse_one_token("HOSTS")
        self.assertEqual(TType.KEYWORD_HOSTS, terminal.symbol_id)
        self.assertEqual("HOSTS", terminal.symbol_value)

        terminal = parse_one_token("hosts")
        self.assertEqual(TType.KEYWORD_HOSTS, terminal.symbol_id)
        self.assertEqual("hosts", terminal.symbol_value)

    def test_keyword_hour(self):
        """测试解析 HOUR 关键字"""
        terminal = parse_one_token("HOUR")
        self.assertEqual(TType.KEYWORD_HOUR, terminal.symbol_id)
        self.assertEqual("HOUR", terminal.symbol_value)

        terminal = parse_one_token("hour")
        self.assertEqual(TType.KEYWORD_HOUR, terminal.symbol_id)
        self.assertEqual("hour", terminal.symbol_value)

    def test_keyword_hour_microsecond(self):
        """测试解析 HOUR_MICROSECOND 关键字"""
        terminal = parse_one_token("HOUR_MICROSECOND")
        self.assertEqual(TType.KEYWORD_HOUR_MICROSECOND, terminal.symbol_id)
        self.assertEqual("HOUR_MICROSECOND", terminal.symbol_value)

        terminal = parse_one_token("hour_microsecond")
        self.assertEqual(TType.KEYWORD_HOUR_MICROSECOND, terminal.symbol_id)
        self.assertEqual("hour_microsecond", terminal.symbol_value)

    def test_keyword_hour_minute(self):
        """测试解析 HOUR_MINUTE 关键字"""
        terminal = parse_one_token("HOUR_MINUTE")
        self.assertEqual(TType.KEYWORD_HOUR_MINUTE, terminal.symbol_id)
        self.assertEqual("HOUR_MINUTE", terminal.symbol_value)

        terminal = parse_one_token("hour_minute")
        self.assertEqual(TType.KEYWORD_HOUR_MINUTE, terminal.symbol_id)
        self.assertEqual("hour_minute", terminal.symbol_value)

    def test_keyword_hour_second(self):
        """测试解析 HOUR_SECOND 关键字"""
        terminal = parse_one_token("HOUR_SECOND")
        self.assertEqual(TType.KEYWORD_HOUR_SECOND, terminal.symbol_id)
        self.assertEqual("HOUR_SECOND", terminal.symbol_value)

        terminal = parse_one_token("hour_second")
        self.assertEqual(TType.KEYWORD_HOUR_SECOND, terminal.symbol_id)
        self.assertEqual("hour_second", terminal.symbol_value)

    def test_keyword_identified(self):
        """测试解析 IDENTIFIED 关键字"""
        terminal = parse_one_token("IDENTIFIED")
        self.assertEqual(TType.KEYWORD_IDENTIFIED, terminal.symbol_id)
        self.assertEqual("IDENTIFIED", terminal.symbol_value)

        terminal = parse_one_token("identified")
        self.assertEqual(TType.KEYWORD_IDENTIFIED, terminal.symbol_id)
        self.assertEqual("identified", terminal.symbol_value)

    def test_keyword_if(self):
        """测试解析 IF 关键字"""
        terminal = parse_one_token("IF")
        self.assertEqual(TType.KEYWORD_IF, terminal.symbol_id)
        self.assertEqual("IF", terminal.symbol_value)

        terminal = parse_one_token("if")
        self.assertEqual(TType.KEYWORD_IF, terminal.symbol_id)
        self.assertEqual("if", terminal.symbol_value)

    def test_keyword_ignore(self):
        """测试解析 IGNORE 关键字"""
        terminal = parse_one_token("IGNORE")
        self.assertEqual(TType.KEYWORD_IGNORE, terminal.symbol_id)
        self.assertEqual("IGNORE", terminal.symbol_value)

        terminal = parse_one_token("ignore")
        self.assertEqual(TType.KEYWORD_IGNORE, terminal.symbol_id)
        self.assertEqual("ignore", terminal.symbol_value)

    def test_keyword_ignore_server_ids(self):
        """测试解析 IGNORE_SERVER_IDS 关键字"""
        terminal = parse_one_token("IGNORE_SERVER_IDS")
        self.assertEqual(TType.KEYWORD_IGNORE_SERVER_IDS, terminal.symbol_id)
        self.assertEqual("IGNORE_SERVER_IDS", terminal.symbol_value)

        terminal = parse_one_token("ignore_server_ids")
        self.assertEqual(TType.KEYWORD_IGNORE_SERVER_IDS, terminal.symbol_id)
        self.assertEqual("ignore_server_ids", terminal.symbol_value)

    def test_keyword_import(self):
        """测试解析 IMPORT 关键字"""
        terminal = parse_one_token("IMPORT")
        self.assertEqual(TType.KEYWORD_IMPORT, terminal.symbol_id)
        self.assertEqual("IMPORT", terminal.symbol_value)

        terminal = parse_one_token("import")
        self.assertEqual(TType.KEYWORD_IMPORT, terminal.symbol_id)
        self.assertEqual("import", terminal.symbol_value)

    def test_keyword_in(self):
        """测试解析 IN 关键字"""
        terminal = parse_one_token("IN")
        self.assertEqual(TType.KEYWORD_IN, terminal.symbol_id)
        self.assertEqual("IN", terminal.symbol_value)

        terminal = parse_one_token("in")
        self.assertEqual(TType.KEYWORD_IN, terminal.symbol_id)
        self.assertEqual("in", terminal.symbol_value)

    def test_keyword_inactive(self):
        """测试解析 INACTIVE 关键字"""
        terminal = parse_one_token("INACTIVE")
        self.assertEqual(TType.KEYWORD_INACTIVE, terminal.symbol_id)
        self.assertEqual("INACTIVE", terminal.symbol_value)

        terminal = parse_one_token("inactive")
        self.assertEqual(TType.KEYWORD_INACTIVE, terminal.symbol_id)
        self.assertEqual("inactive", terminal.symbol_value)

    def test_keyword_index(self):
        """测试解析 INDEX 关键字"""
        terminal = parse_one_token("INDEX")
        self.assertEqual(TType.KEYWORD_INDEX, terminal.symbol_id)
        self.assertEqual("INDEX", terminal.symbol_value)

        terminal = parse_one_token("index")
        self.assertEqual(TType.KEYWORD_INDEX, terminal.symbol_id)
        self.assertEqual("index", terminal.symbol_value)

    def test_keyword_indexes(self):
        """测试解析 INDEXES 关键字"""
        terminal = parse_one_token("INDEXES")
        self.assertEqual(TType.KEYWORD_INDEXES, terminal.symbol_id)
        self.assertEqual("INDEXES", terminal.symbol_value)

        terminal = parse_one_token("indexes")
        self.assertEqual(TType.KEYWORD_INDEXES, terminal.symbol_id)
        self.assertEqual("indexes", terminal.symbol_value)

    def test_keyword_infile(self):
        """测试解析 INFILE 关键字"""
        terminal = parse_one_token("INFILE")
        self.assertEqual(TType.KEYWORD_INFILE, terminal.symbol_id)
        self.assertEqual("INFILE", terminal.symbol_value)

        terminal = parse_one_token("infile")
        self.assertEqual(TType.KEYWORD_INFILE, terminal.symbol_id)
        self.assertEqual("infile", terminal.symbol_value)

    def test_keyword_initial(self):
        """测试解析 INITIAL 关键字"""
        terminal = parse_one_token("INITIAL")
        self.assertEqual(TType.KEYWORD_INITIAL, terminal.symbol_id)
        self.assertEqual("INITIAL", terminal.symbol_value)

        terminal = parse_one_token("initial")
        self.assertEqual(TType.KEYWORD_INITIAL, terminal.symbol_id)
        self.assertEqual("initial", terminal.symbol_value)

    def test_keyword_initial_size(self):
        """测试解析 INITIAL_SIZE 关键字"""
        terminal = parse_one_token("INITIAL_SIZE")
        self.assertEqual(TType.KEYWORD_INITIAL_SIZE, terminal.symbol_id)
        self.assertEqual("INITIAL_SIZE", terminal.symbol_value)

        terminal = parse_one_token("initial_size")
        self.assertEqual(TType.KEYWORD_INITIAL_SIZE, terminal.symbol_id)
        self.assertEqual("initial_size", terminal.symbol_value)

    def test_keyword_initiate(self):
        """测试解析 INITIATE 关键字"""
        terminal = parse_one_token("INITIATE")
        self.assertEqual(TType.KEYWORD_INITIATE, terminal.symbol_id)
        self.assertEqual("INITIATE", terminal.symbol_value)

        terminal = parse_one_token("initiate")
        self.assertEqual(TType.KEYWORD_INITIATE, terminal.symbol_id)
        self.assertEqual("initiate", terminal.symbol_value)

    def test_keyword_inner(self):
        """测试解析 INNER 关键字"""
        terminal = parse_one_token("INNER")
        self.assertEqual(TType.KEYWORD_INNER, terminal.symbol_id)
        self.assertEqual("INNER", terminal.symbol_value)

        terminal = parse_one_token("inner")
        self.assertEqual(TType.KEYWORD_INNER, terminal.symbol_id)
        self.assertEqual("inner", terminal.symbol_value)

    def test_keyword_inout(self):
        """测试解析 INOUT 关键字"""
        terminal = parse_one_token("INOUT")
        self.assertEqual(TType.KEYWORD_INOUT, terminal.symbol_id)
        self.assertEqual("INOUT", terminal.symbol_value)

        terminal = parse_one_token("inout")
        self.assertEqual(TType.KEYWORD_INOUT, terminal.symbol_id)
        self.assertEqual("inout", terminal.symbol_value)

    def test_keyword_insensitive(self):
        """测试解析 INSENSITIVE 关键字"""
        terminal = parse_one_token("INSENSITIVE")
        self.assertEqual(TType.KEYWORD_INSENSITIVE, terminal.symbol_id)
        self.assertEqual("INSENSITIVE", terminal.symbol_value)

        terminal = parse_one_token("insensitive")
        self.assertEqual(TType.KEYWORD_INSENSITIVE, terminal.symbol_id)
        self.assertEqual("insensitive", terminal.symbol_value)

    def test_keyword_insert(self):
        """测试解析 INSERT 关键字"""
        terminal = parse_one_token("INSERT")
        self.assertEqual(TType.KEYWORD_INSERT, terminal.symbol_id)
        self.assertEqual("INSERT", terminal.symbol_value)

        terminal = parse_one_token("insert")
        self.assertEqual(TType.KEYWORD_INSERT, terminal.symbol_id)
        self.assertEqual("insert", terminal.symbol_value)

    def test_keyword_insert_method(self):
        """测试解析 INSERT_METHOD 关键字"""
        terminal = parse_one_token("INSERT_METHOD")
        self.assertEqual(TType.KEYWORD_INSERT_METHOD, terminal.symbol_id)
        self.assertEqual("INSERT_METHOD", terminal.symbol_value)

        terminal = parse_one_token("insert_method")
        self.assertEqual(TType.KEYWORD_INSERT_METHOD, terminal.symbol_id)
        self.assertEqual("insert_method", terminal.symbol_value)

    def test_keyword_install(self):
        """测试解析 INSTALL 关键字"""
        terminal = parse_one_token("INSTALL")
        self.assertEqual(TType.KEYWORD_INSTALL, terminal.symbol_id)
        self.assertEqual("INSTALL", terminal.symbol_value)

        terminal = parse_one_token("install")
        self.assertEqual(TType.KEYWORD_INSTALL, terminal.symbol_id)
        self.assertEqual("install", terminal.symbol_value)

    def test_keyword_instance(self):
        """测试解析 INSTANCE 关键字"""
        terminal = parse_one_token("INSTANCE")
        self.assertEqual(TType.KEYWORD_INSTANCE, terminal.symbol_id)
        self.assertEqual("INSTANCE", terminal.symbol_value)

        terminal = parse_one_token("instance")
        self.assertEqual(TType.KEYWORD_INSTANCE, terminal.symbol_id)
        self.assertEqual("instance", terminal.symbol_value)

    def test_keyword_int(self):
        """测试解析 INT 关键字"""
        terminal = parse_one_token("INT")
        self.assertEqual(TType.KEYWORD_INT, terminal.symbol_id)
        self.assertEqual("INT", terminal.symbol_value)

        terminal = parse_one_token("int")
        self.assertEqual(TType.KEYWORD_INT, terminal.symbol_id)
        self.assertEqual("int", terminal.symbol_value)

    def test_keyword_int1(self):
        """测试解析 INT1 关键字"""
        terminal = parse_one_token("INT1")
        self.assertEqual(TType.KEYWORD_INT1, terminal.symbol_id)
        self.assertEqual("INT1", terminal.symbol_value)

        terminal = parse_one_token("int1")
        self.assertEqual(TType.KEYWORD_INT1, terminal.symbol_id)
        self.assertEqual("int1", terminal.symbol_value)

    def test_keyword_int2(self):
        """测试解析 INT2 关键字"""
        terminal = parse_one_token("INT2")
        self.assertEqual(TType.KEYWORD_INT2, terminal.symbol_id)
        self.assertEqual("INT2", terminal.symbol_value)

        terminal = parse_one_token("int2")
        self.assertEqual(TType.KEYWORD_INT2, terminal.symbol_id)
        self.assertEqual("int2", terminal.symbol_value)

    def test_keyword_int3(self):
        """测试解析 INT3 关键字"""
        terminal = parse_one_token("INT3")
        self.assertEqual(TType.KEYWORD_INT3, terminal.symbol_id)
        self.assertEqual("INT3", terminal.symbol_value)

        terminal = parse_one_token("int3")
        self.assertEqual(TType.KEYWORD_INT3, terminal.symbol_id)
        self.assertEqual("int3", terminal.symbol_value)

    def test_keyword_int4(self):
        """测试解析 INT4 关键字"""
        terminal = parse_one_token("INT4")
        self.assertEqual(TType.KEYWORD_INT4, terminal.symbol_id)
        self.assertEqual("INT4", terminal.symbol_value)

        terminal = parse_one_token("int4")
        self.assertEqual(TType.KEYWORD_INT4, terminal.symbol_id)
        self.assertEqual("int4", terminal.symbol_value)

    def test_keyword_int8(self):
        """测试解析 INT8 关键字"""
        terminal = parse_one_token("INT8")
        self.assertEqual(TType.KEYWORD_INT8, terminal.symbol_id)
        self.assertEqual("INT8", terminal.symbol_value)

        terminal = parse_one_token("int8")
        self.assertEqual(TType.KEYWORD_INT8, terminal.symbol_id)
        self.assertEqual("int8", terminal.symbol_value)

    def test_keyword_integer(self):
        """测试解析 INTEGER 关键字"""
        terminal = parse_one_token("INTEGER")
        self.assertEqual(TType.KEYWORD_INTEGER, terminal.symbol_id)
        self.assertEqual("INTEGER", terminal.symbol_value)

        terminal = parse_one_token("integer")
        self.assertEqual(TType.KEYWORD_INTEGER, terminal.symbol_id)
        self.assertEqual("integer", terminal.symbol_value)

    def test_keyword_intersect(self):
        """测试解析 INTERSECT 关键字"""
        terminal = parse_one_token("INTERSECT")
        self.assertEqual(TType.KEYWORD_INTERSECT, terminal.symbol_id)
        self.assertEqual("INTERSECT", terminal.symbol_value)

        terminal = parse_one_token("intersect")
        self.assertEqual(TType.KEYWORD_INTERSECT, terminal.symbol_id)
        self.assertEqual("intersect", terminal.symbol_value)

    def test_keyword_interval(self):
        """测试解析 INTERVAL 关键字"""
        terminal = parse_one_token("INTERVAL")
        self.assertEqual(TType.KEYWORD_INTERVAL, terminal.symbol_id)
        self.assertEqual("INTERVAL", terminal.symbol_value)

        terminal = parse_one_token("interval")
        self.assertEqual(TType.KEYWORD_INTERVAL, terminal.symbol_id)
        self.assertEqual("interval", terminal.symbol_value)

    def test_keyword_into(self):
        """测试解析 INTO 关键字"""
        terminal = parse_one_token("INTO")
        self.assertEqual(TType.KEYWORD_INTO, terminal.symbol_id)
        self.assertEqual("INTO", terminal.symbol_value)

        terminal = parse_one_token("into")
        self.assertEqual(TType.KEYWORD_INTO, terminal.symbol_id)
        self.assertEqual("into", terminal.symbol_value)

    def test_keyword_invisible(self):
        """测试解析 INVISIBLE 关键字"""
        terminal = parse_one_token("INVISIBLE")
        self.assertEqual(TType.KEYWORD_INVISIBLE, terminal.symbol_id)
        self.assertEqual("INVISIBLE", terminal.symbol_value)

        terminal = parse_one_token("invisible")
        self.assertEqual(TType.KEYWORD_INVISIBLE, terminal.symbol_id)
        self.assertEqual("invisible", terminal.symbol_value)

    def test_keyword_invoker(self):
        """测试解析 INVOKER 关键字"""
        terminal = parse_one_token("INVOKER")
        self.assertEqual(TType.KEYWORD_INVOKER, terminal.symbol_id)
        self.assertEqual("INVOKER", terminal.symbol_value)

        terminal = parse_one_token("invoker")
        self.assertEqual(TType.KEYWORD_INVOKER, terminal.symbol_id)
        self.assertEqual("invoker", terminal.symbol_value)

    def test_keyword_io(self):
        """测试解析 IO 关键字"""
        terminal = parse_one_token("IO")
        self.assertEqual(TType.KEYWORD_IO, terminal.symbol_id)
        self.assertEqual("IO", terminal.symbol_value)

        terminal = parse_one_token("io")
        self.assertEqual(TType.KEYWORD_IO, terminal.symbol_id)
        self.assertEqual("io", terminal.symbol_value)

    def test_keyword_io_after_gtids(self):
        """测试解析 IO_AFTER_GTIDS 关键字"""
        terminal = parse_one_token("IO_AFTER_GTIDS")
        self.assertEqual(TType.KEYWORD_IO_AFTER_GTIDS, terminal.symbol_id)
        self.assertEqual("IO_AFTER_GTIDS", terminal.symbol_value)

        terminal = parse_one_token("io_after_gtids")
        self.assertEqual(TType.KEYWORD_IO_AFTER_GTIDS, terminal.symbol_id)
        self.assertEqual("io_after_gtids", terminal.symbol_value)

    def test_keyword_io_before_gtids(self):
        """测试解析 IO_BEFORE_GTIDS 关键字"""
        terminal = parse_one_token("IO_BEFORE_GTIDS")
        self.assertEqual(TType.KEYWORD_IO_BEFORE_GTIDS, terminal.symbol_id)
        self.assertEqual("IO_BEFORE_GTIDS", terminal.symbol_value)

        terminal = parse_one_token("io_before_gtids")
        self.assertEqual(TType.KEYWORD_IO_BEFORE_GTIDS, terminal.symbol_id)
        self.assertEqual("io_before_gtids", terminal.symbol_value)

    def test_keyword_io_thread(self):
        """测试解析 IO_THREAD 关键字"""
        terminal = parse_one_token("IO_THREAD")
        self.assertEqual(TType.KEYWORD_IO_THREAD, terminal.symbol_id)
        self.assertEqual("IO_THREAD", terminal.symbol_value)

        terminal = parse_one_token("io_thread")
        self.assertEqual(TType.KEYWORD_IO_THREAD, terminal.symbol_id)
        self.assertEqual("io_thread", terminal.symbol_value)

    def test_keyword_ipc(self):
        """测试解析 IPC 关键字"""
        terminal = parse_one_token("IPC")
        self.assertEqual(TType.KEYWORD_IPC, terminal.symbol_id)
        self.assertEqual("IPC", terminal.symbol_value)

        terminal = parse_one_token("ipc")
        self.assertEqual(TType.KEYWORD_IPC, terminal.symbol_id)
        self.assertEqual("ipc", terminal.symbol_value)

    def test_keyword_is(self):
        """测试解析 IS 关键字"""
        terminal = parse_one_token("IS")
        self.assertEqual(TType.KEYWORD_IS, terminal.symbol_id)
        self.assertEqual("IS", terminal.symbol_value)

        terminal = parse_one_token("is")
        self.assertEqual(TType.KEYWORD_IS, terminal.symbol_id)
        self.assertEqual("is", terminal.symbol_value)

    def test_keyword_isolation(self):
        """测试解析 ISOLATION 关键字"""
        terminal = parse_one_token("ISOLATION")
        self.assertEqual(TType.KEYWORD_ISOLATION, terminal.symbol_id)
        self.assertEqual("ISOLATION", terminal.symbol_value)

        terminal = parse_one_token("isolation")
        self.assertEqual(TType.KEYWORD_ISOLATION, terminal.symbol_id)
        self.assertEqual("isolation", terminal.symbol_value)

    def test_keyword_issuer(self):
        """测试解析 ISSUER 关键字"""
        terminal = parse_one_token("ISSUER")
        self.assertEqual(TType.KEYWORD_ISSUER, terminal.symbol_id)
        self.assertEqual("ISSUER", terminal.symbol_value)

        terminal = parse_one_token("issuer")
        self.assertEqual(TType.KEYWORD_ISSUER, terminal.symbol_id)
        self.assertEqual("issuer", terminal.symbol_value)

    def test_keyword_iterate(self):
        """测试解析 ITERATE 关键字"""
        terminal = parse_one_token("ITERATE")
        self.assertEqual(TType.KEYWORD_ITERATE, terminal.symbol_id)
        self.assertEqual("ITERATE", terminal.symbol_value)

        terminal = parse_one_token("iterate")
        self.assertEqual(TType.KEYWORD_ITERATE, terminal.symbol_id)
        self.assertEqual("iterate", terminal.symbol_value)

    def test_keyword_join(self):
        """测试解析 JOIN 关键字"""
        terminal = parse_one_token("JOIN")
        self.assertEqual(TType.KEYWORD_JOIN, terminal.symbol_id)
        self.assertEqual("JOIN", terminal.symbol_value)

        terminal = parse_one_token("join")
        self.assertEqual(TType.KEYWORD_JOIN, terminal.symbol_id)
        self.assertEqual("join", terminal.symbol_value)

    def test_keyword_json(self):
        """测试解析 JSON 关键字"""
        terminal = parse_one_token("JSON")
        self.assertEqual(TType.KEYWORD_JSON, terminal.symbol_id)
        self.assertEqual("JSON", terminal.symbol_value)

        terminal = parse_one_token("json")
        self.assertEqual(TType.KEYWORD_JSON, terminal.symbol_id)
        self.assertEqual("json", terminal.symbol_value)

    def test_keyword_json_table(self):
        """测试解析 JSON_TABLE 关键字"""
        terminal = parse_one_token("JSON_TABLE")
        self.assertEqual(TType.KEYWORD_JSON_TABLE, terminal.symbol_id)
        self.assertEqual("JSON_TABLE", terminal.symbol_value)

        terminal = parse_one_token("json_table")
        self.assertEqual(TType.KEYWORD_JSON_TABLE, terminal.symbol_id)
        self.assertEqual("json_table", terminal.symbol_value)

    def test_keyword_json_value(self):
        """测试解析 JSON_VALUE 关键字"""
        terminal = parse_one_token("JSON_VALUE")
        self.assertEqual(TType.KEYWORD_JSON_VALUE, terminal.symbol_id)
        self.assertEqual("JSON_VALUE", terminal.symbol_value)

        terminal = parse_one_token("json_value")
        self.assertEqual(TType.KEYWORD_JSON_VALUE, terminal.symbol_id)
        self.assertEqual("json_value", terminal.symbol_value)

    def test_keyword_key(self):
        """测试解析 KEY 关键字"""
        terminal = parse_one_token("KEY")
        self.assertEqual(TType.KEYWORD_KEY, terminal.symbol_id)
        self.assertEqual("KEY", terminal.symbol_value)

        terminal = parse_one_token("key")
        self.assertEqual(TType.KEYWORD_KEY, terminal.symbol_id)
        self.assertEqual("key", terminal.symbol_value)

    def test_keyword_keyring(self):
        """测试解析 KEYRING 关键字"""
        terminal = parse_one_token("KEYRING")
        self.assertEqual(TType.KEYWORD_KEYRING, terminal.symbol_id)
        self.assertEqual("KEYRING", terminal.symbol_value)

        terminal = parse_one_token("keyring")
        self.assertEqual(TType.KEYWORD_KEYRING, terminal.symbol_id)
        self.assertEqual("keyring", terminal.symbol_value)

    def test_keyword_keys(self):
        """测试解析 KEYS 关键字"""
        terminal = parse_one_token("KEYS")
        self.assertEqual(TType.KEYWORD_KEYS, terminal.symbol_id)
        self.assertEqual("KEYS", terminal.symbol_value)

        terminal = parse_one_token("keys")
        self.assertEqual(TType.KEYWORD_KEYS, terminal.symbol_id)
        self.assertEqual("keys", terminal.symbol_value)

    def test_keyword_key_block_size(self):
        """测试解析 KEY_BLOCK_SIZE 关键字"""
        terminal = parse_one_token("KEY_BLOCK_SIZE")
        self.assertEqual(TType.KEYWORD_KEY_BLOCK_SIZE, terminal.symbol_id)
        self.assertEqual("KEY_BLOCK_SIZE", terminal.symbol_value)

        terminal = parse_one_token("key_block_size")
        self.assertEqual(TType.KEYWORD_KEY_BLOCK_SIZE, terminal.symbol_id)
        self.assertEqual("key_block_size", terminal.symbol_value)

    def test_keyword_kill(self):
        """测试解析 KILL 关键字"""
        terminal = parse_one_token("KILL")
        self.assertEqual(TType.KEYWORD_KILL, terminal.symbol_id)
        self.assertEqual("KILL", terminal.symbol_value)

        terminal = parse_one_token("kill")
        self.assertEqual(TType.KEYWORD_KILL, terminal.symbol_id)
        self.assertEqual("kill", terminal.symbol_value)

    def test_keyword_lag(self):
        """测试解析 LAG 关键字"""
        terminal = parse_one_token("LAG")
        self.assertEqual(TType.KEYWORD_LAG, terminal.symbol_id)
        self.assertEqual("LAG", terminal.symbol_value)

        terminal = parse_one_token("lag")
        self.assertEqual(TType.KEYWORD_LAG, terminal.symbol_id)
        self.assertEqual("lag", terminal.symbol_value)

    def test_keyword_language(self):
        """测试解析 LANGUAGE 关键字"""
        terminal = parse_one_token("LANGUAGE")
        self.assertEqual(TType.KEYWORD_LANGUAGE, terminal.symbol_id)
        self.assertEqual("LANGUAGE", terminal.symbol_value)

        terminal = parse_one_token("language")
        self.assertEqual(TType.KEYWORD_LANGUAGE, terminal.symbol_id)
        self.assertEqual("language", terminal.symbol_value)

    def test_keyword_last(self):
        """测试解析 LAST 关键字"""
        terminal = parse_one_token("LAST")
        self.assertEqual(TType.KEYWORD_LAST, terminal.symbol_id)
        self.assertEqual("LAST", terminal.symbol_value)

        terminal = parse_one_token("last")
        self.assertEqual(TType.KEYWORD_LAST, terminal.symbol_id)
        self.assertEqual("last", terminal.symbol_value)

    def test_keyword_last_value(self):
        """测试解析 LAST_VALUE 关键字"""
        terminal = parse_one_token("LAST_VALUE")
        self.assertEqual(TType.KEYWORD_LAST_VALUE, terminal.symbol_id)
        self.assertEqual("LAST_VALUE", terminal.symbol_value)

        terminal = parse_one_token("last_value")
        self.assertEqual(TType.KEYWORD_LAST_VALUE, terminal.symbol_id)
        self.assertEqual("last_value", terminal.symbol_value)

    def test_keyword_lateral(self):
        """测试解析 LATERAL 关键字"""
        terminal = parse_one_token("LATERAL")
        self.assertEqual(TType.KEYWORD_LATERAL, terminal.symbol_id)
        self.assertEqual("LATERAL", terminal.symbol_value)

        terminal = parse_one_token("lateral")
        self.assertEqual(TType.KEYWORD_LATERAL, terminal.symbol_id)
        self.assertEqual("lateral", terminal.symbol_value)

    def test_keyword_lead(self):
        """测试解析 LEAD 关键字"""
        terminal = parse_one_token("LEAD")
        self.assertEqual(TType.KEYWORD_LEAD, terminal.symbol_id)
        self.assertEqual("LEAD", terminal.symbol_value)

        terminal = parse_one_token("lead")
        self.assertEqual(TType.KEYWORD_LEAD, terminal.symbol_id)
        self.assertEqual("lead", terminal.symbol_value)

    def test_keyword_leading(self):
        """测试解析 LEADING 关键字"""
        terminal = parse_one_token("LEADING")
        self.assertEqual(TType.KEYWORD_LEADING, terminal.symbol_id)
        self.assertEqual("LEADING", terminal.symbol_value)

        terminal = parse_one_token("leading")
        self.assertEqual(TType.KEYWORD_LEADING, terminal.symbol_id)
        self.assertEqual("leading", terminal.symbol_value)

    def test_keyword_leave(self):
        """测试解析 LEAVE 关键字"""
        terminal = parse_one_token("LEAVE")
        self.assertEqual(TType.KEYWORD_LEAVE, terminal.symbol_id)
        self.assertEqual("LEAVE", terminal.symbol_value)

        terminal = parse_one_token("leave")
        self.assertEqual(TType.KEYWORD_LEAVE, terminal.symbol_id)
        self.assertEqual("leave", terminal.symbol_value)

    def test_keyword_leaves(self):
        """测试解析 LEAVES 关键字"""
        terminal = parse_one_token("LEAVES")
        self.assertEqual(TType.KEYWORD_LEAVES, terminal.symbol_id)
        self.assertEqual("LEAVES", terminal.symbol_value)

        terminal = parse_one_token("leaves")
        self.assertEqual(TType.KEYWORD_LEAVES, terminal.symbol_id)
        self.assertEqual("leaves", terminal.symbol_value)

    def test_keyword_left(self):
        """测试解析 LEFT 关键字"""
        terminal = parse_one_token("LEFT")
        self.assertEqual(TType.KEYWORD_LEFT, terminal.symbol_id)
        self.assertEqual("LEFT", terminal.symbol_value)

        terminal = parse_one_token("left")
        self.assertEqual(TType.KEYWORD_LEFT, terminal.symbol_id)
        self.assertEqual("left", terminal.symbol_value)

    def test_keyword_less(self):
        """测试解析 LESS 关键字"""
        terminal = parse_one_token("LESS")
        self.assertEqual(TType.KEYWORD_LESS, terminal.symbol_id)
        self.assertEqual("LESS", terminal.symbol_value)

        terminal = parse_one_token("less")
        self.assertEqual(TType.KEYWORD_LESS, terminal.symbol_id)
        self.assertEqual("less", terminal.symbol_value)

    def test_keyword_level(self):
        """测试解析 LEVEL 关键字"""
        terminal = parse_one_token("LEVEL")
        self.assertEqual(TType.KEYWORD_LEVEL, terminal.symbol_id)
        self.assertEqual("LEVEL", terminal.symbol_value)

        terminal = parse_one_token("level")
        self.assertEqual(TType.KEYWORD_LEVEL, terminal.symbol_id)
        self.assertEqual("level", terminal.symbol_value)

    def test_keyword_like(self):
        """测试解析 LIKE 关键字"""
        terminal = parse_one_token("LIKE")
        self.assertEqual(TType.KEYWORD_LIKE, terminal.symbol_id)
        self.assertEqual("LIKE", terminal.symbol_value)

        terminal = parse_one_token("like")
        self.assertEqual(TType.KEYWORD_LIKE, terminal.symbol_id)
        self.assertEqual("like", terminal.symbol_value)

    def test_keyword_limit(self):
        """测试解析 LIMIT 关键字"""
        terminal = parse_one_token("LIMIT")
        self.assertEqual(TType.KEYWORD_LIMIT, terminal.symbol_id)
        self.assertEqual("LIMIT", terminal.symbol_value)

        terminal = parse_one_token("limit")
        self.assertEqual(TType.KEYWORD_LIMIT, terminal.symbol_id)
        self.assertEqual("limit", terminal.symbol_value)

    def test_keyword_linear(self):
        """测试解析 LINEAR 关键字"""
        terminal = parse_one_token("LINEAR")
        self.assertEqual(TType.KEYWORD_LINEAR, terminal.symbol_id)
        self.assertEqual("LINEAR", terminal.symbol_value)

        terminal = parse_one_token("linear")
        self.assertEqual(TType.KEYWORD_LINEAR, terminal.symbol_id)
        self.assertEqual("linear", terminal.symbol_value)

    def test_keyword_lines(self):
        """测试解析 LINES 关键字"""
        terminal = parse_one_token("LINES")
        self.assertEqual(TType.KEYWORD_LINES, terminal.symbol_id)
        self.assertEqual("LINES", terminal.symbol_value)

        terminal = parse_one_token("lines")
        self.assertEqual(TType.KEYWORD_LINES, terminal.symbol_id)
        self.assertEqual("lines", terminal.symbol_value)

    def test_keyword_linestring(self):
        """测试解析 LINESTRING 关键字"""
        terminal = parse_one_token("LINESTRING")
        self.assertEqual(TType.KEYWORD_LINESTRING, terminal.symbol_id)
        self.assertEqual("LINESTRING", terminal.symbol_value)

        terminal = parse_one_token("linestring")
        self.assertEqual(TType.KEYWORD_LINESTRING, terminal.symbol_id)
        self.assertEqual("linestring", terminal.symbol_value)

    def test_keyword_list(self):
        """测试解析 LIST 关键字"""
        terminal = parse_one_token("LIST")
        self.assertEqual(TType.KEYWORD_LIST, terminal.symbol_id)
        self.assertEqual("LIST", terminal.symbol_value)

        terminal = parse_one_token("list")
        self.assertEqual(TType.KEYWORD_LIST, terminal.symbol_id)
        self.assertEqual("list", terminal.symbol_value)

    def test_keyword_load(self):
        """测试解析 LOAD 关键字"""
        terminal = parse_one_token("LOAD")
        self.assertEqual(TType.KEYWORD_LOAD, terminal.symbol_id)
        self.assertEqual("LOAD", terminal.symbol_value)

        terminal = parse_one_token("load")
        self.assertEqual(TType.KEYWORD_LOAD, terminal.symbol_id)
        self.assertEqual("load", terminal.symbol_value)

    def test_keyword_local(self):
        """测试解析 LOCAL 关键字"""
        terminal = parse_one_token("LOCAL")
        self.assertEqual(TType.KEYWORD_LOCAL, terminal.symbol_id)
        self.assertEqual("LOCAL", terminal.symbol_value)

        terminal = parse_one_token("local")
        self.assertEqual(TType.KEYWORD_LOCAL, terminal.symbol_id)
        self.assertEqual("local", terminal.symbol_value)

    def test_keyword_localtime(self):
        """测试解析 LOCALTIME 关键字"""
        terminal = parse_one_token("LOCALTIME")
        self.assertEqual(TType.KEYWORD_LOCALTIME, terminal.symbol_id)
        self.assertEqual("LOCALTIME", terminal.symbol_value)

        terminal = parse_one_token("localtime")
        self.assertEqual(TType.KEYWORD_LOCALTIME, terminal.symbol_id)
        self.assertEqual("localtime", terminal.symbol_value)

    def test_keyword_localtimestamp(self):
        """测试解析 LOCALTIMESTAMP 关键字"""
        terminal = parse_one_token("LOCALTIMESTAMP")
        self.assertEqual(TType.KEYWORD_LOCALTIMESTAMP, terminal.symbol_id)
        self.assertEqual("LOCALTIMESTAMP", terminal.symbol_value)

        terminal = parse_one_token("localtimestamp")
        self.assertEqual(TType.KEYWORD_LOCALTIMESTAMP, terminal.symbol_id)
        self.assertEqual("localtimestamp", terminal.symbol_value)

    def test_keyword_lock(self):
        """测试解析 LOCK 关键字"""
        terminal = parse_one_token("LOCK")
        self.assertEqual(TType.KEYWORD_LOCK, terminal.symbol_id)
        self.assertEqual("LOCK", terminal.symbol_value)

        terminal = parse_one_token("lock")
        self.assertEqual(TType.KEYWORD_LOCK, terminal.symbol_id)
        self.assertEqual("lock", terminal.symbol_value)

    def test_keyword_locked(self):
        """测试解析 LOCKED 关键字"""
        terminal = parse_one_token("LOCKED")
        self.assertEqual(TType.KEYWORD_LOCKED, terminal.symbol_id)
        self.assertEqual("LOCKED", terminal.symbol_value)

        terminal = parse_one_token("locked")
        self.assertEqual(TType.KEYWORD_LOCKED, terminal.symbol_id)
        self.assertEqual("locked", terminal.symbol_value)

    def test_keyword_locks(self):
        """测试解析 LOCKS 关键字"""
        terminal = parse_one_token("LOCKS")
        self.assertEqual(TType.KEYWORD_LOCKS, terminal.symbol_id)
        self.assertEqual("LOCKS", terminal.symbol_value)

        terminal = parse_one_token("locks")
        self.assertEqual(TType.KEYWORD_LOCKS, terminal.symbol_id)
        self.assertEqual("locks", terminal.symbol_value)

    def test_keyword_log(self):
        """测试解析 LOG 关键字"""
        terminal = parse_one_token("LOG")
        self.assertEqual(TType.KEYWORD_LOG, terminal.symbol_id)
        self.assertEqual("LOG", terminal.symbol_value)

        terminal = parse_one_token("log")
        self.assertEqual(TType.KEYWORD_LOG, terminal.symbol_id)
        self.assertEqual("log", terminal.symbol_value)

    def test_keyword_logfile(self):
        """测试解析 LOGFILE 关键字"""
        terminal = parse_one_token("LOGFILE")
        self.assertEqual(TType.KEYWORD_LOGFILE, terminal.symbol_id)
        self.assertEqual("LOGFILE", terminal.symbol_value)

        terminal = parse_one_token("logfile")
        self.assertEqual(TType.KEYWORD_LOGFILE, terminal.symbol_id)
        self.assertEqual("logfile", terminal.symbol_value)

    def test_keyword_logs(self):
        """测试解析 LOGS 关键字"""
        terminal = parse_one_token("LOGS")
        self.assertEqual(TType.KEYWORD_LOGS, terminal.symbol_id)
        self.assertEqual("LOGS", terminal.symbol_value)

        terminal = parse_one_token("logs")
        self.assertEqual(TType.KEYWORD_LOGS, terminal.symbol_id)
        self.assertEqual("logs", terminal.symbol_value)

    def test_keyword_long(self):
        """测试解析 LONG 关键字"""
        terminal = parse_one_token("LONG")
        self.assertEqual(TType.KEYWORD_LONG, terminal.symbol_id)
        self.assertEqual("LONG", terminal.symbol_value)

        terminal = parse_one_token("long")
        self.assertEqual(TType.KEYWORD_LONG, terminal.symbol_id)
        self.assertEqual("long", terminal.symbol_value)

    def test_keyword_longblob(self):
        """测试解析 LONGBLOB 关键字"""
        terminal = parse_one_token("LONGBLOB")
        self.assertEqual(TType.KEYWORD_LONGBLOB, terminal.symbol_id)
        self.assertEqual("LONGBLOB", terminal.symbol_value)

        terminal = parse_one_token("longblob")
        self.assertEqual(TType.KEYWORD_LONGBLOB, terminal.symbol_id)
        self.assertEqual("longblob", terminal.symbol_value)

    def test_keyword_longtext(self):
        """测试解析 LONGTEXT 关键字"""
        terminal = parse_one_token("LONGTEXT")
        self.assertEqual(TType.KEYWORD_LONGTEXT, terminal.symbol_id)
        self.assertEqual("LONGTEXT", terminal.symbol_value)

        terminal = parse_one_token("longtext")
        self.assertEqual(TType.KEYWORD_LONGTEXT, terminal.symbol_id)
        self.assertEqual("longtext", terminal.symbol_value)

    def test_keyword_loop(self):
        """测试解析 LOOP 关键字"""
        terminal = parse_one_token("LOOP")
        self.assertEqual(TType.KEYWORD_LOOP, terminal.symbol_id)
        self.assertEqual("LOOP", terminal.symbol_value)

        terminal = parse_one_token("loop")
        self.assertEqual(TType.KEYWORD_LOOP, terminal.symbol_id)
        self.assertEqual("loop", terminal.symbol_value)

    def test_keyword_low_priority(self):
        """测试解析 LOW_PRIORITY 关键字"""
        terminal = parse_one_token("LOW_PRIORITY")
        self.assertEqual(TType.KEYWORD_LOW_PRIORITY, terminal.symbol_id)
        self.assertEqual("LOW_PRIORITY", terminal.symbol_value)

        terminal = parse_one_token("low_priority")
        self.assertEqual(TType.KEYWORD_LOW_PRIORITY, terminal.symbol_id)
        self.assertEqual("low_priority", terminal.symbol_value)

    def test_keyword_manual(self):
        """测试解析 MANUAL 关键字"""
        terminal = parse_one_token("MANUAL")
        self.assertEqual(TType.KEYWORD_MANUAL, terminal.symbol_id)
        self.assertEqual("MANUAL", terminal.symbol_value)

        terminal = parse_one_token("manual")
        self.assertEqual(TType.KEYWORD_MANUAL, terminal.symbol_id)
        self.assertEqual("manual", terminal.symbol_value)

    def test_keyword_master(self):
        """测试解析 MASTER 关键字"""
        terminal = parse_one_token("MASTER")
        self.assertEqual(TType.KEYWORD_MASTER, terminal.symbol_id)
        self.assertEqual("MASTER", terminal.symbol_value)

        terminal = parse_one_token("master")
        self.assertEqual(TType.KEYWORD_MASTER, terminal.symbol_id)
        self.assertEqual("master", terminal.symbol_value)

    def test_keyword_master_auto_position(self):
        """测试解析 MASTER_AUTO_POSITION 关键字"""
        terminal = parse_one_token("MASTER_AUTO_POSITION")
        self.assertEqual(TType.KEYWORD_MASTER_AUTO_POSITION, terminal.symbol_id)
        self.assertEqual("MASTER_AUTO_POSITION", terminal.symbol_value)

        terminal = parse_one_token("master_auto_position")
        self.assertEqual(TType.KEYWORD_MASTER_AUTO_POSITION, terminal.symbol_id)
        self.assertEqual("master_auto_position", terminal.symbol_value)

    def test_keyword_master_bind(self):
        """测试解析 MASTER_BIND 关键字"""
        terminal = parse_one_token("MASTER_BIND")
        self.assertEqual(TType.KEYWORD_MASTER_BIND, terminal.symbol_id)
        self.assertEqual("MASTER_BIND", terminal.symbol_value)

        terminal = parse_one_token("master_bind")
        self.assertEqual(TType.KEYWORD_MASTER_BIND, terminal.symbol_id)
        self.assertEqual("master_bind", terminal.symbol_value)

    def test_keyword_master_compression_algorithm(self):
        """测试解析 MASTER_COMPRESSION_ALGORITHM 关键字"""
        terminal = parse_one_token("MASTER_COMPRESSION_ALGORITHM")
        self.assertEqual(TType.KEYWORD_MASTER_COMPRESSION_ALGORITHM, terminal.symbol_id)
        self.assertEqual("MASTER_COMPRESSION_ALGORITHM", terminal.symbol_value)

        terminal = parse_one_token("master_compression_algorithm")
        self.assertEqual(TType.KEYWORD_MASTER_COMPRESSION_ALGORITHM, terminal.symbol_id)
        self.assertEqual("master_compression_algorithm", terminal.symbol_value)

    def test_keyword_master_connect_retry(self):
        """测试解析 MASTER_CONNECT_RETRY 关键字"""
        terminal = parse_one_token("MASTER_CONNECT_RETRY")
        self.assertEqual(TType.KEYWORD_MASTER_CONNECT_RETRY, terminal.symbol_id)
        self.assertEqual("MASTER_CONNECT_RETRY", terminal.symbol_value)

        terminal = parse_one_token("master_connect_retry")
        self.assertEqual(TType.KEYWORD_MASTER_CONNECT_RETRY, terminal.symbol_id)
        self.assertEqual("master_connect_retry", terminal.symbol_value)

    def test_keyword_master_delay(self):
        """测试解析 MASTER_DELAY 关键字"""
        terminal = parse_one_token("MASTER_DELAY")
        self.assertEqual(TType.KEYWORD_MASTER_DELAY, terminal.symbol_id)
        self.assertEqual("MASTER_DELAY", terminal.symbol_value)

        terminal = parse_one_token("master_delay")
        self.assertEqual(TType.KEYWORD_MASTER_DELAY, terminal.symbol_id)
        self.assertEqual("master_delay", terminal.symbol_value)

    def test_keyword_master_heartbeat_period(self):
        """测试解析 MASTER_HEARTBEAT_PERIOD 关键字"""
        terminal = parse_one_token("MASTER_HEARTBEAT_PERIOD")
        self.assertEqual(TType.KEYWORD_MASTER_HEARTBEAT_PERIOD, terminal.symbol_id)
        self.assertEqual("MASTER_HEARTBEAT_PERIOD", terminal.symbol_value)

        terminal = parse_one_token("master_heartbeat_period")
        self.assertEqual(TType.KEYWORD_MASTER_HEARTBEAT_PERIOD, terminal.symbol_id)
        self.assertEqual("master_heartbeat_period", terminal.symbol_value)

    def test_keyword_master_host(self):
        """测试解析 MASTER_HOST 关键字"""
        terminal = parse_one_token("MASTER_HOST")
        self.assertEqual(TType.KEYWORD_MASTER_HOST, terminal.symbol_id)
        self.assertEqual("MASTER_HOST", terminal.symbol_value)

        terminal = parse_one_token("master_host")
        self.assertEqual(TType.KEYWORD_MASTER_HOST, terminal.symbol_id)
        self.assertEqual("master_host", terminal.symbol_value)

    def test_keyword_master_log_file(self):
        """测试解析 MASTER_LOG_FILE 关键字"""
        terminal = parse_one_token("MASTER_LOG_FILE")
        self.assertEqual(TType.KEYWORD_MASTER_LOG_FILE, terminal.symbol_id)
        self.assertEqual("MASTER_LOG_FILE", terminal.symbol_value)

        terminal = parse_one_token("master_log_file")
        self.assertEqual(TType.KEYWORD_MASTER_LOG_FILE, terminal.symbol_id)
        self.assertEqual("master_log_file", terminal.symbol_value)

    def test_keyword_master_log_pos(self):
        """测试解析 MASTER_LOG_POS 关键字"""
        terminal = parse_one_token("MASTER_LOG_POS")
        self.assertEqual(TType.KEYWORD_MASTER_LOG_POS, terminal.symbol_id)
        self.assertEqual("MASTER_LOG_POS", terminal.symbol_value)

        terminal = parse_one_token("master_log_pos")
        self.assertEqual(TType.KEYWORD_MASTER_LOG_POS, terminal.symbol_id)
        self.assertEqual("master_log_pos", terminal.symbol_value)

    def test_keyword_master_password(self):
        """测试解析 MASTER_PASSWORD 关键字"""
        terminal = parse_one_token("MASTER_PASSWORD")
        self.assertEqual(TType.KEYWORD_MASTER_PASSWORD, terminal.symbol_id)
        self.assertEqual("MASTER_PASSWORD", terminal.symbol_value)

        terminal = parse_one_token("master_password")
        self.assertEqual(TType.KEYWORD_MASTER_PASSWORD, terminal.symbol_id)
        self.assertEqual("master_password", terminal.symbol_value)

    def test_keyword_master_port(self):
        """测试解析 MASTER_PORT 关键字"""
        terminal = parse_one_token("MASTER_PORT")
        self.assertEqual(TType.KEYWORD_MASTER_PORT, terminal.symbol_id)
        self.assertEqual("MASTER_PORT", terminal.symbol_value)

        terminal = parse_one_token("master_port")
        self.assertEqual(TType.KEYWORD_MASTER_PORT, terminal.symbol_id)
        self.assertEqual("master_port", terminal.symbol_value)

    def test_keyword_master_public_key_path(self):
        """测试解析 MASTER_PUBLIC_KEY_PATH 关键字"""
        terminal = parse_one_token("MASTER_PUBLIC_KEY_PATH")
        self.assertEqual(TType.KEYWORD_MASTER_PUBLIC_KEY_PATH, terminal.symbol_id)
        self.assertEqual("MASTER_PUBLIC_KEY_PATH", terminal.symbol_value)

        terminal = parse_one_token("master_public_key_path")
        self.assertEqual(TType.KEYWORD_MASTER_PUBLIC_KEY_PATH, terminal.symbol_id)
        self.assertEqual("master_public_key_path", terminal.symbol_value)

    def test_keyword_master_retry_count(self):
        """测试解析 MASTER_RETRY_COUNT 关键字"""
        terminal = parse_one_token("MASTER_RETRY_COUNT")
        self.assertEqual(TType.KEYWORD_MASTER_RETRY_COUNT, terminal.symbol_id)
        self.assertEqual("MASTER_RETRY_COUNT", terminal.symbol_value)

        terminal = parse_one_token("master_retry_count")
        self.assertEqual(TType.KEYWORD_MASTER_RETRY_COUNT, terminal.symbol_id)
        self.assertEqual("master_retry_count", terminal.symbol_value)

    def test_keyword_master_ssl(self):
        """测试解析 MASTER_SSL 关键字"""
        terminal = parse_one_token("MASTER_SSL")
        self.assertEqual(TType.KEYWORD_MASTER_SSL, terminal.symbol_id)
        self.assertEqual("MASTER_SSL", terminal.symbol_value)

        terminal = parse_one_token("master_ssl")
        self.assertEqual(TType.KEYWORD_MASTER_SSL, terminal.symbol_id)
        self.assertEqual("master_ssl", terminal.symbol_value)

    def test_keyword_master_ssl_ca(self):
        """测试解析 MASTER_SSL_CA 关键字"""
        terminal = parse_one_token("MASTER_SSL_CA")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CA, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_CA", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_ca")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CA, terminal.symbol_id)
        self.assertEqual("master_ssl_ca", terminal.symbol_value)

    def test_keyword_master_ssl_capath(self):
        """测试解析 MASTER_SSL_CAPATH 关键字"""
        terminal = parse_one_token("MASTER_SSL_CAPATH")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CAPATH, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_CAPATH", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_capath")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CAPATH, terminal.symbol_id)
        self.assertEqual("master_ssl_capath", terminal.symbol_value)

    def test_keyword_master_ssl_cert(self):
        """测试解析 MASTER_SSL_CERT 关键字"""
        terminal = parse_one_token("MASTER_SSL_CERT")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CERT, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_CERT", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_cert")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CERT, terminal.symbol_id)
        self.assertEqual("master_ssl_cert", terminal.symbol_value)

    def test_keyword_master_ssl_cipher(self):
        """测试解析 MASTER_SSL_CIPHER 关键字"""
        terminal = parse_one_token("MASTER_SSL_CIPHER")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CIPHER, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_CIPHER", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_cipher")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CIPHER, terminal.symbol_id)
        self.assertEqual("master_ssl_cipher", terminal.symbol_value)

    def test_keyword_master_ssl_crl(self):
        """测试解析 MASTER_SSL_CRL 关键字"""
        terminal = parse_one_token("MASTER_SSL_CRL")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CRL, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_CRL", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_crl")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CRL, terminal.symbol_id)
        self.assertEqual("master_ssl_crl", terminal.symbol_value)

    def test_keyword_master_ssl_crlpath(self):
        """测试解析 MASTER_SSL_CRLPATH 关键字"""
        terminal = parse_one_token("MASTER_SSL_CRLPATH")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CRLPATH, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_CRLPATH", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_crlpath")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_CRLPATH, terminal.symbol_id)
        self.assertEqual("master_ssl_crlpath", terminal.symbol_value)

    def test_keyword_master_ssl_key(self):
        """测试解析 MASTER_SSL_KEY 关键字"""
        terminal = parse_one_token("MASTER_SSL_KEY")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_KEY, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_KEY", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_key")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_KEY, terminal.symbol_id)
        self.assertEqual("master_ssl_key", terminal.symbol_value)

    def test_keyword_master_ssl_verify_server_cert(self):
        """测试解析 MASTER_SSL_VERIFY_SERVER_CERT 关键字"""
        terminal = parse_one_token("MASTER_SSL_VERIFY_SERVER_CERT")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_VERIFY_SERVER_CERT, terminal.symbol_id)
        self.assertEqual("MASTER_SSL_VERIFY_SERVER_CERT", terminal.symbol_value)

        terminal = parse_one_token("master_ssl_verify_server_cert")
        self.assertEqual(TType.KEYWORD_MASTER_SSL_VERIFY_SERVER_CERT, terminal.symbol_id)
        self.assertEqual("master_ssl_verify_server_cert", terminal.symbol_value)

    def test_keyword_master_tls_ciphersuites(self):
        """测试解析 MASTER_TLS_CIPHERSUITES 关键字"""
        terminal = parse_one_token("MASTER_TLS_CIPHERSUITES")
        self.assertEqual(TType.KEYWORD_MASTER_TLS_CIPHERSUITES, terminal.symbol_id)
        self.assertEqual("MASTER_TLS_CIPHERSUITES", terminal.symbol_value)

        terminal = parse_one_token("master_tls_ciphersuites")
        self.assertEqual(TType.KEYWORD_MASTER_TLS_CIPHERSUITES, terminal.symbol_id)
        self.assertEqual("master_tls_ciphersuites", terminal.symbol_value)

    def test_keyword_master_tls_version(self):
        """测试解析 MASTER_TLS_VERSION 关键字"""
        terminal = parse_one_token("MASTER_TLS_VERSION")
        self.assertEqual(TType.KEYWORD_MASTER_TLS_VERSION, terminal.symbol_id)
        self.assertEqual("MASTER_TLS_VERSION", terminal.symbol_value)

        terminal = parse_one_token("master_tls_version")
        self.assertEqual(TType.KEYWORD_MASTER_TLS_VERSION, terminal.symbol_id)
        self.assertEqual("master_tls_version", terminal.symbol_value)

    def test_keyword_master_user(self):
        """测试解析 MASTER_USER 关键字"""
        terminal = parse_one_token("MASTER_USER")
        self.assertEqual(TType.KEYWORD_MASTER_USER, terminal.symbol_id)
        self.assertEqual("MASTER_USER", terminal.symbol_value)

        terminal = parse_one_token("master_user")
        self.assertEqual(TType.KEYWORD_MASTER_USER, terminal.symbol_id)
        self.assertEqual("master_user", terminal.symbol_value)

    def test_keyword_master_zstd_compression_level(self):
        """测试解析 MASTER_ZSTD_COMPRESSION_LEVEL 关键字"""
        terminal = parse_one_token("MASTER_ZSTD_COMPRESSION_LEVEL")
        self.assertEqual(TType.KEYWORD_MASTER_ZSTD_COMPRESSION_LEVEL, terminal.symbol_id)
        self.assertEqual("MASTER_ZSTD_COMPRESSION_LEVEL", terminal.symbol_value)

        terminal = parse_one_token("master_zstd_compression_level")
        self.assertEqual(TType.KEYWORD_MASTER_ZSTD_COMPRESSION_LEVEL, terminal.symbol_id)
        self.assertEqual("master_zstd_compression_level", terminal.symbol_value)

    def test_keyword_match(self):
        """测试解析 MATCH 关键字"""
        terminal = parse_one_token("MATCH")
        self.assertEqual(TType.KEYWORD_MATCH, terminal.symbol_id)
        self.assertEqual("MATCH", terminal.symbol_value)

        terminal = parse_one_token("match")
        self.assertEqual(TType.KEYWORD_MATCH, terminal.symbol_id)
        self.assertEqual("match", terminal.symbol_value)

    def test_keyword_max_value(self):
        """测试解析 MAX_VALUE 关键字"""
        terminal = parse_one_token("MAX_VALUE")
        self.assertEqual(TType.KEYWORD_MAX_VALUE, terminal.symbol_id)
        self.assertEqual("MAX_VALUE", terminal.symbol_value)

        terminal = parse_one_token("max_value")
        self.assertEqual(TType.KEYWORD_MAX_VALUE, terminal.symbol_id)
        self.assertEqual("max_value", terminal.symbol_value)

    def test_keyword_max_connections_per_hour(self):
        """测试解析 MAX_CONNECTIONS_PER_HOUR 关键字"""
        terminal = parse_one_token("MAX_CONNECTIONS_PER_HOUR")
        self.assertEqual(TType.KEYWORD_MAX_CONNECTIONS_PER_HOUR, terminal.symbol_id)
        self.assertEqual("MAX_CONNECTIONS_PER_HOUR", terminal.symbol_value)

        terminal = parse_one_token("max_connections_per_hour")
        self.assertEqual(TType.KEYWORD_MAX_CONNECTIONS_PER_HOUR, terminal.symbol_id)
        self.assertEqual("max_connections_per_hour", terminal.symbol_value)

    def test_keyword_max_queries_per_hour(self):
        """测试解析 MAX_QUERIES_PER_HOUR 关键字"""
        terminal = parse_one_token("MAX_QUERIES_PER_HOUR")
        self.assertEqual(TType.KEYWORD_MAX_QUERIES_PER_HOUR, terminal.symbol_id)
        self.assertEqual("MAX_QUERIES_PER_HOUR", terminal.symbol_value)

        terminal = parse_one_token("max_queries_per_hour")
        self.assertEqual(TType.KEYWORD_MAX_QUERIES_PER_HOUR, terminal.symbol_id)
        self.assertEqual("max_queries_per_hour", terminal.symbol_value)

    def test_keyword_max_rows(self):
        """测试解析 MAX_ROWS 关键字"""
        terminal = parse_one_token("MAX_ROWS")
        self.assertEqual(TType.KEYWORD_MAX_ROWS, terminal.symbol_id)
        self.assertEqual("MAX_ROWS", terminal.symbol_value)

        terminal = parse_one_token("max_rows")
        self.assertEqual(TType.KEYWORD_MAX_ROWS, terminal.symbol_id)
        self.assertEqual("max_rows", terminal.symbol_value)

    def test_keyword_max_size(self):
        """测试解析 MAX_SIZE 关键字"""
        terminal = parse_one_token("MAX_SIZE")
        self.assertEqual(TType.KEYWORD_MAX_SIZE, terminal.symbol_id)
        self.assertEqual("MAX_SIZE", terminal.symbol_value)

        terminal = parse_one_token("max_size")
        self.assertEqual(TType.KEYWORD_MAX_SIZE, terminal.symbol_id)
        self.assertEqual("max_size", terminal.symbol_value)

    def test_keyword_max_updates_per_hour(self):
        """测试解析 MAX_UPDATES_PER_HOUR 关键字"""
        terminal = parse_one_token("MAX_UPDATES_PER_HOUR")
        self.assertEqual(TType.KEYWORD_MAX_UPDATES_PER_HOUR, terminal.symbol_id)
        self.assertEqual("MAX_UPDATES_PER_HOUR", terminal.symbol_value)

        terminal = parse_one_token("max_updates_per_hour")
        self.assertEqual(TType.KEYWORD_MAX_UPDATES_PER_HOUR, terminal.symbol_id)
        self.assertEqual("max_updates_per_hour", terminal.symbol_value)

    def test_keyword_max_user_connections(self):
        """测试解析 MAX_USER_CONNECTIONS 关键字"""
        terminal = parse_one_token("MAX_USER_CONNECTIONS")
        self.assertEqual(TType.KEYWORD_MAX_USER_CONNECTIONS, terminal.symbol_id)
        self.assertEqual("MAX_USER_CONNECTIONS", terminal.symbol_value)

        terminal = parse_one_token("max_user_connections")
        self.assertEqual(TType.KEYWORD_MAX_USER_CONNECTIONS, terminal.symbol_id)
        self.assertEqual("max_user_connections", terminal.symbol_value)

    def test_keyword_medium(self):
        """测试解析 MEDIUM 关键字"""
        terminal = parse_one_token("MEDIUM")
        self.assertEqual(TType.KEYWORD_MEDIUM, terminal.symbol_id)
        self.assertEqual("MEDIUM", terminal.symbol_value)

        terminal = parse_one_token("medium")
        self.assertEqual(TType.KEYWORD_MEDIUM, terminal.symbol_id)
        self.assertEqual("medium", terminal.symbol_value)

    def test_keyword_mediumblob(self):
        """测试解析 MEDIUMBLOB 关键字"""
        terminal = parse_one_token("MEDIUMBLOB")
        self.assertEqual(TType.KEYWORD_MEDIUMBLOB, terminal.symbol_id)
        self.assertEqual("MEDIUMBLOB", terminal.symbol_value)

        terminal = parse_one_token("mediumblob")
        self.assertEqual(TType.KEYWORD_MEDIUMBLOB, terminal.symbol_id)
        self.assertEqual("mediumblob", terminal.symbol_value)

    def test_keyword_mediumint(self):
        """测试解析 MEDIUMINT 关键字"""
        terminal = parse_one_token("MEDIUMINT")
        self.assertEqual(TType.KEYWORD_MEDIUMINT, terminal.symbol_id)
        self.assertEqual("MEDIUMINT", terminal.symbol_value)

        terminal = parse_one_token("mediumint")
        self.assertEqual(TType.KEYWORD_MEDIUMINT, terminal.symbol_id)
        self.assertEqual("mediumint", terminal.symbol_value)

    def test_keyword_mediumtext(self):
        """测试解析 MEDIUMTEXT 关键字"""
        terminal = parse_one_token("MEDIUMTEXT")
        self.assertEqual(TType.KEYWORD_MEDIUMTEXT, terminal.symbol_id)
        self.assertEqual("MEDIUMTEXT", terminal.symbol_value)

        terminal = parse_one_token("mediumtext")
        self.assertEqual(TType.KEYWORD_MEDIUMTEXT, terminal.symbol_id)
        self.assertEqual("mediumtext", terminal.symbol_value)

    def test_keyword_member(self):
        """测试解析 MEMBER 关键字"""
        terminal = parse_one_token("MEMBER")
        self.assertEqual(TType.KEYWORD_MEMBER, terminal.symbol_id)
        self.assertEqual("MEMBER", terminal.symbol_value)

        terminal = parse_one_token("member")
        self.assertEqual(TType.KEYWORD_MEMBER, terminal.symbol_id)
        self.assertEqual("member", terminal.symbol_value)

    def test_keyword_memory(self):
        """测试解析 MEMORY 关键字"""
        terminal = parse_one_token("MEMORY")
        self.assertEqual(TType.KEYWORD_MEMORY, terminal.symbol_id)
        self.assertEqual("MEMORY", terminal.symbol_value)

        terminal = parse_one_token("memory")
        self.assertEqual(TType.KEYWORD_MEMORY, terminal.symbol_id)
        self.assertEqual("memory", terminal.symbol_value)

    def test_keyword_merge(self):
        """测试解析 MERGE 关键字"""
        terminal = parse_one_token("MERGE")
        self.assertEqual(TType.KEYWORD_MERGE, terminal.symbol_id)
        self.assertEqual("MERGE", terminal.symbol_value)

        terminal = parse_one_token("merge")
        self.assertEqual(TType.KEYWORD_MERGE, terminal.symbol_id)
        self.assertEqual("merge", terminal.symbol_value)

    def test_keyword_message_text(self):
        """测试解析 MESSAGE_TEXT 关键字"""
        terminal = parse_one_token("MESSAGE_TEXT")
        self.assertEqual(TType.KEYWORD_MESSAGE_TEXT, terminal.symbol_id)
        self.assertEqual("MESSAGE_TEXT", terminal.symbol_value)

        terminal = parse_one_token("message_text")
        self.assertEqual(TType.KEYWORD_MESSAGE_TEXT, terminal.symbol_id)
        self.assertEqual("message_text", terminal.symbol_value)

    def test_keyword_microsecond(self):
        """测试解析 MICROSECOND 关键字"""
        terminal = parse_one_token("MICROSECOND")
        self.assertEqual(TType.KEYWORD_MICROSECOND, terminal.symbol_id)
        self.assertEqual("MICROSECOND", terminal.symbol_value)

        terminal = parse_one_token("microsecond")
        self.assertEqual(TType.KEYWORD_MICROSECOND, terminal.symbol_id)
        self.assertEqual("microsecond", terminal.symbol_value)

    def test_keyword_middleint(self):
        """测试解析 MIDDLEINT 关键字"""
        terminal = parse_one_token("MIDDLEINT")
        self.assertEqual(TType.KEYWORD_MIDDLEINT, terminal.symbol_id)
        self.assertEqual("MIDDLEINT", terminal.symbol_value)

        terminal = parse_one_token("middleint")
        self.assertEqual(TType.KEYWORD_MIDDLEINT, terminal.symbol_id)
        self.assertEqual("middleint", terminal.symbol_value)

    def test_keyword_migrate(self):
        """测试解析 MIGRATE 关键字"""
        terminal = parse_one_token("MIGRATE")
        self.assertEqual(TType.KEYWORD_MIGRATE, terminal.symbol_id)
        self.assertEqual("MIGRATE", terminal.symbol_value)

        terminal = parse_one_token("migrate")
        self.assertEqual(TType.KEYWORD_MIGRATE, terminal.symbol_id)
        self.assertEqual("migrate", terminal.symbol_value)

    def test_keyword_minute(self):
        """测试解析 MINUTE 关键字"""
        terminal = parse_one_token("MINUTE")
        self.assertEqual(TType.KEYWORD_MINUTE, terminal.symbol_id)
        self.assertEqual("MINUTE", terminal.symbol_value)

        terminal = parse_one_token("minute")
        self.assertEqual(TType.KEYWORD_MINUTE, terminal.symbol_id)
        self.assertEqual("minute", terminal.symbol_value)

    def test_keyword_minute_microsecond(self):
        """测试解析 MINUTE_MICROSECOND 关键字"""
        terminal = parse_one_token("MINUTE_MICROSECOND")
        self.assertEqual(TType.KEYWORD_MINUTE_MICROSECOND, terminal.symbol_id)
        self.assertEqual("MINUTE_MICROSECOND", terminal.symbol_value)

        terminal = parse_one_token("minute_microsecond")
        self.assertEqual(TType.KEYWORD_MINUTE_MICROSECOND, terminal.symbol_id)
        self.assertEqual("minute_microsecond", terminal.symbol_value)

    def test_keyword_minute_second(self):
        """测试解析 MINUTE_SECOND 关键字"""
        terminal = parse_one_token("MINUTE_SECOND")
        self.assertEqual(TType.KEYWORD_MINUTE_SECOND, terminal.symbol_id)
        self.assertEqual("MINUTE_SECOND", terminal.symbol_value)

        terminal = parse_one_token("minute_second")
        self.assertEqual(TType.KEYWORD_MINUTE_SECOND, terminal.symbol_id)
        self.assertEqual("minute_second", terminal.symbol_value)

    def test_keyword_min_rows(self):
        """测试解析 MIN_ROWS 关键字"""
        terminal = parse_one_token("MIN_ROWS")
        self.assertEqual(TType.KEYWORD_MIN_ROWS, terminal.symbol_id)
        self.assertEqual("MIN_ROWS", terminal.symbol_value)

        terminal = parse_one_token("min_rows")
        self.assertEqual(TType.KEYWORD_MIN_ROWS, terminal.symbol_id)
        self.assertEqual("min_rows", terminal.symbol_value)

    def test_keyword_mod(self):
        """测试解析 MOD 关键字"""
        terminal = parse_one_token("MOD")
        self.assertEqual(TType.KEYWORD_MOD, terminal.symbol_id)
        self.assertEqual("MOD", terminal.symbol_value)

        terminal = parse_one_token("mod")
        self.assertEqual(TType.KEYWORD_MOD, terminal.symbol_id)
        self.assertEqual("mod", terminal.symbol_value)

    def test_keyword_mode(self):
        """测试解析 MODE 关键字"""
        terminal = parse_one_token("MODE")
        self.assertEqual(TType.KEYWORD_MODE, terminal.symbol_id)
        self.assertEqual("MODE", terminal.symbol_value)

        terminal = parse_one_token("mode")
        self.assertEqual(TType.KEYWORD_MODE, terminal.symbol_id)
        self.assertEqual("mode", terminal.symbol_value)

    def test_keyword_modifies(self):
        """测试解析 MODIFIES 关键字"""
        terminal = parse_one_token("MODIFIES")
        self.assertEqual(TType.KEYWORD_MODIFIES, terminal.symbol_id)
        self.assertEqual("MODIFIES", terminal.symbol_value)

        terminal = parse_one_token("modifies")
        self.assertEqual(TType.KEYWORD_MODIFIES, terminal.symbol_id)
        self.assertEqual("modifies", terminal.symbol_value)

    def test_keyword_modify(self):
        """测试解析 MODIFY 关键字"""
        terminal = parse_one_token("MODIFY")
        self.assertEqual(TType.KEYWORD_MODIFY, terminal.symbol_id)
        self.assertEqual("MODIFY", terminal.symbol_value)

        terminal = parse_one_token("modify")
        self.assertEqual(TType.KEYWORD_MODIFY, terminal.symbol_id)
        self.assertEqual("modify", terminal.symbol_value)

    def test_keyword_month(self):
        """测试解析 MONTH 关键字"""
        terminal = parse_one_token("MONTH")
        self.assertEqual(TType.KEYWORD_MONTH, terminal.symbol_id)
        self.assertEqual("MONTH", terminal.symbol_value)

        terminal = parse_one_token("month")
        self.assertEqual(TType.KEYWORD_MONTH, terminal.symbol_id)
        self.assertEqual("month", terminal.symbol_value)

    def test_keyword_multilinestring(self):
        """测试解析 MULTILINESTRING 关键字"""
        terminal = parse_one_token("MULTILINESTRING")
        self.assertEqual(TType.KEYWORD_MULTILINESTRING, terminal.symbol_id)
        self.assertEqual("MULTILINESTRING", terminal.symbol_value)

        terminal = parse_one_token("multilinestring")
        self.assertEqual(TType.KEYWORD_MULTILINESTRING, terminal.symbol_id)
        self.assertEqual("multilinestring", terminal.symbol_value)

    def test_keyword_multipoint(self):
        """测试解析 MULTIPOINT 关键字"""
        terminal = parse_one_token("MULTIPOINT")
        self.assertEqual(TType.KEYWORD_MULTIPOINT, terminal.symbol_id)
        self.assertEqual("MULTIPOINT", terminal.symbol_value)

        terminal = parse_one_token("multipoint")
        self.assertEqual(TType.KEYWORD_MULTIPOINT, terminal.symbol_id)
        self.assertEqual("multipoint", terminal.symbol_value)

    def test_keyword_multipolygon(self):
        """测试解析 MULTIPOLYGON 关键字"""
        terminal = parse_one_token("MULTIPOLYGON")
        self.assertEqual(TType.KEYWORD_MULTIPOLYGON, terminal.symbol_id)
        self.assertEqual("MULTIPOLYGON", terminal.symbol_value)

        terminal = parse_one_token("multipolygon")
        self.assertEqual(TType.KEYWORD_MULTIPOLYGON, terminal.symbol_id)
        self.assertEqual("multipolygon", terminal.symbol_value)

    def test_keyword_mutex(self):
        """测试解析 MUTEX 关键字"""
        terminal = parse_one_token("MUTEX")
        self.assertEqual(TType.KEYWORD_MUTEX, terminal.symbol_id)
        self.assertEqual("MUTEX", terminal.symbol_value)

        terminal = parse_one_token("mutex")
        self.assertEqual(TType.KEYWORD_MUTEX, terminal.symbol_id)
        self.assertEqual("mutex", terminal.symbol_value)

    def test_keyword_mysql_errno(self):
        """测试解析 MYSQL_ERRNO 关键字"""
        terminal = parse_one_token("MYSQL_ERRNO")
        self.assertEqual(TType.KEYWORD_MYSQL_ERRNO, terminal.symbol_id)
        self.assertEqual("MYSQL_ERRNO", terminal.symbol_value)

        terminal = parse_one_token("mysql_errno")
        self.assertEqual(TType.KEYWORD_MYSQL_ERRNO, terminal.symbol_id)
        self.assertEqual("mysql_errno", terminal.symbol_value)

    def test_keyword_name(self):
        """测试解析 NAME 关键字"""
        terminal = parse_one_token("NAME")
        self.assertEqual(TType.KEYWORD_NAME, terminal.symbol_id)
        self.assertEqual("NAME", terminal.symbol_value)

        terminal = parse_one_token("name")
        self.assertEqual(TType.KEYWORD_NAME, terminal.symbol_id)
        self.assertEqual("name", terminal.symbol_value)

    def test_keyword_names(self):
        """测试解析 NAMES 关键字"""
        terminal = parse_one_token("NAMES")
        self.assertEqual(TType.KEYWORD_NAMES, terminal.symbol_id)
        self.assertEqual("NAMES", terminal.symbol_value)

        terminal = parse_one_token("names")
        self.assertEqual(TType.KEYWORD_NAMES, terminal.symbol_id)
        self.assertEqual("names", terminal.symbol_value)

    def test_keyword_national(self):
        """测试解析 NATIONAL 关键字"""
        terminal = parse_one_token("NATIONAL")
        self.assertEqual(TType.KEYWORD_NATIONAL, terminal.symbol_id)
        self.assertEqual("NATIONAL", terminal.symbol_value)

        terminal = parse_one_token("national")
        self.assertEqual(TType.KEYWORD_NATIONAL, terminal.symbol_id)
        self.assertEqual("national", terminal.symbol_value)

    def test_keyword_natural(self):
        """测试解析 NATURAL 关键字"""
        terminal = parse_one_token("NATURAL")
        self.assertEqual(TType.KEYWORD_NATURAL, terminal.symbol_id)
        self.assertEqual("NATURAL", terminal.symbol_value)

        terminal = parse_one_token("natural")
        self.assertEqual(TType.KEYWORD_NATURAL, terminal.symbol_id)
        self.assertEqual("natural", terminal.symbol_value)

    def test_keyword_nchar(self):
        """测试解析 NCHAR 关键字"""
        terminal = parse_one_token("NCHAR")
        self.assertEqual(TType.KEYWORD_NCHAR, terminal.symbol_id)
        self.assertEqual("NCHAR", terminal.symbol_value)

        terminal = parse_one_token("nchar")
        self.assertEqual(TType.KEYWORD_NCHAR, terminal.symbol_id)
        self.assertEqual("nchar", terminal.symbol_value)

    def test_keyword_ndb(self):
        """测试解析 NDB 关键字"""
        terminal = parse_one_token("NDB")
        self.assertEqual(TType.KEYWORD_NDB, terminal.symbol_id)
        self.assertEqual("NDB", terminal.symbol_value)

        terminal = parse_one_token("ndb")
        self.assertEqual(TType.KEYWORD_NDB, terminal.symbol_id)
        self.assertEqual("ndb", terminal.symbol_value)

    def test_keyword_ndbcluster(self):
        """测试解析 NDBCLUSTER 关键字"""
        terminal = parse_one_token("NDBCLUSTER")
        self.assertEqual(TType.KEYWORD_NDBCLUSTER, terminal.symbol_id)
        self.assertEqual("NDBCLUSTER", terminal.symbol_value)

        terminal = parse_one_token("ndbcluster")
        self.assertEqual(TType.KEYWORD_NDBCLUSTER, terminal.symbol_id)
        self.assertEqual("ndbcluster", terminal.symbol_value)

    def test_keyword_nested(self):
        """测试解析 NESTED 关键字"""
        terminal = parse_one_token("NESTED")
        self.assertEqual(TType.KEYWORD_NESTED, terminal.symbol_id)
        self.assertEqual("NESTED", terminal.symbol_value)

        terminal = parse_one_token("nested")
        self.assertEqual(TType.KEYWORD_NESTED, terminal.symbol_id)
        self.assertEqual("nested", terminal.symbol_value)

    def test_keyword_network_namespace(self):
        """测试解析 NETWORK_NAMESPACE 关键字"""
        terminal = parse_one_token("NETWORK_NAMESPACE")
        self.assertEqual(TType.KEYWORD_NETWORK_NAMESPACE, terminal.symbol_id)
        self.assertEqual("NETWORK_NAMESPACE", terminal.symbol_value)

        terminal = parse_one_token("network_namespace")
        self.assertEqual(TType.KEYWORD_NETWORK_NAMESPACE, terminal.symbol_id)
        self.assertEqual("network_namespace", terminal.symbol_value)

    def test_keyword_never(self):
        """测试解析 NEVER 关键字"""
        terminal = parse_one_token("NEVER")
        self.assertEqual(TType.KEYWORD_NEVER, terminal.symbol_id)
        self.assertEqual("NEVER", terminal.symbol_value)

        terminal = parse_one_token("never")
        self.assertEqual(TType.KEYWORD_NEVER, terminal.symbol_id)
        self.assertEqual("never", terminal.symbol_value)

    def test_keyword_new(self):
        """测试解析 NEW 关键字"""
        terminal = parse_one_token("NEW")
        self.assertEqual(TType.KEYWORD_NEW, terminal.symbol_id)
        self.assertEqual("NEW", terminal.symbol_value)

        terminal = parse_one_token("new")
        self.assertEqual(TType.KEYWORD_NEW, terminal.symbol_id)
        self.assertEqual("new", terminal.symbol_value)

    def test_keyword_next(self):
        """测试解析 NEXT 关键字"""
        terminal = parse_one_token("NEXT")
        self.assertEqual(TType.KEYWORD_NEXT, terminal.symbol_id)
        self.assertEqual("NEXT", terminal.symbol_value)

        terminal = parse_one_token("next")
        self.assertEqual(TType.KEYWORD_NEXT, terminal.symbol_id)
        self.assertEqual("next", terminal.symbol_value)

    def test_keyword_no(self):
        """测试解析 NO 关键字"""
        terminal = parse_one_token("NO")
        self.assertEqual(TType.KEYWORD_NO, terminal.symbol_id)
        self.assertEqual("NO", terminal.symbol_value)

        terminal = parse_one_token("no")
        self.assertEqual(TType.KEYWORD_NO, terminal.symbol_id)
        self.assertEqual("no", terminal.symbol_value)

    def test_keyword_nodegroup(self):
        """测试解析 NODEGROUP 关键字"""
        terminal = parse_one_token("NODEGROUP")
        self.assertEqual(TType.KEYWORD_NODEGROUP, terminal.symbol_id)
        self.assertEqual("NODEGROUP", terminal.symbol_value)

        terminal = parse_one_token("nodegroup")
        self.assertEqual(TType.KEYWORD_NODEGROUP, terminal.symbol_id)
        self.assertEqual("nodegroup", terminal.symbol_value)

    def test_keyword_none(self):
        """测试解析 NONE 关键字"""
        terminal = parse_one_token("NONE")
        self.assertEqual(TType.KEYWORD_NONE, terminal.symbol_id)
        self.assertEqual("NONE", terminal.symbol_value)

        terminal = parse_one_token("none")
        self.assertEqual(TType.KEYWORD_NONE, terminal.symbol_id)
        self.assertEqual("none", terminal.symbol_value)

    def test_keyword_not(self):
        """测试解析 NOT 关键字"""
        terminal = parse_one_token("NOT")
        self.assertEqual(TType.KEYWORD_NOT, terminal.symbol_id)
        self.assertEqual("NOT", terminal.symbol_value)

        terminal = parse_one_token("not")
        self.assertEqual(TType.KEYWORD_NOT, terminal.symbol_id)
        self.assertEqual("not", terminal.symbol_value)

    def test_keyword_not2(self):
        """测试解析 NOT2 关键字"""
        terminal = parse_one_token("NOT2")
        self.assertEqual(TType.KEYWORD_NOT2, terminal.symbol_id)
        self.assertEqual("NOT2", terminal.symbol_value)

        terminal = parse_one_token("not2")
        self.assertEqual(TType.KEYWORD_NOT2, terminal.symbol_id)
        self.assertEqual("not2", terminal.symbol_value)

    def test_keyword_nowait(self):
        """测试解析 NOWAIT 关键字"""
        terminal = parse_one_token("NOWAIT")
        self.assertEqual(TType.KEYWORD_NOWAIT, terminal.symbol_id)
        self.assertEqual("NOWAIT", terminal.symbol_value)

        terminal = parse_one_token("nowait")
        self.assertEqual(TType.KEYWORD_NOWAIT, terminal.symbol_id)
        self.assertEqual("nowait", terminal.symbol_value)

    def test_keyword_no_wait(self):
        """测试解析 NO_WAIT 关键字"""
        terminal = parse_one_token("NO_WAIT")
        self.assertEqual(TType.KEYWORD_NO_WAIT, terminal.symbol_id)
        self.assertEqual("NO_WAIT", terminal.symbol_value)

        terminal = parse_one_token("no_wait")
        self.assertEqual(TType.KEYWORD_NO_WAIT, terminal.symbol_id)
        self.assertEqual("no_wait", terminal.symbol_value)

    def test_keyword_no_write_to_binlog(self):
        """测试解析 NO_WRITE_TO_BINLOG 关键字"""
        terminal = parse_one_token("NO_WRITE_TO_BINLOG")
        self.assertEqual(TType.KEYWORD_NO_WRITE_TO_BINLOG, terminal.symbol_id)
        self.assertEqual("NO_WRITE_TO_BINLOG", terminal.symbol_value)

        terminal = parse_one_token("no_write_to_binlog")
        self.assertEqual(TType.KEYWORD_NO_WRITE_TO_BINLOG, terminal.symbol_id)
        self.assertEqual("no_write_to_binlog", terminal.symbol_value)

    def test_keyword_nth_value(self):
        """测试解析 NTH_VALUE 关键字"""
        terminal = parse_one_token("NTH_VALUE")
        self.assertEqual(TType.KEYWORD_NTH_VALUE, terminal.symbol_id)
        self.assertEqual("NTH_VALUE", terminal.symbol_value)

        terminal = parse_one_token("nth_value")
        self.assertEqual(TType.KEYWORD_NTH_VALUE, terminal.symbol_id)
        self.assertEqual("nth_value", terminal.symbol_value)

    def test_keyword_ntile(self):
        """测试解析 NTILE 关键字"""
        terminal = parse_one_token("NTILE")
        self.assertEqual(TType.KEYWORD_NTILE, terminal.symbol_id)
        self.assertEqual("NTILE", terminal.symbol_value)

        terminal = parse_one_token("ntile")
        self.assertEqual(TType.KEYWORD_NTILE, terminal.symbol_id)
        self.assertEqual("ntile", terminal.symbol_value)

    def test_keyword_null(self):
        """测试解析 NULL 关键字"""
        terminal = parse_one_token("NULL")
        self.assertEqual(TType.KEYWORD_NULL, terminal.symbol_id)
        self.assertEqual("NULL", terminal.symbol_value)

        terminal = parse_one_token("null")
        self.assertEqual(TType.KEYWORD_NULL, terminal.symbol_id)
        self.assertEqual("null", terminal.symbol_value)

    def test_keyword_nulls(self):
        """测试解析 NULLS 关键字"""
        terminal = parse_one_token("NULLS")
        self.assertEqual(TType.KEYWORD_NULLS, terminal.symbol_id)
        self.assertEqual("NULLS", terminal.symbol_value)

        terminal = parse_one_token("nulls")
        self.assertEqual(TType.KEYWORD_NULLS, terminal.symbol_id)
        self.assertEqual("nulls", terminal.symbol_value)

    def test_keyword_number(self):
        """测试解析 NUMBER 关键字"""
        terminal = parse_one_token("NUMBER")
        self.assertEqual(TType.KEYWORD_NUMBER, terminal.symbol_id)
        self.assertEqual("NUMBER", terminal.symbol_value)

        terminal = parse_one_token("number")
        self.assertEqual(TType.KEYWORD_NUMBER, terminal.symbol_id)
        self.assertEqual("number", terminal.symbol_value)

    def test_keyword_numeric(self):
        """测试解析 NUMERIC 关键字"""
        terminal = parse_one_token("NUMERIC")
        self.assertEqual(TType.KEYWORD_NUMERIC, terminal.symbol_id)
        self.assertEqual("NUMERIC", terminal.symbol_value)

        terminal = parse_one_token("numeric")
        self.assertEqual(TType.KEYWORD_NUMERIC, terminal.symbol_id)
        self.assertEqual("numeric", terminal.symbol_value)

    def test_keyword_nvarchar(self):
        """测试解析 NVARCHAR 关键字"""
        terminal = parse_one_token("NVARCHAR")
        self.assertEqual(TType.KEYWORD_NVARCHAR, terminal.symbol_id)
        self.assertEqual("NVARCHAR", terminal.symbol_value)

        terminal = parse_one_token("nvarchar")
        self.assertEqual(TType.KEYWORD_NVARCHAR, terminal.symbol_id)
        self.assertEqual("nvarchar", terminal.symbol_value)

    def test_keyword_of(self):
        """测试解析 OF 关键字"""
        terminal = parse_one_token("OF")
        self.assertEqual(TType.KEYWORD_OF, terminal.symbol_id)
        self.assertEqual("OF", terminal.symbol_value)

        terminal = parse_one_token("of")
        self.assertEqual(TType.KEYWORD_OF, terminal.symbol_id)
        self.assertEqual("of", terminal.symbol_value)

    def test_keyword_off(self):
        """测试解析 OFF 关键字"""
        terminal = parse_one_token("OFF")
        self.assertEqual(TType.KEYWORD_OFF, terminal.symbol_id)
        self.assertEqual("OFF", terminal.symbol_value)

        terminal = parse_one_token("off")
        self.assertEqual(TType.KEYWORD_OFF, terminal.symbol_id)
        self.assertEqual("off", terminal.symbol_value)

    def test_keyword_offset(self):
        """测试解析 OFFSET 关键字"""
        terminal = parse_one_token("OFFSET")
        self.assertEqual(TType.KEYWORD_OFFSET, terminal.symbol_id)
        self.assertEqual("OFFSET", terminal.symbol_value)

        terminal = parse_one_token("offset")
        self.assertEqual(TType.KEYWORD_OFFSET, terminal.symbol_id)
        self.assertEqual("offset", terminal.symbol_value)

    def test_keyword_oj(self):
        """测试解析 OJ 关键字"""
        terminal = parse_one_token("OJ")
        self.assertEqual(TType.KEYWORD_OJ, terminal.symbol_id)
        self.assertEqual("OJ", terminal.symbol_value)

        terminal = parse_one_token("oj")
        self.assertEqual(TType.KEYWORD_OJ, terminal.symbol_id)
        self.assertEqual("oj", terminal.symbol_value)

    def test_keyword_old(self):
        """测试解析 OLD 关键字"""
        terminal = parse_one_token("OLD")
        self.assertEqual(TType.KEYWORD_OLD, terminal.symbol_id)
        self.assertEqual("OLD", terminal.symbol_value)

        terminal = parse_one_token("old")
        self.assertEqual(TType.KEYWORD_OLD, terminal.symbol_id)
        self.assertEqual("old", terminal.symbol_value)

    def test_keyword_on(self):
        """测试解析 ON 关键字"""
        terminal = parse_one_token("ON")
        self.assertEqual(TType.KEYWORD_ON, terminal.symbol_id)
        self.assertEqual("ON", terminal.symbol_value)

        terminal = parse_one_token("on")
        self.assertEqual(TType.KEYWORD_ON, terminal.symbol_id)
        self.assertEqual("on", terminal.symbol_value)

    def test_keyword_one(self):
        """测试解析 ONE 关键字"""
        terminal = parse_one_token("ONE")
        self.assertEqual(TType.KEYWORD_ONE, terminal.symbol_id)
        self.assertEqual("ONE", terminal.symbol_value)

        terminal = parse_one_token("one")
        self.assertEqual(TType.KEYWORD_ONE, terminal.symbol_id)
        self.assertEqual("one", terminal.symbol_value)

    def test_keyword_only(self):
        """测试解析 ONLY 关键字"""
        terminal = parse_one_token("ONLY")
        self.assertEqual(TType.KEYWORD_ONLY, terminal.symbol_id)
        self.assertEqual("ONLY", terminal.symbol_value)

        terminal = parse_one_token("only")
        self.assertEqual(TType.KEYWORD_ONLY, terminal.symbol_id)
        self.assertEqual("only", terminal.symbol_value)

    def test_keyword_open(self):
        """测试解析 OPEN 关键字"""
        terminal = parse_one_token("OPEN")
        self.assertEqual(TType.KEYWORD_OPEN, terminal.symbol_id)
        self.assertEqual("OPEN", terminal.symbol_value)

        terminal = parse_one_token("open")
        self.assertEqual(TType.KEYWORD_OPEN, terminal.symbol_id)
        self.assertEqual("open", terminal.symbol_value)

    def test_keyword_optimize(self):
        """测试解析 OPTIMIZE 关键字"""
        terminal = parse_one_token("OPTIMIZE")
        self.assertEqual(TType.KEYWORD_OPTIMIZE, terminal.symbol_id)
        self.assertEqual("OPTIMIZE", terminal.symbol_value)

        terminal = parse_one_token("optimize")
        self.assertEqual(TType.KEYWORD_OPTIMIZE, terminal.symbol_id)
        self.assertEqual("optimize", terminal.symbol_value)

    def test_keyword_optimizer_costs(self):
        """测试解析 OPTIMIZER_COSTS 关键字"""
        terminal = parse_one_token("OPTIMIZER_COSTS")
        self.assertEqual(TType.KEYWORD_OPTIMIZER_COSTS, terminal.symbol_id)
        self.assertEqual("OPTIMIZER_COSTS", terminal.symbol_value)

        terminal = parse_one_token("optimizer_costs")
        self.assertEqual(TType.KEYWORD_OPTIMIZER_COSTS, terminal.symbol_id)
        self.assertEqual("optimizer_costs", terminal.symbol_value)

    def test_keyword_option(self):
        """测试解析 OPTION 关键字"""
        terminal = parse_one_token("OPTION")
        self.assertEqual(TType.KEYWORD_OPTION, terminal.symbol_id)
        self.assertEqual("OPTION", terminal.symbol_value)

        terminal = parse_one_token("option")
        self.assertEqual(TType.KEYWORD_OPTION, terminal.symbol_id)
        self.assertEqual("option", terminal.symbol_value)

    def test_keyword_optional(self):
        """测试解析 OPTIONAL 关键字"""
        terminal = parse_one_token("OPTIONAL")
        self.assertEqual(TType.KEYWORD_OPTIONAL, terminal.symbol_id)
        self.assertEqual("OPTIONAL", terminal.symbol_value)

        terminal = parse_one_token("optional")
        self.assertEqual(TType.KEYWORD_OPTIONAL, terminal.symbol_id)
        self.assertEqual("optional", terminal.symbol_value)

    def test_keyword_optionally(self):
        """测试解析 OPTIONALLY 关键字"""
        terminal = parse_one_token("OPTIONALLY")
        self.assertEqual(TType.KEYWORD_OPTIONALLY, terminal.symbol_id)
        self.assertEqual("OPTIONALLY", terminal.symbol_value)

        terminal = parse_one_token("optionally")
        self.assertEqual(TType.KEYWORD_OPTIONALLY, terminal.symbol_id)
        self.assertEqual("optionally", terminal.symbol_value)

    def test_keyword_options(self):
        """测试解析 OPTIONS 关键字"""
        terminal = parse_one_token("OPTIONS")
        self.assertEqual(TType.KEYWORD_OPTIONS, terminal.symbol_id)
        self.assertEqual("OPTIONS", terminal.symbol_value)

        terminal = parse_one_token("options")
        self.assertEqual(TType.KEYWORD_OPTIONS, terminal.symbol_id)
        self.assertEqual("options", terminal.symbol_value)

    def test_keyword_or(self):
        """测试解析 OR 关键字"""
        terminal = parse_one_token("OR")
        self.assertEqual(TType.KEYWORD_OR, terminal.symbol_id)
        self.assertEqual("OR", terminal.symbol_value)

        terminal = parse_one_token("or")
        self.assertEqual(TType.KEYWORD_OR, terminal.symbol_id)
        self.assertEqual("or", terminal.symbol_value)

    def test_keyword_or2(self):
        """测试解析 OR2 关键字"""
        terminal = parse_one_token("OR2")
        self.assertEqual(TType.KEYWORD_OR2, terminal.symbol_id)
        self.assertEqual("OR2", terminal.symbol_value)

        terminal = parse_one_token("or2")
        self.assertEqual(TType.KEYWORD_OR2, terminal.symbol_id)
        self.assertEqual("or2", terminal.symbol_value)

    def test_keyword_order(self):
        """测试解析 ORDER 关键字"""
        terminal = parse_one_token("ORDER")
        self.assertEqual(TType.KEYWORD_ORDER, terminal.symbol_id)
        self.assertEqual("ORDER", terminal.symbol_value)

        terminal = parse_one_token("order")
        self.assertEqual(TType.KEYWORD_ORDER, terminal.symbol_id)
        self.assertEqual("order", terminal.symbol_value)

    def test_keyword_ordinality(self):
        """测试解析 ORDINALITY 关键字"""
        terminal = parse_one_token("ORDINALITY")
        self.assertEqual(TType.KEYWORD_ORDINALITY, terminal.symbol_id)
        self.assertEqual("ORDINALITY", terminal.symbol_value)

        terminal = parse_one_token("ordinality")
        self.assertEqual(TType.KEYWORD_ORDINALITY, terminal.symbol_id)
        self.assertEqual("ordinality", terminal.symbol_value)

    def test_keyword_organization(self):
        """测试解析 ORGANIZATION 关键字"""
        terminal = parse_one_token("ORGANIZATION")
        self.assertEqual(TType.KEYWORD_ORGANIZATION, terminal.symbol_id)
        self.assertEqual("ORGANIZATION", terminal.symbol_value)

        terminal = parse_one_token("organization")
        self.assertEqual(TType.KEYWORD_ORGANIZATION, terminal.symbol_id)
        self.assertEqual("organization", terminal.symbol_value)

    def test_keyword_others(self):
        """测试解析 OTHERS 关键字"""
        terminal = parse_one_token("OTHERS")
        self.assertEqual(TType.KEYWORD_OTHERS, terminal.symbol_id)
        self.assertEqual("OTHERS", terminal.symbol_value)

        terminal = parse_one_token("others")
        self.assertEqual(TType.KEYWORD_OTHERS, terminal.symbol_id)
        self.assertEqual("others", terminal.symbol_value)

    def test_keyword_out(self):
        """测试解析 OUT 关键字"""
        terminal = parse_one_token("OUT")
        self.assertEqual(TType.KEYWORD_OUT, terminal.symbol_id)
        self.assertEqual("OUT", terminal.symbol_value)

        terminal = parse_one_token("out")
        self.assertEqual(TType.KEYWORD_OUT, terminal.symbol_id)
        self.assertEqual("out", terminal.symbol_value)

    def test_keyword_outer(self):
        """测试解析 OUTER 关键字"""
        terminal = parse_one_token("OUTER")
        self.assertEqual(TType.KEYWORD_OUTER, terminal.symbol_id)
        self.assertEqual("OUTER", terminal.symbol_value)

        terminal = parse_one_token("outer")
        self.assertEqual(TType.KEYWORD_OUTER, terminal.symbol_id)
        self.assertEqual("outer", terminal.symbol_value)

    def test_keyword_outfile(self):
        """测试解析 OUTFILE 关键字"""
        terminal = parse_one_token("OUTFILE")
        self.assertEqual(TType.KEYWORD_OUTFILE, terminal.symbol_id)
        self.assertEqual("OUTFILE", terminal.symbol_value)

        terminal = parse_one_token("outfile")
        self.assertEqual(TType.KEYWORD_OUTFILE, terminal.symbol_id)
        self.assertEqual("outfile", terminal.symbol_value)

    def test_keyword_over(self):
        """测试解析 OVER 关键字"""
        terminal = parse_one_token("OVER")
        self.assertEqual(TType.KEYWORD_OVER, terminal.symbol_id)
        self.assertEqual("OVER", terminal.symbol_value)

        terminal = parse_one_token("over")
        self.assertEqual(TType.KEYWORD_OVER, terminal.symbol_id)
        self.assertEqual("over", terminal.symbol_value)

    def test_keyword_owner(self):
        """测试解析 OWNER 关键字"""
        terminal = parse_one_token("OWNER")
        self.assertEqual(TType.KEYWORD_OWNER, terminal.symbol_id)
        self.assertEqual("OWNER", terminal.symbol_value)

        terminal = parse_one_token("owner")
        self.assertEqual(TType.KEYWORD_OWNER, terminal.symbol_id)
        self.assertEqual("owner", terminal.symbol_value)

    def test_keyword_pack_keys(self):
        """测试解析 PACK_KEYS 关键字"""
        terminal = parse_one_token("PACK_KEYS")
        self.assertEqual(TType.KEYWORD_PACK_KEYS, terminal.symbol_id)
        self.assertEqual("PACK_KEYS", terminal.symbol_value)

        terminal = parse_one_token("pack_keys")
        self.assertEqual(TType.KEYWORD_PACK_KEYS, terminal.symbol_id)
        self.assertEqual("pack_keys", terminal.symbol_value)

    def test_keyword_page(self):
        """测试解析 PAGE 关键字"""
        terminal = parse_one_token("PAGE")
        self.assertEqual(TType.KEYWORD_PAGE, terminal.symbol_id)
        self.assertEqual("PAGE", terminal.symbol_value)

        terminal = parse_one_token("page")
        self.assertEqual(TType.KEYWORD_PAGE, terminal.symbol_id)
        self.assertEqual("page", terminal.symbol_value)

    def test_keyword_parallel(self):
        """测试解析 PARALLEL 关键字"""
        terminal = parse_one_token("PARALLEL")
        self.assertEqual(TType.KEYWORD_PARALLEL, terminal.symbol_id)
        self.assertEqual("PARALLEL", terminal.symbol_value)

        terminal = parse_one_token("parallel")
        self.assertEqual(TType.KEYWORD_PARALLEL, terminal.symbol_id)
        self.assertEqual("parallel", terminal.symbol_value)

    def test_keyword_parser(self):
        """测试解析 PARSER 关键字"""
        terminal = parse_one_token("PARSER")
        self.assertEqual(TType.KEYWORD_PARSER, terminal.symbol_id)
        self.assertEqual("PARSER", terminal.symbol_value)

        terminal = parse_one_token("parser")
        self.assertEqual(TType.KEYWORD_PARSER, terminal.symbol_id)
        self.assertEqual("parser", terminal.symbol_value)

    def test_keyword_parse_tree(self):
        """测试解析 PARSE_TREE 关键字"""
        terminal = parse_one_token("PARSE_TREE")
        self.assertEqual(TType.KEYWORD_PARSE_TREE, terminal.symbol_id)
        self.assertEqual("PARSE_TREE", terminal.symbol_value)

        terminal = parse_one_token("parse_tree")
        self.assertEqual(TType.KEYWORD_PARSE_TREE, terminal.symbol_id)
        self.assertEqual("parse_tree", terminal.symbol_value)

    def test_keyword_partial(self):
        """测试解析 PARTIAL 关键字"""
        terminal = parse_one_token("PARTIAL")
        self.assertEqual(TType.KEYWORD_PARTIAL, terminal.symbol_id)
        self.assertEqual("PARTIAL", terminal.symbol_value)

        terminal = parse_one_token("partial")
        self.assertEqual(TType.KEYWORD_PARTIAL, terminal.symbol_id)
        self.assertEqual("partial", terminal.symbol_value)

    def test_keyword_partition(self):
        """测试解析 PARTITION 关键字"""
        terminal = parse_one_token("PARTITION")
        self.assertEqual(TType.KEYWORD_PARTITION, terminal.symbol_id)
        self.assertEqual("PARTITION", terminal.symbol_value)

        terminal = parse_one_token("partition")
        self.assertEqual(TType.KEYWORD_PARTITION, terminal.symbol_id)
        self.assertEqual("partition", terminal.symbol_value)

    def test_keyword_partitioning(self):
        """测试解析 PARTITIONING 关键字"""
        terminal = parse_one_token("PARTITIONING")
        self.assertEqual(TType.KEYWORD_PARTITIONING, terminal.symbol_id)
        self.assertEqual("PARTITIONING", terminal.symbol_value)

        terminal = parse_one_token("partitioning")
        self.assertEqual(TType.KEYWORD_PARTITIONING, terminal.symbol_id)
        self.assertEqual("partitioning", terminal.symbol_value)

    def test_keyword_partitions(self):
        """测试解析 PARTITIONS 关键字"""
        terminal = parse_one_token("PARTITIONS")
        self.assertEqual(TType.KEYWORD_PARTITIONS, terminal.symbol_id)
        self.assertEqual("PARTITIONS", terminal.symbol_value)

        terminal = parse_one_token("partitions")
        self.assertEqual(TType.KEYWORD_PARTITIONS, terminal.symbol_id)
        self.assertEqual("partitions", terminal.symbol_value)

    def test_keyword_password(self):
        """测试解析 PASSWORD 关键字"""
        terminal = parse_one_token("PASSWORD")
        self.assertEqual(TType.KEYWORD_PASSWORD, terminal.symbol_id)
        self.assertEqual("PASSWORD", terminal.symbol_value)

        terminal = parse_one_token("password")
        self.assertEqual(TType.KEYWORD_PASSWORD, terminal.symbol_id)
        self.assertEqual("password", terminal.symbol_value)

    def test_keyword_password_lock_time(self):
        """测试解析 PASSWORD_LOCK_TIME 关键字"""
        terminal = parse_one_token("PASSWORD_LOCK_TIME")
        self.assertEqual(TType.KEYWORD_PASSWORD_LOCK_TIME, terminal.symbol_id)
        self.assertEqual("PASSWORD_LOCK_TIME", terminal.symbol_value)

        terminal = parse_one_token("password_lock_time")
        self.assertEqual(TType.KEYWORD_PASSWORD_LOCK_TIME, terminal.symbol_id)
        self.assertEqual("password_lock_time", terminal.symbol_value)

    def test_keyword_path(self):
        """测试解析 PATH 关键字"""
        terminal = parse_one_token("PATH")
        self.assertEqual(TType.KEYWORD_PATH, terminal.symbol_id)
        self.assertEqual("PATH", terminal.symbol_value)

        terminal = parse_one_token("path")
        self.assertEqual(TType.KEYWORD_PATH, terminal.symbol_id)
        self.assertEqual("path", terminal.symbol_value)

    def test_keyword_percent_rank(self):
        """测试解析 PERCENT_RANK 关键字"""
        terminal = parse_one_token("PERCENT_RANK")
        self.assertEqual(TType.KEYWORD_PERCENT_RANK, terminal.symbol_id)
        self.assertEqual("PERCENT_RANK", terminal.symbol_value)

        terminal = parse_one_token("percent_rank")
        self.assertEqual(TType.KEYWORD_PERCENT_RANK, terminal.symbol_id)
        self.assertEqual("percent_rank", terminal.symbol_value)

    def test_keyword_persist(self):
        """测试解析 PERSIST 关键字"""
        terminal = parse_one_token("PERSIST")
        self.assertEqual(TType.KEYWORD_PERSIST, terminal.symbol_id)
        self.assertEqual("PERSIST", terminal.symbol_value)

        terminal = parse_one_token("persist")
        self.assertEqual(TType.KEYWORD_PERSIST, terminal.symbol_id)
        self.assertEqual("persist", terminal.symbol_value)

    def test_keyword_persist_only(self):
        """测试解析 PERSIST_ONLY 关键字"""
        terminal = parse_one_token("PERSIST_ONLY")
        self.assertEqual(TType.KEYWORD_PERSIST_ONLY, terminal.symbol_id)
        self.assertEqual("PERSIST_ONLY", terminal.symbol_value)

        terminal = parse_one_token("persist_only")
        self.assertEqual(TType.KEYWORD_PERSIST_ONLY, terminal.symbol_id)
        self.assertEqual("persist_only", terminal.symbol_value)

    def test_keyword_phase(self):
        """测试解析 PHASE 关键字"""
        terminal = parse_one_token("PHASE")
        self.assertEqual(TType.KEYWORD_PHASE, terminal.symbol_id)
        self.assertEqual("PHASE", terminal.symbol_value)

        terminal = parse_one_token("phase")
        self.assertEqual(TType.KEYWORD_PHASE, terminal.symbol_id)
        self.assertEqual("phase", terminal.symbol_value)

    def test_keyword_plugin(self):
        """测试解析 PLUGIN 关键字"""
        terminal = parse_one_token("PLUGIN")
        self.assertEqual(TType.KEYWORD_PLUGIN, terminal.symbol_id)
        self.assertEqual("PLUGIN", terminal.symbol_value)

        terminal = parse_one_token("plugin")
        self.assertEqual(TType.KEYWORD_PLUGIN, terminal.symbol_id)
        self.assertEqual("plugin", terminal.symbol_value)

    def test_keyword_plugins(self):
        """测试解析 PLUGINS 关键字"""
        terminal = parse_one_token("PLUGINS")
        self.assertEqual(TType.KEYWORD_PLUGINS, terminal.symbol_id)
        self.assertEqual("PLUGINS", terminal.symbol_value)

        terminal = parse_one_token("plugins")
        self.assertEqual(TType.KEYWORD_PLUGINS, terminal.symbol_id)
        self.assertEqual("plugins", terminal.symbol_value)

    def test_keyword_plugin_dir(self):
        """测试解析 PLUGIN_DIR 关键字"""
        terminal = parse_one_token("PLUGIN_DIR")
        self.assertEqual(TType.KEYWORD_PLUGIN_DIR, terminal.symbol_id)
        self.assertEqual("PLUGIN_DIR", terminal.symbol_value)

        terminal = parse_one_token("plugin_dir")
        self.assertEqual(TType.KEYWORD_PLUGIN_DIR, terminal.symbol_id)
        self.assertEqual("plugin_dir", terminal.symbol_value)

    def test_keyword_point(self):
        """测试解析 POINT 关键字"""
        terminal = parse_one_token("POINT")
        self.assertEqual(TType.KEYWORD_POINT, terminal.symbol_id)
        self.assertEqual("POINT", terminal.symbol_value)

        terminal = parse_one_token("point")
        self.assertEqual(TType.KEYWORD_POINT, terminal.symbol_id)
        self.assertEqual("point", terminal.symbol_value)

    def test_keyword_polygon(self):
        """测试解析 POLYGON 关键字"""
        terminal = parse_one_token("POLYGON")
        self.assertEqual(TType.KEYWORD_POLYGON, terminal.symbol_id)
        self.assertEqual("POLYGON", terminal.symbol_value)

        terminal = parse_one_token("polygon")
        self.assertEqual(TType.KEYWORD_POLYGON, terminal.symbol_id)
        self.assertEqual("polygon", terminal.symbol_value)

    def test_keyword_port(self):
        """测试解析 PORT 关键字"""
        terminal = parse_one_token("PORT")
        self.assertEqual(TType.KEYWORD_PORT, terminal.symbol_id)
        self.assertEqual("PORT", terminal.symbol_value)

        terminal = parse_one_token("port")
        self.assertEqual(TType.KEYWORD_PORT, terminal.symbol_id)
        self.assertEqual("port", terminal.symbol_value)

    def test_keyword_precedes(self):
        """测试解析 PRECEDES 关键字"""
        terminal = parse_one_token("PRECEDES")
        self.assertEqual(TType.KEYWORD_PRECEDES, terminal.symbol_id)
        self.assertEqual("PRECEDES", terminal.symbol_value)

        terminal = parse_one_token("precedes")
        self.assertEqual(TType.KEYWORD_PRECEDES, terminal.symbol_id)
        self.assertEqual("precedes", terminal.symbol_value)

    def test_keyword_preceding(self):
        """测试解析 PRECEDING 关键字"""
        terminal = parse_one_token("PRECEDING")
        self.assertEqual(TType.KEYWORD_PRECEDING, terminal.symbol_id)
        self.assertEqual("PRECEDING", terminal.symbol_value)

        terminal = parse_one_token("preceding")
        self.assertEqual(TType.KEYWORD_PRECEDING, terminal.symbol_id)
        self.assertEqual("preceding", terminal.symbol_value)

    def test_keyword_precision(self):
        """测试解析 PRECISION 关键字"""
        terminal = parse_one_token("PRECISION")
        self.assertEqual(TType.KEYWORD_PRECISION, terminal.symbol_id)
        self.assertEqual("PRECISION", terminal.symbol_value)

        terminal = parse_one_token("precision")
        self.assertEqual(TType.KEYWORD_PRECISION, terminal.symbol_id)
        self.assertEqual("precision", terminal.symbol_value)

    def test_keyword_prepare(self):
        """测试解析 PREPARE 关键字"""
        terminal = parse_one_token("PREPARE")
        self.assertEqual(TType.KEYWORD_PREPARE, terminal.symbol_id)
        self.assertEqual("PREPARE", terminal.symbol_value)

        terminal = parse_one_token("prepare")
        self.assertEqual(TType.KEYWORD_PREPARE, terminal.symbol_id)
        self.assertEqual("prepare", terminal.symbol_value)

    def test_keyword_preserve(self):
        """测试解析 PRESERVE 关键字"""
        terminal = parse_one_token("PRESERVE")
        self.assertEqual(TType.KEYWORD_PRESERVE, terminal.symbol_id)
        self.assertEqual("PRESERVE", terminal.symbol_value)

        terminal = parse_one_token("preserve")
        self.assertEqual(TType.KEYWORD_PRESERVE, terminal.symbol_id)
        self.assertEqual("preserve", terminal.symbol_value)

    def test_keyword_prev(self):
        """测试解析 PREV 关键字"""
        terminal = parse_one_token("PREV")
        self.assertEqual(TType.KEYWORD_PREV, terminal.symbol_id)
        self.assertEqual("PREV", terminal.symbol_value)

        terminal = parse_one_token("prev")
        self.assertEqual(TType.KEYWORD_PREV, terminal.symbol_id)
        self.assertEqual("prev", terminal.symbol_value)

    def test_keyword_primary(self):
        """测试解析 PRIMARY 关键字"""
        terminal = parse_one_token("PRIMARY")
        self.assertEqual(TType.KEYWORD_PRIMARY, terminal.symbol_id)
        self.assertEqual("PRIMARY", terminal.symbol_value)

        terminal = parse_one_token("primary")
        self.assertEqual(TType.KEYWORD_PRIMARY, terminal.symbol_id)
        self.assertEqual("primary", terminal.symbol_value)

    def test_keyword_privileges(self):
        """测试解析 PRIVILEGES 关键字"""
        terminal = parse_one_token("PRIVILEGES")
        self.assertEqual(TType.KEYWORD_PRIVILEGES, terminal.symbol_id)
        self.assertEqual("PRIVILEGES", terminal.symbol_value)

        terminal = parse_one_token("privileges")
        self.assertEqual(TType.KEYWORD_PRIVILEGES, terminal.symbol_id)
        self.assertEqual("privileges", terminal.symbol_value)

    def test_keyword_privilege_checks_user(self):
        """测试解析 PRIVILEGE_CHECKS_USER 关键字"""
        terminal = parse_one_token("PRIVILEGE_CHECKS_USER")
        self.assertEqual(TType.KEYWORD_PRIVILEGE_CHECKS_USER, terminal.symbol_id)
        self.assertEqual("PRIVILEGE_CHECKS_USER", terminal.symbol_value)

        terminal = parse_one_token("privilege_checks_user")
        self.assertEqual(TType.KEYWORD_PRIVILEGE_CHECKS_USER, terminal.symbol_id)
        self.assertEqual("privilege_checks_user", terminal.symbol_value)

    def test_keyword_procedure(self):
        """测试解析 PROCEDURE 关键字"""
        terminal = parse_one_token("PROCEDURE")
        self.assertEqual(TType.KEYWORD_PROCEDURE, terminal.symbol_id)
        self.assertEqual("PROCEDURE", terminal.symbol_value)

        terminal = parse_one_token("procedure")
        self.assertEqual(TType.KEYWORD_PROCEDURE, terminal.symbol_id)
        self.assertEqual("procedure", terminal.symbol_value)

    def test_keyword_process(self):
        """测试解析 PROCESS 关键字"""
        terminal = parse_one_token("PROCESS")
        self.assertEqual(TType.KEYWORD_PROCESS, terminal.symbol_id)
        self.assertEqual("PROCESS", terminal.symbol_value)

        terminal = parse_one_token("process")
        self.assertEqual(TType.KEYWORD_PROCESS, terminal.symbol_id)
        self.assertEqual("process", terminal.symbol_value)

    def test_keyword_processlist(self):
        """测试解析 PROCESSLIST 关键字"""
        terminal = parse_one_token("PROCESSLIST")
        self.assertEqual(TType.KEYWORD_PROCESSLIST, terminal.symbol_id)
        self.assertEqual("PROCESSLIST", terminal.symbol_value)

        terminal = parse_one_token("processlist")
        self.assertEqual(TType.KEYWORD_PROCESSLIST, terminal.symbol_id)
        self.assertEqual("processlist", terminal.symbol_value)

    def test_keyword_profile(self):
        """测试解析 PROFILE 关键字"""
        terminal = parse_one_token("PROFILE")
        self.assertEqual(TType.KEYWORD_PROFILE, terminal.symbol_id)
        self.assertEqual("PROFILE", terminal.symbol_value)

        terminal = parse_one_token("profile")
        self.assertEqual(TType.KEYWORD_PROFILE, terminal.symbol_id)
        self.assertEqual("profile", terminal.symbol_value)

    def test_keyword_profiles(self):
        """测试解析 PROFILES 关键字"""
        terminal = parse_one_token("PROFILES")
        self.assertEqual(TType.KEYWORD_PROFILES, terminal.symbol_id)
        self.assertEqual("PROFILES", terminal.symbol_value)

        terminal = parse_one_token("profiles")
        self.assertEqual(TType.KEYWORD_PROFILES, terminal.symbol_id)
        self.assertEqual("profiles", terminal.symbol_value)

    def test_keyword_proxy(self):
        """测试解析 PROXY 关键字"""
        terminal = parse_one_token("PROXY")
        self.assertEqual(TType.KEYWORD_PROXY, terminal.symbol_id)
        self.assertEqual("PROXY", terminal.symbol_value)

        terminal = parse_one_token("proxy")
        self.assertEqual(TType.KEYWORD_PROXY, terminal.symbol_id)
        self.assertEqual("proxy", terminal.symbol_value)

    def test_keyword_purge(self):
        """测试解析 PURGE 关键字"""
        terminal = parse_one_token("PURGE")
        self.assertEqual(TType.KEYWORD_PURGE, terminal.symbol_id)
        self.assertEqual("PURGE", terminal.symbol_value)

        terminal = parse_one_token("purge")
        self.assertEqual(TType.KEYWORD_PURGE, terminal.symbol_id)
        self.assertEqual("purge", terminal.symbol_value)

    def test_keyword_qualify(self):
        """测试解析 QUALIFY 关键字"""
        terminal = parse_one_token("QUALIFY")
        self.assertEqual(TType.KEYWORD_QUALIFY, terminal.symbol_id)
        self.assertEqual("QUALIFY", terminal.symbol_value)

        terminal = parse_one_token("qualify")
        self.assertEqual(TType.KEYWORD_QUALIFY, terminal.symbol_id)
        self.assertEqual("qualify", terminal.symbol_value)

    def test_keyword_quarter(self):
        """测试解析 QUARTER 关键字"""
        terminal = parse_one_token("QUARTER")
        self.assertEqual(TType.KEYWORD_QUARTER, terminal.symbol_id)
        self.assertEqual("QUARTER", terminal.symbol_value)

        terminal = parse_one_token("quarter")
        self.assertEqual(TType.KEYWORD_QUARTER, terminal.symbol_id)
        self.assertEqual("quarter", terminal.symbol_value)

    def test_keyword_query(self):
        """测试解析 QUERY 关键字"""
        terminal = parse_one_token("QUERY")
        self.assertEqual(TType.KEYWORD_QUERY, terminal.symbol_id)
        self.assertEqual("QUERY", terminal.symbol_value)

        terminal = parse_one_token("query")
        self.assertEqual(TType.KEYWORD_QUERY, terminal.symbol_id)
        self.assertEqual("query", terminal.symbol_value)

    def test_keyword_quick(self):
        """测试解析 QUICK 关键字"""
        terminal = parse_one_token("QUICK")
        self.assertEqual(TType.KEYWORD_QUICK, terminal.symbol_id)
        self.assertEqual("QUICK", terminal.symbol_value)

        terminal = parse_one_token("quick")
        self.assertEqual(TType.KEYWORD_QUICK, terminal.symbol_id)
        self.assertEqual("quick", terminal.symbol_value)

    def test_keyword_random(self):
        """测试解析 RANDOM 关键字"""
        terminal = parse_one_token("RANDOM")
        self.assertEqual(TType.KEYWORD_RANDOM, terminal.symbol_id)
        self.assertEqual("RANDOM", terminal.symbol_value)

        terminal = parse_one_token("random")
        self.assertEqual(TType.KEYWORD_RANDOM, terminal.symbol_id)
        self.assertEqual("random", terminal.symbol_value)

    def test_keyword_range(self):
        """测试解析 RANGE 关键字"""
        terminal = parse_one_token("RANGE")
        self.assertEqual(TType.KEYWORD_RANGE, terminal.symbol_id)
        self.assertEqual("RANGE", terminal.symbol_value)

        terminal = parse_one_token("range")
        self.assertEqual(TType.KEYWORD_RANGE, terminal.symbol_id)
        self.assertEqual("range", terminal.symbol_value)

    def test_keyword_rank(self):
        """测试解析 RANK 关键字"""
        terminal = parse_one_token("RANK")
        self.assertEqual(TType.KEYWORD_RANK, terminal.symbol_id)
        self.assertEqual("RANK", terminal.symbol_value)

        terminal = parse_one_token("rank")
        self.assertEqual(TType.KEYWORD_RANK, terminal.symbol_id)
        self.assertEqual("rank", terminal.symbol_value)

    def test_keyword_read(self):
        """测试解析 READ 关键字"""
        terminal = parse_one_token("READ")
        self.assertEqual(TType.KEYWORD_READ, terminal.symbol_id)
        self.assertEqual("READ", terminal.symbol_value)

        terminal = parse_one_token("read")
        self.assertEqual(TType.KEYWORD_READ, terminal.symbol_id)
        self.assertEqual("read", terminal.symbol_value)

    def test_keyword_reads(self):
        """测试解析 READS 关键字"""
        terminal = parse_one_token("READS")
        self.assertEqual(TType.KEYWORD_READS, terminal.symbol_id)
        self.assertEqual("READS", terminal.symbol_value)

        terminal = parse_one_token("reads")
        self.assertEqual(TType.KEYWORD_READS, terminal.symbol_id)
        self.assertEqual("reads", terminal.symbol_value)

    def test_keyword_read_only(self):
        """测试解析 READ_ONLY 关键字"""
        terminal = parse_one_token("READ_ONLY")
        self.assertEqual(TType.KEYWORD_READ_ONLY, terminal.symbol_id)
        self.assertEqual("READ_ONLY", terminal.symbol_value)

        terminal = parse_one_token("read_only")
        self.assertEqual(TType.KEYWORD_READ_ONLY, terminal.symbol_id)
        self.assertEqual("read_only", terminal.symbol_value)

    def test_keyword_read_write(self):
        """测试解析 READ_WRITE 关键字"""
        terminal = parse_one_token("READ_WRITE")
        self.assertEqual(TType.KEYWORD_READ_WRITE, terminal.symbol_id)
        self.assertEqual("READ_WRITE", terminal.symbol_value)

        terminal = parse_one_token("read_write")
        self.assertEqual(TType.KEYWORD_READ_WRITE, terminal.symbol_id)
        self.assertEqual("read_write", terminal.symbol_value)

    def test_keyword_real(self):
        """测试解析 REAL 关键字"""
        terminal = parse_one_token("REAL")
        self.assertEqual(TType.KEYWORD_REAL, terminal.symbol_id)
        self.assertEqual("REAL", terminal.symbol_value)

        terminal = parse_one_token("real")
        self.assertEqual(TType.KEYWORD_REAL, terminal.symbol_id)
        self.assertEqual("real", terminal.symbol_value)

    def test_keyword_rebuild(self):
        """测试解析 REBUILD 关键字"""
        terminal = parse_one_token("REBUILD")
        self.assertEqual(TType.KEYWORD_REBUILD, terminal.symbol_id)
        self.assertEqual("REBUILD", terminal.symbol_value)

        terminal = parse_one_token("rebuild")
        self.assertEqual(TType.KEYWORD_REBUILD, terminal.symbol_id)
        self.assertEqual("rebuild", terminal.symbol_value)

    def test_keyword_recover(self):
        """测试解析 RECOVER 关键字"""
        terminal = parse_one_token("RECOVER")
        self.assertEqual(TType.KEYWORD_RECOVER, terminal.symbol_id)
        self.assertEqual("RECOVER", terminal.symbol_value)

        terminal = parse_one_token("recover")
        self.assertEqual(TType.KEYWORD_RECOVER, terminal.symbol_id)
        self.assertEqual("recover", terminal.symbol_value)

    def test_keyword_recursive(self):
        """测试解析 RECURSIVE 关键字"""
        terminal = parse_one_token("RECURSIVE")
        self.assertEqual(TType.KEYWORD_RECURSIVE, terminal.symbol_id)
        self.assertEqual("RECURSIVE", terminal.symbol_value)

        terminal = parse_one_token("recursive")
        self.assertEqual(TType.KEYWORD_RECURSIVE, terminal.symbol_id)
        self.assertEqual("recursive", terminal.symbol_value)

    def test_keyword_redo_buffer_size(self):
        """测试解析 REDO_BUFFER_SIZE 关键字"""
        terminal = parse_one_token("REDO_BUFFER_SIZE")
        self.assertEqual(TType.KEYWORD_REDO_BUFFER_SIZE, terminal.symbol_id)
        self.assertEqual("REDO_BUFFER_SIZE", terminal.symbol_value)

        terminal = parse_one_token("redo_buffer_size")
        self.assertEqual(TType.KEYWORD_REDO_BUFFER_SIZE, terminal.symbol_id)
        self.assertEqual("redo_buffer_size", terminal.symbol_value)

    def test_keyword_redundant(self):
        """测试解析 REDUNDANT 关键字"""
        terminal = parse_one_token("REDUNDANT")
        self.assertEqual(TType.KEYWORD_REDUNDANT, terminal.symbol_id)
        self.assertEqual("REDUNDANT", terminal.symbol_value)

        terminal = parse_one_token("redundant")
        self.assertEqual(TType.KEYWORD_REDUNDANT, terminal.symbol_id)
        self.assertEqual("redundant", terminal.symbol_value)

    def test_keyword_reference(self):
        """测试解析 REFERENCE 关键字"""
        terminal = parse_one_token("REFERENCE")
        self.assertEqual(TType.KEYWORD_REFERENCE, terminal.symbol_id)
        self.assertEqual("REFERENCE", terminal.symbol_value)

        terminal = parse_one_token("reference")
        self.assertEqual(TType.KEYWORD_REFERENCE, terminal.symbol_id)
        self.assertEqual("reference", terminal.symbol_value)

    def test_keyword_references(self):
        """测试解析 REFERENCES 关键字"""
        terminal = parse_one_token("REFERENCES")
        self.assertEqual(TType.KEYWORD_REFERENCES, terminal.symbol_id)
        self.assertEqual("REFERENCES", terminal.symbol_value)

        terminal = parse_one_token("references")
        self.assertEqual(TType.KEYWORD_REFERENCES, terminal.symbol_id)
        self.assertEqual("references", terminal.symbol_value)

    def test_keyword_regexp(self):
        """测试解析 REGEXP 关键字"""
        terminal = parse_one_token("REGEXP")
        self.assertEqual(TType.KEYWORD_REGEXP, terminal.symbol_id)
        self.assertEqual("REGEXP", terminal.symbol_value)

        terminal = parse_one_token("regexp")
        self.assertEqual(TType.KEYWORD_REGEXP, terminal.symbol_id)
        self.assertEqual("regexp", terminal.symbol_value)

    def test_keyword_registration(self):
        """测试解析 REGISTRATION 关键字"""
        terminal = parse_one_token("REGISTRATION")
        self.assertEqual(TType.KEYWORD_REGISTRATION, terminal.symbol_id)
        self.assertEqual("REGISTRATION", terminal.symbol_value)

        terminal = parse_one_token("registration")
        self.assertEqual(TType.KEYWORD_REGISTRATION, terminal.symbol_id)
        self.assertEqual("registration", terminal.symbol_value)

    def test_keyword_relay(self):
        """测试解析 RELAY 关键字"""
        terminal = parse_one_token("RELAY")
        self.assertEqual(TType.KEYWORD_RELAY, terminal.symbol_id)
        self.assertEqual("RELAY", terminal.symbol_value)

        terminal = parse_one_token("relay")
        self.assertEqual(TType.KEYWORD_RELAY, terminal.symbol_id)
        self.assertEqual("relay", terminal.symbol_value)

    def test_keyword_relaylog(self):
        """测试解析 RELAYLOG 关键字"""
        terminal = parse_one_token("RELAYLOG")
        self.assertEqual(TType.KEYWORD_RELAYLOG, terminal.symbol_id)
        self.assertEqual("RELAYLOG", terminal.symbol_value)

        terminal = parse_one_token("relaylog")
        self.assertEqual(TType.KEYWORD_RELAYLOG, terminal.symbol_id)
        self.assertEqual("relaylog", terminal.symbol_value)

    def test_keyword_relay_log_file(self):
        """测试解析 RELAY_LOG_FILE 关键字"""
        terminal = parse_one_token("RELAY_LOG_FILE")
        self.assertEqual(TType.KEYWORD_RELAY_LOG_FILE, terminal.symbol_id)
        self.assertEqual("RELAY_LOG_FILE", terminal.symbol_value)

        terminal = parse_one_token("relay_log_file")
        self.assertEqual(TType.KEYWORD_RELAY_LOG_FILE, terminal.symbol_id)
        self.assertEqual("relay_log_file", terminal.symbol_value)

    def test_keyword_relay_log_pos(self):
        """测试解析 RELAY_LOG_POS 关键字"""
        terminal = parse_one_token("RELAY_LOG_POS")
        self.assertEqual(TType.KEYWORD_RELAY_LOG_POS, terminal.symbol_id)
        self.assertEqual("RELAY_LOG_POS", terminal.symbol_value)

        terminal = parse_one_token("relay_log_pos")
        self.assertEqual(TType.KEYWORD_RELAY_LOG_POS, terminal.symbol_id)
        self.assertEqual("relay_log_pos", terminal.symbol_value)

    def test_keyword_relay_thread(self):
        """测试解析 RELAY_THREAD 关键字"""
        terminal = parse_one_token("RELAY_THREAD")
        self.assertEqual(TType.KEYWORD_RELAY_THREAD, terminal.symbol_id)
        self.assertEqual("RELAY_THREAD", terminal.symbol_value)

        terminal = parse_one_token("relay_thread")
        self.assertEqual(TType.KEYWORD_RELAY_THREAD, terminal.symbol_id)
        self.assertEqual("relay_thread", terminal.symbol_value)

    def test_keyword_release(self):
        """测试解析 RELEASE 关键字"""
        terminal = parse_one_token("RELEASE")
        self.assertEqual(TType.KEYWORD_RELEASE, terminal.symbol_id)
        self.assertEqual("RELEASE", terminal.symbol_value)

        terminal = parse_one_token("release")
        self.assertEqual(TType.KEYWORD_RELEASE, terminal.symbol_id)
        self.assertEqual("release", terminal.symbol_value)

    def test_keyword_reload(self):
        """测试解析 RELOAD 关键字"""
        terminal = parse_one_token("RELOAD")
        self.assertEqual(TType.KEYWORD_RELOAD, terminal.symbol_id)
        self.assertEqual("RELOAD", terminal.symbol_value)

        terminal = parse_one_token("reload")
        self.assertEqual(TType.KEYWORD_RELOAD, terminal.symbol_id)
        self.assertEqual("reload", terminal.symbol_value)

    def test_keyword_remove(self):
        """测试解析 REMOVE 关键字"""
        terminal = parse_one_token("REMOVE")
        self.assertEqual(TType.KEYWORD_REMOVE, terminal.symbol_id)
        self.assertEqual("REMOVE", terminal.symbol_value)

        terminal = parse_one_token("remove")
        self.assertEqual(TType.KEYWORD_REMOVE, terminal.symbol_id)
        self.assertEqual("remove", terminal.symbol_value)

    def test_keyword_rename(self):
        """测试解析 RENAME 关键字"""
        terminal = parse_one_token("RENAME")
        self.assertEqual(TType.KEYWORD_RENAME, terminal.symbol_id)
        self.assertEqual("RENAME", terminal.symbol_value)

        terminal = parse_one_token("rename")
        self.assertEqual(TType.KEYWORD_RENAME, terminal.symbol_id)
        self.assertEqual("rename", terminal.symbol_value)

    def test_keyword_reorganize(self):
        """测试解析 REORGANIZE 关键字"""
        terminal = parse_one_token("REORGANIZE")
        self.assertEqual(TType.KEYWORD_REORGANIZE, terminal.symbol_id)
        self.assertEqual("REORGANIZE", terminal.symbol_value)

        terminal = parse_one_token("reorganize")
        self.assertEqual(TType.KEYWORD_REORGANIZE, terminal.symbol_id)
        self.assertEqual("reorganize", terminal.symbol_value)

    def test_keyword_repair(self):
        """测试解析 REPAIR 关键字"""
        terminal = parse_one_token("REPAIR")
        self.assertEqual(TType.KEYWORD_REPAIR, terminal.symbol_id)
        self.assertEqual("REPAIR", terminal.symbol_value)

        terminal = parse_one_token("repair")
        self.assertEqual(TType.KEYWORD_REPAIR, terminal.symbol_id)
        self.assertEqual("repair", terminal.symbol_value)

    def test_keyword_repeat(self):
        """测试解析 REPEAT 关键字"""
        terminal = parse_one_token("REPEAT")
        self.assertEqual(TType.KEYWORD_REPEAT, terminal.symbol_id)
        self.assertEqual("REPEAT", terminal.symbol_value)

        terminal = parse_one_token("repeat")
        self.assertEqual(TType.KEYWORD_REPEAT, terminal.symbol_id)
        self.assertEqual("repeat", terminal.symbol_value)

    def test_keyword_repeatable(self):
        """测试解析 REPEATABLE 关键字"""
        terminal = parse_one_token("REPEATABLE")
        self.assertEqual(TType.KEYWORD_REPEATABLE, terminal.symbol_id)
        self.assertEqual("REPEATABLE", terminal.symbol_value)

        terminal = parse_one_token("repeatable")
        self.assertEqual(TType.KEYWORD_REPEATABLE, terminal.symbol_id)
        self.assertEqual("repeatable", terminal.symbol_value)

    def test_keyword_replace(self):
        """测试解析 REPLACE 关键字"""
        terminal = parse_one_token("REPLACE")
        self.assertEqual(TType.KEYWORD_REPLACE, terminal.symbol_id)
        self.assertEqual("REPLACE", terminal.symbol_value)

        terminal = parse_one_token("replace")
        self.assertEqual(TType.KEYWORD_REPLACE, terminal.symbol_id)
        self.assertEqual("replace", terminal.symbol_value)

    def test_keyword_replica(self):
        """测试解析 REPLICA 关键字"""
        terminal = parse_one_token("REPLICA")
        self.assertEqual(TType.KEYWORD_REPLICA, terminal.symbol_id)
        self.assertEqual("REPLICA", terminal.symbol_value)

        terminal = parse_one_token("replica")
        self.assertEqual(TType.KEYWORD_REPLICA, terminal.symbol_id)
        self.assertEqual("replica", terminal.symbol_value)

    def test_keyword_replicas(self):
        """测试解析 REPLICAS 关键字"""
        terminal = parse_one_token("REPLICAS")
        self.assertEqual(TType.KEYWORD_REPLICAS, terminal.symbol_id)
        self.assertEqual("REPLICAS", terminal.symbol_value)

        terminal = parse_one_token("replicas")
        self.assertEqual(TType.KEYWORD_REPLICAS, terminal.symbol_id)
        self.assertEqual("replicas", terminal.symbol_value)

    def test_keyword_replicate_do_db(self):
        """测试解析 REPLICATE_DO_DB 关键字"""
        terminal = parse_one_token("REPLICATE_DO_DB")
        self.assertEqual(TType.KEYWORD_REPLICATE_DO_DB, terminal.symbol_id)
        self.assertEqual("REPLICATE_DO_DB", terminal.symbol_value)

        terminal = parse_one_token("replicate_do_db")
        self.assertEqual(TType.KEYWORD_REPLICATE_DO_DB, terminal.symbol_id)
        self.assertEqual("replicate_do_db", terminal.symbol_value)

    def test_keyword_replicate_do_table(self):
        """测试解析 REPLICATE_DO_TABLE 关键字"""
        terminal = parse_one_token("REPLICATE_DO_TABLE")
        self.assertEqual(TType.KEYWORD_REPLICATE_DO_TABLE, terminal.symbol_id)
        self.assertEqual("REPLICATE_DO_TABLE", terminal.symbol_value)

        terminal = parse_one_token("replicate_do_table")
        self.assertEqual(TType.KEYWORD_REPLICATE_DO_TABLE, terminal.symbol_id)
        self.assertEqual("replicate_do_table", terminal.symbol_value)

    def test_keyword_replicate_ignore_db(self):
        """测试解析 REPLICATE_IGNORE_DB 关键字"""
        terminal = parse_one_token("REPLICATE_IGNORE_DB")
        self.assertEqual(TType.KEYWORD_REPLICATE_IGNORE_DB, terminal.symbol_id)
        self.assertEqual("REPLICATE_IGNORE_DB", terminal.symbol_value)

        terminal = parse_one_token("replicate_ignore_db")
        self.assertEqual(TType.KEYWORD_REPLICATE_IGNORE_DB, terminal.symbol_id)
        self.assertEqual("replicate_ignore_db", terminal.symbol_value)

    def test_keyword_replicate_ignore_table(self):
        """测试解析 REPLICATE_IGNORE_TABLE 关键字"""
        terminal = parse_one_token("REPLICATE_IGNORE_TABLE")
        self.assertEqual(TType.KEYWORD_REPLICATE_IGNORE_TABLE, terminal.symbol_id)
        self.assertEqual("REPLICATE_IGNORE_TABLE", terminal.symbol_value)

        terminal = parse_one_token("replicate_ignore_table")
        self.assertEqual(TType.KEYWORD_REPLICATE_IGNORE_TABLE, terminal.symbol_id)
        self.assertEqual("replicate_ignore_table", terminal.symbol_value)

    def test_keyword_replicate_rewrite_db(self):
        """测试解析 REPLICATE_REWRITE_DB 关键字"""
        terminal = parse_one_token("REPLICATE_REWRITE_DB")
        self.assertEqual(TType.KEYWORD_REPLICATE_REWRITE_DB, terminal.symbol_id)
        self.assertEqual("REPLICATE_REWRITE_DB", terminal.symbol_value)

        terminal = parse_one_token("replicate_rewrite_db")
        self.assertEqual(TType.KEYWORD_REPLICATE_REWRITE_DB, terminal.symbol_id)
        self.assertEqual("replicate_rewrite_db", terminal.symbol_value)

    def test_keyword_replicate_wild_do_table(self):
        """测试解析 REPLICATE_WILD_DO_TABLE 关键字"""
        terminal = parse_one_token("REPLICATE_WILD_DO_TABLE")
        self.assertEqual(TType.KEYWORD_REPLICATE_WILD_DO_TABLE, terminal.symbol_id)
        self.assertEqual("REPLICATE_WILD_DO_TABLE", terminal.symbol_value)

        terminal = parse_one_token("replicate_wild_do_table")
        self.assertEqual(TType.KEYWORD_REPLICATE_WILD_DO_TABLE, terminal.symbol_id)
        self.assertEqual("replicate_wild_do_table", terminal.symbol_value)

    def test_keyword_replicate_wild_ignore_table(self):
        """测试解析 REPLICATE_WILD_IGNORE_TABLE 关键字"""
        terminal = parse_one_token("REPLICATE_WILD_IGNORE_TABLE")
        self.assertEqual(TType.KEYWORD_REPLICATE_WILD_IGNORE_TABLE, terminal.symbol_id)
        self.assertEqual("REPLICATE_WILD_IGNORE_TABLE", terminal.symbol_value)

        terminal = parse_one_token("replicate_wild_ignore_table")
        self.assertEqual(TType.KEYWORD_REPLICATE_WILD_IGNORE_TABLE, terminal.symbol_id)
        self.assertEqual("replicate_wild_ignore_table", terminal.symbol_value)

    def test_keyword_replication(self):
        """测试解析 REPLICATION 关键字"""
        terminal = parse_one_token("REPLICATION")
        self.assertEqual(TType.KEYWORD_REPLICATION, terminal.symbol_id)
        self.assertEqual("REPLICATION", terminal.symbol_value)

        terminal = parse_one_token("replication")
        self.assertEqual(TType.KEYWORD_REPLICATION, terminal.symbol_id)
        self.assertEqual("replication", terminal.symbol_value)

    def test_keyword_require(self):
        """测试解析 REQUIRE 关键字"""
        terminal = parse_one_token("REQUIRE")
        self.assertEqual(TType.KEYWORD_REQUIRE, terminal.symbol_id)
        self.assertEqual("REQUIRE", terminal.symbol_value)

        terminal = parse_one_token("require")
        self.assertEqual(TType.KEYWORD_REQUIRE, terminal.symbol_id)
        self.assertEqual("require", terminal.symbol_value)

    def test_keyword_require_row_format(self):
        """测试解析 REQUIRE_ROW_FORMAT 关键字"""
        terminal = parse_one_token("REQUIRE_ROW_FORMAT")
        self.assertEqual(TType.KEYWORD_REQUIRE_ROW_FORMAT, terminal.symbol_id)
        self.assertEqual("REQUIRE_ROW_FORMAT", terminal.symbol_value)

        terminal = parse_one_token("require_row_format")
        self.assertEqual(TType.KEYWORD_REQUIRE_ROW_FORMAT, terminal.symbol_id)
        self.assertEqual("require_row_format", terminal.symbol_value)

    def test_keyword_reset(self):
        """测试解析 RESET 关键字"""
        terminal = parse_one_token("RESET")
        self.assertEqual(TType.KEYWORD_RESET, terminal.symbol_id)
        self.assertEqual("RESET", terminal.symbol_value)

        terminal = parse_one_token("reset")
        self.assertEqual(TType.KEYWORD_RESET, terminal.symbol_id)
        self.assertEqual("reset", terminal.symbol_value)

    def test_keyword_resignal(self):
        """测试解析 RESIGNAL 关键字"""
        terminal = parse_one_token("RESIGNAL")
        self.assertEqual(TType.KEYWORD_RESIGNAL, terminal.symbol_id)
        self.assertEqual("RESIGNAL", terminal.symbol_value)

        terminal = parse_one_token("resignal")
        self.assertEqual(TType.KEYWORD_RESIGNAL, terminal.symbol_id)
        self.assertEqual("resignal", terminal.symbol_value)

    def test_keyword_resource(self):
        """测试解析 RESOURCE 关键字"""
        terminal = parse_one_token("RESOURCE")
        self.assertEqual(TType.KEYWORD_RESOURCE, terminal.symbol_id)
        self.assertEqual("RESOURCE", terminal.symbol_value)

        terminal = parse_one_token("resource")
        self.assertEqual(TType.KEYWORD_RESOURCE, terminal.symbol_id)
        self.assertEqual("resource", terminal.symbol_value)

    def test_keyword_respect(self):
        """测试解析 RESPECT 关键字"""
        terminal = parse_one_token("RESPECT")
        self.assertEqual(TType.KEYWORD_RESPECT, terminal.symbol_id)
        self.assertEqual("RESPECT", terminal.symbol_value)

        terminal = parse_one_token("respect")
        self.assertEqual(TType.KEYWORD_RESPECT, terminal.symbol_id)
        self.assertEqual("respect", terminal.symbol_value)

    def test_keyword_restart(self):
        """测试解析 RESTART 关键字"""
        terminal = parse_one_token("RESTART")
        self.assertEqual(TType.KEYWORD_RESTART, terminal.symbol_id)
        self.assertEqual("RESTART", terminal.symbol_value)

        terminal = parse_one_token("restart")
        self.assertEqual(TType.KEYWORD_RESTART, terminal.symbol_id)
        self.assertEqual("restart", terminal.symbol_value)

    def test_keyword_restore(self):
        """测试解析 RESTORE 关键字"""
        terminal = parse_one_token("RESTORE")
        self.assertEqual(TType.KEYWORD_RESTORE, terminal.symbol_id)
        self.assertEqual("RESTORE", terminal.symbol_value)

        terminal = parse_one_token("restore")
        self.assertEqual(TType.KEYWORD_RESTORE, terminal.symbol_id)
        self.assertEqual("restore", terminal.symbol_value)

    def test_keyword_restrict(self):
        """测试解析 RESTRICT 关键字"""
        terminal = parse_one_token("RESTRICT")
        self.assertEqual(TType.KEYWORD_RESTRICT, terminal.symbol_id)
        self.assertEqual("RESTRICT", terminal.symbol_value)

        terminal = parse_one_token("restrict")
        self.assertEqual(TType.KEYWORD_RESTRICT, terminal.symbol_id)
        self.assertEqual("restrict", terminal.symbol_value)

    def test_keyword_resume(self):
        """测试解析 RESUME 关键字"""
        terminal = parse_one_token("RESUME")
        self.assertEqual(TType.KEYWORD_RESUME, terminal.symbol_id)
        self.assertEqual("RESUME", terminal.symbol_value)

        terminal = parse_one_token("resume")
        self.assertEqual(TType.KEYWORD_RESUME, terminal.symbol_id)
        self.assertEqual("resume", terminal.symbol_value)

    def test_keyword_retain(self):
        """测试解析 RETAIN 关键字"""
        terminal = parse_one_token("RETAIN")
        self.assertEqual(TType.KEYWORD_RETAIN, terminal.symbol_id)
        self.assertEqual("RETAIN", terminal.symbol_value)

        terminal = parse_one_token("retain")
        self.assertEqual(TType.KEYWORD_RETAIN, terminal.symbol_id)
        self.assertEqual("retain", terminal.symbol_value)

    def test_keyword_return(self):
        """测试解析 RETURN 关键字"""
        terminal = parse_one_token("RETURN")
        self.assertEqual(TType.KEYWORD_RETURN, terminal.symbol_id)
        self.assertEqual("RETURN", terminal.symbol_value)

        terminal = parse_one_token("return")
        self.assertEqual(TType.KEYWORD_RETURN, terminal.symbol_id)
        self.assertEqual("return", terminal.symbol_value)

    def test_keyword_returned_sqlstate(self):
        """测试解析 RETURNED_SQLSTATE 关键字"""
        terminal = parse_one_token("RETURNED_SQLSTATE")
        self.assertEqual(TType.KEYWORD_RETURNED_SQLSTATE, terminal.symbol_id)
        self.assertEqual("RETURNED_SQLSTATE", terminal.symbol_value)

        terminal = parse_one_token("returned_sqlstate")
        self.assertEqual(TType.KEYWORD_RETURNED_SQLSTATE, terminal.symbol_id)
        self.assertEqual("returned_sqlstate", terminal.symbol_value)

    def test_keyword_returning(self):
        """测试解析 RETURNING 关键字"""
        terminal = parse_one_token("RETURNING")
        self.assertEqual(TType.KEYWORD_RETURNING, terminal.symbol_id)
        self.assertEqual("RETURNING", terminal.symbol_value)

        terminal = parse_one_token("returning")
        self.assertEqual(TType.KEYWORD_RETURNING, terminal.symbol_id)
        self.assertEqual("returning", terminal.symbol_value)

    def test_keyword_returns(self):
        """测试解析 RETURNS 关键字"""
        terminal = parse_one_token("RETURNS")
        self.assertEqual(TType.KEYWORD_RETURNS, terminal.symbol_id)
        self.assertEqual("RETURNS", terminal.symbol_value)

        terminal = parse_one_token("returns")
        self.assertEqual(TType.KEYWORD_RETURNS, terminal.symbol_id)
        self.assertEqual("returns", terminal.symbol_value)

    def test_keyword_reuse(self):
        """测试解析 REUSE 关键字"""
        terminal = parse_one_token("REUSE")
        self.assertEqual(TType.KEYWORD_REUSE, terminal.symbol_id)
        self.assertEqual("REUSE", terminal.symbol_value)

        terminal = parse_one_token("reuse")
        self.assertEqual(TType.KEYWORD_REUSE, terminal.symbol_id)
        self.assertEqual("reuse", terminal.symbol_value)

    def test_keyword_reverse(self):
        """测试解析 REVERSE 关键字"""
        terminal = parse_one_token("REVERSE")
        self.assertEqual(TType.KEYWORD_REVERSE, terminal.symbol_id)
        self.assertEqual("REVERSE", terminal.symbol_value)

        terminal = parse_one_token("reverse")
        self.assertEqual(TType.KEYWORD_REVERSE, terminal.symbol_id)
        self.assertEqual("reverse", terminal.symbol_value)

    def test_keyword_revoke(self):
        """测试解析 REVOKE 关键字"""
        terminal = parse_one_token("REVOKE")
        self.assertEqual(TType.KEYWORD_REVOKE, terminal.symbol_id)
        self.assertEqual("REVOKE", terminal.symbol_value)

        terminal = parse_one_token("revoke")
        self.assertEqual(TType.KEYWORD_REVOKE, terminal.symbol_id)
        self.assertEqual("revoke", terminal.symbol_value)

    def test_keyword_right(self):
        """测试解析 RIGHT 关键字"""
        terminal = parse_one_token("RIGHT")
        self.assertEqual(TType.KEYWORD_RIGHT, terminal.symbol_id)
        self.assertEqual("RIGHT", terminal.symbol_value)

        terminal = parse_one_token("right")
        self.assertEqual(TType.KEYWORD_RIGHT, terminal.symbol_id)
        self.assertEqual("right", terminal.symbol_value)

    def test_keyword_rlike(self):
        """测试解析 RLIKE 关键字"""
        terminal = parse_one_token("RLIKE")
        self.assertEqual(TType.KEYWORD_RLIKE, terminal.symbol_id)
        self.assertEqual("RLIKE", terminal.symbol_value)

        terminal = parse_one_token("rlike")
        self.assertEqual(TType.KEYWORD_RLIKE, terminal.symbol_id)
        self.assertEqual("rlike", terminal.symbol_value)

    def test_keyword_role(self):
        """测试解析 ROLE 关键字"""
        terminal = parse_one_token("ROLE")
        self.assertEqual(TType.KEYWORD_ROLE, terminal.symbol_id)
        self.assertEqual("ROLE", terminal.symbol_value)

        terminal = parse_one_token("role")
        self.assertEqual(TType.KEYWORD_ROLE, terminal.symbol_id)
        self.assertEqual("role", terminal.symbol_value)

    def test_keyword_rollback(self):
        """测试解析 ROLLBACK 关键字"""
        terminal = parse_one_token("ROLLBACK")
        self.assertEqual(TType.KEYWORD_ROLLBACK, terminal.symbol_id)
        self.assertEqual("ROLLBACK", terminal.symbol_value)

        terminal = parse_one_token("rollback")
        self.assertEqual(TType.KEYWORD_ROLLBACK, terminal.symbol_id)
        self.assertEqual("rollback", terminal.symbol_value)

    def test_keyword_rollup(self):
        """测试解析 ROLLUP 关键字"""
        terminal = parse_one_token("ROLLUP")
        self.assertEqual(TType.KEYWORD_ROLLUP, terminal.symbol_id)
        self.assertEqual("ROLLUP", terminal.symbol_value)

        terminal = parse_one_token("rollup")
        self.assertEqual(TType.KEYWORD_ROLLUP, terminal.symbol_id)
        self.assertEqual("rollup", terminal.symbol_value)

    def test_keyword_rotate(self):
        """测试解析 ROTATE 关键字"""
        terminal = parse_one_token("ROTATE")
        self.assertEqual(TType.KEYWORD_ROTATE, terminal.symbol_id)
        self.assertEqual("ROTATE", terminal.symbol_value)

        terminal = parse_one_token("rotate")
        self.assertEqual(TType.KEYWORD_ROTATE, terminal.symbol_id)
        self.assertEqual("rotate", terminal.symbol_value)

    def test_keyword_routine(self):
        """测试解析 ROUTINE 关键字"""
        terminal = parse_one_token("ROUTINE")
        self.assertEqual(TType.KEYWORD_ROUTINE, terminal.symbol_id)
        self.assertEqual("ROUTINE", terminal.symbol_value)

        terminal = parse_one_token("routine")
        self.assertEqual(TType.KEYWORD_ROUTINE, terminal.symbol_id)
        self.assertEqual("routine", terminal.symbol_value)

    def test_keyword_row(self):
        """测试解析 ROW 关键字"""
        terminal = parse_one_token("ROW")
        self.assertEqual(TType.KEYWORD_ROW, terminal.symbol_id)
        self.assertEqual("ROW", terminal.symbol_value)

        terminal = parse_one_token("row")
        self.assertEqual(TType.KEYWORD_ROW, terminal.symbol_id)
        self.assertEqual("row", terminal.symbol_value)

    def test_keyword_rows(self):
        """测试解析 ROWS 关键字"""
        terminal = parse_one_token("ROWS")
        self.assertEqual(TType.KEYWORD_ROWS, terminal.symbol_id)
        self.assertEqual("ROWS", terminal.symbol_value)

        terminal = parse_one_token("rows")
        self.assertEqual(TType.KEYWORD_ROWS, terminal.symbol_id)
        self.assertEqual("rows", terminal.symbol_value)

    def test_keyword_row_count(self):
        """测试解析 ROW_COUNT 关键字"""
        terminal = parse_one_token("ROW_COUNT")
        self.assertEqual(TType.KEYWORD_ROW_COUNT, terminal.symbol_id)
        self.assertEqual("ROW_COUNT", terminal.symbol_value)

        terminal = parse_one_token("row_count")
        self.assertEqual(TType.KEYWORD_ROW_COUNT, terminal.symbol_id)
        self.assertEqual("row_count", terminal.symbol_value)

    def test_keyword_row_format(self):
        """测试解析 ROW_FORMAT 关键字"""
        terminal = parse_one_token("ROW_FORMAT")
        self.assertEqual(TType.KEYWORD_ROW_FORMAT, terminal.symbol_id)
        self.assertEqual("ROW_FORMAT", terminal.symbol_value)

        terminal = parse_one_token("row_format")
        self.assertEqual(TType.KEYWORD_ROW_FORMAT, terminal.symbol_id)
        self.assertEqual("row_format", terminal.symbol_value)

    def test_keyword_row_number(self):
        """测试解析 ROW_NUMBER 关键字"""
        terminal = parse_one_token("ROW_NUMBER")
        self.assertEqual(TType.KEYWORD_ROW_NUMBER, terminal.symbol_id)
        self.assertEqual("ROW_NUMBER", terminal.symbol_value)

        terminal = parse_one_token("row_number")
        self.assertEqual(TType.KEYWORD_ROW_NUMBER, terminal.symbol_id)
        self.assertEqual("row_number", terminal.symbol_value)

    def test_keyword_rtree(self):
        """测试解析 RTREE 关键字"""
        terminal = parse_one_token("RTREE")
        self.assertEqual(TType.KEYWORD_RTREE, terminal.symbol_id)
        self.assertEqual("RTREE", terminal.symbol_value)

        terminal = parse_one_token("rtree")
        self.assertEqual(TType.KEYWORD_RTREE, terminal.symbol_id)
        self.assertEqual("rtree", terminal.symbol_value)

    def test_keyword_s3(self):
        """测试解析 S3 关键字"""
        terminal = parse_one_token("S3")
        self.assertEqual(TType.KEYWORD_S3, terminal.symbol_id)
        self.assertEqual("S3", terminal.symbol_value)

        terminal = parse_one_token("s3")
        self.assertEqual(TType.KEYWORD_S3, terminal.symbol_id)
        self.assertEqual("s3", terminal.symbol_value)

    def test_keyword_savepoint(self):
        """测试解析 SAVEPOINT 关键字"""
        terminal = parse_one_token("SAVEPOINT")
        self.assertEqual(TType.KEYWORD_SAVEPOINT, terminal.symbol_id)
        self.assertEqual("SAVEPOINT", terminal.symbol_value)

        terminal = parse_one_token("savepoint")
        self.assertEqual(TType.KEYWORD_SAVEPOINT, terminal.symbol_id)
        self.assertEqual("savepoint", terminal.symbol_value)

    def test_keyword_schedule(self):
        """测试解析 SCHEDULE 关键字"""
        terminal = parse_one_token("SCHEDULE")
        self.assertEqual(TType.KEYWORD_SCHEDULE, terminal.symbol_id)
        self.assertEqual("SCHEDULE", terminal.symbol_value)

        terminal = parse_one_token("schedule")
        self.assertEqual(TType.KEYWORD_SCHEDULE, terminal.symbol_id)
        self.assertEqual("schedule", terminal.symbol_value)

    def test_keyword_schema(self):
        """测试解析 SCHEMA 关键字"""
        terminal = parse_one_token("SCHEMA")
        self.assertEqual(TType.KEYWORD_SCHEMA, terminal.symbol_id)
        self.assertEqual("SCHEMA", terminal.symbol_value)

        terminal = parse_one_token("schema")
        self.assertEqual(TType.KEYWORD_SCHEMA, terminal.symbol_id)
        self.assertEqual("schema", terminal.symbol_value)

    def test_keyword_schemas(self):
        """测试解析 SCHEMAS 关键字"""
        terminal = parse_one_token("SCHEMAS")
        self.assertEqual(TType.KEYWORD_SCHEMAS, terminal.symbol_id)
        self.assertEqual("SCHEMAS", terminal.symbol_value)

        terminal = parse_one_token("schemas")
        self.assertEqual(TType.KEYWORD_SCHEMAS, terminal.symbol_id)
        self.assertEqual("schemas", terminal.symbol_value)

    def test_keyword_schema_name(self):
        """测试解析 SCHEMA_NAME 关键字"""
        terminal = parse_one_token("SCHEMA_NAME")
        self.assertEqual(TType.KEYWORD_SCHEMA_NAME, terminal.symbol_id)
        self.assertEqual("SCHEMA_NAME", terminal.symbol_value)

        terminal = parse_one_token("schema_name")
        self.assertEqual(TType.KEYWORD_SCHEMA_NAME, terminal.symbol_id)
        self.assertEqual("schema_name", terminal.symbol_value)

    def test_keyword_second(self):
        """测试解析 SECOND 关键字"""
        terminal = parse_one_token("SECOND")
        self.assertEqual(TType.KEYWORD_SECOND, terminal.symbol_id)
        self.assertEqual("SECOND", terminal.symbol_value)

        terminal = parse_one_token("second")
        self.assertEqual(TType.KEYWORD_SECOND, terminal.symbol_id)
        self.assertEqual("second", terminal.symbol_value)

    def test_keyword_secondary(self):
        """测试解析 SECONDARY 关键字"""
        terminal = parse_one_token("SECONDARY")
        self.assertEqual(TType.KEYWORD_SECONDARY, terminal.symbol_id)
        self.assertEqual("SECONDARY", terminal.symbol_value)

        terminal = parse_one_token("secondary")
        self.assertEqual(TType.KEYWORD_SECONDARY, terminal.symbol_id)
        self.assertEqual("secondary", terminal.symbol_value)

    def test_keyword_secondary_engine(self):
        """测试解析 SECONDARY_ENGINE 关键字"""
        terminal = parse_one_token("SECONDARY_ENGINE")
        self.assertEqual(TType.KEYWORD_SECONDARY_ENGINE, terminal.symbol_id)
        self.assertEqual("SECONDARY_ENGINE", terminal.symbol_value)

        terminal = parse_one_token("secondary_engine")
        self.assertEqual(TType.KEYWORD_SECONDARY_ENGINE, terminal.symbol_id)
        self.assertEqual("secondary_engine", terminal.symbol_value)

    def test_keyword_secondary_engine_attribute(self):
        """测试解析 SECONDARY_ENGINE_ATTRIBUTE 关键字"""
        terminal = parse_one_token("SECONDARY_ENGINE_ATTRIBUTE")
        self.assertEqual(TType.KEYWORD_SECONDARY_ENGINE_ATTRIBUTE, terminal.symbol_id)
        self.assertEqual("SECONDARY_ENGINE_ATTRIBUTE", terminal.symbol_value)

        terminal = parse_one_token("secondary_engine_attribute")
        self.assertEqual(TType.KEYWORD_SECONDARY_ENGINE_ATTRIBUTE, terminal.symbol_id)
        self.assertEqual("secondary_engine_attribute", terminal.symbol_value)

    def test_keyword_secondary_load(self):
        """测试解析 SECONDARY_LOAD 关键字"""
        terminal = parse_one_token("SECONDARY_LOAD")
        self.assertEqual(TType.KEYWORD_SECONDARY_LOAD, terminal.symbol_id)
        self.assertEqual("SECONDARY_LOAD", terminal.symbol_value)

        terminal = parse_one_token("secondary_load")
        self.assertEqual(TType.KEYWORD_SECONDARY_LOAD, terminal.symbol_id)
        self.assertEqual("secondary_load", terminal.symbol_value)

    def test_keyword_secondary_unload(self):
        """测试解析 SECONDARY_UNLOAD 关键字"""
        terminal = parse_one_token("SECONDARY_UNLOAD")
        self.assertEqual(TType.KEYWORD_SECONDARY_UNLOAD, terminal.symbol_id)
        self.assertEqual("SECONDARY_UNLOAD", terminal.symbol_value)

        terminal = parse_one_token("secondary_unload")
        self.assertEqual(TType.KEYWORD_SECONDARY_UNLOAD, terminal.symbol_id)
        self.assertEqual("secondary_unload", terminal.symbol_value)

    def test_keyword_second_microsecond(self):
        """测试解析 SECOND_MICROSECOND 关键字"""
        terminal = parse_one_token("SECOND_MICROSECOND")
        self.assertEqual(TType.KEYWORD_SECOND_MICROSECOND, terminal.symbol_id)
        self.assertEqual("SECOND_MICROSECOND", terminal.symbol_value)

        terminal = parse_one_token("second_microsecond")
        self.assertEqual(TType.KEYWORD_SECOND_MICROSECOND, terminal.symbol_id)
        self.assertEqual("second_microsecond", terminal.symbol_value)

    def test_keyword_security(self):
        """测试解析 SECURITY 关键字"""
        terminal = parse_one_token("SECURITY")
        self.assertEqual(TType.KEYWORD_SECURITY, terminal.symbol_id)
        self.assertEqual("SECURITY", terminal.symbol_value)

        terminal = parse_one_token("security")
        self.assertEqual(TType.KEYWORD_SECURITY, terminal.symbol_id)
        self.assertEqual("security", terminal.symbol_value)

    def test_keyword_select(self):
        """测试解析 SELECT 关键字"""
        terminal = parse_one_token("SELECT")
        self.assertEqual(TType.KEYWORD_SELECT, terminal.symbol_id)
        self.assertEqual("SELECT", terminal.symbol_value)

        terminal = parse_one_token("select")
        self.assertEqual(TType.KEYWORD_SELECT, terminal.symbol_id)
        self.assertEqual("select", terminal.symbol_value)

    def test_keyword_sensitive(self):
        """测试解析 SENSITIVE 关键字"""
        terminal = parse_one_token("SENSITIVE")
        self.assertEqual(TType.KEYWORD_SENSITIVE, terminal.symbol_id)
        self.assertEqual("SENSITIVE", terminal.symbol_value)

        terminal = parse_one_token("sensitive")
        self.assertEqual(TType.KEYWORD_SENSITIVE, terminal.symbol_id)
        self.assertEqual("sensitive", terminal.symbol_value)

    def test_keyword_separator(self):
        """测试解析 SEPARATOR 关键字"""
        terminal = parse_one_token("SEPARATOR")
        self.assertEqual(TType.KEYWORD_SEPARATOR, terminal.symbol_id)
        self.assertEqual("SEPARATOR", terminal.symbol_value)

        terminal = parse_one_token("separator")
        self.assertEqual(TType.KEYWORD_SEPARATOR, terminal.symbol_id)
        self.assertEqual("separator", terminal.symbol_value)

    def test_keyword_serial(self):
        """测试解析 SERIAL 关键字"""
        terminal = parse_one_token("SERIAL")
        self.assertEqual(TType.KEYWORD_SERIAL, terminal.symbol_id)
        self.assertEqual("SERIAL", terminal.symbol_value)

        terminal = parse_one_token("serial")
        self.assertEqual(TType.KEYWORD_SERIAL, terminal.symbol_id)
        self.assertEqual("serial", terminal.symbol_value)

    def test_keyword_serializable(self):
        """测试解析 SERIALIZABLE 关键字"""
        terminal = parse_one_token("SERIALIZABLE")
        self.assertEqual(TType.KEYWORD_SERIALIZABLE, terminal.symbol_id)
        self.assertEqual("SERIALIZABLE", terminal.symbol_value)

        terminal = parse_one_token("serializable")
        self.assertEqual(TType.KEYWORD_SERIALIZABLE, terminal.symbol_id)
        self.assertEqual("serializable", terminal.symbol_value)

    def test_keyword_server(self):
        """测试解析 SERVER 关键字"""
        terminal = parse_one_token("SERVER")
        self.assertEqual(TType.KEYWORD_SERVER, terminal.symbol_id)
        self.assertEqual("SERVER", terminal.symbol_value)

        terminal = parse_one_token("server")
        self.assertEqual(TType.KEYWORD_SERVER, terminal.symbol_id)
        self.assertEqual("server", terminal.symbol_value)

    def test_keyword_session(self):
        """测试解析 SESSION 关键字"""
        terminal = parse_one_token("SESSION")
        self.assertEqual(TType.KEYWORD_SESSION, terminal.symbol_id)
        self.assertEqual("SESSION", terminal.symbol_value)

        terminal = parse_one_token("session")
        self.assertEqual(TType.KEYWORD_SESSION, terminal.symbol_id)
        self.assertEqual("session", terminal.symbol_value)

    def test_keyword_set(self):
        """测试解析 SET 关键字"""
        terminal = parse_one_token("SET")
        self.assertEqual(TType.KEYWORD_SET, terminal.symbol_id)
        self.assertEqual("SET", terminal.symbol_value)

        terminal = parse_one_token("set")
        self.assertEqual(TType.KEYWORD_SET, terminal.symbol_id)
        self.assertEqual("set", terminal.symbol_value)

    def test_keyword_share(self):
        """测试解析 SHARE 关键字"""
        terminal = parse_one_token("SHARE")
        self.assertEqual(TType.KEYWORD_SHARE, terminal.symbol_id)
        self.assertEqual("SHARE", terminal.symbol_value)

        terminal = parse_one_token("share")
        self.assertEqual(TType.KEYWORD_SHARE, terminal.symbol_id)
        self.assertEqual("share", terminal.symbol_value)

    def test_keyword_show(self):
        """测试解析 SHOW 关键字"""
        terminal = parse_one_token("SHOW")
        self.assertEqual(TType.KEYWORD_SHOW, terminal.symbol_id)
        self.assertEqual("SHOW", terminal.symbol_value)

        terminal = parse_one_token("show")
        self.assertEqual(TType.KEYWORD_SHOW, terminal.symbol_id)
        self.assertEqual("show", terminal.symbol_value)

    def test_keyword_shutdown(self):
        """测试解析 SHUTDOWN 关键字"""
        terminal = parse_one_token("SHUTDOWN")
        self.assertEqual(TType.KEYWORD_SHUTDOWN, terminal.symbol_id)
        self.assertEqual("SHUTDOWN", terminal.symbol_value)

        terminal = parse_one_token("shutdown")
        self.assertEqual(TType.KEYWORD_SHUTDOWN, terminal.symbol_id)
        self.assertEqual("shutdown", terminal.symbol_value)

    def test_keyword_signal(self):
        """测试解析 SIGNAL 关键字"""
        terminal = parse_one_token("SIGNAL")
        self.assertEqual(TType.KEYWORD_SIGNAL, terminal.symbol_id)
        self.assertEqual("SIGNAL", terminal.symbol_value)

        terminal = parse_one_token("signal")
        self.assertEqual(TType.KEYWORD_SIGNAL, terminal.symbol_id)
        self.assertEqual("signal", terminal.symbol_value)

    def test_keyword_signed(self):
        """测试解析 SIGNED 关键字"""
        terminal = parse_one_token("SIGNED")
        self.assertEqual(TType.KEYWORD_SIGNED, terminal.symbol_id)
        self.assertEqual("SIGNED", terminal.symbol_value)

        terminal = parse_one_token("signed")
        self.assertEqual(TType.KEYWORD_SIGNED, terminal.symbol_id)
        self.assertEqual("signed", terminal.symbol_value)

    def test_keyword_simple(self):
        """测试解析 SIMPLE 关键字"""
        terminal = parse_one_token("SIMPLE")
        self.assertEqual(TType.KEYWORD_SIMPLE, terminal.symbol_id)
        self.assertEqual("SIMPLE", terminal.symbol_value)

        terminal = parse_one_token("simple")
        self.assertEqual(TType.KEYWORD_SIMPLE, terminal.symbol_id)
        self.assertEqual("simple", terminal.symbol_value)

    def test_keyword_skip(self):
        """测试解析 SKIP 关键字"""
        terminal = parse_one_token("SKIP")
        self.assertEqual(TType.KEYWORD_SKIP, terminal.symbol_id)
        self.assertEqual("SKIP", terminal.symbol_value)

        terminal = parse_one_token("skip")
        self.assertEqual(TType.KEYWORD_SKIP, terminal.symbol_id)
        self.assertEqual("skip", terminal.symbol_value)

    def test_keyword_slave(self):
        """测试解析 SLAVE 关键字"""
        terminal = parse_one_token("SLAVE")
        self.assertEqual(TType.KEYWORD_SLAVE, terminal.symbol_id)
        self.assertEqual("SLAVE", terminal.symbol_value)

        terminal = parse_one_token("slave")
        self.assertEqual(TType.KEYWORD_SLAVE, terminal.symbol_id)
        self.assertEqual("slave", terminal.symbol_value)

    def test_keyword_slow(self):
        """测试解析 SLOW 关键字"""
        terminal = parse_one_token("SLOW")
        self.assertEqual(TType.KEYWORD_SLOW, terminal.symbol_id)
        self.assertEqual("SLOW", terminal.symbol_value)

        terminal = parse_one_token("slow")
        self.assertEqual(TType.KEYWORD_SLOW, terminal.symbol_id)
        self.assertEqual("slow", terminal.symbol_value)

    def test_keyword_smallint(self):
        """测试解析 SMALLINT 关键字"""
        terminal = parse_one_token("SMALLINT")
        self.assertEqual(TType.KEYWORD_SMALLINT, terminal.symbol_id)
        self.assertEqual("SMALLINT", terminal.symbol_value)

        terminal = parse_one_token("smallint")
        self.assertEqual(TType.KEYWORD_SMALLINT, terminal.symbol_id)
        self.assertEqual("smallint", terminal.symbol_value)

    def test_keyword_snapshot(self):
        """测试解析 SNAPSHOT 关键字"""
        terminal = parse_one_token("SNAPSHOT")
        self.assertEqual(TType.KEYWORD_SNAPSHOT, terminal.symbol_id)
        self.assertEqual("SNAPSHOT", terminal.symbol_value)

        terminal = parse_one_token("snapshot")
        self.assertEqual(TType.KEYWORD_SNAPSHOT, terminal.symbol_id)
        self.assertEqual("snapshot", terminal.symbol_value)

    def test_keyword_socket(self):
        """测试解析 SOCKET 关键字"""
        terminal = parse_one_token("SOCKET")
        self.assertEqual(TType.KEYWORD_SOCKET, terminal.symbol_id)
        self.assertEqual("SOCKET", terminal.symbol_value)

        terminal = parse_one_token("socket")
        self.assertEqual(TType.KEYWORD_SOCKET, terminal.symbol_id)
        self.assertEqual("socket", terminal.symbol_value)

    def test_keyword_some(self):
        """测试解析 SOME 关键字"""
        terminal = parse_one_token("SOME")
        self.assertEqual(TType.KEYWORD_SOME, terminal.symbol_id)
        self.assertEqual("SOME", terminal.symbol_value)

        terminal = parse_one_token("some")
        self.assertEqual(TType.KEYWORD_SOME, terminal.symbol_id)
        self.assertEqual("some", terminal.symbol_value)

    def test_keyword_soname(self):
        """测试解析 SONAME 关键字"""
        terminal = parse_one_token("SONAME")
        self.assertEqual(TType.KEYWORD_SONAME, terminal.symbol_id)
        self.assertEqual("SONAME", terminal.symbol_value)

        terminal = parse_one_token("soname")
        self.assertEqual(TType.KEYWORD_SONAME, terminal.symbol_id)
        self.assertEqual("soname", terminal.symbol_value)

    def test_keyword_sounds(self):
        """测试解析 SOUNDS 关键字"""
        terminal = parse_one_token("SOUNDS")
        self.assertEqual(TType.KEYWORD_SOUNDS, terminal.symbol_id)
        self.assertEqual("SOUNDS", terminal.symbol_value)

        terminal = parse_one_token("sounds")
        self.assertEqual(TType.KEYWORD_SOUNDS, terminal.symbol_id)
        self.assertEqual("sounds", terminal.symbol_value)

    def test_keyword_source(self):
        """测试解析 SOURCE 关键字"""
        terminal = parse_one_token("SOURCE")
        self.assertEqual(TType.KEYWORD_SOURCE, terminal.symbol_id)
        self.assertEqual("SOURCE", terminal.symbol_value)

        terminal = parse_one_token("source")
        self.assertEqual(TType.KEYWORD_SOURCE, terminal.symbol_id)
        self.assertEqual("source", terminal.symbol_value)

    def test_keyword_source_auto_position(self):
        """测试解析 SOURCE_AUTO_POSITION 关键字"""
        terminal = parse_one_token("SOURCE_AUTO_POSITION")
        self.assertEqual(TType.KEYWORD_SOURCE_AUTO_POSITION, terminal.symbol_id)
        self.assertEqual("SOURCE_AUTO_POSITION", terminal.symbol_value)

        terminal = parse_one_token("source_auto_position")
        self.assertEqual(TType.KEYWORD_SOURCE_AUTO_POSITION, terminal.symbol_id)
        self.assertEqual("source_auto_position", terminal.symbol_value)

    def test_keyword_source_bind(self):
        """测试解析 SOURCE_BIND 关键字"""
        terminal = parse_one_token("SOURCE_BIND")
        self.assertEqual(TType.KEYWORD_SOURCE_BIND, terminal.symbol_id)
        self.assertEqual("SOURCE_BIND", terminal.symbol_value)

        terminal = parse_one_token("source_bind")
        self.assertEqual(TType.KEYWORD_SOURCE_BIND, terminal.symbol_id)
        self.assertEqual("source_bind", terminal.symbol_value)

    def test_keyword_source_compression_algorithm(self):
        """测试解析 SOURCE_COMPRESSION_ALGORITHM 关键字"""
        terminal = parse_one_token("SOURCE_COMPRESSION_ALGORITHM")
        self.assertEqual(TType.KEYWORD_SOURCE_COMPRESSION_ALGORITHM, terminal.symbol_id)
        self.assertEqual("SOURCE_COMPRESSION_ALGORITHM", terminal.symbol_value)

        terminal = parse_one_token("source_compression_algorithm")
        self.assertEqual(TType.KEYWORD_SOURCE_COMPRESSION_ALGORITHM, terminal.symbol_id)
        self.assertEqual("source_compression_algorithm", terminal.symbol_value)

    def test_keyword_source_connect_retry(self):
        """测试解析 SOURCE_CONNECT_RETRY 关键字"""
        terminal = parse_one_token("SOURCE_CONNECT_RETRY")
        self.assertEqual(TType.KEYWORD_SOURCE_CONNECT_RETRY, terminal.symbol_id)
        self.assertEqual("SOURCE_CONNECT_RETRY", terminal.symbol_value)

        terminal = parse_one_token("source_connect_retry")
        self.assertEqual(TType.KEYWORD_SOURCE_CONNECT_RETRY, terminal.symbol_id)
        self.assertEqual("source_connect_retry", terminal.symbol_value)

    def test_keyword_source_delay(self):
        """测试解析 SOURCE_DELAY 关键字"""
        terminal = parse_one_token("SOURCE_DELAY")
        self.assertEqual(TType.KEYWORD_SOURCE_DELAY, terminal.symbol_id)
        self.assertEqual("SOURCE_DELAY", terminal.symbol_value)

        terminal = parse_one_token("source_delay")
        self.assertEqual(TType.KEYWORD_SOURCE_DELAY, terminal.symbol_id)
        self.assertEqual("source_delay", terminal.symbol_value)

    def test_keyword_source_heartbeat_period(self):
        """测试解析 SOURCE_HEARTBEAT_PERIOD 关键字"""
        terminal = parse_one_token("SOURCE_HEARTBEAT_PERIOD")
        self.assertEqual(TType.KEYWORD_SOURCE_HEARTBEAT_PERIOD, terminal.symbol_id)
        self.assertEqual("SOURCE_HEARTBEAT_PERIOD", terminal.symbol_value)

        terminal = parse_one_token("source_heartbeat_period")
        self.assertEqual(TType.KEYWORD_SOURCE_HEARTBEAT_PERIOD, terminal.symbol_id)
        self.assertEqual("source_heartbeat_period", terminal.symbol_value)

    def test_keyword_source_host(self):
        """测试解析 SOURCE_HOST 关键字"""
        terminal = parse_one_token("SOURCE_HOST")
        self.assertEqual(TType.KEYWORD_SOURCE_HOST, terminal.symbol_id)
        self.assertEqual("SOURCE_HOST", terminal.symbol_value)

        terminal = parse_one_token("source_host")
        self.assertEqual(TType.KEYWORD_SOURCE_HOST, terminal.symbol_id)
        self.assertEqual("source_host", terminal.symbol_value)

    def test_keyword_source_log_file(self):
        """测试解析 SOURCE_LOG_FILE 关键字"""
        terminal = parse_one_token("SOURCE_LOG_FILE")
        self.assertEqual(TType.KEYWORD_SOURCE_LOG_FILE, terminal.symbol_id)
        self.assertEqual("SOURCE_LOG_FILE", terminal.symbol_value)

        terminal = parse_one_token("source_log_file")
        self.assertEqual(TType.KEYWORD_SOURCE_LOG_FILE, terminal.symbol_id)
        self.assertEqual("source_log_file", terminal.symbol_value)

    def test_keyword_source_log_pos(self):
        """测试解析 SOURCE_LOG_POS 关键字"""
        terminal = parse_one_token("SOURCE_LOG_POS")
        self.assertEqual(TType.KEYWORD_SOURCE_LOG_POS, terminal.symbol_id)
        self.assertEqual("SOURCE_LOG_POS", terminal.symbol_value)

        terminal = parse_one_token("source_log_pos")
        self.assertEqual(TType.KEYWORD_SOURCE_LOG_POS, terminal.symbol_id)
        self.assertEqual("source_log_pos", terminal.symbol_value)

    def test_keyword_source_password(self):
        """测试解析 SOURCE_PASSWORD 关键字"""
        terminal = parse_one_token("SOURCE_PASSWORD")
        self.assertEqual(TType.KEYWORD_SOURCE_PASSWORD, terminal.symbol_id)
        self.assertEqual("SOURCE_PASSWORD", terminal.symbol_value)

        terminal = parse_one_token("source_password")
        self.assertEqual(TType.KEYWORD_SOURCE_PASSWORD, terminal.symbol_id)
        self.assertEqual("source_password", terminal.symbol_value)

    def test_keyword_source_port(self):
        """测试解析 SOURCE_PORT 关键字"""
        terminal = parse_one_token("SOURCE_PORT")
        self.assertEqual(TType.KEYWORD_SOURCE_PORT, terminal.symbol_id)
        self.assertEqual("SOURCE_PORT", terminal.symbol_value)

        terminal = parse_one_token("source_port")
        self.assertEqual(TType.KEYWORD_SOURCE_PORT, terminal.symbol_id)
        self.assertEqual("source_port", terminal.symbol_value)

    def test_keyword_source_public_key_path(self):
        """测试解析 SOURCE_PUBLIC_KEY_PATH 关键字"""
        terminal = parse_one_token("SOURCE_PUBLIC_KEY_PATH")
        self.assertEqual(TType.KEYWORD_SOURCE_PUBLIC_KEY_PATH, terminal.symbol_id)
        self.assertEqual("SOURCE_PUBLIC_KEY_PATH", terminal.symbol_value)

        terminal = parse_one_token("source_public_key_path")
        self.assertEqual(TType.KEYWORD_SOURCE_PUBLIC_KEY_PATH, terminal.symbol_id)
        self.assertEqual("source_public_key_path", terminal.symbol_value)

    def test_keyword_source_retry_count(self):
        """测试解析 SOURCE_RETRY_COUNT 关键字"""
        terminal = parse_one_token("SOURCE_RETRY_COUNT")
        self.assertEqual(TType.KEYWORD_SOURCE_RETRY_COUNT, terminal.symbol_id)
        self.assertEqual("SOURCE_RETRY_COUNT", terminal.symbol_value)

        terminal = parse_one_token("source_retry_count")
        self.assertEqual(TType.KEYWORD_SOURCE_RETRY_COUNT, terminal.symbol_id)
        self.assertEqual("source_retry_count", terminal.symbol_value)

    def test_keyword_source_ssl(self):
        """测试解析 SOURCE_SSL 关键字"""
        terminal = parse_one_token("SOURCE_SSL")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL", terminal.symbol_value)

        terminal = parse_one_token("source_ssl")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL, terminal.symbol_id)
        self.assertEqual("source_ssl", terminal.symbol_value)

    def test_keyword_source_ssl_ca(self):
        """测试解析 SOURCE_SSL_CA 关键字"""
        terminal = parse_one_token("SOURCE_SSL_CA")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CA, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_CA", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_ca")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CA, terminal.symbol_id)
        self.assertEqual("source_ssl_ca", terminal.symbol_value)

    def test_keyword_source_ssl_capath(self):
        """测试解析 SOURCE_SSL_CAPATH 关键字"""
        terminal = parse_one_token("SOURCE_SSL_CAPATH")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CAPATH, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_CAPATH", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_capath")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CAPATH, terminal.symbol_id)
        self.assertEqual("source_ssl_capath", terminal.symbol_value)

    def test_keyword_source_ssl_cert(self):
        """测试解析 SOURCE_SSL_CERT 关键字"""
        terminal = parse_one_token("SOURCE_SSL_CERT")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CERT, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_CERT", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_cert")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CERT, terminal.symbol_id)
        self.assertEqual("source_ssl_cert", terminal.symbol_value)

    def test_keyword_source_ssl_cipher(self):
        """测试解析 SOURCE_SSL_CIPHER 关键字"""
        terminal = parse_one_token("SOURCE_SSL_CIPHER")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CIPHER, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_CIPHER", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_cipher")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CIPHER, terminal.symbol_id)
        self.assertEqual("source_ssl_cipher", terminal.symbol_value)

    def test_keyword_source_ssl_crl(self):
        """测试解析 SOURCE_SSL_CRL 关键字"""
        terminal = parse_one_token("SOURCE_SSL_CRL")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CRL, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_CRL", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_crl")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CRL, terminal.symbol_id)
        self.assertEqual("source_ssl_crl", terminal.symbol_value)

    def test_keyword_source_ssl_crlpath(self):
        """测试解析 SOURCE_SSL_CRLPATH 关键字"""
        terminal = parse_one_token("SOURCE_SSL_CRLPATH")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CRLPATH, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_CRLPATH", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_crlpath")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_CRLPATH, terminal.symbol_id)
        self.assertEqual("source_ssl_crlpath", terminal.symbol_value)

    def test_keyword_source_ssl_key(self):
        """测试解析 SOURCE_SSL_KEY 关键字"""
        terminal = parse_one_token("SOURCE_SSL_KEY")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_KEY, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_KEY", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_key")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_KEY, terminal.symbol_id)
        self.assertEqual("source_ssl_key", terminal.symbol_value)

    def test_keyword_source_ssl_verify_server_cert(self):
        """测试解析 SOURCE_SSL_VERIFY_SERVER_CERT 关键字"""
        terminal = parse_one_token("SOURCE_SSL_VERIFY_SERVER_CERT")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_VERIFY_SERVER_CERT, terminal.symbol_id)
        self.assertEqual("SOURCE_SSL_VERIFY_SERVER_CERT", terminal.symbol_value)

        terminal = parse_one_token("source_ssl_verify_server_cert")
        self.assertEqual(TType.KEYWORD_SOURCE_SSL_VERIFY_SERVER_CERT, terminal.symbol_id)
        self.assertEqual("source_ssl_verify_server_cert", terminal.symbol_value)

    def test_keyword_source_tls_ciphersuites(self):
        """测试解析 SOURCE_TLS_CIPHERSUITES 关键字"""
        terminal = parse_one_token("SOURCE_TLS_CIPHERSUITES")
        self.assertEqual(TType.KEYWORD_SOURCE_TLS_CIPHERSUITES, terminal.symbol_id)
        self.assertEqual("SOURCE_TLS_CIPHERSUITES", terminal.symbol_value)

        terminal = parse_one_token("source_tls_ciphersuites")
        self.assertEqual(TType.KEYWORD_SOURCE_TLS_CIPHERSUITES, terminal.symbol_id)
        self.assertEqual("source_tls_ciphersuites", terminal.symbol_value)

    def test_keyword_source_tls_version(self):
        """测试解析 SOURCE_TLS_VERSION 关键字"""
        terminal = parse_one_token("SOURCE_TLS_VERSION")
        self.assertEqual(TType.KEYWORD_SOURCE_TLS_VERSION, terminal.symbol_id)
        self.assertEqual("SOURCE_TLS_VERSION", terminal.symbol_value)

        terminal = parse_one_token("source_tls_version")
        self.assertEqual(TType.KEYWORD_SOURCE_TLS_VERSION, terminal.symbol_id)
        self.assertEqual("source_tls_version", terminal.symbol_value)

    def test_keyword_source_user(self):
        """测试解析 SOURCE_USER 关键字"""
        terminal = parse_one_token("SOURCE_USER")
        self.assertEqual(TType.KEYWORD_SOURCE_USER, terminal.symbol_id)
        self.assertEqual("SOURCE_USER", terminal.symbol_value)

        terminal = parse_one_token("source_user")
        self.assertEqual(TType.KEYWORD_SOURCE_USER, terminal.symbol_id)
        self.assertEqual("source_user", terminal.symbol_value)

    def test_keyword_source_zstd_compression_level(self):
        """测试解析 SOURCE_ZSTD_COMPRESSION_LEVEL 关键字"""
        terminal = parse_one_token("SOURCE_ZSTD_COMPRESSION_LEVEL")
        self.assertEqual(TType.KEYWORD_SOURCE_ZSTD_COMPRESSION_LEVEL, terminal.symbol_id)
        self.assertEqual("SOURCE_ZSTD_COMPRESSION_LEVEL", terminal.symbol_value)

        terminal = parse_one_token("source_zstd_compression_level")
        self.assertEqual(TType.KEYWORD_SOURCE_ZSTD_COMPRESSION_LEVEL, terminal.symbol_id)
        self.assertEqual("source_zstd_compression_level", terminal.symbol_value)

    def test_keyword_spatial(self):
        """测试解析 SPATIAL 关键字"""
        terminal = parse_one_token("SPATIAL")
        self.assertEqual(TType.KEYWORD_SPATIAL, terminal.symbol_id)
        self.assertEqual("SPATIAL", terminal.symbol_value)

        terminal = parse_one_token("spatial")
        self.assertEqual(TType.KEYWORD_SPATIAL, terminal.symbol_id)
        self.assertEqual("spatial", terminal.symbol_value)

    def test_keyword_specific(self):
        """测试解析 SPECIFIC 关键字"""
        terminal = parse_one_token("SPECIFIC")
        self.assertEqual(TType.KEYWORD_SPECIFIC, terminal.symbol_id)
        self.assertEqual("SPECIFIC", terminal.symbol_value)

        terminal = parse_one_token("specific")
        self.assertEqual(TType.KEYWORD_SPECIFIC, terminal.symbol_id)
        self.assertEqual("specific", terminal.symbol_value)

    def test_keyword_sql(self):
        """测试解析 SQL 关键字"""
        terminal = parse_one_token("SQL")
        self.assertEqual(TType.KEYWORD_SQL, terminal.symbol_id)
        self.assertEqual("SQL", terminal.symbol_value)

        terminal = parse_one_token("sql")
        self.assertEqual(TType.KEYWORD_SQL, terminal.symbol_id)
        self.assertEqual("sql", terminal.symbol_value)

    def test_keyword_sqlexception(self):
        """测试解析 SQLEXCEPTION 关键字"""
        terminal = parse_one_token("SQLEXCEPTION")
        self.assertEqual(TType.KEYWORD_SQLEXCEPTION, terminal.symbol_id)
        self.assertEqual("SQLEXCEPTION", terminal.symbol_value)

        terminal = parse_one_token("sqlexception")
        self.assertEqual(TType.KEYWORD_SQLEXCEPTION, terminal.symbol_id)
        self.assertEqual("sqlexception", terminal.symbol_value)

    def test_keyword_sqlstate(self):
        """测试解析 SQLSTATE 关键字"""
        terminal = parse_one_token("SQLSTATE")
        self.assertEqual(TType.KEYWORD_SQLSTATE, terminal.symbol_id)
        self.assertEqual("SQLSTATE", terminal.symbol_value)

        terminal = parse_one_token("sqlstate")
        self.assertEqual(TType.KEYWORD_SQLSTATE, terminal.symbol_id)
        self.assertEqual("sqlstate", terminal.symbol_value)

    def test_keyword_sqlwarning(self):
        """测试解析 SQLWARNING 关键字"""
        terminal = parse_one_token("SQLWARNING")
        self.assertEqual(TType.KEYWORD_SQLWARNING, terminal.symbol_id)
        self.assertEqual("SQLWARNING", terminal.symbol_value)

        terminal = parse_one_token("sqlwarning")
        self.assertEqual(TType.KEYWORD_SQLWARNING, terminal.symbol_id)
        self.assertEqual("sqlwarning", terminal.symbol_value)

    def test_keyword_sql_after_gtids(self):
        """测试解析 SQL_AFTER_GTIDS 关键字"""
        terminal = parse_one_token("SQL_AFTER_GTIDS")
        self.assertEqual(TType.KEYWORD_SQL_AFTER_GTIDS, terminal.symbol_id)
        self.assertEqual("SQL_AFTER_GTIDS", terminal.symbol_value)

        terminal = parse_one_token("sql_after_gtids")
        self.assertEqual(TType.KEYWORD_SQL_AFTER_GTIDS, terminal.symbol_id)
        self.assertEqual("sql_after_gtids", terminal.symbol_value)

    def test_keyword_sql_after_mts_gaps(self):
        """测试解析 SQL_AFTER_MTS_GAPS 关键字"""
        terminal = parse_one_token("SQL_AFTER_MTS_GAPS")
        self.assertEqual(TType.KEYWORD_SQL_AFTER_MTS_GAPS, terminal.symbol_id)
        self.assertEqual("SQL_AFTER_MTS_GAPS", terminal.symbol_value)

        terminal = parse_one_token("sql_after_mts_gaps")
        self.assertEqual(TType.KEYWORD_SQL_AFTER_MTS_GAPS, terminal.symbol_id)
        self.assertEqual("sql_after_mts_gaps", terminal.symbol_value)

    def test_keyword_sql_before_gtids(self):
        """测试解析 SQL_BEFORE_GTIDS 关键字"""
        terminal = parse_one_token("SQL_BEFORE_GTIDS")
        self.assertEqual(TType.KEYWORD_SQL_BEFORE_GTIDS, terminal.symbol_id)
        self.assertEqual("SQL_BEFORE_GTIDS", terminal.symbol_value)

        terminal = parse_one_token("sql_before_gtids")
        self.assertEqual(TType.KEYWORD_SQL_BEFORE_GTIDS, terminal.symbol_id)
        self.assertEqual("sql_before_gtids", terminal.symbol_value)

    def test_keyword_sql_big_result(self):
        """测试解析 SQL_BIG_RESULT 关键字"""
        terminal = parse_one_token("SQL_BIG_RESULT")
        self.assertEqual(TType.KEYWORD_SQL_BIG_RESULT, terminal.symbol_id)
        self.assertEqual("SQL_BIG_RESULT", terminal.symbol_value)

        terminal = parse_one_token("sql_big_result")
        self.assertEqual(TType.KEYWORD_SQL_BIG_RESULT, terminal.symbol_id)
        self.assertEqual("sql_big_result", terminal.symbol_value)

    def test_keyword_sql_buffer_result(self):
        """测试解析 SQL_BUFFER_RESULT 关键字"""
        terminal = parse_one_token("SQL_BUFFER_RESULT")
        self.assertEqual(TType.KEYWORD_SQL_BUFFER_RESULT, terminal.symbol_id)
        self.assertEqual("SQL_BUFFER_RESULT", terminal.symbol_value)

        terminal = parse_one_token("sql_buffer_result")
        self.assertEqual(TType.KEYWORD_SQL_BUFFER_RESULT, terminal.symbol_id)
        self.assertEqual("sql_buffer_result", terminal.symbol_value)

    def test_keyword_sql_calc_found_rows(self):
        """测试解析 SQL_CALC_FOUND_ROWS 关键字"""
        terminal = parse_one_token("SQL_CALC_FOUND_ROWS")
        self.assertEqual(TType.KEYWORD_SQL_CALC_FOUND_ROWS, terminal.symbol_id)
        self.assertEqual("SQL_CALC_FOUND_ROWS", terminal.symbol_value)

        terminal = parse_one_token("sql_calc_found_rows")
        self.assertEqual(TType.KEYWORD_SQL_CALC_FOUND_ROWS, terminal.symbol_id)
        self.assertEqual("sql_calc_found_rows", terminal.symbol_value)

    def test_keyword_sql_no_cache(self):
        """测试解析 SQL_NO_CACHE 关键字"""
        terminal = parse_one_token("SQL_NO_CACHE")
        self.assertEqual(TType.KEYWORD_SQL_NO_CACHE, terminal.symbol_id)
        self.assertEqual("SQL_NO_CACHE", terminal.symbol_value)

        terminal = parse_one_token("sql_no_cache")
        self.assertEqual(TType.KEYWORD_SQL_NO_CACHE, terminal.symbol_id)
        self.assertEqual("sql_no_cache", terminal.symbol_value)

    def test_keyword_sql_small_result(self):
        """测试解析 SQL_SMALL_RESULT 关键字"""
        terminal = parse_one_token("SQL_SMALL_RESULT")
        self.assertEqual(TType.KEYWORD_SQL_SMALL_RESULT, terminal.symbol_id)
        self.assertEqual("SQL_SMALL_RESULT", terminal.symbol_value)

        terminal = parse_one_token("sql_small_result")
        self.assertEqual(TType.KEYWORD_SQL_SMALL_RESULT, terminal.symbol_id)
        self.assertEqual("sql_small_result", terminal.symbol_value)

    def test_keyword_sql_thread(self):
        """测试解析 SQL_THREAD 关键字"""
        terminal = parse_one_token("SQL_THREAD")
        self.assertEqual(TType.KEYWORD_SQL_THREAD, terminal.symbol_id)
        self.assertEqual("SQL_THREAD", terminal.symbol_value)

        terminal = parse_one_token("sql_thread")
        self.assertEqual(TType.KEYWORD_SQL_THREAD, terminal.symbol_id)
        self.assertEqual("sql_thread", terminal.symbol_value)

    def test_keyword_sql_tsi_day(self):
        """测试解析 SQL_TSI_DAY 关键字"""
        terminal = parse_one_token("SQL_TSI_DAY")
        self.assertEqual(TType.KEYWORD_SQL_TSI_DAY, terminal.symbol_id)
        self.assertEqual("SQL_TSI_DAY", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_day")
        self.assertEqual(TType.KEYWORD_SQL_TSI_DAY, terminal.symbol_id)
        self.assertEqual("sql_tsi_day", terminal.symbol_value)

    def test_keyword_sql_tsi_hour(self):
        """测试解析 SQL_TSI_HOUR 关键字"""
        terminal = parse_one_token("SQL_TSI_HOUR")
        self.assertEqual(TType.KEYWORD_SQL_TSI_HOUR, terminal.symbol_id)
        self.assertEqual("SQL_TSI_HOUR", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_hour")
        self.assertEqual(TType.KEYWORD_SQL_TSI_HOUR, terminal.symbol_id)
        self.assertEqual("sql_tsi_hour", terminal.symbol_value)

    def test_keyword_sql_tsi_minute(self):
        """测试解析 SQL_TSI_MINUTE 关键字"""
        terminal = parse_one_token("SQL_TSI_MINUTE")
        self.assertEqual(TType.KEYWORD_SQL_TSI_MINUTE, terminal.symbol_id)
        self.assertEqual("SQL_TSI_MINUTE", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_minute")
        self.assertEqual(TType.KEYWORD_SQL_TSI_MINUTE, terminal.symbol_id)
        self.assertEqual("sql_tsi_minute", terminal.symbol_value)

    def test_keyword_sql_tsi_month(self):
        """测试解析 SQL_TSI_MONTH 关键字"""
        terminal = parse_one_token("SQL_TSI_MONTH")
        self.assertEqual(TType.KEYWORD_SQL_TSI_MONTH, terminal.symbol_id)
        self.assertEqual("SQL_TSI_MONTH", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_month")
        self.assertEqual(TType.KEYWORD_SQL_TSI_MONTH, terminal.symbol_id)
        self.assertEqual("sql_tsi_month", terminal.symbol_value)

    def test_keyword_sql_tsi_quarter(self):
        """测试解析 SQL_TSI_QUARTER 关键字"""
        terminal = parse_one_token("SQL_TSI_QUARTER")
        self.assertEqual(TType.KEYWORD_SQL_TSI_QUARTER, terminal.symbol_id)
        self.assertEqual("SQL_TSI_QUARTER", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_quarter")
        self.assertEqual(TType.KEYWORD_SQL_TSI_QUARTER, terminal.symbol_id)
        self.assertEqual("sql_tsi_quarter", terminal.symbol_value)

    def test_keyword_sql_tsi_second(self):
        """测试解析 SQL_TSI_SECOND 关键字"""
        terminal = parse_one_token("SQL_TSI_SECOND")
        self.assertEqual(TType.KEYWORD_SQL_TSI_SECOND, terminal.symbol_id)
        self.assertEqual("SQL_TSI_SECOND", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_second")
        self.assertEqual(TType.KEYWORD_SQL_TSI_SECOND, terminal.symbol_id)
        self.assertEqual("sql_tsi_second", terminal.symbol_value)

    def test_keyword_sql_tsi_week(self):
        """测试解析 SQL_TSI_WEEK 关键字"""
        terminal = parse_one_token("SQL_TSI_WEEK")
        self.assertEqual(TType.KEYWORD_SQL_TSI_WEEK, terminal.symbol_id)
        self.assertEqual("SQL_TSI_WEEK", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_week")
        self.assertEqual(TType.KEYWORD_SQL_TSI_WEEK, terminal.symbol_id)
        self.assertEqual("sql_tsi_week", terminal.symbol_value)

    def test_keyword_sql_tsi_year(self):
        """测试解析 SQL_TSI_YEAR 关键字"""
        terminal = parse_one_token("SQL_TSI_YEAR")
        self.assertEqual(TType.KEYWORD_SQL_TSI_YEAR, terminal.symbol_id)
        self.assertEqual("SQL_TSI_YEAR", terminal.symbol_value)

        terminal = parse_one_token("sql_tsi_year")
        self.assertEqual(TType.KEYWORD_SQL_TSI_YEAR, terminal.symbol_id)
        self.assertEqual("sql_tsi_year", terminal.symbol_value)

    def test_keyword_srid(self):
        """测试解析 SRID 关键字"""
        terminal = parse_one_token("SRID")
        self.assertEqual(TType.KEYWORD_SRID, terminal.symbol_id)
        self.assertEqual("SRID", terminal.symbol_value)

        terminal = parse_one_token("srid")
        self.assertEqual(TType.KEYWORD_SRID, terminal.symbol_id)
        self.assertEqual("srid", terminal.symbol_value)

    def test_keyword_ssl(self):
        """测试解析 SSL 关键字"""
        terminal = parse_one_token("SSL")
        self.assertEqual(TType.KEYWORD_SSL, terminal.symbol_id)
        self.assertEqual("SSL", terminal.symbol_value)

        terminal = parse_one_token("ssl")
        self.assertEqual(TType.KEYWORD_SSL, terminal.symbol_id)
        self.assertEqual("ssl", terminal.symbol_value)

    def test_keyword_stacked(self):
        """测试解析 STACKED 关键字"""
        terminal = parse_one_token("STACKED")
        self.assertEqual(TType.KEYWORD_STACKED, terminal.symbol_id)
        self.assertEqual("STACKED", terminal.symbol_value)

        terminal = parse_one_token("stacked")
        self.assertEqual(TType.KEYWORD_STACKED, terminal.symbol_id)
        self.assertEqual("stacked", terminal.symbol_value)

    def test_keyword_start(self):
        """测试解析 START 关键字"""
        terminal = parse_one_token("START")
        self.assertEqual(TType.KEYWORD_START, terminal.symbol_id)
        self.assertEqual("START", terminal.symbol_value)

        terminal = parse_one_token("start")
        self.assertEqual(TType.KEYWORD_START, terminal.symbol_id)
        self.assertEqual("start", terminal.symbol_value)

    def test_keyword_starting(self):
        """测试解析 STARTING 关键字"""
        terminal = parse_one_token("STARTING")
        self.assertEqual(TType.KEYWORD_STARTING, terminal.symbol_id)
        self.assertEqual("STARTING", terminal.symbol_value)

        terminal = parse_one_token("starting")
        self.assertEqual(TType.KEYWORD_STARTING, terminal.symbol_id)
        self.assertEqual("starting", terminal.symbol_value)

    def test_keyword_starts(self):
        """测试解析 STARTS 关键字"""
        terminal = parse_one_token("STARTS")
        self.assertEqual(TType.KEYWORD_STARTS, terminal.symbol_id)
        self.assertEqual("STARTS", terminal.symbol_value)

        terminal = parse_one_token("starts")
        self.assertEqual(TType.KEYWORD_STARTS, terminal.symbol_id)
        self.assertEqual("starts", terminal.symbol_value)

    def test_keyword_stats_auto_recalc(self):
        """测试解析 STATS_AUTO_RECALC 关键字"""
        terminal = parse_one_token("STATS_AUTO_RECALC")
        self.assertEqual(TType.KEYWORD_STATS_AUTO_RECALC, terminal.symbol_id)
        self.assertEqual("STATS_AUTO_RECALC", terminal.symbol_value)

        terminal = parse_one_token("stats_auto_recalc")
        self.assertEqual(TType.KEYWORD_STATS_AUTO_RECALC, terminal.symbol_id)
        self.assertEqual("stats_auto_recalc", terminal.symbol_value)

    def test_keyword_stats_persistent(self):
        """测试解析 STATS_PERSISTENT 关键字"""
        terminal = parse_one_token("STATS_PERSISTENT")
        self.assertEqual(TType.KEYWORD_STATS_PERSISTENT, terminal.symbol_id)
        self.assertEqual("STATS_PERSISTENT", terminal.symbol_value)

        terminal = parse_one_token("stats_persistent")
        self.assertEqual(TType.KEYWORD_STATS_PERSISTENT, terminal.symbol_id)
        self.assertEqual("stats_persistent", terminal.symbol_value)

    def test_keyword_stats_sample_pages(self):
        """测试解析 STATS_SAMPLE_PAGES 关键字"""
        terminal = parse_one_token("STATS_SAMPLE_PAGES")
        self.assertEqual(TType.KEYWORD_STATS_SAMPLE_PAGES, terminal.symbol_id)
        self.assertEqual("STATS_SAMPLE_PAGES", terminal.symbol_value)

        terminal = parse_one_token("stats_sample_pages")
        self.assertEqual(TType.KEYWORD_STATS_SAMPLE_PAGES, terminal.symbol_id)
        self.assertEqual("stats_sample_pages", terminal.symbol_value)

    def test_keyword_status(self):
        """测试解析 STATUS 关键字"""
        terminal = parse_one_token("STATUS")
        self.assertEqual(TType.KEYWORD_STATUS, terminal.symbol_id)
        self.assertEqual("STATUS", terminal.symbol_value)

        terminal = parse_one_token("status")
        self.assertEqual(TType.KEYWORD_STATUS, terminal.symbol_id)
        self.assertEqual("status", terminal.symbol_value)

    def test_keyword_stop(self):
        """测试解析 STOP 关键字"""
        terminal = parse_one_token("STOP")
        self.assertEqual(TType.KEYWORD_STOP, terminal.symbol_id)
        self.assertEqual("STOP", terminal.symbol_value)

        terminal = parse_one_token("stop")
        self.assertEqual(TType.KEYWORD_STOP, terminal.symbol_id)
        self.assertEqual("stop", terminal.symbol_value)

    def test_keyword_storage(self):
        """测试解析 STORAGE 关键字"""
        terminal = parse_one_token("STORAGE")
        self.assertEqual(TType.KEYWORD_STORAGE, terminal.symbol_id)
        self.assertEqual("STORAGE", terminal.symbol_value)

        terminal = parse_one_token("storage")
        self.assertEqual(TType.KEYWORD_STORAGE, terminal.symbol_id)
        self.assertEqual("storage", terminal.symbol_value)

    def test_keyword_stored(self):
        """测试解析 STORED 关键字"""
        terminal = parse_one_token("STORED")
        self.assertEqual(TType.KEYWORD_STORED, terminal.symbol_id)
        self.assertEqual("STORED", terminal.symbol_value)

        terminal = parse_one_token("stored")
        self.assertEqual(TType.KEYWORD_STORED, terminal.symbol_id)
        self.assertEqual("stored", terminal.symbol_value)

    def test_keyword_straight_join(self):
        """测试解析 STRAIGHT_JOIN 关键字"""
        terminal = parse_one_token("STRAIGHT_JOIN")
        self.assertEqual(TType.KEYWORD_STRAIGHT_JOIN, terminal.symbol_id)
        self.assertEqual("STRAIGHT_JOIN", terminal.symbol_value)

        terminal = parse_one_token("straight_join")
        self.assertEqual(TType.KEYWORD_STRAIGHT_JOIN, terminal.symbol_id)
        self.assertEqual("straight_join", terminal.symbol_value)

    def test_keyword_stream(self):
        """测试解析 STREAM 关键字"""
        terminal = parse_one_token("STREAM")
        self.assertEqual(TType.KEYWORD_STREAM, terminal.symbol_id)
        self.assertEqual("STREAM", terminal.symbol_value)

        terminal = parse_one_token("stream")
        self.assertEqual(TType.KEYWORD_STREAM, terminal.symbol_id)
        self.assertEqual("stream", terminal.symbol_value)

    def test_keyword_string(self):
        """测试解析 STRING 关键字"""
        terminal = parse_one_token("STRING")
        self.assertEqual(TType.KEYWORD_STRING, terminal.symbol_id)
        self.assertEqual("STRING", terminal.symbol_value)

        terminal = parse_one_token("string")
        self.assertEqual(TType.KEYWORD_STRING, terminal.symbol_id)
        self.assertEqual("string", terminal.symbol_value)

    def test_keyword_subclass_origin(self):
        """测试解析 SUBCLASS_ORIGIN 关键字"""
        terminal = parse_one_token("SUBCLASS_ORIGIN")
        self.assertEqual(TType.KEYWORD_SUBCLASS_ORIGIN, terminal.symbol_id)
        self.assertEqual("SUBCLASS_ORIGIN", terminal.symbol_value)

        terminal = parse_one_token("subclass_origin")
        self.assertEqual(TType.KEYWORD_SUBCLASS_ORIGIN, terminal.symbol_id)
        self.assertEqual("subclass_origin", terminal.symbol_value)

    def test_keyword_subject(self):
        """测试解析 SUBJECT 关键字"""
        terminal = parse_one_token("SUBJECT")
        self.assertEqual(TType.KEYWORD_SUBJECT, terminal.symbol_id)
        self.assertEqual("SUBJECT", terminal.symbol_value)

        terminal = parse_one_token("subject")
        self.assertEqual(TType.KEYWORD_SUBJECT, terminal.symbol_id)
        self.assertEqual("subject", terminal.symbol_value)

    def test_keyword_subpartition(self):
        """测试解析 SUBPARTITION 关键字"""
        terminal = parse_one_token("SUBPARTITION")
        self.assertEqual(TType.KEYWORD_SUBPARTITION, terminal.symbol_id)
        self.assertEqual("SUBPARTITION", terminal.symbol_value)

        terminal = parse_one_token("subpartition")
        self.assertEqual(TType.KEYWORD_SUBPARTITION, terminal.symbol_id)
        self.assertEqual("subpartition", terminal.symbol_value)

    def test_keyword_subpartitions(self):
        """测试解析 SUBPARTITIONS 关键字"""
        terminal = parse_one_token("SUBPARTITIONS")
        self.assertEqual(TType.KEYWORD_SUBPARTITIONS, terminal.symbol_id)
        self.assertEqual("SUBPARTITIONS", terminal.symbol_value)

        terminal = parse_one_token("subpartitions")
        self.assertEqual(TType.KEYWORD_SUBPARTITIONS, terminal.symbol_id)
        self.assertEqual("subpartitions", terminal.symbol_value)

    def test_keyword_super(self):
        """测试解析 SUPER 关键字"""
        terminal = parse_one_token("SUPER")
        self.assertEqual(TType.KEYWORD_SUPER, terminal.symbol_id)
        self.assertEqual("SUPER", terminal.symbol_value)

        terminal = parse_one_token("super")
        self.assertEqual(TType.KEYWORD_SUPER, terminal.symbol_id)
        self.assertEqual("super", terminal.symbol_value)

    def test_keyword_suspend(self):
        """测试解析 SUSPEND 关键字"""
        terminal = parse_one_token("SUSPEND")
        self.assertEqual(TType.KEYWORD_SUSPEND, terminal.symbol_id)
        self.assertEqual("SUSPEND", terminal.symbol_value)

        terminal = parse_one_token("suspend")
        self.assertEqual(TType.KEYWORD_SUSPEND, terminal.symbol_id)
        self.assertEqual("suspend", terminal.symbol_value)

    def test_keyword_swaps(self):
        """测试解析 SWAPS 关键字"""
        terminal = parse_one_token("SWAPS")
        self.assertEqual(TType.KEYWORD_SWAPS, terminal.symbol_id)
        self.assertEqual("SWAPS", terminal.symbol_value)

        terminal = parse_one_token("swaps")
        self.assertEqual(TType.KEYWORD_SWAPS, terminal.symbol_id)
        self.assertEqual("swaps", terminal.symbol_value)

    def test_keyword_switches(self):
        """测试解析 SWITCHES 关键字"""
        terminal = parse_one_token("SWITCHES")
        self.assertEqual(TType.KEYWORD_SWITCHES, terminal.symbol_id)
        self.assertEqual("SWITCHES", terminal.symbol_value)

        terminal = parse_one_token("switches")
        self.assertEqual(TType.KEYWORD_SWITCHES, terminal.symbol_id)
        self.assertEqual("switches", terminal.symbol_value)

    def test_keyword_system(self):
        """测试解析 SYSTEM 关键字"""
        terminal = parse_one_token("SYSTEM")
        self.assertEqual(TType.KEYWORD_SYSTEM, terminal.symbol_id)
        self.assertEqual("SYSTEM", terminal.symbol_value)

        terminal = parse_one_token("system")
        self.assertEqual(TType.KEYWORD_SYSTEM, terminal.symbol_id)
        self.assertEqual("system", terminal.symbol_value)

    def test_keyword_table(self):
        """测试解析 TABLE 关键字"""
        terminal = parse_one_token("TABLE")
        self.assertEqual(TType.KEYWORD_TABLE, terminal.symbol_id)
        self.assertEqual("TABLE", terminal.symbol_value)

        terminal = parse_one_token("table")
        self.assertEqual(TType.KEYWORD_TABLE, terminal.symbol_id)
        self.assertEqual("table", terminal.symbol_value)

    def test_keyword_tables(self):
        """测试解析 TABLES 关键字"""
        terminal = parse_one_token("TABLES")
        self.assertEqual(TType.KEYWORD_TABLES, terminal.symbol_id)
        self.assertEqual("TABLES", terminal.symbol_value)

        terminal = parse_one_token("tables")
        self.assertEqual(TType.KEYWORD_TABLES, terminal.symbol_id)
        self.assertEqual("tables", terminal.symbol_value)

    def test_keyword_tablesample(self):
        """测试解析 TABLESAMPLE 关键字"""
        terminal = parse_one_token("TABLESAMPLE")
        self.assertEqual(TType.KEYWORD_TABLESAMPLE, terminal.symbol_id)
        self.assertEqual("TABLESAMPLE", terminal.symbol_value)

        terminal = parse_one_token("tablesample")
        self.assertEqual(TType.KEYWORD_TABLESAMPLE, terminal.symbol_id)
        self.assertEqual("tablesample", terminal.symbol_value)

    def test_keyword_tablespace(self):
        """测试解析 TABLESPACE 关键字"""
        terminal = parse_one_token("TABLESPACE")
        self.assertEqual(TType.KEYWORD_TABLESPACE, terminal.symbol_id)
        self.assertEqual("TABLESPACE", terminal.symbol_value)

        terminal = parse_one_token("tablespace")
        self.assertEqual(TType.KEYWORD_TABLESPACE, terminal.symbol_id)
        self.assertEqual("tablespace", terminal.symbol_value)

    def test_keyword_table_checksum(self):
        """测试解析 TABLE_CHECKSUM 关键字"""
        terminal = parse_one_token("TABLE_CHECKSUM")
        self.assertEqual(TType.KEYWORD_TABLE_CHECKSUM, terminal.symbol_id)
        self.assertEqual("TABLE_CHECKSUM", terminal.symbol_value)

        terminal = parse_one_token("table_checksum")
        self.assertEqual(TType.KEYWORD_TABLE_CHECKSUM, terminal.symbol_id)
        self.assertEqual("table_checksum", terminal.symbol_value)

    def test_keyword_table_name(self):
        """测试解析 TABLE_NAME 关键字"""
        terminal = parse_one_token("TABLE_NAME")
        self.assertEqual(TType.KEYWORD_TABLE_NAME, terminal.symbol_id)
        self.assertEqual("TABLE_NAME", terminal.symbol_value)

        terminal = parse_one_token("table_name")
        self.assertEqual(TType.KEYWORD_TABLE_NAME, terminal.symbol_id)
        self.assertEqual("table_name", terminal.symbol_value)

    def test_keyword_temporary(self):
        """测试解析 TEMPORARY 关键字"""
        terminal = parse_one_token("TEMPORARY")
        self.assertEqual(TType.KEYWORD_TEMPORARY, terminal.symbol_id)
        self.assertEqual("TEMPORARY", terminal.symbol_value)

        terminal = parse_one_token("temporary")
        self.assertEqual(TType.KEYWORD_TEMPORARY, terminal.symbol_id)
        self.assertEqual("temporary", terminal.symbol_value)

    def test_keyword_temptable(self):
        """测试解析 TEMPTABLE 关键字"""
        terminal = parse_one_token("TEMPTABLE")
        self.assertEqual(TType.KEYWORD_TEMPTABLE, terminal.symbol_id)
        self.assertEqual("TEMPTABLE", terminal.symbol_value)

        terminal = parse_one_token("temptable")
        self.assertEqual(TType.KEYWORD_TEMPTABLE, terminal.symbol_id)
        self.assertEqual("temptable", terminal.symbol_value)

    def test_keyword_terminated(self):
        """测试解析 TERMINATED 关键字"""
        terminal = parse_one_token("TERMINATED")
        self.assertEqual(TType.KEYWORD_TERMINATED, terminal.symbol_id)
        self.assertEqual("TERMINATED", terminal.symbol_value)

        terminal = parse_one_token("terminated")
        self.assertEqual(TType.KEYWORD_TERMINATED, terminal.symbol_id)
        self.assertEqual("terminated", terminal.symbol_value)

    def test_keyword_text(self):
        """测试解析 TEXT 关键字"""
        terminal = parse_one_token("TEXT")
        self.assertEqual(TType.KEYWORD_TEXT, terminal.symbol_id)
        self.assertEqual("TEXT", terminal.symbol_value)

        terminal = parse_one_token("text")
        self.assertEqual(TType.KEYWORD_TEXT, terminal.symbol_id)
        self.assertEqual("text", terminal.symbol_value)

    def test_keyword_than(self):
        """测试解析 THAN 关键字"""
        terminal = parse_one_token("THAN")
        self.assertEqual(TType.KEYWORD_THAN, terminal.symbol_id)
        self.assertEqual("THAN", terminal.symbol_value)

        terminal = parse_one_token("than")
        self.assertEqual(TType.KEYWORD_THAN, terminal.symbol_id)
        self.assertEqual("than", terminal.symbol_value)

    def test_keyword_then(self):
        """测试解析 THEN 关键字"""
        terminal = parse_one_token("THEN")
        self.assertEqual(TType.KEYWORD_THEN, terminal.symbol_id)
        self.assertEqual("THEN", terminal.symbol_value)

        terminal = parse_one_token("then")
        self.assertEqual(TType.KEYWORD_THEN, terminal.symbol_id)
        self.assertEqual("then", terminal.symbol_value)

    def test_keyword_thread_priority(self):
        """测试解析 THREAD_PRIORITY 关键字"""
        terminal = parse_one_token("THREAD_PRIORITY")
        self.assertEqual(TType.KEYWORD_THREAD_PRIORITY, terminal.symbol_id)
        self.assertEqual("THREAD_PRIORITY", terminal.symbol_value)

        terminal = parse_one_token("thread_priority")
        self.assertEqual(TType.KEYWORD_THREAD_PRIORITY, terminal.symbol_id)
        self.assertEqual("thread_priority", terminal.symbol_value)

    def test_keyword_ties(self):
        """测试解析 TIES 关键字"""
        terminal = parse_one_token("TIES")
        self.assertEqual(TType.KEYWORD_TIES, terminal.symbol_id)
        self.assertEqual("TIES", terminal.symbol_value)

        terminal = parse_one_token("ties")
        self.assertEqual(TType.KEYWORD_TIES, terminal.symbol_id)
        self.assertEqual("ties", terminal.symbol_value)

    def test_keyword_time(self):
        """测试解析 TIME 关键字"""
        terminal = parse_one_token("TIME")
        self.assertEqual(TType.KEYWORD_TIME, terminal.symbol_id)
        self.assertEqual("TIME", terminal.symbol_value)

        terminal = parse_one_token("time")
        self.assertEqual(TType.KEYWORD_TIME, terminal.symbol_id)
        self.assertEqual("time", terminal.symbol_value)

    def test_keyword_timestamp(self):
        """测试解析 TIMESTAMP 关键字"""
        terminal = parse_one_token("TIMESTAMP")
        self.assertEqual(TType.KEYWORD_TIMESTAMP, terminal.symbol_id)
        self.assertEqual("TIMESTAMP", terminal.symbol_value)

        terminal = parse_one_token("timestamp")
        self.assertEqual(TType.KEYWORD_TIMESTAMP, terminal.symbol_id)
        self.assertEqual("timestamp", terminal.symbol_value)

    def test_keyword_timestamp_add(self):
        """测试解析 TIMESTAMP_ADD 关键字"""
        terminal = parse_one_token("TIMESTAMP_ADD")
        self.assertEqual(TType.KEYWORD_TIMESTAMP_ADD, terminal.symbol_id)
        self.assertEqual("TIMESTAMP_ADD", terminal.symbol_value)

        terminal = parse_one_token("timestamp_add")
        self.assertEqual(TType.KEYWORD_TIMESTAMP_ADD, terminal.symbol_id)
        self.assertEqual("timestamp_add", terminal.symbol_value)

    def test_keyword_timestamp_diff(self):
        """测试解析 TIMESTAMP_DIFF 关键字"""
        terminal = parse_one_token("TIMESTAMP_DIFF")
        self.assertEqual(TType.KEYWORD_TIMESTAMP_DIFF, terminal.symbol_id)
        self.assertEqual("TIMESTAMP_DIFF", terminal.symbol_value)

        terminal = parse_one_token("timestamp_diff")
        self.assertEqual(TType.KEYWORD_TIMESTAMP_DIFF, terminal.symbol_id)
        self.assertEqual("timestamp_diff", terminal.symbol_value)

    def test_keyword_tinyblob(self):
        """测试解析 TINYBLOB 关键字"""
        terminal = parse_one_token("TINYBLOB")
        self.assertEqual(TType.KEYWORD_TINYBLOB, terminal.symbol_id)
        self.assertEqual("TINYBLOB", terminal.symbol_value)

        terminal = parse_one_token("tinyblob")
        self.assertEqual(TType.KEYWORD_TINYBLOB, terminal.symbol_id)
        self.assertEqual("tinyblob", terminal.symbol_value)

    def test_keyword_tinyint(self):
        """测试解析 TINYINT 关键字"""
        terminal = parse_one_token("TINYINT")
        self.assertEqual(TType.KEYWORD_TINYINT, terminal.symbol_id)
        self.assertEqual("TINYINT", terminal.symbol_value)

        terminal = parse_one_token("tinyint")
        self.assertEqual(TType.KEYWORD_TINYINT, terminal.symbol_id)
        self.assertEqual("tinyint", terminal.symbol_value)

    def test_keyword_tinytext_syn(self):
        """测试解析 TINYTEXT_SYN 关键字"""
        terminal = parse_one_token("TINYTEXT_SYN")
        self.assertEqual(TType.KEYWORD_TINYTEXT_SYN, terminal.symbol_id)
        self.assertEqual("TINYTEXT_SYN", terminal.symbol_value)

        terminal = parse_one_token("tinytext_syn")
        self.assertEqual(TType.KEYWORD_TINYTEXT_SYN, terminal.symbol_id)
        self.assertEqual("tinytext_syn", terminal.symbol_value)

    def test_keyword_tls(self):
        """测试解析 TLS 关键字"""
        terminal = parse_one_token("TLS")
        self.assertEqual(TType.KEYWORD_TLS, terminal.symbol_id)
        self.assertEqual("TLS", terminal.symbol_value)

        terminal = parse_one_token("tls")
        self.assertEqual(TType.KEYWORD_TLS, terminal.symbol_id)
        self.assertEqual("tls", terminal.symbol_value)

    def test_keyword_to(self):
        """测试解析 TO 关键字"""
        terminal = parse_one_token("TO")
        self.assertEqual(TType.KEYWORD_TO, terminal.symbol_id)
        self.assertEqual("TO", terminal.symbol_value)

        terminal = parse_one_token("to")
        self.assertEqual(TType.KEYWORD_TO, terminal.symbol_id)
        self.assertEqual("to", terminal.symbol_value)

    def test_keyword_trailing(self):
        """测试解析 TRAILING 关键字"""
        terminal = parse_one_token("TRAILING")
        self.assertEqual(TType.KEYWORD_TRAILING, terminal.symbol_id)
        self.assertEqual("TRAILING", terminal.symbol_value)

        terminal = parse_one_token("trailing")
        self.assertEqual(TType.KEYWORD_TRAILING, terminal.symbol_id)
        self.assertEqual("trailing", terminal.symbol_value)

    def test_keyword_transaction(self):
        """测试解析 TRANSACTION 关键字"""
        terminal = parse_one_token("TRANSACTION")
        self.assertEqual(TType.KEYWORD_TRANSACTION, terminal.symbol_id)
        self.assertEqual("TRANSACTION", terminal.symbol_value)

        terminal = parse_one_token("transaction")
        self.assertEqual(TType.KEYWORD_TRANSACTION, terminal.symbol_id)
        self.assertEqual("transaction", terminal.symbol_value)

    def test_keyword_trigger(self):
        """测试解析 TRIGGER 关键字"""
        terminal = parse_one_token("TRIGGER")
        self.assertEqual(TType.KEYWORD_TRIGGER, terminal.symbol_id)
        self.assertEqual("TRIGGER", terminal.symbol_value)

        terminal = parse_one_token("trigger")
        self.assertEqual(TType.KEYWORD_TRIGGER, terminal.symbol_id)
        self.assertEqual("trigger", terminal.symbol_value)

    def test_keyword_triggers(self):
        """测试解析 TRIGGERS 关键字"""
        terminal = parse_one_token("TRIGGERS")
        self.assertEqual(TType.KEYWORD_TRIGGERS, terminal.symbol_id)
        self.assertEqual("TRIGGERS", terminal.symbol_value)

        terminal = parse_one_token("triggers")
        self.assertEqual(TType.KEYWORD_TRIGGERS, terminal.symbol_id)
        self.assertEqual("triggers", terminal.symbol_value)

    def test_keyword_true(self):
        """测试解析 TRUE 关键字"""
        terminal = parse_one_token("TRUE")
        self.assertEqual(TType.KEYWORD_TRUE, terminal.symbol_id)
        self.assertEqual("TRUE", terminal.symbol_value)

        terminal = parse_one_token("true")
        self.assertEqual(TType.KEYWORD_TRUE, terminal.symbol_id)
        self.assertEqual("true", terminal.symbol_value)

    def test_keyword_truncate(self):
        """测试解析 TRUNCATE 关键字"""
        terminal = parse_one_token("TRUNCATE")
        self.assertEqual(TType.KEYWORD_TRUNCATE, terminal.symbol_id)
        self.assertEqual("TRUNCATE", terminal.symbol_value)

        terminal = parse_one_token("truncate")
        self.assertEqual(TType.KEYWORD_TRUNCATE, terminal.symbol_id)
        self.assertEqual("truncate", terminal.symbol_value)

    def test_keyword_type(self):
        """测试解析 TYPE 关键字"""
        terminal = parse_one_token("TYPE")
        self.assertEqual(TType.KEYWORD_TYPE, terminal.symbol_id)
        self.assertEqual("TYPE", terminal.symbol_value)

        terminal = parse_one_token("type")
        self.assertEqual(TType.KEYWORD_TYPE, terminal.symbol_id)
        self.assertEqual("type", terminal.symbol_value)

    def test_keyword_types(self):
        """测试解析 TYPES 关键字"""
        terminal = parse_one_token("TYPES")
        self.assertEqual(TType.KEYWORD_TYPES, terminal.symbol_id)
        self.assertEqual("TYPES", terminal.symbol_value)

        terminal = parse_one_token("types")
        self.assertEqual(TType.KEYWORD_TYPES, terminal.symbol_id)
        self.assertEqual("types", terminal.symbol_value)

    def test_keyword_unbounded(self):
        """测试解析 UNBOUNDED 关键字"""
        terminal = parse_one_token("UNBOUNDED")
        self.assertEqual(TType.KEYWORD_UNBOUNDED, terminal.symbol_id)
        self.assertEqual("UNBOUNDED", terminal.symbol_value)

        terminal = parse_one_token("unbounded")
        self.assertEqual(TType.KEYWORD_UNBOUNDED, terminal.symbol_id)
        self.assertEqual("unbounded", terminal.symbol_value)

    def test_keyword_uncommitted(self):
        """测试解析 UNCOMMITTED 关键字"""
        terminal = parse_one_token("UNCOMMITTED")
        self.assertEqual(TType.KEYWORD_UNCOMMITTED, terminal.symbol_id)
        self.assertEqual("UNCOMMITTED", terminal.symbol_value)

        terminal = parse_one_token("uncommitted")
        self.assertEqual(TType.KEYWORD_UNCOMMITTED, terminal.symbol_id)
        self.assertEqual("uncommitted", terminal.symbol_value)

    def test_keyword_undefined(self):
        """测试解析 UNDEFINED 关键字"""
        terminal = parse_one_token("UNDEFINED")
        self.assertEqual(TType.KEYWORD_UNDEFINED, terminal.symbol_id)
        self.assertEqual("UNDEFINED", terminal.symbol_value)

        terminal = parse_one_token("undefined")
        self.assertEqual(TType.KEYWORD_UNDEFINED, terminal.symbol_id)
        self.assertEqual("undefined", terminal.symbol_value)

    def test_keyword_undo(self):
        """测试解析 UNDO 关键字"""
        terminal = parse_one_token("UNDO")
        self.assertEqual(TType.KEYWORD_UNDO, terminal.symbol_id)
        self.assertEqual("UNDO", terminal.symbol_value)

        terminal = parse_one_token("undo")
        self.assertEqual(TType.KEYWORD_UNDO, terminal.symbol_id)
        self.assertEqual("undo", terminal.symbol_value)

    def test_keyword_undofile(self):
        """测试解析 UNDOFILE 关键字"""
        terminal = parse_one_token("UNDOFILE")
        self.assertEqual(TType.KEYWORD_UNDOFILE, terminal.symbol_id)
        self.assertEqual("UNDOFILE", terminal.symbol_value)

        terminal = parse_one_token("undofile")
        self.assertEqual(TType.KEYWORD_UNDOFILE, terminal.symbol_id)
        self.assertEqual("undofile", terminal.symbol_value)

    def test_keyword_undo_buffer_size(self):
        """测试解析 UNDO_BUFFER_SIZE 关键字"""
        terminal = parse_one_token("UNDO_BUFFER_SIZE")
        self.assertEqual(TType.KEYWORD_UNDO_BUFFER_SIZE, terminal.symbol_id)
        self.assertEqual("UNDO_BUFFER_SIZE", terminal.symbol_value)

        terminal = parse_one_token("undo_buffer_size")
        self.assertEqual(TType.KEYWORD_UNDO_BUFFER_SIZE, terminal.symbol_id)
        self.assertEqual("undo_buffer_size", terminal.symbol_value)

    def test_keyword_unicode(self):
        """测试解析 UNICODE 关键字"""
        terminal = parse_one_token("UNICODE")
        self.assertEqual(TType.KEYWORD_UNICODE, terminal.symbol_id)
        self.assertEqual("UNICODE", terminal.symbol_value)

        terminal = parse_one_token("unicode")
        self.assertEqual(TType.KEYWORD_UNICODE, terminal.symbol_id)
        self.assertEqual("unicode", terminal.symbol_value)

    def test_keyword_uninstall(self):
        """测试解析 UNINSTALL 关键字"""
        terminal = parse_one_token("UNINSTALL")
        self.assertEqual(TType.KEYWORD_UNINSTALL, terminal.symbol_id)
        self.assertEqual("UNINSTALL", terminal.symbol_value)

        terminal = parse_one_token("uninstall")
        self.assertEqual(TType.KEYWORD_UNINSTALL, terminal.symbol_id)
        self.assertEqual("uninstall", terminal.symbol_value)

    def test_keyword_union(self):
        """测试解析 UNION 关键字"""
        terminal = parse_one_token("UNION")
        self.assertEqual(TType.KEYWORD_UNION, terminal.symbol_id)
        self.assertEqual("UNION", terminal.symbol_value)

        terminal = parse_one_token("union")
        self.assertEqual(TType.KEYWORD_UNION, terminal.symbol_id)
        self.assertEqual("union", terminal.symbol_value)

    def test_keyword_unique(self):
        """测试解析 UNIQUE 关键字"""
        terminal = parse_one_token("UNIQUE")
        self.assertEqual(TType.KEYWORD_UNIQUE, terminal.symbol_id)
        self.assertEqual("UNIQUE", terminal.symbol_value)

        terminal = parse_one_token("unique")
        self.assertEqual(TType.KEYWORD_UNIQUE, terminal.symbol_id)
        self.assertEqual("unique", terminal.symbol_value)

    def test_keyword_unknown(self):
        """测试解析 UNKNOWN 关键字"""
        terminal = parse_one_token("UNKNOWN")
        self.assertEqual(TType.KEYWORD_UNKNOWN, terminal.symbol_id)
        self.assertEqual("UNKNOWN", terminal.symbol_value)

        terminal = parse_one_token("unknown")
        self.assertEqual(TType.KEYWORD_UNKNOWN, terminal.symbol_id)
        self.assertEqual("unknown", terminal.symbol_value)

    def test_keyword_unlock(self):
        """测试解析 UNLOCK 关键字"""
        terminal = parse_one_token("UNLOCK")
        self.assertEqual(TType.KEYWORD_UNLOCK, terminal.symbol_id)
        self.assertEqual("UNLOCK", terminal.symbol_value)

        terminal = parse_one_token("unlock")
        self.assertEqual(TType.KEYWORD_UNLOCK, terminal.symbol_id)
        self.assertEqual("unlock", terminal.symbol_value)

    def test_keyword_unregister(self):
        """测试解析 UNREGISTER 关键字"""
        terminal = parse_one_token("UNREGISTER")
        self.assertEqual(TType.KEYWORD_UNREGISTER, terminal.symbol_id)
        self.assertEqual("UNREGISTER", terminal.symbol_value)

        terminal = parse_one_token("unregister")
        self.assertEqual(TType.KEYWORD_UNREGISTER, terminal.symbol_id)
        self.assertEqual("unregister", terminal.symbol_value)

    def test_keyword_unsigned(self):
        """测试解析 UNSIGNED 关键字"""
        terminal = parse_one_token("UNSIGNED")
        self.assertEqual(TType.KEYWORD_UNSIGNED, terminal.symbol_id)
        self.assertEqual("UNSIGNED", terminal.symbol_value)

        terminal = parse_one_token("unsigned")
        self.assertEqual(TType.KEYWORD_UNSIGNED, terminal.symbol_id)
        self.assertEqual("unsigned", terminal.symbol_value)

    def test_keyword_until(self):
        """测试解析 UNTIL 关键字"""
        terminal = parse_one_token("UNTIL")
        self.assertEqual(TType.KEYWORD_UNTIL, terminal.symbol_id)
        self.assertEqual("UNTIL", terminal.symbol_value)

        terminal = parse_one_token("until")
        self.assertEqual(TType.KEYWORD_UNTIL, terminal.symbol_id)
        self.assertEqual("until", terminal.symbol_value)

    def test_keyword_update(self):
        """测试解析 UPDATE 关键字"""
        terminal = parse_one_token("UPDATE")
        self.assertEqual(TType.KEYWORD_UPDATE, terminal.symbol_id)
        self.assertEqual("UPDATE", terminal.symbol_value)

        terminal = parse_one_token("update")
        self.assertEqual(TType.KEYWORD_UPDATE, terminal.symbol_id)
        self.assertEqual("update", terminal.symbol_value)

    def test_keyword_upgrade(self):
        """测试解析 UPGRADE 关键字"""
        terminal = parse_one_token("UPGRADE")
        self.assertEqual(TType.KEYWORD_UPGRADE, terminal.symbol_id)
        self.assertEqual("UPGRADE", terminal.symbol_value)

        terminal = parse_one_token("upgrade")
        self.assertEqual(TType.KEYWORD_UPGRADE, terminal.symbol_id)
        self.assertEqual("upgrade", terminal.symbol_value)

    def test_keyword_url(self):
        """测试解析 URL 关键字"""
        terminal = parse_one_token("URL")
        self.assertEqual(TType.KEYWORD_URL, terminal.symbol_id)
        self.assertEqual("URL", terminal.symbol_value)

        terminal = parse_one_token("url")
        self.assertEqual(TType.KEYWORD_URL, terminal.symbol_id)
        self.assertEqual("url", terminal.symbol_value)

    def test_keyword_usage(self):
        """测试解析 USAGE 关键字"""
        terminal = parse_one_token("USAGE")
        self.assertEqual(TType.KEYWORD_USAGE, terminal.symbol_id)
        self.assertEqual("USAGE", terminal.symbol_value)

        terminal = parse_one_token("usage")
        self.assertEqual(TType.KEYWORD_USAGE, terminal.symbol_id)
        self.assertEqual("usage", terminal.symbol_value)

    def test_keyword_use(self):
        """测试解析 USE 关键字"""
        terminal = parse_one_token("USE")
        self.assertEqual(TType.KEYWORD_USE, terminal.symbol_id)
        self.assertEqual("USE", terminal.symbol_value)

        terminal = parse_one_token("use")
        self.assertEqual(TType.KEYWORD_USE, terminal.symbol_id)
        self.assertEqual("use", terminal.symbol_value)

    def test_keyword_user(self):
        """测试解析 USER 关键字"""
        terminal = parse_one_token("USER")
        self.assertEqual(TType.KEYWORD_USER, terminal.symbol_id)
        self.assertEqual("USER", terminal.symbol_value)

        terminal = parse_one_token("user")
        self.assertEqual(TType.KEYWORD_USER, terminal.symbol_id)
        self.assertEqual("user", terminal.symbol_value)

    def test_keyword_user_resources(self):
        """测试解析 USER_RESOURCES 关键字"""
        terminal = parse_one_token("USER_RESOURCES")
        self.assertEqual(TType.KEYWORD_USER_RESOURCES, terminal.symbol_id)
        self.assertEqual("USER_RESOURCES", terminal.symbol_value)

        terminal = parse_one_token("user_resources")
        self.assertEqual(TType.KEYWORD_USER_RESOURCES, terminal.symbol_id)
        self.assertEqual("user_resources", terminal.symbol_value)

    def test_keyword_use_frm(self):
        """测试解析 USE_FRM 关键字"""
        terminal = parse_one_token("USE_FRM")
        self.assertEqual(TType.KEYWORD_USE_FRM, terminal.symbol_id)
        self.assertEqual("USE_FRM", terminal.symbol_value)

        terminal = parse_one_token("use_frm")
        self.assertEqual(TType.KEYWORD_USE_FRM, terminal.symbol_id)
        self.assertEqual("use_frm", terminal.symbol_value)

    def test_keyword_using(self):
        """测试解析 USING 关键字"""
        terminal = parse_one_token("USING")
        self.assertEqual(TType.KEYWORD_USING, terminal.symbol_id)
        self.assertEqual("USING", terminal.symbol_value)

        terminal = parse_one_token("using")
        self.assertEqual(TType.KEYWORD_USING, terminal.symbol_id)
        self.assertEqual("using", terminal.symbol_value)

    def test_keyword_utc_date(self):
        """测试解析 UTC_DATE 关键字"""
        terminal = parse_one_token("UTC_DATE")
        self.assertEqual(TType.KEYWORD_UTC_DATE, terminal.symbol_id)
        self.assertEqual("UTC_DATE", terminal.symbol_value)

        terminal = parse_one_token("utc_date")
        self.assertEqual(TType.KEYWORD_UTC_DATE, terminal.symbol_id)
        self.assertEqual("utc_date", terminal.symbol_value)

    def test_keyword_utc_time(self):
        """测试解析 UTC_TIME 关键字"""
        terminal = parse_one_token("UTC_TIME")
        self.assertEqual(TType.KEYWORD_UTC_TIME, terminal.symbol_id)
        self.assertEqual("UTC_TIME", terminal.symbol_value)

        terminal = parse_one_token("utc_time")
        self.assertEqual(TType.KEYWORD_UTC_TIME, terminal.symbol_id)
        self.assertEqual("utc_time", terminal.symbol_value)

    def test_keyword_utc_timestamp(self):
        """测试解析 UTC_TIMESTAMP 关键字"""
        terminal = parse_one_token("UTC_TIMESTAMP")
        self.assertEqual(TType.KEYWORD_UTC_TIMESTAMP, terminal.symbol_id)
        self.assertEqual("UTC_TIMESTAMP", terminal.symbol_value)

        terminal = parse_one_token("utc_timestamp")
        self.assertEqual(TType.KEYWORD_UTC_TIMESTAMP, terminal.symbol_id)
        self.assertEqual("utc_timestamp", terminal.symbol_value)

    def test_keyword_validation(self):
        """测试解析 VALIDATION 关键字"""
        terminal = parse_one_token("VALIDATION")
        self.assertEqual(TType.KEYWORD_VALIDATION, terminal.symbol_id)
        self.assertEqual("VALIDATION", terminal.symbol_value)

        terminal = parse_one_token("validation")
        self.assertEqual(TType.KEYWORD_VALIDATION, terminal.symbol_id)
        self.assertEqual("validation", terminal.symbol_value)

    def test_keyword_value(self):
        """测试解析 VALUE 关键字"""
        terminal = parse_one_token("VALUE")
        self.assertEqual(TType.KEYWORD_VALUE, terminal.symbol_id)
        self.assertEqual("VALUE", terminal.symbol_value)

        terminal = parse_one_token("value")
        self.assertEqual(TType.KEYWORD_VALUE, terminal.symbol_id)
        self.assertEqual("value", terminal.symbol_value)

    def test_keyword_values(self):
        """测试解析 VALUES 关键字"""
        terminal = parse_one_token("VALUES")
        self.assertEqual(TType.KEYWORD_VALUES, terminal.symbol_id)
        self.assertEqual("VALUES", terminal.symbol_value)

        terminal = parse_one_token("values")
        self.assertEqual(TType.KEYWORD_VALUES, terminal.symbol_id)
        self.assertEqual("values", terminal.symbol_value)

    def test_keyword_varbinary(self):
        """测试解析 VARBINARY 关键字"""
        terminal = parse_one_token("VARBINARY")
        self.assertEqual(TType.KEYWORD_VARBINARY, terminal.symbol_id)
        self.assertEqual("VARBINARY", terminal.symbol_value)

        terminal = parse_one_token("varbinary")
        self.assertEqual(TType.KEYWORD_VARBINARY, terminal.symbol_id)
        self.assertEqual("varbinary", terminal.symbol_value)

    def test_keyword_varchar(self):
        """测试解析 VARCHAR 关键字"""
        terminal = parse_one_token("VARCHAR")
        self.assertEqual(TType.KEYWORD_VARCHAR, terminal.symbol_id)
        self.assertEqual("VARCHAR", terminal.symbol_value)

        terminal = parse_one_token("varchar")
        self.assertEqual(TType.KEYWORD_VARCHAR, terminal.symbol_id)
        self.assertEqual("varchar", terminal.symbol_value)

    def test_keyword_varcharacter(self):
        """测试解析 VARCHARACTER 关键字"""
        terminal = parse_one_token("VARCHARACTER")
        self.assertEqual(TType.KEYWORD_VARCHARACTER, terminal.symbol_id)
        self.assertEqual("VARCHARACTER", terminal.symbol_value)

        terminal = parse_one_token("varcharacter")
        self.assertEqual(TType.KEYWORD_VARCHARACTER, terminal.symbol_id)
        self.assertEqual("varcharacter", terminal.symbol_value)

    def test_keyword_variables(self):
        """测试解析 VARIABLES 关键字"""
        terminal = parse_one_token("VARIABLES")
        self.assertEqual(TType.KEYWORD_VARIABLES, terminal.symbol_id)
        self.assertEqual("VARIABLES", terminal.symbol_value)

        terminal = parse_one_token("variables")
        self.assertEqual(TType.KEYWORD_VARIABLES, terminal.symbol_id)
        self.assertEqual("variables", terminal.symbol_value)

    def test_keyword_varying(self):
        """测试解析 VARYING 关键字"""
        terminal = parse_one_token("VARYING")
        self.assertEqual(TType.KEYWORD_VARYING, terminal.symbol_id)
        self.assertEqual("VARYING", terminal.symbol_value)

        terminal = parse_one_token("varying")
        self.assertEqual(TType.KEYWORD_VARYING, terminal.symbol_id)
        self.assertEqual("varying", terminal.symbol_value)

    def test_keyword_vcpu(self):
        """测试解析 VCPU 关键字"""
        terminal = parse_one_token("VCPU")
        self.assertEqual(TType.KEYWORD_VCPU, terminal.symbol_id)
        self.assertEqual("VCPU", terminal.symbol_value)

        terminal = parse_one_token("vcpu")
        self.assertEqual(TType.KEYWORD_VCPU, terminal.symbol_id)
        self.assertEqual("vcpu", terminal.symbol_value)

    def test_keyword_view(self):
        """测试解析 VIEW 关键字"""
        terminal = parse_one_token("VIEW")
        self.assertEqual(TType.KEYWORD_VIEW, terminal.symbol_id)
        self.assertEqual("VIEW", terminal.symbol_value)

        terminal = parse_one_token("view")
        self.assertEqual(TType.KEYWORD_VIEW, terminal.symbol_id)
        self.assertEqual("view", terminal.symbol_value)

    def test_keyword_virtual(self):
        """测试解析 VIRTUAL 关键字"""
        terminal = parse_one_token("VIRTUAL")
        self.assertEqual(TType.KEYWORD_VIRTUAL, terminal.symbol_id)
        self.assertEqual("VIRTUAL", terminal.symbol_value)

        terminal = parse_one_token("virtual")
        self.assertEqual(TType.KEYWORD_VIRTUAL, terminal.symbol_id)
        self.assertEqual("virtual", terminal.symbol_value)

    def test_keyword_visible(self):
        """测试解析 VISIBLE 关键字"""
        terminal = parse_one_token("VISIBLE")
        self.assertEqual(TType.KEYWORD_VISIBLE, terminal.symbol_id)
        self.assertEqual("VISIBLE", terminal.symbol_value)

        terminal = parse_one_token("visible")
        self.assertEqual(TType.KEYWORD_VISIBLE, terminal.symbol_id)
        self.assertEqual("visible", terminal.symbol_value)

    def test_keyword_wait(self):
        """测试解析 WAIT 关键字"""
        terminal = parse_one_token("WAIT")
        self.assertEqual(TType.KEYWORD_WAIT, terminal.symbol_id)
        self.assertEqual("WAIT", terminal.symbol_value)

        terminal = parse_one_token("wait")
        self.assertEqual(TType.KEYWORD_WAIT, terminal.symbol_id)
        self.assertEqual("wait", terminal.symbol_value)

    def test_keyword_warnings(self):
        """测试解析 WARNINGS 关键字"""
        terminal = parse_one_token("WARNINGS")
        self.assertEqual(TType.KEYWORD_WARNINGS, terminal.symbol_id)
        self.assertEqual("WARNINGS", terminal.symbol_value)

        terminal = parse_one_token("warnings")
        self.assertEqual(TType.KEYWORD_WARNINGS, terminal.symbol_id)
        self.assertEqual("warnings", terminal.symbol_value)

    def test_keyword_week(self):
        """测试解析 WEEK 关键字"""
        terminal = parse_one_token("WEEK")
        self.assertEqual(TType.KEYWORD_WEEK, terminal.symbol_id)
        self.assertEqual("WEEK", terminal.symbol_value)

        terminal = parse_one_token("week")
        self.assertEqual(TType.KEYWORD_WEEK, terminal.symbol_id)
        self.assertEqual("week", terminal.symbol_value)

    def test_keyword_weight_string(self):
        """测试解析 WEIGHT_STRING 关键字"""
        terminal = parse_one_token("WEIGHT_STRING")
        self.assertEqual(TType.KEYWORD_WEIGHT_STRING, terminal.symbol_id)
        self.assertEqual("WEIGHT_STRING", terminal.symbol_value)

        terminal = parse_one_token("weight_string")
        self.assertEqual(TType.KEYWORD_WEIGHT_STRING, terminal.symbol_id)
        self.assertEqual("weight_string", terminal.symbol_value)

    def test_keyword_when(self):
        """测试解析 WHEN 关键字"""
        terminal = parse_one_token("WHEN")
        self.assertEqual(TType.KEYWORD_WHEN, terminal.symbol_id)
        self.assertEqual("WHEN", terminal.symbol_value)

        terminal = parse_one_token("when")
        self.assertEqual(TType.KEYWORD_WHEN, terminal.symbol_id)
        self.assertEqual("when", terminal.symbol_value)

    def test_keyword_where(self):
        """测试解析 WHERE 关键字"""
        terminal = parse_one_token("WHERE")
        self.assertEqual(TType.KEYWORD_WHERE, terminal.symbol_id)
        self.assertEqual("WHERE", terminal.symbol_value)

        terminal = parse_one_token("where")
        self.assertEqual(TType.KEYWORD_WHERE, terminal.symbol_id)
        self.assertEqual("where", terminal.symbol_value)

    def test_keyword_while(self):
        """测试解析 WHILE 关键字"""
        terminal = parse_one_token("WHILE")
        self.assertEqual(TType.KEYWORD_WHILE, terminal.symbol_id)
        self.assertEqual("WHILE", terminal.symbol_value)

        terminal = parse_one_token("while")
        self.assertEqual(TType.KEYWORD_WHILE, terminal.symbol_id)
        self.assertEqual("while", terminal.symbol_value)

    def test_keyword_window(self):
        """测试解析 WINDOW 关键字"""
        terminal = parse_one_token("WINDOW")
        self.assertEqual(TType.KEYWORD_WINDOW, terminal.symbol_id)
        self.assertEqual("WINDOW", terminal.symbol_value)

        terminal = parse_one_token("window")
        self.assertEqual(TType.KEYWORD_WINDOW, terminal.symbol_id)
        self.assertEqual("window", terminal.symbol_value)

    def test_keyword_with(self):
        """测试解析 WITH 关键字"""
        terminal = parse_one_token("WITH")
        self.assertEqual(TType.KEYWORD_WITH, terminal.symbol_id)
        self.assertEqual("WITH", terminal.symbol_value)

        terminal = parse_one_token("with")
        self.assertEqual(TType.KEYWORD_WITH, terminal.symbol_id)
        self.assertEqual("with", terminal.symbol_value)

    def test_keyword_without(self):
        """测试解析 WITHOUT 关键字"""
        terminal = parse_one_token("WITHOUT")
        self.assertEqual(TType.KEYWORD_WITHOUT, terminal.symbol_id)
        self.assertEqual("WITHOUT", terminal.symbol_value)

        terminal = parse_one_token("without")
        self.assertEqual(TType.KEYWORD_WITHOUT, terminal.symbol_id)
        self.assertEqual("without", terminal.symbol_value)

    def test_keyword_work(self):
        """测试解析 WORK 关键字"""
        terminal = parse_one_token("WORK")
        self.assertEqual(TType.KEYWORD_WORK, terminal.symbol_id)
        self.assertEqual("WORK", terminal.symbol_value)

        terminal = parse_one_token("work")
        self.assertEqual(TType.KEYWORD_WORK, terminal.symbol_id)
        self.assertEqual("work", terminal.symbol_value)

    def test_keyword_wrapper(self):
        """测试解析 WRAPPER 关键字"""
        terminal = parse_one_token("WRAPPER")
        self.assertEqual(TType.KEYWORD_WRAPPER, terminal.symbol_id)
        self.assertEqual("WRAPPER", terminal.symbol_value)

        terminal = parse_one_token("wrapper")
        self.assertEqual(TType.KEYWORD_WRAPPER, terminal.symbol_id)
        self.assertEqual("wrapper", terminal.symbol_value)

    def test_keyword_write(self):
        """测试解析 WRITE 关键字"""
        terminal = parse_one_token("WRITE")
        self.assertEqual(TType.KEYWORD_WRITE, terminal.symbol_id)
        self.assertEqual("WRITE", terminal.symbol_value)

        terminal = parse_one_token("write")
        self.assertEqual(TType.KEYWORD_WRITE, terminal.symbol_id)
        self.assertEqual("write", terminal.symbol_value)

    def test_keyword_x509(self):
        """测试解析 X509 关键字"""
        terminal = parse_one_token("X509")
        self.assertEqual(TType.KEYWORD_X509, terminal.symbol_id)
        self.assertEqual("X509", terminal.symbol_value)

        terminal = parse_one_token("x509")
        self.assertEqual(TType.KEYWORD_X509, terminal.symbol_id)
        self.assertEqual("x509", terminal.symbol_value)

    def test_keyword_xa(self):
        """测试解析 XA 关键字"""
        terminal = parse_one_token("XA")
        self.assertEqual(TType.KEYWORD_XA, terminal.symbol_id)
        self.assertEqual("XA", terminal.symbol_value)

        terminal = parse_one_token("xa")
        self.assertEqual(TType.KEYWORD_XA, terminal.symbol_id)
        self.assertEqual("xa", terminal.symbol_value)

    def test_keyword_xid(self):
        """测试解析 XID 关键字"""
        terminal = parse_one_token("XID")
        self.assertEqual(TType.KEYWORD_XID, terminal.symbol_id)
        self.assertEqual("XID", terminal.symbol_value)

        terminal = parse_one_token("xid")
        self.assertEqual(TType.KEYWORD_XID, terminal.symbol_id)
        self.assertEqual("xid", terminal.symbol_value)

    def test_keyword_xml(self):
        """测试解析 XML 关键字"""
        terminal = parse_one_token("XML")
        self.assertEqual(TType.KEYWORD_XML, terminal.symbol_id)
        self.assertEqual("XML", terminal.symbol_value)

        terminal = parse_one_token("xml")
        self.assertEqual(TType.KEYWORD_XML, terminal.symbol_id)
        self.assertEqual("xml", terminal.symbol_value)

    def test_keyword_xor(self):
        """测试解析 XOR 关键字"""
        terminal = parse_one_token("XOR")
        self.assertEqual(TType.KEYWORD_XOR, terminal.symbol_id)
        self.assertEqual("XOR", terminal.symbol_value)

        terminal = parse_one_token("xor")
        self.assertEqual(TType.KEYWORD_XOR, terminal.symbol_id)
        self.assertEqual("xor", terminal.symbol_value)

    def test_keyword_year(self):
        """测试解析 YEAR 关键字"""
        terminal = parse_one_token("YEAR")
        self.assertEqual(TType.KEYWORD_YEAR, terminal.symbol_id)
        self.assertEqual("YEAR", terminal.symbol_value)

        terminal = parse_one_token("year")
        self.assertEqual(TType.KEYWORD_YEAR, terminal.symbol_id)
        self.assertEqual("year", terminal.symbol_value)

    def test_keyword_year_month(self):
        """测试解析 YEAR_MONTH 关键字"""
        terminal = parse_one_token("YEAR_MONTH")
        self.assertEqual(TType.KEYWORD_YEAR_MONTH, terminal.symbol_id)
        self.assertEqual("YEAR_MONTH", terminal.symbol_value)

        terminal = parse_one_token("year_month")
        self.assertEqual(TType.KEYWORD_YEAR_MONTH, terminal.symbol_id)
        self.assertEqual("year_month", terminal.symbol_value)

    def test_keyword_zerofill(self):
        """测试解析 ZEROFILL 关键字"""
        terminal = parse_one_token("ZEROFILL")
        self.assertEqual(TType.KEYWORD_ZEROFILL, terminal.symbol_id)
        self.assertEqual("ZEROFILL", terminal.symbol_value)

        terminal = parse_one_token("zerofill")
        self.assertEqual(TType.KEYWORD_ZEROFILL, terminal.symbol_id)
        self.assertEqual("zerofill", terminal.symbol_value)

    def test_keyword_zone(self):
        """测试解析 ZONE 关键字"""
        terminal = parse_one_token("ZONE")
        self.assertEqual(TType.KEYWORD_ZONE, terminal.symbol_id)
        self.assertEqual("ZONE", terminal.symbol_value)

        terminal = parse_one_token("zone")
        self.assertEqual(TType.KEYWORD_ZONE, terminal.symbol_id)
        self.assertEqual("zone", terminal.symbol_value)

    def test_keyword_with_rollup(self):
        """测试解析 WITH_ROLLUP 关键字"""
        terminal = parse_one_token("WITH_ROLLUP")
        self.assertEqual(TType.KEYWORD_WITH_ROLLUP, terminal.symbol_id)
        self.assertEqual("WITH_ROLLUP", terminal.symbol_value)

        terminal = parse_one_token("with_rollup")
        self.assertEqual(TType.KEYWORD_WITH_ROLLUP, terminal.symbol_id)
        self.assertEqual("with_rollup", terminal.symbol_value)
