"""
SYSTEM_END_OF_INPUT(0): 终结符
SYSTEM_ABORT(1): 终结符
OPERATOR_PLUS(2): 终结符
OPERATOR_CARET(3): 终结符
OPERATOR_TILDE(4): 终结符
OPERATOR_PERCENT(5): 终结符
OPERATOR_SUB(6): 终结符
OPERATOR_LT(7): 终结符
OPERATOR_GT(8): 终结符
OPERATOR_EQ(9): 终结符
OPERATOR_STAR(10): 终结符
OPERATOR_SLASH(11): 终结符
OPERATOR_BANG(12): 终结符
OPERATOR_AMP(13): 终结符
OPERATOR_BAR(14): 终结符
OPERATOR_COLON(15): 终结符
OPERATOR_LPAREN(16): 终结符
OPERATOR_RPAREN(17): 终结符
OPERATOR_COMMA(18): 终结符
OPERATOR_LBRACE(19): 终结符
OPERATOR_RBRACE(20): 终结符
OPERATOR_DOT(21): 终结符
OPERATOR_AT(22): 终结符
OPERATOR_SEMICOLON(23): 终结符
OPERATOR_DOLLAR(24): 终结符
OPERATOR_AMP_AMP(25): 终结符
OPERATOR_LT_EQ_GT(26): 终结符
OPERATOR_GT_EQ(27): 终结符
OPERATOR_LT_EQ(28): 终结符
OPERATOR_BANG_EQ(29): 终结符
OPERATOR_BAR_BAR(30): 终结符
OPERATOR_LT_LT(31): 终结符
OPERATOR_GT_GT(32): 终结符
OPERATOR_SUB_GT(33): 终结符
OPERATOR_SUB_GT_GT(34): 终结符
OPERATOR_COLON_EQ(35): 终结符
LITERAL_BIN_NUM(36): 终结符
LITERAL_HEX_NUM(37): 终结符
LITERAL_DECIMAL_NUM(38): 终结符
LITERAL_FLOAT_NUM(39): 终结符
LITERAL_INT_NUM(40): 终结符
LITERAL_NCHAR_STRING(41): 终结符
LITERAL_TEXT_STRING(42): 终结符
LITERAL_UNDERSCORE_CHARSET(43): 终结符
IDENT(44): 终结符
IDENT_QUOTED(45): 终结符
LEX_HOSTNAME(46): 终结符
PARAM_MARKER(47): 终结符
KEYWORD_ACCESSIBLE(48): 终结符
KEYWORD_ACCOUNT(49): 终结符
KEYWORD_ACTION(50): 终结符
KEYWORD_ACTIVE(51): 终结符
KEYWORD_ADD(52): 终结符
KEYWORD_ADMIN(53): 终结符
KEYWORD_AFTER(54): 终结符
KEYWORD_AGAINST(55): 终结符
KEYWORD_AGGREGATE(56): 终结符
KEYWORD_ALGORITHM(57): 终结符
KEYWORD_ALL(58): 终结符
KEYWORD_ALTER(59): 终结符
KEYWORD_ALWAYS(60): 终结符
KEYWORD_ANALYZE(61): 终结符
KEYWORD_AND(62): 终结符
KEYWORD_ANY(63): 终结符
KEYWORD_ARRAY(64): 终结符
KEYWORD_AS(65): 终结符
KEYWORD_ASC(66): 终结符
KEYWORD_ASCII(67): 终结符
KEYWORD_ASENSITIVE(68): 终结符
KEYWORD_AT(69): 终结符
KEYWORD_ATTRIBUTE(70): 终结符
KEYWORD_AUTHENTICATION(71): 终结符
KEYWORD_AUTO_INC(72): 终结符
KEYWORD_AUTOEXTEND_SIZE(73): 终结符
KEYWORD_AUTO_INCREMENT(74): 终结符
KEYWORD_AVG(75): 终结符
KEYWORD_AVG_ROW_LENGTH(76): 终结符
KEYWORD_BACKUP(77): 终结符
KEYWORD_BEFORE(78): 终结符
KEYWORD_BEGIN(79): 终结符
KEYWORD_BERNOULLI(80): 终结符
KEYWORD_BETWEEN(81): 终结符
KEYWORD_BIGINT(82): 终结符
KEYWORD_BINARY(83): 终结符
KEYWORD_BINLOG(84): 终结符
KEYWORD_BIT(85): 终结符
KEYWORD_BLOB(86): 终结符
KEYWORD_BLOCK(87): 终结符
KEYWORD_BOOL(88): 终结符
KEYWORD_BOOLEAN(89): 终结符
KEYWORD_BOTH(90): 终结符
KEYWORD_BTREE(91): 终结符
KEYWORD_BUCKETS(92): 终结符
KEYWORD_BULK(93): 终结符
KEYWORD_BY(94): 终结符
KEYWORD_BYTE(95): 终结符
KEYWORD_CACHE(96): 终结符
KEYWORD_CALL(97): 终结符
KEYWORD_CASCADE(98): 终结符
KEYWORD_CASCADED(99): 终结符
KEYWORD_CASE(100): 终结符
KEYWORD_CATALOG_NAME(101): 终结符
KEYWORD_CHAIN(102): 终结符
KEYWORD_CHALLENGE_RESPONSE(103): 终结符
KEYWORD_CHANGE(104): 终结符
KEYWORD_CHANGED(105): 终结符
KEYWORD_CHANNEL(106): 终结符
KEYWORD_CHAR(107): 终结符
KEYWORD_CHARACTER(108): 终结符
KEYWORD_CHARSET(109): 终结符
KEYWORD_CHECK(110): 终结符
KEYWORD_CHECKSUM(111): 终结符
KEYWORD_CIPHER(112): 终结符
KEYWORD_CLASS_ORIGIN(113): 终结符
KEYWORD_CLIENT(114): 终结符
KEYWORD_CLONE(115): 终结符
KEYWORD_CLOSE(116): 终结符
KEYWORD_COALESCE(117): 终结符
KEYWORD_CODE(118): 终结符
KEYWORD_COLLATE(119): 终结符
KEYWORD_COLLATION(120): 终结符
KEYWORD_COLUMN(121): 终结符
KEYWORD_COLUMNS(122): 终结符
KEYWORD_COLUMN_FORMAT(123): 终结符
KEYWORD_COLUMN_NAME(124): 终结符
KEYWORD_COMMENT(125): 终结符
KEYWORD_COMMIT(126): 终结符
KEYWORD_COMMITTED(127): 终结符
KEYWORD_COMPACT(128): 终结符
KEYWORD_COMPLETION(129): 终结符
KEYWORD_COMPONENT(130): 终结符
KEYWORD_COMPRESSED(131): 终结符
KEYWORD_COMPRESSION(132): 终结符
KEYWORD_CONCURRENT(133): 终结符
KEYWORD_CONDITION(134): 终结符
KEYWORD_CONNECTION(135): 终结符
KEYWORD_CONSISTENT(136): 终结符
KEYWORD_CONSTRAINT(137): 终结符
KEYWORD_CONSTRAINT_CATALOG(138): 终结符
KEYWORD_CONSTRAINT_NAME(139): 终结符
KEYWORD_CONSTRAINT_SCHEMA(140): 终结符
KEYWORD_CONTAINS(141): 终结符
KEYWORD_CONTEXT(142): 终结符
KEYWORD_CONTINUE(143): 终结符
KEYWORD_CONVERT(144): 终结符
KEYWORD_CPU(145): 终结符
KEYWORD_CREATE(146): 终结符
KEYWORD_CROSS(147): 终结符
KEYWORD_CUBE(148): 终结符
KEYWORD_CUME_DIST(149): 终结符
KEYWORD_CURRENT(150): 终结符
KEYWORD_CURRENT_DATE(151): 终结符
KEYWORD_CURRENT_TIME(152): 终结符
KEYWORD_CURRENT_TIMESTAMP(153): 终结符
KEYWORD_CURRENT_USER(154): 终结符
KEYWORD_CURSOR(155): 终结符
KEYWORD_CURSOR_NAME(156): 终结符
KEYWORD_DATA(157): 终结符
KEYWORD_DATABASE(158): 终结符
KEYWORD_DATABASES(159): 终结符
KEYWORD_DATAFILE(160): 终结符
KEYWORD_DATE(161): 终结符
KEYWORD_DATETIME(162): 终结符
KEYWORD_DAY(163): 终结符
KEYWORD_DAY_HOUR(164): 终结符
KEYWORD_DAY_MICROSECOND(165): 终结符
KEYWORD_DAY_MINUTE(166): 终结符
KEYWORD_DAY_SECOND(167): 终结符
KEYWORD_DEALLOCATE(168): 终结符
KEYWORD_DEC(169): 终结符
KEYWORD_DECIMAL(170): 终结符
KEYWORD_DECLARE(171): 终结符
KEYWORD_DEFAULT(172): 终结符
KEYWORD_DEFAULT_AUTH(173): 终结符
KEYWORD_DEFINER(174): 终结符
KEYWORD_DEFINITION(175): 终结符
KEYWORD_DELAYED(176): 终结符
KEYWORD_DELAY_KEY_WRITE(177): 终结符
KEYWORD_DELETE(178): 终结符
KEYWORD_DENSE_RANK(179): 终结符
KEYWORD_DESC(180): 终结符
KEYWORD_DESCRIBE(181): 终结符
KEYWORD_DESCRIPTION(182): 终结符
KEYWORD_DETERMINISTIC(183): 终结符
KEYWORD_DIAGNOSTICS(184): 终结符
KEYWORD_DIRECTORY(185): 终结符
KEYWORD_DISABLE(186): 终结符
KEYWORD_DISCARD(187): 终结符
KEYWORD_DISK(188): 终结符
KEYWORD_DISTINCT(189): 终结符
KEYWORD_DISTINCTROW(190): 终结符
KEYWORD_DIV(191): 终结符
KEYWORD_DO(192): 终结符
KEYWORD_DOUBLE(193): 终结符
KEYWORD_DROP(194): 终结符
KEYWORD_DUAL(195): 终结符
KEYWORD_DUMPFILE(196): 终结符
KEYWORD_DUPLICATE(197): 终结符
KEYWORD_DYNAMIC(198): 终结符
KEYWORD_EACH(199): 终结符
KEYWORD_ELSE(200): 终结符
KEYWORD_ELSEIF(201): 终结符
KEYWORD_EMPTY(202): 终结符
KEYWORD_ENABLE(203): 终结符
KEYWORD_ENCLOSED(204): 终结符
KEYWORD_ENCRYPTION(205): 终结符
KEYWORD_END(206): 终结符
KEYWORD_ENDS(207): 终结符
KEYWORD_ENFORCED(208): 终结符
KEYWORD_ENGINE(209): 终结符
KEYWORD_ENGINES(210): 终结符
KEYWORD_ENGINE_ATTRIBUTE(211): 终结符
KEYWORD_ENUM(212): 终结符
KEYWORD_ERROR(213): 终结符
KEYWORD_ERRORS(214): 终结符
KEYWORD_ESCAPE(215): 终结符
KEYWORD_ESCAPED(216): 终结符
KEYWORD_EVENT(217): 终结符
KEYWORD_EVENTS(218): 终结符
KEYWORD_EVERY(219): 终结符
KEYWORD_EXCEPT(220): 终结符
KEYWORD_EXCHANGE(221): 终结符
KEYWORD_EXCLUDE(222): 终结符
KEYWORD_EXECUTE(223): 终结符
KEYWORD_EXISTS(224): 终结符
KEYWORD_EXIT(225): 终结符
KEYWORD_EXPANSION(226): 终结符
KEYWORD_EXPIRE(227): 终结符
KEYWORD_EXPLAIN(228): 终结符
KEYWORD_EXPORT(229): 终结符
KEYWORD_EXTENDED(230): 终结符
KEYWORD_EXTENT_SIZE(231): 终结符
KEYWORD_FACTOR(232): 终结符
KEYWORD_FAILED_LOGIN_ATTEMPTS(233): 终结符
KEYWORD_FALSE(234): 终结符
KEYWORD_FAST(235): 终结符
KEYWORD_FAULTS(236): 终结符
KEYWORD_FETCH(237): 终结符
KEYWORD_FIELDS(238): 终结符
KEYWORD_FILE(239): 终结符
KEYWORD_FILE_BLOCK_SIZE(240): 终结符
KEYWORD_FILTER(241): 终结符
KEYWORD_FINISH(242): 终结符
KEYWORD_FIRST(243): 终结符
KEYWORD_FIRST_VALUE(244): 终结符
KEYWORD_FIXED(245): 终结符
KEYWORD_FLOAT(246): 终结符
KEYWORD_FLOAT4(247): 终结符
KEYWORD_FLOAT8(248): 终结符
KEYWORD_FLUSH(249): 终结符
KEYWORD_FOLLOWING(250): 终结符
KEYWORD_FOLLOWS(251): 终结符
KEYWORD_FOR(252): 终结符
KEYWORD_FORCE(253): 终结符
KEYWORD_FOREIGN(254): 终结符
KEYWORD_FORMAT(255): 终结符
KEYWORD_FOUND(256): 终结符
KEYWORD_FROM(257): 终结符
KEYWORD_FULL(258): 终结符
KEYWORD_FULLTEXT(259): 终结符
KEYWORD_FUNCTION(260): 终结符
KEYWORD_GENERAL(261): 终结符
KEYWORD_GENERATE(262): 终结符
KEYWORD_GENERATED(263): 终结符
KEYWORD_GEOMCOLLECTION(264): 终结符
KEYWORD_GEOMETRY(265): 终结符
KEYWORD_GEOMETRYCOLLECTION(266): 终结符
KEYWORD_GET(267): 终结符
KEYWORD_GET_MASTER_PUBLIC_KEY(268): 终结符
KEYWORD_GET_FORMAT(269): 终结符
KEYWORD_GET_SOURCE_PUBLIC_KEY(270): 终结符
KEYWORD_GLOBAL(271): 终结符
KEYWORD_GRANT(272): 终结符
KEYWORD_GRANTS(273): 终结符
KEYWORD_GROUP(274): 终结符
KEYWORD_GROUPING(275): 终结符
KEYWORD_GROUPS(276): 终结符
KEYWORD_GROUP_REPLICATION(277): 终结符
KEYWORD_GTIDS(278): 终结符
KEYWORD_GTID_ONLY(279): 终结符
KEYWORD_HANDLER(280): 终结符
KEYWORD_HASH(281): 终结符
KEYWORD_HAVING(282): 终结符
KEYWORD_HELP(283): 终结符
KEYWORD_HIGH_PRIORITY(284): 终结符
KEYWORD_HISTOGRAM(285): 终结符
KEYWORD_HISTORY(286): 终结符
KEYWORD_HOST(287): 终结符
KEYWORD_HOSTS(288): 终结符
KEYWORD_HOUR(289): 终结符
KEYWORD_HOUR_MICROSECOND(290): 终结符
KEYWORD_HOUR_MINUTE(291): 终结符
KEYWORD_HOUR_SECOND(292): 终结符
KEYWORD_IDENTIFIED(293): 终结符
KEYWORD_IF(294): 终结符
KEYWORD_IGNORE(295): 终结符
KEYWORD_IGNORE_SERVER_IDS(296): 终结符
KEYWORD_IMPORT(297): 终结符
KEYWORD_IN(298): 终结符
KEYWORD_INACTIVE(299): 终结符
KEYWORD_INDEX(300): 终结符
KEYWORD_INDEXES(301): 终结符
KEYWORD_INFILE(302): 终结符
KEYWORD_INITIAL(303): 终结符
KEYWORD_INITIAL_SIZE(304): 终结符
KEYWORD_INITIATE(305): 终结符
KEYWORD_INNER(306): 终结符
KEYWORD_INOUT(307): 终结符
KEYWORD_INSENSITIVE(308): 终结符
KEYWORD_INSERT(309): 终结符
KEYWORD_INSERT_METHOD(310): 终结符
KEYWORD_INSTALL(311): 终结符
KEYWORD_INSTANCE(312): 终结符
KEYWORD_INT(313): 终结符
KEYWORD_INT1(314): 终结符
KEYWORD_INT2(315): 终结符
KEYWORD_INT3(316): 终结符
KEYWORD_INT4(317): 终结符
KEYWORD_INT8(318): 终结符
KEYWORD_INTEGER(319): 终结符
KEYWORD_INTERSECT(320): 终结符
KEYWORD_INTERVAL(321): 终结符
KEYWORD_INTO(322): 终结符
KEYWORD_INVISIBLE(323): 终结符
KEYWORD_INVOKER(324): 终结符
KEYWORD_IO(325): 终结符
KEYWORD_IO_AFTER_GTIDS(326): 终结符
KEYWORD_IO_BEFORE_GTIDS(327): 终结符
KEYWORD_IO_THREAD(328): 终结符
KEYWORD_IPC(329): 终结符
KEYWORD_IS(330): 终结符
KEYWORD_ISOLATION(331): 终结符
KEYWORD_ISSUER(332): 终结符
KEYWORD_ITERATE(333): 终结符
KEYWORD_JOIN(334): 终结符
KEYWORD_JSON(335): 终结符
KEYWORD_JSON_TABLE(336): 终结符
KEYWORD_JSON_VALUE(337): 终结符
KEYWORD_KEY(338): 终结符
KEYWORD_KEYRING(339): 终结符
KEYWORD_KEYS(340): 终结符
KEYWORD_KEY_BLOCK_SIZE(341): 终结符
KEYWORD_KILL(342): 终结符
KEYWORD_LAG(343): 终结符
KEYWORD_LANGUAGE(344): 终结符
KEYWORD_LAST(345): 终结符
KEYWORD_LAST_VALUE(346): 终结符
KEYWORD_LATERAL(347): 终结符
KEYWORD_LEAD(348): 终结符
KEYWORD_LEADING(349): 终结符
KEYWORD_LEAVE(350): 终结符
KEYWORD_LEAVES(351): 终结符
KEYWORD_LEFT(352): 终结符
KEYWORD_LESS(353): 终结符
KEYWORD_LEVEL(354): 终结符
KEYWORD_LIKE(355): 终结符
KEYWORD_LIMIT(356): 终结符
KEYWORD_LINEAR(357): 终结符
KEYWORD_LINES(358): 终结符
KEYWORD_LINESTRING(359): 终结符
KEYWORD_LIST(360): 终结符
KEYWORD_LOAD(361): 终结符
KEYWORD_LOCAL(362): 终结符
KEYWORD_LOCALTIME(363): 终结符
KEYWORD_LOCALTIMESTAMP(364): 终结符
KEYWORD_LOCK(365): 终结符
KEYWORD_LOCKED(366): 终结符
KEYWORD_LOCKS(367): 终结符
KEYWORD_LOG(368): 终结符
KEYWORD_LOGFILE(369): 终结符
KEYWORD_LOGS(370): 终结符
KEYWORD_LONG(371): 终结符
KEYWORD_LONGBLOB(372): 终结符
KEYWORD_LONGTEXT(373): 终结符
KEYWORD_LOOP(374): 终结符
KEYWORD_LOW_PRIORITY(375): 终结符
KEYWORD_MANUAL(376): 终结符
KEYWORD_MASTER(377): 终结符
KEYWORD_MASTER_AUTO_POSITION(378): 终结符
KEYWORD_MASTER_BIND(379): 终结符
KEYWORD_MASTER_COMPRESSION_ALGORITHM(380): 终结符
KEYWORD_MASTER_CONNECT_RETRY(381): 终结符
KEYWORD_MASTER_DELAY(382): 终结符
KEYWORD_MASTER_HEARTBEAT_PERIOD(383): 终结符
KEYWORD_MASTER_HOST(384): 终结符
KEYWORD_MASTER_LOG_FILE(385): 终结符
KEYWORD_MASTER_LOG_POS(386): 终结符
KEYWORD_MASTER_PASSWORD(387): 终结符
KEYWORD_MASTER_PORT(388): 终结符
KEYWORD_MASTER_PUBLIC_KEY_PATH(389): 终结符
KEYWORD_MASTER_RETRY_COUNT(390): 终结符
KEYWORD_MASTER_SSL(391): 终结符
KEYWORD_MASTER_SSL_CA(392): 终结符
KEYWORD_MASTER_SSL_CAPATH(393): 终结符
KEYWORD_MASTER_SSL_CERT(394): 终结符
KEYWORD_MASTER_SSL_CIPHER(395): 终结符
KEYWORD_MASTER_SSL_CRL(396): 终结符
KEYWORD_MASTER_SSL_CRLPATH(397): 终结符
KEYWORD_MASTER_SSL_KEY(398): 终结符
KEYWORD_MASTER_SSL_VERIFY_SERVER_CERT(399): 终结符
KEYWORD_MASTER_TLS_CIPHERSUITES(400): 终结符
KEYWORD_MASTER_TLS_VERSION(401): 终结符
KEYWORD_MASTER_USER(402): 终结符
KEYWORD_MASTER_ZSTD_COMPRESSION_LEVEL(403): 终结符
KEYWORD_MATCH(404): 终结符
KEYWORD_MAX_VALUE(405): 终结符
KEYWORD_MAX_CONNECTIONS_PER_HOUR(406): 终结符
KEYWORD_MAX_QUERIES_PER_HOUR(407): 终结符
KEYWORD_MAX_ROWS(408): 终结符
KEYWORD_MAX_SIZE(409): 终结符
KEYWORD_MAX_UPDATES_PER_HOUR(410): 终结符
KEYWORD_MAX_USER_CONNECTIONS(411): 终结符
KEYWORD_MEDIUM(412): 终结符
KEYWORD_MEDIUMBLOB(413): 终结符
KEYWORD_MEDIUMINT(414): 终结符
KEYWORD_MEDIUMTEXT(415): 终结符
KEYWORD_MEMBER(416): 终结符
KEYWORD_MEMORY(417): 终结符
KEYWORD_MERGE(418): 终结符
KEYWORD_MESSAGE_TEXT(419): 终结符
KEYWORD_MICROSECOND(420): 终结符
KEYWORD_MIDDLEINT(421): 终结符
KEYWORD_MIGRATE(422): 终结符
KEYWORD_MINUTE(423): 终结符
KEYWORD_MINUTE_MICROSECOND(424): 终结符
KEYWORD_MINUTE_SECOND(425): 终结符
KEYWORD_MIN_ROWS(426): 终结符
KEYWORD_MOD(427): 终结符
KEYWORD_MODE(428): 终结符
KEYWORD_MODIFIES(429): 终结符
KEYWORD_MODIFY(430): 终结符
KEYWORD_MONTH(431): 终结符
KEYWORD_MULTILINESTRING(432): 终结符
KEYWORD_MULTIPOINT(433): 终结符
KEYWORD_MULTIPOLYGON(434): 终结符
KEYWORD_MUTEX(435): 终结符
KEYWORD_MYSQL_ERRNO(436): 终结符
KEYWORD_NAME(437): 终结符
KEYWORD_NAMES(438): 终结符
KEYWORD_NATIONAL(439): 终结符
KEYWORD_NATURAL(440): 终结符
KEYWORD_NCHAR(441): 终结符
KEYWORD_NDB(442): 终结符
KEYWORD_NDBCLUSTER(443): 终结符
KEYWORD_NESTED(444): 终结符
KEYWORD_NETWORK_NAMESPACE(445): 终结符
KEYWORD_NEVER(446): 终结符
KEYWORD_NEW(447): 终结符
KEYWORD_NEXT(448): 终结符
KEYWORD_NO(449): 终结符
KEYWORD_NODEGROUP(450): 终结符
KEYWORD_NONE(451): 终结符
KEYWORD_NOT(452): 终结符
KEYWORD_NOT2(453): 终结符
KEYWORD_NOWAIT(454): 终结符
KEYWORD_NO_WAIT(455): 终结符
KEYWORD_NO_WRITE_TO_BINLOG(456): 终结符
KEYWORD_NTH_VALUE(457): 终结符
KEYWORD_NTILE(458): 终结符
KEYWORD_NULL(459): 终结符
KEYWORD_NULLS(460): 终结符
KEYWORD_NUMBER(461): 终结符
KEYWORD_NUMERIC(462): 终结符
KEYWORD_NVARCHAR(463): 终结符
KEYWORD_OF(464): 终结符
KEYWORD_OFF(465): 终结符
KEYWORD_OFFSET(466): 终结符
KEYWORD_OJ(467): 终结符
KEYWORD_OLD(468): 终结符
KEYWORD_ON(469): 终结符
KEYWORD_ONE(470): 终结符
KEYWORD_ONLY(471): 终结符
KEYWORD_OPEN(472): 终结符
KEYWORD_OPTIMIZE(473): 终结符
KEYWORD_OPTIMIZER_COSTS(474): 终结符
KEYWORD_OPTION(475): 终结符
KEYWORD_OPTIONAL(476): 终结符
KEYWORD_OPTIONALLY(477): 终结符
KEYWORD_OPTIONS(478): 终结符
KEYWORD_OR(479): 终结符
KEYWORD_OR2(480): 终结符
KEYWORD_ORDER(481): 终结符
KEYWORD_ORDINALITY(482): 终结符
KEYWORD_ORGANIZATION(483): 终结符
KEYWORD_OTHERS(484): 终结符
KEYWORD_OUT(485): 终结符
KEYWORD_OUTER(486): 终结符
KEYWORD_OUTFILE(487): 终结符
KEYWORD_OVER(488): 终结符
KEYWORD_OWNER(489): 终结符
KEYWORD_PACK_KEYS(490): 终结符
KEYWORD_PAGE(491): 终结符
KEYWORD_PARALLEL(492): 终结符
KEYWORD_PARSER(493): 终结符
KEYWORD_PARSE_TREE(494): 终结符
KEYWORD_PARTIAL(495): 终结符
KEYWORD_PARTITION(496): 终结符
KEYWORD_PARTITIONING(497): 终结符
KEYWORD_PARTITIONS(498): 终结符
KEYWORD_PASSWORD(499): 终结符
KEYWORD_PASSWORD_LOCK_TIME(500): 终结符
KEYWORD_PATH(501): 终结符
KEYWORD_PERCENT_RANK(502): 终结符
KEYWORD_PERSIST(503): 终结符
KEYWORD_PERSIST_ONLY(504): 终结符
KEYWORD_PHASE(505): 终结符
KEYWORD_PLUGIN(506): 终结符
KEYWORD_PLUGINS(507): 终结符
KEYWORD_PLUGIN_DIR(508): 终结符
KEYWORD_POINT(509): 终结符
KEYWORD_POLYGON(510): 终结符
KEYWORD_PORT(511): 终结符
KEYWORD_PRECEDES(512): 终结符
KEYWORD_PRECEDING(513): 终结符
KEYWORD_PRECISION(514): 终结符
KEYWORD_PREPARE(515): 终结符
KEYWORD_PRESERVE(516): 终结符
KEYWORD_PREV(517): 终结符
KEYWORD_PRIMARY(518): 终结符
KEYWORD_PRIVILEGES(519): 终结符
KEYWORD_PRIVILEGE_CHECKS_USER(520): 终结符
KEYWORD_PROCEDURE(521): 终结符
KEYWORD_PROCESS(522): 终结符
KEYWORD_PROCESSLIST(523): 终结符
KEYWORD_PROFILE(524): 终结符
KEYWORD_PROFILES(525): 终结符
KEYWORD_PROXY(526): 终结符
KEYWORD_PURGE(527): 终结符
KEYWORD_QUALIFY(528): 终结符
KEYWORD_QUARTER(529): 终结符
KEYWORD_QUERY(530): 终结符
KEYWORD_QUICK(531): 终结符
KEYWORD_RANDOM(532): 终结符
KEYWORD_RANGE(533): 终结符
KEYWORD_RANK(534): 终结符
KEYWORD_READ(535): 终结符
KEYWORD_READS(536): 终结符
KEYWORD_READ_ONLY(537): 终结符
KEYWORD_READ_WRITE(538): 终结符
KEYWORD_REAL(539): 终结符
KEYWORD_REBUILD(540): 终结符
KEYWORD_RECOVER(541): 终结符
KEYWORD_RECURSIVE(542): 终结符
KEYWORD_REDO_BUFFER_SIZE(543): 终结符
KEYWORD_REDUNDANT(544): 终结符
KEYWORD_REFERENCE(545): 终结符
KEYWORD_REFERENCES(546): 终结符
KEYWORD_REGEXP(547): 终结符
KEYWORD_REGISTRATION(548): 终结符
KEYWORD_RELAY(549): 终结符
KEYWORD_RELAYLOG(550): 终结符
KEYWORD_RELAY_LOG_FILE(551): 终结符
KEYWORD_RELAY_LOG_POS(552): 终结符
KEYWORD_RELAY_THREAD(553): 终结符
KEYWORD_RELEASE(554): 终结符
KEYWORD_RELOAD(555): 终结符
KEYWORD_REMOVE(556): 终结符
KEYWORD_RENAME(557): 终结符
KEYWORD_REORGANIZE(558): 终结符
KEYWORD_REPAIR(559): 终结符
KEYWORD_REPEAT(560): 终结符
KEYWORD_REPEATABLE(561): 终结符
KEYWORD_REPLACE(562): 终结符
KEYWORD_REPLICA(563): 终结符
KEYWORD_REPLICAS(564): 终结符
KEYWORD_REPLICATE_DO_DB(565): 终结符
KEYWORD_REPLICATE_DO_TABLE(566): 终结符
KEYWORD_REPLICATE_IGNORE_DB(567): 终结符
KEYWORD_REPLICATE_IGNORE_TABLE(568): 终结符
KEYWORD_REPLICATE_REWRITE_DB(569): 终结符
KEYWORD_REPLICATE_WILD_DO_TABLE(570): 终结符
KEYWORD_REPLICATE_WILD_IGNORE_TABLE(571): 终结符
KEYWORD_REPLICATION(572): 终结符
KEYWORD_REQUIRE(573): 终结符
KEYWORD_REQUIRE_ROW_FORMAT(574): 终结符
KEYWORD_RESET(575): 终结符
KEYWORD_RESIGNAL(576): 终结符
KEYWORD_RESOURCE(577): 终结符
KEYWORD_RESPECT(578): 终结符
KEYWORD_RESTART(579): 终结符
KEYWORD_RESTORE(580): 终结符
KEYWORD_RESTRICT(581): 终结符
KEYWORD_RESUME(582): 终结符
KEYWORD_RETAIN(583): 终结符
KEYWORD_RETURN(584): 终结符
KEYWORD_RETURNED_SQLSTATE(585): 终结符
KEYWORD_RETURNING(586): 终结符
KEYWORD_RETURNS(587): 终结符
KEYWORD_REUSE(588): 终结符
KEYWORD_REVERSE(589): 终结符
KEYWORD_REVOKE(590): 终结符
KEYWORD_RIGHT(591): 终结符
KEYWORD_RLIKE(592): 终结符
KEYWORD_ROLE(593): 终结符
KEYWORD_ROLLBACK(594): 终结符
KEYWORD_ROLLUP(595): 终结符
KEYWORD_ROTATE(596): 终结符
KEYWORD_ROUTINE(597): 终结符
KEYWORD_ROW(598): 终结符
KEYWORD_ROWS(599): 终结符
KEYWORD_ROW_COUNT(600): 终结符
KEYWORD_ROW_FORMAT(601): 终结符
KEYWORD_ROW_NUMBER(602): 终结符
KEYWORD_RTREE(603): 终结符
KEYWORD_S3(604): 终结符
KEYWORD_SAVEPOINT(605): 终结符
KEYWORD_SCHEDULE(606): 终结符
KEYWORD_SCHEMA(607): 终结符
KEYWORD_SCHEMAS(608): 终结符
KEYWORD_SCHEMA_NAME(609): 终结符
KEYWORD_SECOND(610): 终结符
KEYWORD_SECONDARY(611): 终结符
KEYWORD_SECONDARY_ENGINE(612): 终结符
KEYWORD_SECONDARY_ENGINE_ATTRIBUTE(613): 终结符
KEYWORD_SECONDARY_LOAD(614): 终结符
KEYWORD_SECONDARY_UNLOAD(615): 终结符
KEYWORD_SECOND_MICROSECOND(616): 终结符
KEYWORD_SECURITY(617): 终结符
KEYWORD_SELECT(618): 终结符
KEYWORD_SENSITIVE(619): 终结符
KEYWORD_SEPARATOR(620): 终结符
KEYWORD_SERIAL(621): 终结符
KEYWORD_SERIALIZABLE(622): 终结符
KEYWORD_SERVER(623): 终结符
KEYWORD_SESSION(624): 终结符
KEYWORD_SET(625): 终结符
KEYWORD_SHARE(626): 终结符
KEYWORD_SHOW(627): 终结符
KEYWORD_SHUTDOWN(628): 终结符
KEYWORD_SIGNAL(629): 终结符
KEYWORD_SIGNED(630): 终结符
KEYWORD_SIMPLE(631): 终结符
KEYWORD_SKIP(632): 终结符
KEYWORD_SLAVE(633): 终结符
KEYWORD_SLOW(634): 终结符
KEYWORD_SMALLINT(635): 终结符
KEYWORD_SNAPSHOT(636): 终结符
KEYWORD_SOCKET(637): 终结符
KEYWORD_SOME(638): 终结符
KEYWORD_SONAME(639): 终结符
KEYWORD_SOUNDS(640): 终结符
KEYWORD_SOURCE(641): 终结符
KEYWORD_SOURCE_AUTO_POSITION(642): 终结符
KEYWORD_SOURCE_BIND(643): 终结符
KEYWORD_SOURCE_COMPRESSION_ALGORITHM(644): 终结符
KEYWORD_SOURCE_CONNECT_RETRY(645): 终结符
KEYWORD_SOURCE_DELAY(646): 终结符
KEYWORD_SOURCE_HEARTBEAT_PERIOD(647): 终结符
KEYWORD_SOURCE_HOST(648): 终结符
KEYWORD_SOURCE_LOG_FILE(649): 终结符
KEYWORD_SOURCE_LOG_POS(650): 终结符
KEYWORD_SOURCE_PASSWORD(651): 终结符
KEYWORD_SOURCE_PORT(652): 终结符
KEYWORD_SOURCE_PUBLIC_KEY_PATH(653): 终结符
KEYWORD_SOURCE_RETRY_COUNT(654): 终结符
KEYWORD_SOURCE_SSL(655): 终结符
KEYWORD_SOURCE_SSL_CA(656): 终结符
KEYWORD_SOURCE_SSL_CAPATH(657): 终结符
KEYWORD_SOURCE_SSL_CERT(658): 终结符
KEYWORD_SOURCE_SSL_CIPHER(659): 终结符
KEYWORD_SOURCE_SSL_CRL(660): 终结符
KEYWORD_SOURCE_SSL_CRLPATH(661): 终结符
KEYWORD_SOURCE_SSL_KEY(662): 终结符
KEYWORD_SOURCE_SSL_VERIFY_SERVER_CERT(663): 终结符
KEYWORD_SOURCE_TLS_CIPHERSUITES(664): 终结符
KEYWORD_SOURCE_TLS_VERSION(665): 终结符
KEYWORD_SOURCE_USER(666): 终结符
KEYWORD_SOURCE_ZSTD_COMPRESSION_LEVEL(667): 终结符
KEYWORD_SPATIAL(668): 终结符
KEYWORD_SPECIFIC(669): 终结符
KEYWORD_SQL(670): 终结符
KEYWORD_SQLEXCEPTION(671): 终结符
KEYWORD_SQLSTATE(672): 终结符
KEYWORD_SQLWARNING(673): 终结符
KEYWORD_SQL_AFTER_GTIDS(674): 终结符
KEYWORD_SQL_AFTER_MTS_GAPS(675): 终结符
KEYWORD_SQL_BEFORE_GTIDS(676): 终结符
KEYWORD_SQL_BIG_RESULT(677): 终结符
KEYWORD_SQL_BUFFER_RESULT(678): 终结符
KEYWORD_SQL_CALC_FOUND_ROWS(679): 终结符
KEYWORD_SQL_NO_CACHE(680): 终结符
KEYWORD_SQL_SMALL_RESULT(681): 终结符
KEYWORD_SQL_THREAD(682): 终结符
KEYWORD_SQL_TSI_DAY(683): 终结符
KEYWORD_SQL_TSI_HOUR(684): 终结符
KEYWORD_SQL_TSI_MINUTE(685): 终结符
KEYWORD_SQL_TSI_MONTH(686): 终结符
KEYWORD_SQL_TSI_QUARTER(687): 终结符
KEYWORD_SQL_TSI_SECOND(688): 终结符
KEYWORD_SQL_TSI_WEEK(689): 终结符
KEYWORD_SQL_TSI_YEAR(690): 终结符
KEYWORD_SRID(691): 终结符
KEYWORD_SSL(692): 终结符
KEYWORD_STACKED(693): 终结符
KEYWORD_START(694): 终结符
KEYWORD_STARTING(695): 终结符
KEYWORD_STARTS(696): 终结符
KEYWORD_STATS_AUTO_RECALC(697): 终结符
KEYWORD_STATS_PERSISTENT(698): 终结符
KEYWORD_STATS_SAMPLE_PAGES(699): 终结符
KEYWORD_STATUS(700): 终结符
KEYWORD_STOP(701): 终结符
KEYWORD_STORAGE(702): 终结符
KEYWORD_STORED(703): 终结符
KEYWORD_STRAIGHT_JOIN(704): 终结符
KEYWORD_STREAM(705): 终结符
KEYWORD_STRING(706): 终结符
KEYWORD_SUBCLASS_ORIGIN(707): 终结符
KEYWORD_SUBJECT(708): 终结符
KEYWORD_SUBPARTITION(709): 终结符
KEYWORD_SUBPARTITIONS(710): 终结符
KEYWORD_SUPER(711): 终结符
KEYWORD_SUSPEND(712): 终结符
KEYWORD_SWAPS(713): 终结符
KEYWORD_SWITCHES(714): 终结符
KEYWORD_SYSTEM(715): 终结符
KEYWORD_TABLE(716): 终结符
KEYWORD_TABLES(717): 终结符
KEYWORD_TABLESAMPLE(718): 终结符
KEYWORD_TABLESPACE(719): 终结符
KEYWORD_TABLE_CHECKSUM(720): 终结符
KEYWORD_TABLE_NAME(721): 终结符
KEYWORD_TEMPORARY(722): 终结符
KEYWORD_TEMPTABLE(723): 终结符
KEYWORD_TERMINATED(724): 终结符
KEYWORD_TEXT(725): 终结符
KEYWORD_THAN(726): 终结符
KEYWORD_THEN(727): 终结符
KEYWORD_THREAD_PRIORITY(728): 终结符
KEYWORD_TIES(729): 终结符
KEYWORD_TIME(730): 终结符
KEYWORD_TIMESTAMP(731): 终结符
KEYWORD_TIMESTAMP_ADD(732): 终结符
KEYWORD_TIMESTAMP_DIFF(733): 终结符
KEYWORD_TINYBLOB(734): 终结符
KEYWORD_TINYINT(735): 终结符
KEYWORD_TINYTEXT_SYN(736): 终结符
KEYWORD_TLS(737): 终结符
KEYWORD_TO(738): 终结符
KEYWORD_TRAILING(739): 终结符
KEYWORD_TRANSACTION(740): 终结符
KEYWORD_TRIGGER(741): 终结符
KEYWORD_TRIGGERS(742): 终结符
KEYWORD_TRUE(743): 终结符
KEYWORD_TRUNCATE(744): 终结符
KEYWORD_TYPE(745): 终结符
KEYWORD_TYPES(746): 终结符
KEYWORD_UNBOUNDED(747): 终结符
KEYWORD_UNCOMMITTED(748): 终结符
KEYWORD_UNDEFINED(749): 终结符
KEYWORD_UNDO(750): 终结符
KEYWORD_UNDOFILE(751): 终结符
KEYWORD_UNDO_BUFFER_SIZE(752): 终结符
KEYWORD_UNICODE(753): 终结符
KEYWORD_UNINSTALL(754): 终结符
KEYWORD_UNION(755): 终结符
KEYWORD_UNIQUE(756): 终结符
KEYWORD_UNKNOWN(757): 终结符
KEYWORD_UNLOCK(758): 终结符
KEYWORD_UNREGISTER(759): 终结符
KEYWORD_UNSIGNED(760): 终结符
KEYWORD_UNTIL(761): 终结符
KEYWORD_UPDATE(762): 终结符
KEYWORD_UPGRADE(763): 终结符
KEYWORD_URL(764): 终结符
KEYWORD_USAGE(765): 终结符
KEYWORD_USE(766): 终结符
KEYWORD_USER(767): 终结符
KEYWORD_USER_RESOURCES(768): 终结符
KEYWORD_USE_FRM(769): 终结符
KEYWORD_USING(770): 终结符
KEYWORD_UTC_DATE(771): 终结符
KEYWORD_UTC_TIME(772): 终结符
KEYWORD_UTC_TIMESTAMP(773): 终结符
KEYWORD_VALIDATION(774): 终结符
KEYWORD_VALUE(775): 终结符
KEYWORD_VALUES(776): 终结符
KEYWORD_VARBINARY(777): 终结符
KEYWORD_VARCHAR(778): 终结符
KEYWORD_VARCHARACTER(779): 终结符
KEYWORD_VARIABLES(780): 终结符
KEYWORD_VARYING(781): 终结符
KEYWORD_VCPU(782): 终结符
KEYWORD_VIEW(783): 终结符
KEYWORD_VIRTUAL(784): 终结符
KEYWORD_VISIBLE(785): 终结符
KEYWORD_WAIT(786): 终结符
KEYWORD_WARNINGS(787): 终结符
KEYWORD_WEEK(788): 终结符
KEYWORD_WEIGHT_STRING(789): 终结符
KEYWORD_WHEN(790): 终结符
KEYWORD_WHERE(791): 终结符
KEYWORD_WHILE(792): 终结符
KEYWORD_WINDOW(793): 终结符
KEYWORD_WITH(794): 终结符
KEYWORD_WITHOUT(795): 终结符
KEYWORD_WORK(796): 终结符
KEYWORD_WRAPPER(797): 终结符
KEYWORD_WRITE(798): 终结符
KEYWORD_X509(799): 终结符
KEYWORD_XA(800): 终结符
KEYWORD_XID(801): 终结符
KEYWORD_XML(802): 终结符
KEYWORD_XOR(803): 终结符
KEYWORD_YEAR(804): 终结符
KEYWORD_YEAR_MONTH(805): 终结符
KEYWORD_ZEROFILL(806): 终结符
KEYWORD_ZONE(807): 终结符
KEYWORD_WITH_ROLLUP(808): 终结符
WORD_ADDDATE(809): 终结符
WORD_CURDATE(810): 终结符
WORD_CURTIME(811): 终结符
WORD_DATE_ADD_INTERVAL(812): 终结符
WORD_DATE_SUB_INTERVAL(813): 终结符
WORD_EXTRACT(814): 终结符
WORD_NOW(815): 终结符
WORD_SUBDATE(816): 终结符
WORD_SYSDATE(817): 终结符
WORD_BIT_AND(818): 终结符
WORD_BIT_OR(819): 终结符
WORD_BIT_XOR(820): 终结符
WORD_COUNT(821): 终结符
WORD_GROUP_CONCAT(822): 终结符
WORD_JSON_ARRAYAGG(823): 终结符
WORD_JSON_OBJECTAGG(824): 终结符
WORD_MAX(825): 终结符
WORD_MIN(826): 终结符
WORD_STD(827): 终结符
WORD_STDDEV_SAMP(828): 终结符
WORD_SUM(829): 终结符
WORD_VAR_SAMP(830): 终结符
WORD_VARIANCE(831): 终结符
WORD_SUBSTRING(832): 终结符
WORD_TRIM(833): 终结符
WORD_CAST(834): 终结符
WORD_ST_COLLECT(835): 终结符
entry(836): [836->·841, 836->·848]
ident(837): [837->·44, 837->·45]
ident_2(838): [838->·837 21 837]
ident_3(839): [839->·837 21 837 21 837]
simple_ident(840): [840->·837, 840->·838, 840->·839]
simple_ident_list(841): [841->·841 18 840, 841->·840]
text_literal(842): [842->·42, 842->·41]
int_literal(843): [843->·40]
num_literal(844): [844->·843, 844->·39, 844->·38]
temporal_literal(845): [845->·161 42, 845->·730 42, 845->·162 42]
literal(846): [846->·842, 846->·844, 846->·845, 846->·234, 846->·743, 846->·37, 846->·36, 846->·43 37, 846->·43 36]
null_literal(847): [847->·459]
literal_or_null(848): [848->·846, 848->·847]
S'(849): [849->·836]
"""

from typing import Any, Callable, List, Optional, Tuple

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast


def action_shift_13(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(13)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_13, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_8(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(8)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_8, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_2(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(2)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_2, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_3(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(3)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_3, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_5(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(5)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_5, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_20(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(20)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_20, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_22(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(22)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_22, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_24(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(24)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_24, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_29(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(29)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_29, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_30(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(30)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_30, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_27(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(27)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_27, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_28(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(28)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_28, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_17(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(17)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_17, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_18(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(18)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_18, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_16(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(16)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_16, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_14(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(14)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_14, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_15(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(15)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_15, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_31(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(31)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_31, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_21(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(21)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_21, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_23(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(23)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_23, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_26(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(26)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_26, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_36(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(36)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_36, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_25(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(25)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_25, True  # 返回状态栈常量状态的终结符行为函数


def action_shift_32(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    status_stack.append(32)  # 向状态栈中压入常量
    symbol_stack.append(terminal.symbol_value)  # 向符号栈中压入当前终结符的值
    return status_32, True  # 返回状态栈常量状态的终结符行为函数


def action_reduce_0_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = symbol_stack[-1]
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 836)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_2_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.Ident(symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 837)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_3_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.Ident(symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 837)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_4_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.Ident2D(value1=symbol_stack[-3], value2=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-4], 838)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-3:] = [symbol_value]  # 出栈 3 个参数，入栈新生成的非终结符的值
    status_stack[-3:] = [next_status]  # 出栈 3 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_6_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = symbol_stack[-1]
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 840)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_7_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.Ident3D(value1=symbol_stack[-5], value2=symbol_stack[-3], value3=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-6], 839)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-5:] = [symbol_value]  # 出栈 5 个参数，入栈新生成的非终结符的值
    status_stack[-5:] = [next_status]  # 出栈 5 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_11_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = [symbol_stack[-1]]
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 841)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_12_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = symbol_stack[-3] + [symbol_stack[-1]]
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-4], 841)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-3:] = [symbol_value]  # 出栈 3 个参数，入栈新生成的非终结符的值
    status_stack[-3:] = [next_status]  # 出栈 3 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_14_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.StringLiteral(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 842)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_15_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.StringLiteral(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 842)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_16_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.IntLiteral(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 843)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_17_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.DecimalLiteral(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 844)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_18_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.FloatLiteral(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 844)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_19_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = symbol_stack[-1]
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 844)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_20_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.TemporalLiteral.create_date_literal(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-3], 845)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-2:] = [symbol_value]  # 出栈 2 个参数，入栈新生成的非终结符的值
    status_stack[-2:] = [next_status]  # 出栈 2 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_22_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.TemporalLiteral.create_datetime_literal(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-3], 845)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-2:] = [symbol_value]  # 出栈 2 个参数，入栈新生成的非终结符的值
    status_stack[-2:] = [next_status]  # 出栈 2 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_24_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.TemporalLiteral.create_time_literal(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-3], 845)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-2:] = [symbol_value]  # 出栈 2 个参数，入栈新生成的非终结符的值
    status_stack[-2:] = [next_status]  # 出栈 2 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_26_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.FalseLiteral()
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 846)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_27_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.BinStringLiteral(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 846)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_28_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.HexStringLiteral(value=symbol_stack[-1])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 846)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_29_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.BinStringLiteral(value=symbol_stack[-1], charset=symbol_stack[-2])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-3], 846)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-2:] = [symbol_value]  # 出栈 2 个参数，入栈新生成的非终结符的值
    status_stack[-2:] = [next_status]  # 出栈 2 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_30_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.HexStringLiteral(value=symbol_stack[-1], charset=symbol_stack[-2])
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-3], 846)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-2:] = [symbol_value]  # 出栈 2 个参数，入栈新生成的非终结符的值
    status_stack[-2:] = [next_status]  # 出栈 2 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_32_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.TrueLiteral()
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 846)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_33_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = symbol_stack[-1]
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 846)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_36_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = ast.NullLiteral()
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 847)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_reduce_37_1(status_stack: List[int], symbol_stack: List[Any], _: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    symbol_value = symbol_stack[-1]
    next_status = STATUS_SYMBOL_GOTO_HASH[(status_stack[-2], 848)]  # 根据状态和生成的非终结符获取需要 GOTO 的状态
    symbol_stack[-1:] = [symbol_value]  # 出栈 1 个参数，入栈新生成的非终结符的值
    status_stack[-1:] = [next_status]  # 出栈 1 个参数，入栈 GOTO 的新状态
    return STATUS_HASH[next_status], False  # 返回新状态的行为函数


def action_accept(_1: List[int], _2: List[Any], _3: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    return None, True


STATUS_0_TERMINAL_ACTION_HASH = {
    0: action_reduce_0_1,
    18: action_shift_13,
}


def status_0(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_0_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_1_TERMINAL_ACTION_HASH = {
    0: action_reduce_0_1,
}


def status_1(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_1_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_2_TERMINAL_ACTION_HASH = {
    0: action_reduce_2_1,
    18: action_reduce_2_1,
    21: action_reduce_2_1,
}


def status_2(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_2_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_3_TERMINAL_ACTION_HASH = {
    0: action_reduce_3_1,
    18: action_reduce_3_1,
    21: action_reduce_3_1,
}


def status_3(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_3_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_4_TERMINAL_ACTION_HASH = {
    0: action_reduce_4_1,
    18: action_reduce_4_1,
    21: action_shift_8,
}


def status_4(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_4_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_5_TERMINAL_ACTION_HASH = {
    44: action_shift_2,
    45: action_shift_3,
}


def status_5(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_5_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_6_TERMINAL_ACTION_HASH = {
    0: action_reduce_6_1,
    18: action_reduce_6_1,
    21: action_shift_5,
}


def status_6(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_6_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_7_TERMINAL_ACTION_HASH = {
    0: action_reduce_7_1,
    18: action_reduce_7_1,
}


def status_7(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_7_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_8_TERMINAL_ACTION_HASH = {
    44: action_shift_2,
    45: action_shift_3,
}


def status_8(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_8_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_9_TERMINAL_ACTION_HASH = {
    0: action_reduce_6_1,
    18: action_reduce_6_1,
}


def status_9(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_9_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_10_TERMINAL_ACTION_HASH = {
    0: action_reduce_6_1,
    18: action_reduce_6_1,
}


def status_10(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_10_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_11_TERMINAL_ACTION_HASH = {
    0: action_reduce_11_1,
    18: action_reduce_11_1,
}


def status_11(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_11_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_12_TERMINAL_ACTION_HASH = {
    0: action_reduce_12_1,
    18: action_reduce_12_1,
}


def status_12(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_12_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_13_TERMINAL_ACTION_HASH = {
    44: action_shift_2,
    45: action_shift_3,
}


def status_13(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_13_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_14_TERMINAL_ACTION_HASH = {
    0: action_reduce_14_1,
}


def status_14(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_14_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_15_TERMINAL_ACTION_HASH = {
    0: action_reduce_15_1,
}


def status_15(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_15_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_16_TERMINAL_ACTION_HASH = {
    0: action_reduce_16_1,
}


def status_16(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_16_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_17_TERMINAL_ACTION_HASH = {
    0: action_reduce_17_1,
}


def status_17(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_17_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_18_TERMINAL_ACTION_HASH = {
    0: action_reduce_18_1,
}


def status_18(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_18_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_19_TERMINAL_ACTION_HASH = {
    0: action_reduce_19_1,
}


def status_19(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_19_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_20_TERMINAL_ACTION_HASH = {
    0: action_reduce_20_1,
}


def status_20(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_20_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_21_TERMINAL_ACTION_HASH = {
    42: action_shift_20,
}


def status_21(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_21_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_22_TERMINAL_ACTION_HASH = {
    0: action_reduce_22_1,
}


def status_22(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_22_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_23_TERMINAL_ACTION_HASH = {
    42: action_shift_22,
}


def status_23(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_23_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_24_TERMINAL_ACTION_HASH = {
    0: action_reduce_24_1,
}


def status_24(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_24_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_25_TERMINAL_ACTION_HASH = {
    42: action_shift_24,
}


def status_25(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_25_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_26_TERMINAL_ACTION_HASH = {
    0: action_reduce_26_1,
}


def status_26(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_26_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_27_TERMINAL_ACTION_HASH = {
    0: action_reduce_27_1,
}


def status_27(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_27_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_28_TERMINAL_ACTION_HASH = {
    0: action_reduce_28_1,
}


def status_28(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_28_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_29_TERMINAL_ACTION_HASH = {
    0: action_reduce_29_1,
}


def status_29(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_29_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_30_TERMINAL_ACTION_HASH = {
    0: action_reduce_30_1,
}


def status_30(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_30_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_31_TERMINAL_ACTION_HASH = {
    36: action_shift_29,
    37: action_shift_30,
}


def status_31(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_31_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_32_TERMINAL_ACTION_HASH = {
    0: action_reduce_32_1,
}


def status_32(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_32_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_33_TERMINAL_ACTION_HASH = {
    0: action_reduce_33_1,
}


def status_33(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_33_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_34_TERMINAL_ACTION_HASH = {
    0: action_reduce_33_1,
}


def status_34(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_34_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_35_TERMINAL_ACTION_HASH = {
    0: action_reduce_33_1,
}


def status_35(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_35_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_36_TERMINAL_ACTION_HASH = {
    0: action_reduce_36_1,
}


def status_36(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_36_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_37_TERMINAL_ACTION_HASH = {
    0: action_reduce_37_1,
}


def status_37(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_37_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_38_TERMINAL_ACTION_HASH = {
    0: action_reduce_37_1,
}


def status_38(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_38_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_39_TERMINAL_ACTION_HASH = {
    0: action_accept,
}


def status_39(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_39_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_40_TERMINAL_ACTION_HASH = {
    36: action_shift_27,
    37: action_shift_28,
    38: action_shift_17,
    39: action_shift_18,
    40: action_shift_16,
    41: action_shift_14,
    42: action_shift_15,
    43: action_shift_31,
    44: action_shift_2,
    45: action_shift_3,
    161: action_shift_21,
    162: action_shift_23,
    234: action_shift_26,
    459: action_shift_36,
    730: action_shift_25,
    743: action_shift_32,
}


def status_40(status_stack: List[int], symbol_stack: List[Any], terminal: ms_parser.symbol.Terminal) -> Tuple[Optional[Callable], bool]:
    move_action = STATUS_40_TERMINAL_ACTION_HASH[terminal.symbol_id]  # 通过哈希映射获取行为函数
    return move_action(status_stack, symbol_stack, terminal)  # 执行行为函数


STATUS_SYMBOL_GOTO_HASH = {
    (5, 837): 4, 
    (8, 837): 7, 
    (13, 837): 6, 
    (13, 838): 9, 
    (13, 839): 10, 
    (13, 840): 12, 
    (40, 836): 39, 
    (40, 837): 6, 
    (40, 838): 9, 
    (40, 839): 10, 
    (40, 840): 11, 
    (40, 841): 0, 
    (40, 842): 33, 
    (40, 843): 19, 
    (40, 844): 34, 
    (40, 845): 35, 
    (40, 846): 37, 
    (40, 847): 38, 
    (40, 848): 1, 
}


# 状态 > 状态函数的字典
STATUS_HASH = {
    0: status_0,
    1: status_1,
    2: status_2,
    3: status_3,
    4: status_4,
    5: status_5,
    6: status_6,
    7: status_7,
    8: status_8,
    9: status_9,
    10: status_10,
    11: status_11,
    12: status_12,
    13: status_13,
    14: status_14,
    15: status_15,
    16: status_16,
    17: status_17,
    18: status_18,
    19: status_19,
    20: status_20,
    21: status_21,
    22: status_22,
    23: status_23,
    24: status_24,
    25: status_25,
    26: status_26,
    27: status_27,
    28: status_28,
    29: status_29,
    30: status_30,
    31: status_31,
    32: status_32,
    33: status_33,
    34: status_34,
    35: status_35,
    36: status_36,
    37: status_37,
    38: status_38,
    39: status_39,
    40: status_40,
}


def parse(lexical_iterator: ms_parser.lexical.LexicalBase):
    status_stack = [40]  # 初始化状态栈
    symbol_stack = []  # 初始化对象栈

    action = status_40  # 初始化状态函数
    terminal = lexical_iterator.lex()  # 词法解析出下一个终结符
    next_terminal = False
    try:
        while action:
            if next_terminal is True:
                terminal = lexical_iterator.lex()  # 词法解析出下一个终结符
            action, next_terminal = action(status_stack, symbol_stack, terminal)  # 调用状态函数
    except KeyError as e:
        next_terminal_list = []
        for _ in range(10):
            if terminal.is_end:
                break
            next_terminal_list.append(terminal.symbol_value)
            terminal = lexical_iterator.lex()
        next_terminal_text = "".join(next_terminal_list)
        raise KeyError("解析失败:", next_terminal_text) from e

    return symbol_stack[0]  # 返回最终结果

