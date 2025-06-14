- 语句（statement）：SQL 语法树的根节点；代表一条独立的、可执行的命令；语句节点的属性通常为子句节点。
  - 【每种语句一个文件】
- 子句（clause）：SQL 语法树的中间节点；通常是由一个关键字引导，用于定义语句中某一部分的功能或逻辑；子句节点的属性通常为表达式节点或元素节点，子句之间允许相互引用，但需要保证子句之间的引用关系满足严格的拓扑关系。
  - OVER 子句（over clause）

  - ORDER BY 子句（order by clause）
  
  - PARTITION BY 子句（partition by clause）
- 短语（pharse）：SQL 语法树的中间节点或叶子节点；用于定义特定场景下定义某种功能或逻辑（适用于多个不同子句或表达式场景，否则在整理时直接作为子句的一部分处理）；短语节点的属性中仅包含表达式节点（抽象类）、基础元素节点和其他短语节点。
  - 字段类型（field type）
  - 别名（alias）
  - JSON 表选项（json table option）
- 表达式（expression）：SQL 语法树的中间节点或叶子节点，节点均继承自抽象节点 `Expression`；用于表示通用场景下可以计算出一个值的组合；表达式节点的属性中仅包含其他表达式节点、短语节点或基础元素节点。
  - 通用表达式（general expression）
  - 聚集函数表达式（sum expression）
  - 窗口函数表达式（window function expression）
  - 普通函数表达式（function expression）
  - 运算符（operator）【待处理】
- 基础元素（basic）：SQL 语法树的叶子节点；用于表示不可（不需要）切分的语法单元；节点的属性为 Python 标准类型。
  - 关键字固定组合用法（fixed word）：语义组没有返回值。
  - 标识符（ident）：命名数据库对象的字符串（例如库名、表名、字段名、函数名等）。
  - 字符集名称（charset name）：指定字符集名称的关键字及标识符。
  - 字面值（literal）
  - 时间单位类型（time unit）

在引用关系上，除抽象类外，语句引用子句，子句引用短语、表达式和基础元素，表达式引用短语、基础元素，短语引用基础元素。

> 只有当 MySQL 语义组没有直接对应的语义组时，才会使用如下标记：
>
> 【部分】：表示语义组为 MySQL 语义组中的部分备选规则。
>
> 【包含】：表示语义组的某个部分包含 MySQL 语义组，但在备选规则中还包含了 MySQL 语义组中不存在的 Token。
>
> 【超集】：表示语义组包含 MySQL 语义组中的所有备选规则，但同时也包含了 MySQL 语义组中不存在的其他备选规则。
>
> 【不兼容】：表示语义组应包含 MySQL 语义组中的所有备选规则，但实际不兼容且已明确添加到不兼容清单中。

# 顶层节点（top level node）

解析下一个语句，直至输入流结束或遇到下一个 `;`。

| 水杉解析器语义组名称  | 语义组类型                | 返回值类型                | MySQL 语义组名称                                            |
| --------------------- | ------------------------- | ------------------------- | ----------------------------------------------------------- |
| `start_entry`         | 入口语义组                | `Optional[ast.Statement]` | `start_entry`                                               |
| `sql_statement_entry` | 标准 SQL 语句的入口语义组 | `Optional[ast.Statement]` | `sql_statement`                                             |
| `sql_statement`       | 标准 SQL 语句             | `ast.Statement`           | `simple_statement_or_begin`<br />`simple_statement`【超集】 |
| `opt_end_of_input`    | 可选的输入流结束符        | -                         | `opt_end_of_input`                                          |

# 语句（statement）

#### ALTER TABLE 语句（alter table statement）

| 水杉解析器语义组名称 | 语义组类型    | 返回值类型            | MySQL 语义组名称      |
| -------------------- | ------------- | --------------------- | --------------------- |
| `binlog_statement`   | `BINLOG` 语句 | `ast.BinlogStatement` | `binlog_base64_event` |

#### ANALYZE TABLE 语句（analyze table statement）

| 水杉解析器语义组名称         | 语义组类型           | 返回值类型                  | MySQL 语义组名称             |
| ---------------------------- | -------------------- | --------------------------- | ---------------------------- |
| `analyze_table_statement`    | `ANALYZE TABLE` 语句 | `ast.AnalyzeTableStatement` | `analyze_table_stmt`         |
| `opt_histogram`              | 可选的直方图参数     | `ast.Histogram`             | `opt_histogram`              |
| `opt_histogram_update_param` | 直方图的更新参数     | `ast.HistogramUpdateParam`  | `opt_histogram_update_param` |

#### BINLOG 语句（binlog statement）

| 水杉解析器语义组名称 | 语义组类型  | 返回值类型          | MySQL 语义组名称 |
| -------------------- | ----------- | ------------------- | ---------------- |
| `call_statement`     | `CALL` 语句 | `ast.CallStatement` | `call_stmt`      |

#### CALL 语句（call statement）

| 水杉解析器语义组名称 | 语义组类型  | 返回值类型          | MySQL 语义组名称 |
| -------------------- | ----------- | ------------------- | ---------------- |
| `call_statement`     | `CALL` 语句 | `ast.CallStatement` | `call_stmt`      |

#### CHECK TABLE 语句（check table statement）

| 水杉解析器语义组名称    | 语义组类型         | 返回值类型                | MySQL 语义组名称   |
| ----------------------- | ------------------ | ------------------------- | ------------------ |
| `check_table_statement` | `CHECK TABLE` 语句 | `ast.CheckTableStatement` | `check_table_stmt` |

#### CHECKSUM 语句（checksum statement）

| 水杉解析器语义组名称 | 语义组类型      | 返回值类型              | MySQL 语义组名称 |
| -------------------- | --------------- | ----------------------- | ---------------- |
| `checksum_statement` | `CHECKSUM` 语句 | `ast.ChecksumStatement` | `checksum`       |

#### CLONE 语句（clone statement）

| 水杉解析器语义组名称 | 语义组类型                                | 返回值类型       | MySQL 语义组名称  |
| -------------------- | ----------------------------------------- | ---------------- | ----------------- |
| `clone_statement`    | `CLONE` 语句                              | `CloneStatement` | `clone_stmt`      |
| `opt_datadir_ssl`    | `CLONE` 语句的临时数据目录和 SSL 选项信息 | `TempDatadirSsl` | `opt_datadir_ssl` |

#### COMMIT 语句（commit statement）

| 水杉解析器语义组名称 | 语义组类型    | 返回值类型        | MySQL 语义组名称 |
| -------------------- | ------------- | ----------------- | ---------------- |
| `commit_statement`   | `COMMIT` 语句 | `CommitStatement` | `commit`         |

#### CREATE INDEX 语句（create index statement）

| 水杉解析器语义组名称     | 语义组类型             | 返回值类型            | MySQL 语义组名称    |
| ------------------------ | ---------------------- | --------------------- | ------------------- |
| `create_index_statement` | `CREATE INDEX` 语句    | `ast.CreateIndexStmt` | `create_index_stmt` |
| `opt_keyword_unique`     | 可选的 `UNIQUE` 关键字 | `ast.EnumIndexType`   | `opt_unique`        |

#### CREATE TABLE 语句（create table statement）

| 水杉解析器语义组名称         | 语义组类型                                 | 返回值类型                  | MySQL 语义组名称               |
| ---------------------------- | ------------------------------------------ | --------------------------- | ------------------------------ |
| `create_table_statement`     | `CREATE TABLE` 语句                        | `ast.CreateTableStatement`  | `create_table_stmt`            |
| `opt_create_table_option_1`  | `CREATE TABLE` 的选项（第 1 层）           | `ast.TempCreateTableOption` | `opt_create_table_options_etc` |
| `opt_create_table_option_2`  | `CREATE TABLE` 的选项（第 2 层）           | `ast.TempCreateTableOption` | `opt_create_partitioning_etc`  |
| `opt_create_table_option_3`  | `CREATE TABLE` 的选项（第 3 层）           | `ast.TempCreateTableOption` | `opt_duplicate_as_qe`          |
| `as_create_query_expression` | 可选择是否包含前置 `AS` 关键字的查询表达式 | `ast.QueryExpression`       | `as_create_query_expression`   |

#### DELETE 语句（delete statement）

| 水杉解析器语义组名称 | 语义组类型    | 返回值类型            | MySQL 语义组名称 |
| -------------------- | ------------- | --------------------- | ---------------- |
| `delete_statement`   | `DELETE` 语句 | `ast.DeleteStatement` | `delete_stmt`    |

#### DESCRIBE 语句（describe statement）

| 水杉解析器语义组名称  | 语义组类型                 | 返回值类型          | MySQL 语义组名称      |
| --------------------- | -------------------------- | ------------------- | --------------------- |
| `describe_statement`  | `DESCRIBE` 语句            | `DescribeStatement` | `describe_stmt`       |
| `opt_describe_column` | 可选的 `DESCRIBE` 描述字段 | `Optional[str]`     | `opt_describe_column` |

#### DO 语句（do statement）

| 水杉解析器语义组名称 | 语义组类型 | 返回值类型    | MySQL 语义组名称 |
| -------------------- | ---------- | ------------- | ---------------- |
| `do_statement`       | `DO` 语句  | `DoStatement` | `do_stmt`        |

#### DROP 语句（drop statement）

| 水杉解析器语义组名称             | 语义组类型                           | 返回值类型                        | MySQL 语义组名称            |
| -------------------------------- | ------------------------------------ | --------------------------------- | --------------------------- |
| `drop_database_statement`        | `DROP DATABASE` 语句                 | `ast.DropDatabaseStatement`       | `drop_database_stmt`        |
| `drop_event_statement`           | `DROP EVENT` 语句                    | `ast.DropEventStatement`          | `drop_event_stmt`           |
| `drop_function_statement`        | `DROP FUNCTION` 语句                 | `ast.DropFunctionStatement`       | `drop_function_stmt`        |
| `drop_index_statement`           | `DROP INDEX` 语句                    | `ast.DropIndexStatement`          | `drop_index_stmt`           |
| `drop_logfile_statement`         | `DROP LOGFILE` 语句                  | `ast.DropLogfileStatement`        | `drop_logfile_stmt`         |
| `drop_procedure_statement`       | `DROP PROCEDURE` 语句                | `ast.DropProcedureStatement`      | `drop_procedure_stmt`       |
| `drop_resource_group_statement`  | `DROP RESOURCE GROUP` 语句           | `ast.DropResourceGroupStatement`  | `drop_resource_group_stmt`  |
| `drop_role_statement`            | `DROP ROLE` 语句                     | `ast.DropRoleStatement`           | `drop_role_stmt`            |
| `drop_server_statement`          | `DROP SERVER` 语句                   | `ast.DropServerStatement`         | `drop_server_stmt`          |
| `drop_srs_statement`             | `DROP SPATIAL REFERENCE SYSTEM` 语句 | `ast.DropSrsStatement`            | `drop_srs_stmt`             |
| `drop_tablespace_statement`      | `DROP TABLESPACE` 语句               | `ast.DropTablespaceStatement`     | `drop_tablespace_stmt`      |
| `drop_undo_tablespace_statement` | `DROP UNDO TABLESPACE` 语句          | `ast.DropUndoTablespaceStatement` | `drop_undo_tablespace_stmt` |
| `drop_table_statement`           | `DROP TABLE` 语句                    | `ast.DropTableStatement`          | `drop_table_stmt`           |
| `drop_trigger_statement`         | `DROP TRIGGER` 语句                  | `ast.DropTriggerStatement`        | `drop_trigger_stmt`         |
| `drop_user_statement`            | `DROP USER` 语句                     | `ast.DropUserStatement`           | `drop_user_stmt`            |
| `drop_view_statement`            | `DROP VIEW` 语句                     | `ast.DropViewStatement`           | `drop_view_stmt`            |

#### EXPLAIN 语句（explain statement）

| 水杉解析器语义组名称     | 语义组类型                                     | 返回值类型                   | MySQL 语义组名称                               |
| ------------------------ | ---------------------------------------------- | ---------------------------- | ---------------------------------------------- |
| `explain_statement`      | `EXPLAIN` 语句                                 | `ast.ExplainStatement`       | `explain_stmt`<br />`explainable_stmt`【包含】 |
| `opt_explain_options`    | 可选的 `EXPLAIN` 分析选项                      | `ast.ExplainOptions`         | `opt_explain_options`                          |
| `opt_explain_format`     | 可选的 `FORMAT` 引导的指定分析结果格式子句     | `Optional[str]`              | `opt_explain_format`                           |
| `opt_explain_into`       | 可选的 `INTO` 引导的指定分析结果写入变量子句   | `Optional[ast.UserVariable]` | `opt_explain_into`                             |
| `opt_explain_for_schema` | 可选的 `FOR DATABASE` 引导的指定分析数据库子句 | `Optional[str]`              | `opt_explain_for_schema`                       |

#### IMPORT TABLE 语句（import table statement）

| 水杉解析器语义组名称     | 语义组类型          | 返回值类型                 | MySQL 语义组名称 |
| ------------------------ | ------------------- | -------------------------- | ---------------- |
| `import_table_statement` | `IMPORT TABLE` 语句 | `ast.ImportTableStatement` | `insert_stmt`    |

#### INSERT 语句和 REPLACE 语句（insert or replace statement）

| 水杉解析器语义组名称      | 语义组类型                                        | 返回值类型                     | MySQL 语义组名称          |
| ------------------------- | ------------------------------------------------- | ------------------------------ | ------------------------- |
| `insert_statement`        | `INSERT` 语句                                     | `ast.InsertOrReplaceStatement` | `insert_stmt`             |
| `replace_stmt`            | `REPLACE` 语句                                    | `ast.InsertOrReplaceStatement` | `replace_stmt`            |
| `insert_from_constructor` | 通过值列表构造的多行数据                          | `ast.TempInsertColumnAndValue` | `insert_from_constructor` |
| `insert_values`           | `VALUE` 或 `VALUES` 关键字引导的多行数据          | `List[ast.RowValue]`           | `insert_values`           |
| `keyword_value_or_values` | `VALUE` 关键字或 `VALUES` 关键字                  | -                              | `value_or_values`         |
| `row_value_list`          | `INSERT` 和 `REPLACE` 语句中的行数据的列表        | `List[ast.RowValue]`           | `values_list`             |
| `row_value`               | `INSERT` 和 `REPLACE` 语句中的行数据              | `ast.RowValue`                 | `row_value`               |
| `insert_from_query`       | 通过查询构造的多行数据                            | `ast.TempInsertColumnAndQuery` | `insert_query_expression` |
| `opt_insert_alias`        | `INSERT` 语句中 `AS` 关键字引导的表别名和字段别名 | `ast.TempInsertAlias`          | `opt_values_reference`    |
| `opt_insert_update_list`  | 可选的 `ON DUPLICATE KEY UPDATE` 子句             | `List[ast.UpdateElement]`      | `opt_insert_update_list`  |

#### INSTALL 语句和 UNINSTALL 语句（install and uninstall statement）

| 水杉解析器语义组名称         | 语义组类型                                   | 返回值类型              | MySQL 语义组名称             |
| ---------------------------- | -------------------------------------------- | ----------------------- | ---------------------------- |
| `install_set_rvalue`         | `INSTALL` 语句的 `SET` 子句中的右值          | `Expression`            | `install_set_rvalue`         |
| `install_set_value`          | `INSTALL` 语句的 `SET` 子句中的单个值        | `InstallSetValue`       | `install_set_value`          |
| `install_set_value_list`     | `INSTALL` 语句的 `SET` 子句中值的列表        | `List[InstallSetValue]` | `install_set_value_list`     |
| `opt_install_set_value_list` | 可选的 `INSTALL` 语句的 `SET` 子句中值的列表 | `List[InstallSetValue]` | `opt_install_set_value_list` |
| `install_statement`          | `INSTALL` 语句                               | `InstallStatement`      | `install_stmt`               |
| `uninstall`                  | `UNINSTALL` 语句                             | `UninstallStatement`    | `uninstall`                  |

#### KILL 语句（kill statement）

| 水杉解析器语义组名称 | 语义组类型  | 返回值类型      | MySQL 语义组名称 |
| -------------------- | ----------- | --------------- | ---------------- |
| `kill_statement`     | `KILL` 语句 | `KillStatement` | `kill`           |

#### LOCK 语句和 UNLOCK 语句（lock and unlock statement）

| 水杉解析器语义组名称 | 语义组类型             | 返回值类型        | MySQL 语义组名称  |
| -------------------- | ---------------------- | ----------------- | ----------------- |
| `lock_statement`     | `LOCK` 语句            | `LockStatement`   | `lock`            |
| `unlock_statement`   | `UNLOCK` 语句          | `UnlockStatement` | `unlock`          |
| `table_lock_list`    | 单个表的锁定信息的列表 | `List[TableLock]` | `table_lock_list` |
| `table_lock`         | 单个表的锁定信息       | `TableLock`       | `table_lock`      |

#### OPTIMIZE TABLE 语句（optimize table statement）

| 水杉解析器语义组名称       | 语义组类型            | 返回值类型                   | MySQL 语义组名称      |
| -------------------------- | --------------------- | ---------------------------- | --------------------- |
| `optimize_table_statement` | `OPTIMIZE TABLE` 语句 | `ast.OptimizeTableStatement` | `optimize_table_stmt` |

#### RENAME 语句（rename statement）

| 水杉解析器语义组名称 | 语义组类型                          | 返回值类型                            | MySQL 语义组名称      |
| -------------------- | ----------------------------------- | ------------------------------------- | --------------------- |
| `rename_statement`   | `RENAME` 语句                       | `ast.RenameStatement`                 | `rename`              |
| `rename_user_list`   | `RENAME` 语句中的用户重命名对的列表 | `List[Tuple[UserName, UserName]]`     | `rename_list`         |
| `rename_table_list`  | `RENAME` 语句中的表重命名对的列表   | `List[Tuple[Identifier, Identifier]]` | `table_to_table_list` |
| `rename_table_item`  | `RENAME` 语句中的表重命名对         | `Tuple[Identifier, Identifier]`       | `table_to_table`      |

#### REPAIR TABLE 语句（repair table statement）

| 水杉解析器语义组名称     | 语义组类型          | 返回值类型                 | MySQL 语义组名称    |
| ------------------------ | ------------------- | -------------------------- | ------------------- |
| `repair_table_statement` | `REPAIR TABLE` 语句 | `ast.RepairTableStatement` | `repair_table_stmt` |

#### SELECT 语句（select statement）

| 水杉解析器语义组名称      | 语义组类型                                                   | 返回值类型                  | MySQL 语义组名称                                     |
| ------------------------- | ------------------------------------------------------------ | --------------------------- | ---------------------------------------------------- |
| `simple_query`            | 简单查询（包括查询选项、查询字段表达式、`INTO` 子句、`FROM` 子句、`WHERE` 子句、`GROUP BY` 子句、`HAVING` 子句、`WINDOW` 子句和 `QUALIFY` 子句） | `ast.SimpleQuery`           | `query_specification`                                |
| `opt_select_option_list`  | 可选的查询选项的列表                                         | `ast.SelectOption`          | `select_options`                                     |
| `select_option_list`      | 查询选项的列表                                               | `ast.SelectOption`          | `select_option_list`                                 |
| `select_option`           | 查询选项                                                     | `ast.SelectOption`          | `select_option`<br />`query_spec_option`【超集】     |
| `select_item_list`        | `SELECT` 子句中的查询字段表达式的列表                        | `List[Expression]`          | `select_item_list`                                   |
| `select_item`             | `SELECT` 子句中的查询字段表达式                              | `ast.Expression`            | `select_item`                                        |
| `table_wild`              | 表中所有字段的通配符                                         | `ast.TableWild`             | `table_wild`                                         |
| `table_value_constructor` | 通过值列表构造的查询                                         | `ast.TableValueConstructor` | `table_value_constructor`                            |
| `row_value_explicit_list` | `ROW` 关键字引导的值列表的列表                               | `List[ast.Row]`             | `values_row_list`                                    |
| `row_value_explicit`      | `ROW` 关键字引导的值列表                                     | `ast.Row`                   | `row_value_explicit`                                 |
| `explicit_table`          | 明确指定表的查询                                             | `ast.ExplicitTable`         | `explicit_table`                                     |
| `query_primary`           | 初级查询（简单查询、通过值列表构造的查询或明确指定表的查询） | `ast.Query`                 | `query_primary`                                      |
| `query_expression_body`   | 中级查询（在初级查询的基础上，包含 `UNION`、`EXCEPT` 或 `INTERSECT`） | `ast.Query`                 | `query_expression_body`                              |
| `union_option`            | 联合类型                                                     | `ast.UnionOption`           | `union_option`                                       |
| `query_expression_bare`   | 高级查询（在中级查询的基础上，包含 `WITH`、`ORDER BY` 和 `LIMIT` 子句） | `ast.QueryExpression`       | `query_expression`                                   |
| `query_expression`        | 查询表达式（在高级查询的基础上，包含可选的锁指定子句）       | `ast.QueryExpression`       | `query_expression_with_opt_locking_clauses`          |
| `query_expression_parens` | 嵌套任意层括号的查询表达式                                   | `ast.QueryExpression`       | `query_expression_parens`                            |
| `select_statement`        | `SELECT` 语句                                                | `ast.SelectStatement`       | `select_stmt`<br />`select_stmt_with_into`【不兼容】 |

#### SHOW 语句（show statement）

| 水杉解析器语义组名称               | 语义组类型                                     | 返回值类型                         | MySQL 语义组名称              |
| ---------------------------------- | ---------------------------------------------- | ---------------------------------- | ----------------------------- |
| `show_binary_log_status_statement` | `SHOW BINARY LOG STATUS` 语句                  | `ast.ShowBinaryLogStatusStatement` | `show_binary_log_status_stmt` |
| `show_binary_logs_statement`       | `SHOW BINARY LOGS` 语句                        | `ast.ShowBinaryLogsStatement`      | `show_binary_logs_stmt`       |
| `show_binlog_events_statement`     | `SHOW BINLOG EVENTS` 语句                      | `ast.ShowBinlogEventsStatement`    | `show_binlog_events_stmt`     |
| `show_char_set_statement`          | `SHOW CHAR SET` 语句                           | `ast.ShowCharSetStatement`         | `show_character_set_stmt`     |
| `show_collation_statement`         | `SHOW COLLATION` 语句                          | `ast.ShowCollationStatement`       | `show_collation_stmt`         |
| `show_columns_statement`           | `SHOW COLUMNS` 语句                            | `ast.ShowColumnsStatement`         | `show_columns_stmt`           |
| `show_count_errors_statement`      | `SHOW COUNT ERRORS` 语句                       | `ast.ShowCountErrorsStatement`     | `show_count_errors_stmt`      |
| `show_count_warnings_statement`    | `SHOW COUNT WARNINGS` 语句                     | `ast.ShowCountWarningsStatement`   | `show_count_warnings_stmt`    |
| `show_create_database_stmt`        | `SHOW CREATE DATABASE` 语句                    | `ast.ShowCreateDatabaseStatement`  | `show_create_database_stmt`   |
| `show_create_event_statement`      | `SHOW CREATE EVENT` 语句                       | `ast.ShowCreateEventStatement`     | `show_create_event_stmt`      |
| `show_create_function_statement`   | `SHOW CREATE FUNCTION` 语句                    | `ast.ShowCreateFunctionStatement`  | `show_create_function_stmt`   |
| `show_create_procedure_statement`  | `SHOW CREATE PROCEDURE` 语句                   | `ast.ShowCreateProcedureStatement` | `show_create_procedure_stmt`  |
| `show_create_table_statement`      | `SHOW CREATE TABLE` 语句                       | `ast.ShowCreateTableStatement`     | `show_create_table_stmt`      |
| `show_create_trigger_statement`    | `SHOW CREATE TRIGGER` 语句                     | `ast.ShowCreateTriggerStatement`   | `show_create_trigger_stmt`    |
| `show_create_user_statement`       | `SHOW CREATE USER` 语句                        | `ast.ShowCreateUserStatement`      | `show_create_user_stmt`       |
| `show_create_view_statement`       | `SHOW CREATE VIEW` 语句                        | `ast.ShowCreateViewStatement`      | `show_create_view_stmt`       |
| `show_databases_statement`         | `SHOW DATABASES` 语句                          | `ast.ShowDatabasesStatement`       | `show_databases_stmt`         |
| `show_engine_logs_statement`       | `SHOW ENGINE LOGS` 语句                        | `ast.ShowEngineLogsStatement`      | `show_engine_logs_stmt`       |
| `show_engine_mutex_stmt`           | `SHOW ENGINE MUTEX` 语句                       | `ast.ShowEngineMutexStatement`     | `show_engine_mutex_stmt`      |
| `show_engine_status_stmt`          | `SHOW ENGINE STATUS` 语句                      | `ast.ShowEngineStatusStatement`    | `show_engine_status_stmt`     |
| `show_engines_statement`           | `SHOW ENGINES` 语句                            | `ast.ShowEnginesStatement`         | `show_engines_stmt`           |
| `show_errors_statement`            | `SHOW ERRORS` 语句                             | `ast.ShowErrorsStatement`          | `show_errors_stmt`            |
| `show_events_statement`            | `SHOW EVENTS` 语句                             | `ast.ShowEventsStatement`          | `show_events_stmt`            |
| `show_function_code_statement`     | `SHOW FUNCTION CODE` 语句                      | `ast.ShowFunctionCodeStatement`    | `show_function_code_stmt`     |
| `show_function_status_statement`   | `SHOW FUNCTION STATUS` 语句                    | `ast.ShowFunctionStatusStatement`  | `show_function_status_stmt`   |
| `show_grants_statement`            | `SHOW GRANTS` 语句                             | `ast.ShowEnginesStatement`         | `show_grants_stmt`            |
| `show_keys_statement`              | `SHOW KEYS` 语句                               | `ast.ShowKeysStatement`            | `show_keys_stmt`              |
| `show_master_status_statement`     | `SHOW MASTER STATUS` 语句                      | `ast.ShowMasterStatusStatement`    | `show_master_status_stmt`     |
| `show_open_tables_statement`       | `SHOW OPEN TABLES` 语句                        | `ast.ShowOpenTablesStatement`      | `show_open_tables_stmt`       |
| `show_parse_tree_statement`        | `SHOW PARSE TREE` 语句                         | `ast.ShowParseTreeStatement`       | `show_parse_tree_stmt`        |
| `show_plugins_statement`           | `SHOW PLUGINS` 语句                            | `ast.ShowPluginsStatement`         | `show_plugins_stmt`           |
| `show_privileges_statement`        | `SHOW PRIVILEGES` 语句                         | `ast.ShowPrivilegesStatement`      | `show_privileges_stmt`        |
| `show_procedure_code_statement`    | `SHOW PROCEDURE CODE` 语句                     | `ast.ShowProcedureCodeStatement`   | `show_procedure_code_stmt`    |
| `show_procedure_status_statement`  | `SHOW PROCEDURE STATUS` 语句                   | `ast.ShowProcedureStatusStatement` | `show_procedure_status_stmt`  |
| `show_processlist_statement`       | `SHOW PROCESSLIST` 语句                        | `ast.ShowProcesslistStatement`     | `show_processlist_stmt`       |
| `show_profile_statement`           | `SHOW PROFILE` 语句                            | `ast.ShowProfileStatement`         | `show_profile_stmt`           |
| `show_profiles_statement`          | `SHOW PROFILES` 语句                           | `ast.ShowProfilesStatement`        | `show_profiles_stmt`          |
| `show_relaylog_events_statement`   | `SHOW RELAYLOG EVENTS` 语句                    | `ast.ShowRelaylogEventsStatement`  | `show_relaylog_events_stmt`   |
| `show_replica_status_statement`    | `SHOW REPLICA STATUS` 语句                     | `ast.ShowReplicaStatusStatement`   | `show_replica_status_stmt`    |
| `show_replicas_statement`          | `SHOW REPLICAS` 语句                           | `ast.ShowReplicasStatement`        | `show_replicas_stmt`          |
| `show_status_statement`            | `SHOW STATUS` 语句                             | `ast.ShowStatusStatement`          | `show_status_stmt`            |
| `show_table_status_statement`      | `SHOW TABLE STATUS` 语句                       | `ast.ShowTableStatusStatement`     | `show_table_status_stmt`      |
| `show_tables_statement`            | `SHOW TABLES` 语句                             | `ast.ShowTablesStatement`          | `show_tables_stmt`            |
| `show_triggers_statement`          | `SHOW TRIGGERS` 语句                           | `ast.ShowTriggersStatement`        | `show_triggers_stmt`          |
| `show_warnings_statement`          | `SHOW WARNINGS` 语句                           | `ast.ShowWarningsStatement`        | `show_variables_stmt`         |
| `show_variables_statement`         | `SHOW VARIABLES` 语句                          | `ast.ShowVariablesStatement`       | `show_warnings_stmt`          |
| `opt_binlog_in`                    | 可选的 `IN` 关键字引导的指定文件名子句         | `Optional[str]`                    | `opt_binlog_in`               |
| `opt_binlog_from`                  | 可选的 `FROM` 关键字引导指定位事件开始位置子句 | `Optional[int]`                    | `binlog_from`                 |
| `opt_wild_or_where`                | 可选的通配符或 `WHERE` 子句                    | `ast.TempWildOrWhere`              | `opt_wild_or_where`           |
| `opt_show_schema`                  | `SHOW` 语句中可选的数据库名称                  | `Optional[str]`                    | `opt_db`                      |
| `engine_name_or_all`               | 引擎名称或 `ALL` 关键字                        | `Optional[str]`                    | `engine_or_all`               |
| `opt_for_query`                    | 可选的 `FOR QUERY` 引导的线程 ID               | `Optional[int]`                    | `opt_for_query`               |
| `opt_for_channel`                  | 可选的 `FOR CHANNEL` 引导的通道名              | `Optional[str]`                    | `opt_channel`                 |

#### START TRANSACTION 语句（start transaction statement）

| 水杉解析器语义组名称                 | 语义组类型               | 返回值类型                      | MySQL 语义组名称                    |
| ------------------------------------ | ------------------------ | ------------------------------- | ----------------------------------- |
| `start_transaction_statement`        | `START TRANSACTION` 语句 | `ast.StartTransactionStatement` | `start`                             |
| `opt_start_transaction_options_list` | 可选的事务选项的列表     | `ast.StartTransactionOption`    | `opt_start_transaction_option_list` |
| `start_transaction_options_list`     | 事务选项的列表           | `ast.StartTransactionOption`    | `start_transaction_option_list`     |
| `start_transaction_options`          | 事务选项                 | `ast.StartTransactionOption`    | `start_transaction_option`          |

#### TRUNCATE 语句（truncate statement）

| 水杉解析器语义组名称 | 语义组类型      | 返回值类型          | MySQL 语义组名称 |
| -------------------- | --------------- | ------------------- | ---------------- |
| `truncate_statement` | `TRUNCATE` 语句 | `TruncateStatement` | `truncate_stmt`  |

#### UPDATE 语句（update statement）

| 水杉解析器语义组名称  | 语义组类型                    | 返回值类型            | MySQL 语义组名称 |
| --------------------- | ----------------------------- | --------------------- | ---------------- |
| `update_statement`    | `UPDATE` 语句                 | `UpdateStatement`     | `update_stmt`    |
| `update_element_list` | `UPDATE` 语句中的更新项的列表 | `List[UpdateElement]` | `update_list`    |
| `update_element`      | `UPDATE` 语句中的更新项       | `UpdateElement`       | `update_elem`    |

# 子句（clause）

#### FROM 子句（from clause）

| 水杉解析器语义组名称 | 语义组类型         | 返回值类型        | MySQL 语义组名称                         |
| -------------------- | ------------------ | ----------------- | ---------------------------------------- |
| `opt_from_clause`    | 可选的 `FROM` 子句 | `List[ast.Table]` | `opt_from_clause`                        |
| `from_clause`        | `FROM` 子句        | `List[ast.Table]` | `from_clause`<br />`from_tables`【包含】 |

#### GROUP BY 子句（group by clause）

| 水杉解析器语义组名称  | 语义组类型                          | 返回值类型                    | MySQL 语义组名称   |
| --------------------- | ----------------------------------- | ----------------------------- | ------------------ |
| `opt_group_by_clause` | 可选的 `GROUP BY` 子句              | `Optional[ast.GroupByClause]` | `opt_group_clause` |
| `olap_opt`            | `GROUP BY` 子句中的分组统计信息规则 | `ast.EnumOlapOpt`             | `olap_opt`         |

#### HAVING 子句（having clause）

| 水杉解析器语义组名称 | 语义组类型           | 返回值类型                 | MySQL 语义组名称    |
| -------------------- | -------------------- | -------------------------- | ------------------- |
| `opt_having_clause`  | 可选的 `HAVING` 子句 | `Optional[ast.Expression]` | `opt_having_clause` |

#### 索引指定子句（index hint clause）

| 水杉解析器语义组名称     | 语义组类型                         | 返回值类型              | MySQL 语义组名称                                 |
| ------------------------ | ---------------------------------- | ----------------------- | ------------------------------------------------ |
| `index_hint_for`         | 索引指定子句中的索引用途           | `ast.EnumIndexHintFor`  | `index_hint_clause`                              |
| `index_hint_type`        | 索引指定子句中指定类型             | `ast.EnumIndexHintType` | `index_hint_type`                                |
| `hint_key_name`          | 索引指定子句中的索引名称           | `str`                   | `key_usage_element`                              |
| `hint_key_name_list`     | 索引指定子句中的索引名称的列表     | `List[str]`             | `key_usage_list`                                 |
| `opt_hint_key_name_list` | 索引指定子句中可选的索引名称的列表 | `List[str]`             | `opt_key_usage_list`                             |
| `index_hint`             | 索引指定子句                       | `ast.IndexHint`         | `index_hint_definition`                          |
| `index_hint_list`        | 索引指定子句的列表                 | `List[ast.IndexHint]`   | `index_hints_list`                               |
| `opt_index_hint_list`    | 可选的索引指定子句的列表           | `List[ast.IndexHint]`   | `opt_index_hints_list`<br />`opt_key_definition` |

#### INTO 子句（into clause）

| 水杉解析器语义组名称    | 语义组类型                                         | 返回值类型            | MySQL 语义组名称        |
| ----------------------- | -------------------------------------------------- | --------------------- | ----------------------- |
| `opt_into_clause`       | 可选的 `INTO` 子句                                 | `ast.IntoClauseBase`  | `into_clause`【超集】   |
| `into_destination`      | `INTO` 子句中的写入目标                            | `ast.IntoClauseBase`  | `into_destination`      |
| `opt_load_data_charset` | 可选的 `INTO` 子句和 `LOAD` 语句中指定字符集的子句 | `ast.Charset`         | `opt_load_data_charset` |
| `opt_field_term`        | 可选的 `COLUMNS` 引导的外部文件字段格式选项的列表  | `ast.FileFieldOption` | `opt_field_term`        |
| `field_term_list`       | 外部文件字段格式选项的列表                         | `ast.FileFieldOption` | `field_term_list`       |
| `field_term`            | 外部文件字段格式选项                               | `ast.FileFieldOption` | `field_term`            |
| `opt_line_term`         | 可选的 `LINES` 引导的外部文件行格式选项的列表      | `ast.FileLineOption`  | `opt_line_term`         |
| `line_term_list`        | 外部文件行格式选项的列表                           | `ast.FileLineOption`  | `line_term_list`        |
| `line_term`             | 外部文件行格式选项                                 | `ast.FileLineOption`  | `line_term`             |

#### LIMIT 子句（limit clause）

| 水杉解析器语义组名称      | 语义组类型                                  | 返回值类型                  | MySQL 语义组名称                            |
| ------------------------- | ------------------------------------------- | --------------------------- | ------------------------------------------- |
| `opt_limit_clause`        | 可选的 `LIMIT` 子句                         | `Optional[ast.LimitClause]` | `opt_limit_clause`                          |
| `limit_clause`            | `LIMIT` 子句                                | `ast.LimitClause`           | `limit_clause`<br />`limit_options`【超集】 |
| `opt_simple_limit_clause` | 可选的简单 `LIMIT` 子句（不支持指定偏移量） | `Optional[ast.LimitClause]` | `opt_simple_limit`                          |
| `limit_option`            | `LIMIT` 子句中的数量                        | `ast.Expression`            | `limit_option`                              |

#### 锁指定子句（locking clause）

| 水杉解析器语义组名称    | 语义组类型                                            | 返回值类型                | MySQL 语义组名称                                         |
| ----------------------- | ----------------------------------------------------- | ------------------------- | -------------------------------------------------------- |
| `locking_clause_list`   | 锁指定子句的列表                                      | `List[ast.LockingClause]` | `locking_clause_list`                                    |
| `locking_clause`        | 锁指定子句                                            | `ast.LockingClause`       | `locking_clause`<br />`table_locking_list`【包含】       |
| `lock_strength`         | 指定锁类型的关键字（`UPDATE` 或 `SHARE`）             | `ast.LockStrength`        | `lock_strength`                                          |
| `opt_locked_row_action` | 可选的指定锁行为的关键字（`SKIP LOCKED` 或 `NOWAIT`） | `ast.LockedRowAction`     | `opt_locked_row_action`<br />`locked_row_action`【超集】 |

#### ORDER BY 子句（order by clause）

| 水杉解析器语义组名称  | 语义组类型                                  | 返回值类型                    | MySQL 语义组名称                                             |
| --------------------- | ------------------------------------------- | ----------------------------- | ------------------------------------------------------------ |
| `order_direction`     | 指定排序方向的 `ASC` 或 `DESC` 关键字       | `ast.EnumOrderDirection`      | `ordering_direction`                                         |
| `opt_order_direction` | 可选的指定排序方向的 `ASC` 或 `DESC` 关键字 | `ast.EnumOrderDirection`      | `opt_ordering_direction`                                     |
| `order_expr`          | 指定排序条件及方向的表达式                  | `ast.OrderExpression`         | `order_expr`                                                 |
| `order_by_list`       | 指定排序条件及方向的表达式的列表            | `ast.OrderClause`             | `order_list`<br />`gorder_list`                              |
| `opt_order_by_clause` | 可选的 `ORDER BY` 子句                      | `Optional[ast.OrderByClause]` | `opt_order_clause`<br />`order_clause`<br />`opt_window_order_by_clause`<br />`opt_gorder_clause` |

#### OVER 子句（over clause）

| 水杉解析器语义组名称      | 语义组类型                                             | 返回值类型                    | MySQL 语义组名称                                             |
| ------------------------- | ------------------------------------------------------ | ----------------------------- | ------------------------------------------------------------ |
| `window_border_type`      | 窗口的边界类型                                         | `ast.WindowBorderTypeEnum`    | `window_frame_units`                                         |
| `opt_window_exclude`      | 窗口函数中可选的 `EXCLUDE` 子句                        | `ast.WindowExclusionTypeEnum` | `opt_window_frame_exclusion`                                 |
| `window_frame_start`      | 窗口开始边界                                           | `ast.WindowBorder`            | `window_frame_start`                                         |
| `window_frame_bound`      | 窗口开始边界或窗口结束边界                             | `ast.WindowBorder`            | `window_frame_bound`                                         |
| `window_frame_extent`     | 窗口的开始和结束边界                                   | `ast.WindowBorders`           | `window_frame_extent`<br />`window_frame_between`            |
| `opt_window_frame_clause` | 窗口框架（包括边界类型、边界值、排除值）               | `ast.WindowFrame`             | `opt_window_frame_clause`                                    |
| `window_name_or_spec`     | `OVER` 关键字引导的窗口子句（不含 `OVER` 关键字）      | `ast.Window`                  | `window_name_or_spec`<br />`window_spec`<br />`window_spec_details` |
| `windowing_clause`        | `OVER` 关键字引导的窗口子句（含 `OVER` 关键字）        | `ast.Window`                  | `windowing_clause`                                           |
| `opt_windowing_clause`    | 可选的 `OVER` 关键字引导的窗口子句（含 `OVER` 关键字） | `ast.Window`                  | `opt_windowing_clause`                                       |

#### PARTITION 子句（partition clause）

用于 DQL 语句中的表子句、`INSERT` 语句、`REPLACE` 语句、`DELETE` 语句和 `LOAD` 语句，指定使用的分区列表。

| 水杉解析器语义组名称   | 语义组类型              | 返回值类型                       | MySQL 语义组名称    |
| ---------------------- | ----------------------- | -------------------------------- | ------------------- |
| `opt_partition_clause` | 可选的 `PARTITION` 子句 | `Optional[List[ast.Expression]]` | `opt_use_partition` |
| `partition_clause`     | `PARTITION` 子句        | `List[ast.Expression]`           | `use_partition`     |

#### 窗口函数中的 PARTITION BY 子句（window partition by clause）

用于窗口函数中的 `OVER` 子句，指定窗口分区规则。

| 水杉解析器语义组名称      | 语义组类型                 | 返回值类型             | MySQL 语义组名称       |
| ------------------------- | -------------------------- | ---------------------- | ---------------------- |
| `opt_partition_by_clause` | 可选的 `PARTITION BY` 子句 | `List[ast.Expression]` | `opt_partition_clause` |

#### QUALIFY 子句（qualify clause）

| 水杉解析器语义组名称 | 语义组类型            | 返回值类型                 | MySQL 语义组名称     |
| -------------------- | --------------------- | -------------------------- | -------------------- |
| `opt_qualify_clause` | 可选的 `QUALIFY` 子句 | `Optional[ast.Expression]` | `opt_qualify_clause` |

#### WHERE 子句（where clause）

| 水杉解析器语义组名称 | 语义组类型          | 返回值类型                 | MySQL 语义组名称   |
| -------------------- | ------------------- | -------------------------- | ------------------ |
| `opt_where_clause`   | 可选的 `WHERE` 子句 | `Optional[ast.Expression]` | `opt_where_clause` |
| `where_clause`       | `WHERE` 子句        | `ast.Expression`           | `where_clause`     |

#### WINDOW 子句（window clause）

| 水杉解析器语义组名称     | 语义组类型           | 返回值类型                   | MySQL 语义组名称                                             |
| ------------------------ | -------------------- | ---------------------------- | ------------------------------------------------------------ |
| `opt_window_clause`      | 可选的 `WINDOW` 子句 | `Optional[List[ast.Window]]` | `opt_window_clause`                                          |
| `window_definition_list` | 窗口定义子句的列表   | `List[ast.Window]`           | `window_definition_list`                                     |
| `window_definition`      | 窗口定义子句         | `ast.Window`                 | `window_definition`<br />`window_spec`【包含】<br />`window_spec_details`【包含】 |

#### WITH 子句（with clause）

| 水杉解析器语义组名称 | 语义组类型              | 返回值类型                 | MySQL 语义组名称    |
| -------------------- | ----------------------- | -------------------------- | ------------------- |
| `opt_with_clause`    | 可选的 `WITH` 子句      | `Optional[ast.WithClause]` | `opt_with_clause`   |
| `with_clause`        | `WITH` 子句             | `ast.WithClause`           | `with_clause`       |
| `with_table_list`    | `WITH` 子句中的表的列表 | `List[ast.WithTable]`      | `with_list`         |
| `with_table`         | `WITH` 子句中的表       | `ast.WithTable`            | `common_table_expr` |

#### DDL 中的 PARTITION BY 子句（ddl partition by clause）

| 水杉解析器语义组名称               | 语义组类型                                           | 返回值类型                         | MySQL 语义组名称                                             |
| ---------------------------------- | ---------------------------------------------------- | ---------------------------------- | ------------------------------------------------------------ |
| `ddl_partition_by_clause`          | DDL 中的 `PARTITION BY` 子句                         | `ast.DdlPartitionByClause`         | `partition_clause`                                           |
| `partition_type_definition`        | DDL 的分区类型定义子句                               | `ast.PartitionTypeDefinition`      | `part_type_def`                                              |
| `opt_key_algorithm`                | 可选的 `ALGORITHM` 关键字引导的指定分区算法子句      | `Optional[ast.IntLiteral]`         | `opt_key_algo`                                               |
| `opt_keyword_linear`               | 可选的 `linear` 关键字                               | -                                  | `opt_linear`                                                 |
| `opt_num_partitions`               | 可选的 `PARTITIONS` 关键字引导的指定分区数量子句     | `Optional[int]`                    | `opt_num_parts`                                              |
| `opt_subpartition_type_definition` | 可选的子分区的类型定义子句                           | `ast.SubPartitionTypeDefinition`   | `opt_sub_part`                                               |
| `opt_num_subpartitions`            | 可选的 `SUBPARTITION` 关键字引导的指定子分区数量子句 | `Optional[int]`                    | `opt_num_subparts`                                           |
| `opt_partition_definition_list`    | 可选的括号嵌套的分区定义子句的列表                   | `List[ast.PartitionDefinition]`    | `opt_part_defs`                                              |
| `partition_definition_list`        | 分区定义子句的列表                                   | `List[ast.PartitionDefinition]`    | `part_def_list`                                              |
| `partition_definition`             | 分区定义子句                                         | `ast.PartitionDefinition`          | `part_definition`                                            |
| `opt_partition_values`             | 可选的 `VALUES` 关键字引导的分区值列表子句           | `Optional[ast.PartitionValues]`    | `opt_part_values`<br />`part_func_max`【包含】<br />`part_values_in`【包含】 |
| `partition_value_list_parens_list` | “括号嵌套的分区值的列表” 的列表                      | `List[List[ast.PartitionValue]]`   | `part_value_list`                                            |
| `partition_value_list_parens`      | 括号嵌套的分区值的列表                               | `List[ast.PartitionValue]`         | `part_value_item_list_paren`                                 |
| `partition_value_list`             | 分区值的列表                                         | `List[ast.PartitionValue]`         | `part_value_item_list`                                       |
| `partition_value`                  | 分区值                                               | `ast.PartitionValue`               | `part_value_item`                                            |
| `opt_subpartition_definition_list` | 可选的括号嵌套的定义子分区子句的列表                 | `List[ast.SubPartitionDefinition]` | `opt_sub_partition`                                          |
| `subpartition_definition_list`     | 定义子分区子句的列表                                 | `List[ast.SubPartitionDefinition]` | `sub_part_list`                                              |
| `subpartition_definition`          | 定义子分区子句                                       | `ast.SubPartitionDefinition`       | `sub_part_definition`                                        |
| `opt_partition_option_list`        | 可选的分区配置选项的列表                             | `List[ast.PartitionOption]`        | `opt_part_options`                                           |
| `partition_option_list`            | 分区配置选项的列表                                   | `List[ast.PartitionOption]`        | `part_option_list`                                           |
| `partition_option`                 | 分区配置选项                                         | `ast.PartitionOption`              | `part_option`                                                |

# 短语（pharse）

#### DDL 表属性（ddl table option）

| 水杉解析器语义组名称                       | 语义组含义                                           | 返回值类型                      | MySQL 语义组名称                                          |
| ------------------------------------------ | ---------------------------------------------------- | ------------------------------- | --------------------------------------------------------- |
| `create_table_option_list`                 | 逗号或空格分隔的 `CREATE TABLE` 语句中的表属性的列表 | `List[ast.TableOption]`         | `create_table_options`                                    |
| `create_table_option_list_space_separated` | 空格分隔的 `CREATE TABLE` 语句中的表属性的列表       | `List[ast.TableOption]`         | `create_table_options_space_separated`                    |
| `create_table_option`                      | `CREATE TABLE` 语句中的表属性                        | `ast.TableOption`               | `create_table_option`                                     |
| `ternary_option`                           | 整数字面值、十六进制字面值或 `DEFAULT` 关键字        | `ast.Expression`                | `ternary_option`                                          |
| `row_format`                               | 行格式类型的枚举值                                   | `ast.EnumRowFormat`             | `row_types`                                               |
| `default_charset_option`                   | 指定默认字符集的数据库选项或表选项                   | `ast.TableOptionDefaultCharset` | `default_charset`                                         |
| `default_collate_option`                   | 指定默认排序规则的数据库选项或表选项                 | `ast.TableOptionDefaultCollate` | `default_collation`                                       |
| `merge_insert_type`                        | 向 MERGE 表插入数据的类型的枚举值                    | `ast.EnumMergeInsertType`       | `merge_insert_types`                                      |
| `autoextend_size_option`                   | 指定表空间每次自动扩展的大小属性                     | `ast.TableOptionAutoextendSize` | `option_autoextend_size`<br />`ts_option_autoextend_size` |

#### 字段类型（field type）

| 水杉解析器语义组名称       | 语义组含义                                                   | 返回值类型            | MySQL 语义组名称                                 |
| -------------------------- | ------------------------------------------------------------ | --------------------- | ------------------------------------------------ |
| `field_type_param_1`       | 括号中的 1 个字段类型参数                                    | `ast.FieldTypeParams` | `field_length`<br />`type_datetime_precision`    |
| `opt_field_type_param_1`   | 可选的括号中的 1 个字段类型参数                              | `ast.FieldTypeParams` | `opt_field_length`<br />`standard_float_options` |
| `field_type_param_2`       | 括号中的 2 个字段类型参数                                    | `ast.FieldTypeParams` | `precision`                                      |
| `opt_field_type_param_2`   | 可选的括号中的 2 个字段类型参数                              | `ast.FieldTypeParams` | `opt_precision`                                  |
| `opt_field_type_param_0_1` | 可选的括号中的 0 个或 1 个字段类型参数                       | `ast.FieldTypeParams` | `func_datetime_precision`                        |
| `opt_field_type_param_1_2` | 可选的括号中的 1 个或 2 个字段类型参数                       | `ast.FieldTypeParams` | `float_options`                                  |
| `cast_type`                | `CAST` 函数、`CONVERT` 函数以及 `JSON_VALUE` 函数中指定的返回值类型 | `ast.CastType`        | `cast_type`                                      |
| `opt_returning_type`       | `JSON_VALUE` 函数中可选的返回值类型                          | `ast.CastType`        | `opt_returning_type`                             |
| `field_option`             | 单个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）           | `ast.FieldOption`     | `field_option`                                   |
| `field_option_list`        | 多个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）           | `ast.FieldOption`     | `field_opt_list`                                 |
| `opt_field_option_list`    | 可选的多个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）     | `ast.FieldOption`     | `field_options`                                  |
| `field_type`               | DDL 语句中的字段类型                                         | `ast.FieldType`       | `type`                                           |

#### DDL 表元素（ddl table element）

| 水杉解析器语义组名称                  | 语义组含义                                                   | 返回值类型                           | MySQL 语义组名称                                |
| ------------------------------------- | ------------------------------------------------------------ | ------------------------------------ | ----------------------------------------------- |
| `table_element_list`                  | DDL 定义表中的元素的列表                                     | `List[ast.TableElement]`             | `table_element_list`                            |
| `table_element`                       | DDL 定义表中的元素                                           | `ast.TableElement`                   | `table_element`                                 |
| `column_definition`                   | DDL 的字段定义信息（含外键）                                 | `ast.ColumnDefinition`               | `column_def`                                    |
| `field_definition`                    | DDL 的字段基本信息（不含外键约束）                           | `ast.FieldDefinition`                | `field_def`                                     |
| `opt_generated_always`                | 可选的 `GENERATED ALWAYS` 关键字                             | `bool`                               | `opt_generated_always`                          |
| `opt_stored_attribute`                | 可选的 `VIRTUAL` 或 `STORED` 关键字                          | `ast.EnumStoredAttribute`            | `opt_stored_attribute`                          |
| `opt_references_definition`           | 可选的 `REFERENCES` 关键字引导的指定外键约束子句             | `Optional[ast.ReferencesDefinition]` | `opt_references`                                |
| `references_definition`               | `REFERENCES` 关键字引导的指定外键约束子句                    | `ast.ReferencesDefinition`           | `references`                                    |
| `opt_match_clause`                    | 外键约束中可选的 `MATCH` 子句                                | `ast.EnumReferenceMatch`             | `opt_match_clause`                              |
| `opt_on_update_on_delete`             | `REFERENCES` 指定外键约束子句中的 `ON UPDATE` 和 `ON DELETE` 子句 | `ast.TempOnUpdateOnDelete`           | `opt_on_update_delete`                          |
| `reference_action_option`             | `REFERENCE` 子句中指定外键变化时行为的选项                   | `ast.EnumReferenceActionOption`      | `delete_option`                                 |
| `index_definition`                    | DDL 的索引定义信息                                           | `ast.TableElement`                   | `table_constraint_def`                          |
| `opt_index_name_and_type`             | 可选的索引名称和索引数据结构                                 | `ast.TempIndexNameAndType`           | `opt_index_name_and_type`                       |
| `index_key_definition_list`           | 索引字段定义的列表                                           | `List[ast.IndexKeyDefinition]`       | `key_list`                                      |
| `index_key_definition`                | 索引字段定义                                                 | `ast.IndexKeyDefinition`             | `key_part`                                      |
| `index_key_definition_with_expr_list` | 包含使用表达式的索引字段定义的列表                           | `List[ast.IndexKeyDefinition]`       | `key_list_with_expression`                      |
| `index_key_definition_with_expr`      | 包含使用表达式的索引字段定义                                 | `ast.IndexKeyDefinition`             | `key_part_with_expression`                      |
| `constraint_index_type`               | 约束类索引类型（主键索引或唯一索引）                         | `ast.EnumIndexType`                  | `constraint_key_type`                           |
| `opt_keyword_key_or_index`            | 可选的 `KEY` 或 `INDEX` 关键字                               | -                                    | `opt_key_or_index`                              |
| `keyword_key_or_index`                | `KEY` 或 `INDEX` 关键字                                      | -                                    | `key_or_index`                                  |
| `keyword_keys_or_index`               | `KEYS`、`INDEX` 或 `INDEXES` 关键字                          | -                                    |                                                 |
| `opt_constraint_enforcement`          | 可选的 `ENFORCED`、`NOT ENFORCED` 关键字                     | `Optional[bool]`                     | `opt_constraint_enforcement`                    |
| `constraint_enforcement`              | `ENFORCED`、`NOT ENFORCED` 关键字                            | `bool`                               | `constraint_enforcement`<br />`opt_not`【包含】 |

#### DDL 字段属性（ddl column attribute）

| 水杉解析器语义组名称        | 语义组含义                               | 返回值类型                  | MySQL 语义组名称                                             |
| --------------------------- | ---------------------------------------- | --------------------------- | ------------------------------------------------------------ |
| `opt_column_attribute_list` | 可选的 DDL 字段属性的列表                | `List[ast.ColumnAttribute]` | `opt_column_attribute_list`                                  |
| `column_attribute_list`     | DDL 字段属性的列表                       | `List[ast.ColumnAttribute]` | `column_attribute_list`                                      |
| `column_attribute`          | DDL 字段属性                             | `ast.ColumnAttribute`       | `column_attribute`<br />`opt_keyword_primary`【包含】<br />`constraint_enforcement`【包含】 |
| `now_or_signed_literal`     | `NOW` 关键字或数值字面值                 | `ast.Expression`            | `now_or_signed_literal`                                      |
| `column_format`             | DDL 字段存储格式的枚举                   | `ast.EnumColumnFormat`      | `column_format`                                              |
| `storage_media`             | DDL 字段存储介质的枚举                   | `ast.EnumStorageMedia`      | `storage_media`                                              |
| `opt_constraint_name`       | 可选的 `CONSTRAINT` 关键字引导的约束名称 | `Optional[str]`             | `opt_constraint_name`                                        |
| `check_constraint`          | 指定约束条件的 `CHECK` 子句              | `ast.Expression`            | `check_constraint`                                           |

#### DDL 索引属性（ddl index attribute）

| 水杉解析器语义组名称                | 语义组含义                             | 返回值类型                              | MySQL 语义组名称             |
| ----------------------------------- | -------------------------------------- | --------------------------------------- | ---------------------------- |
| `opt_spatial_index_attribute_list`  | 可选的 `SPATIAL` 类型索引的属性的列表  | `List[ast.IndexAttribute]`              | `opt_spatial_index_options`  |
| `spatial_index_attribute_list`      | `SPATIAL` 类型索引的属性的列表         | `List[ast.IndexAttribute]`              | `spatial_index_options`      |
| `spatial_index_attribute`           | `SPATIAL` 类型索引的属性               | `ast.IndexAttribute`                    | `spatial_index_option`       |
| `opt_fulltext_index_attribute_list` | 可选的 `FULLTEXT` 类型索引的属性的列表 | `List[ast.IndexAttribute]`              | `opt_fulltext_index_options` |
| `fulltext_index_attribute_list`     | `FULLTEXT` 类型索引的属性的列表        | `List[ast.IndexAttribute]`              | `fulltext_index_options`     |
| `fulltext_index_attribute`          | `FULLTEXT` 类型索引的属性              | `ast.IndexAttribute`                    | `fulltext_index_option`      |
| `opt_normal_index_attribute_list`   | 可选的普通类型索引的属性的列表         | `List[ast.IndexAttribute]`              | `opt_index_options`          |
| `normal_index_attribute_list`       | 普通类型索引的属性的列表               | `List[ast.IndexAttribute]`              | `index_options`              |
| `normal_index_attribute`            | 普通类型索引的属性                     | `ast.IndexAttribute`                    | `index_option`               |
| `common_index_attribute`            | 各索引类型通用的属性                   | `ast.IndexAttribute`                    | `common_index_option`        |
| `opt_index_type_clause`             | 可选的指定索引数据结构类型的子句       | `Optional[ast.IndexAttrUsingIndexType]` | `opt_index_type_clause`      |
| `index_type_clause`                 | 指定索引数据结构类型的子句             | `ast.IndexAttrUsingIndexType`           | `index_type_clause`          |
| `index_structure_type`              | 索引数据结构类型                       | `ast.EnumIndexStructureType`            | `index_type`                 |

`spatial_index_option` 语义组与 `common_index_attribute` 语义组逻辑一致，但为保证可拓展性将其拆分为两个语义组。

#### 别名（alias）

| 水杉解析器语义组名称 | 语义组含义                          | 返回值类型      | MySQL 语义组名称  |
| -------------------- | ----------------------------------- | --------------- | ----------------- |
| `opt_keyword_as`     | 可选的 `AS` 关键字                  | -               | `opt_as`          |
| `opt_select_alias`   | 可选的字段表达式和 UDF 表达式的别名 | `Optional[str]` | `select_alias`    |
| `opt_table_alias`    | 可选的表表达式的别名                | `Optional[str]` | `opt_table_alias` |

#### JSON 表选项（json table option）

| 水杉解析器语义组名称     | 语义组含义                          | 返回值类型               | MySQL 语义组名称                                             |
| ------------------------ | ----------------------------------- | ------------------------ | ------------------------------------------------------------ |
| `json_on_response`       | Json 解析失败时的返回值             | `ast.JsonOnResponse`     | `json_on_response`                                           |
| `json_on_empty`          | Json 解析遇到空值时的处理方法       | `ast.JsonOnResponse`     | `on_empty`                                                   |
| `json_on_error`          | Json 解析遇到错误时的处理方法       | `ast.JsonOnResponse`     | `on_error`                                                   |
| `json_on_empty_on_error` | Json 解析遇到空值或错误时的处理方法 | `ast.JsonOnEmptyOnError` | `opt_on_empty_or_error`<br />`opt_on_empty_or_error_json_table` |

#### 时间间隔（time interval）

| 水杉解析器语义组名称 | 语义组含义     | 返回值类型         | MySQL 语义组名称                             |
| -------------------- | -------------- | ------------------ | -------------------------------------------- |
| `time_interval`      | 时间间隔表达式 | `ast.TimeInterval` | 无对应语义组（`INTERVAL_SYM expr interval`） |

#### DML 语句选项（dml option）

| 水杉解析器语义组名称       | 语义组含义                                                   | 返回值类型      | MySQL 语义组名称      |
| -------------------------- | ------------------------------------------------------------ | --------------- | --------------------- |
| `opt_keyword_ignore`       | 可选的 `IGNORE` 关键字                                       | `ast.DmlOption` | `opt_ignore`          |
| `opt_keyword_low_priority` | 可选的 `LOW_PRIORITY` 关键字                                 | `ast.DmlOption` | `opt_low_priority`    |
| `opt_delete_option_list`   | 可选的 `DELETE` 语句中的选项的列表                           | `ast.DmlOption` | `opt_delete_options`  |
| `delete_option_list`       | `DELETE` 语句中的选项的列表                                  | `ast.DmlOption` |                       |
| `delete_option`            | `DELETE` 语句中的选项（`quick`、`LOW_PRIORITY` 或 `IGNORE` 关键字） | `ast.DmlOption` | `opt_delete_option`   |
| `opt_insert_option`        | 可选的 `INSERT` 语句中的选项                                 | `ast.DmlOption` | `insert_lock_option`  |
| `opt_replace_option`       | 可选的 `REPLACE` 语句中的选项                                | `ast.DmlOption` | `replace_lock_option` |

#### 重复值处理规则（on duplicate）

| 水杉解析器语义组名称 | 语义组含义                                              | 返回值类型        | MySQL 语义组名称 |
| -------------------- | ------------------------------------------------------- | ----------------- | ---------------- |
| `opt_on_duplicate`   | 可选的指定重复值处理规则的 `REPLACE` 或 `IGNORE` 关键字 | `ast.OnDuplicate` | `opt_duplicate`  |
| `on_duplicate`       | 指定重复值处理规则的 `REPLACE` 或 `IGNORE` 关键字       | `ast.OnDuplicate` | `duplicate`      |

#### DDL 修改表选项（ddl alter option）

| 水杉解析器语义组名称                   | 语义组含义                                                   | 返回值类型                      | MySQL 语义组名称                                             |
| -------------------------------------- | ------------------------------------------------------------ | ------------------------------- | ------------------------------------------------------------ |
| `alter_command_modifier_list`          | `ALTER` 命令的修饰选项的列表                                 | `ast.TempAlterOptionList`       | `alter_commands_modifier_list`                               |
| `alter_command_modifier`               | `ALTER` 命令的修饰选项                                       | `ast.TempAlterOptionList`       | `alter_commands_modifier`                                    |
| `opt_alter_option_lock_and_algorithm`  | 可选的任意顺序的 `ALGORITHM` 和 `LOCK` 修改表选项子句        | `ast.TempAlterOptionList`       | `opt_index_lock_and_algorithm`                               |
| `alter_option_algorithm`               | DDL 修改表选项：`ALGORITHM`（创建索引时使用的算法或机制）    | `ast.AlterAlgorithmOption`      | `alter_algorithm_option`<br />`alter_algorithm_option_value`【包含】 |
| `alter_option_lock`                    | DDL 修改表选项：`LOCK`（指定创建索引时对表施加的锁类型）     | `ast.AlterLockOption`           | `alter_lock_option`<br />`alter_lock_option_value`【包含】   |
| `opt_alter_option_with_validation`     | 可选的 DDL 修改表选项：`WITH VALIDATION` 或 `WITHOUT VALIDATION` | `ast.AlterOptionWithValidation` | `opt_with_validation`                                        |
| `alter_option_with_validation`         | DDL 修改表选项：`WITH VALIDATION` 或 `WITHOUT VALIDATION`    | `ast.AlterOptionWithValidation` | `with_validation`                                            |
| `opt_drop_tablespace_option_list`      | 可选的 `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表      | `List[ast.AlterOption]`         | `opt_drop_ts_options`                                        |
| `drop_tablespace_option_list`          | `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表             | `List[ast.AlterOption]`         | `drop_ts_option_list`                                        |
| `drop_tablespace_option`               | `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项                   | `ast.AlterOption`               | `drop_ts_option`                                             |
| `opt_drop_undo_tablespace_option_list` | 可选的 `UNDO TABLESPACE` 的选项的列表                        | `List[ast.AlterOption]`         | `opt_undo_tablespace_options`                                |
| `drop_undo_tablespace_option_list`     | `UNDO TABLESPACE` 的选项的列表                               | `List[ast.AlterOption]`         | `undo_tablespace_option_list`                                |
| `drop_undo_tablespace_option`          | `UNDO TABLESPACE` 的选项                                     | `ast.AlterOption`               | `undo_tablespace_option`                                     |
| `alter_option_engine`                  | ALTER 选项：`ENGINE`                                         | `ast.AlterOptionEngine`         | `ts_option_engine`                                           |
| `alter_option_wait`                    | ALTER 选项：`WAIT` 或 `NO_WAIT`                              | `ast.AlterOptionWait`           | `ts_option_wait`                                             |

`drop_undo_tablespace_option` 语义组与 `alter_option_engine` 语义组一致，但考虑可拓展性保留单独的 `drop_undo_tablespace_option` 语义组。

#### CPU 范围（cpu range）

| 水杉解析器语义组名称           | 语义组含义                                       | 返回值类型       | MySQL 语义组名称               |
| ------------------------------ | ------------------------------------------------ | ---------------- | ------------------------------ |
| `opt_resource_group_vcpu_list` | `VCPU` 关键字引导的指定 CPU 编号或范围列表的等式 | `List[CpuRange]` | `opt_resource_group_vcpu_list` |
| `cpu_num_or_range_list`        | CPU 编号或范围的列表                             | `List[CpuRange]` | `vcpu_range_spec_list`         |
| `cpu_num_or_range`             | CPU 编号或范围                                   | `CpuRange`       | `vcpu_num_or_range`            |

# 表（table）

MySQL 有一种语法扩展，允许将逗号分隔的表引用列表本身作为一个表引用使用。例如：

```sql
SELECT * FROM (t1, t2) JOIN t3 ON 1
```

这种写法在标准 SQL 中是不允许的。该语法等价于：

```sql
SELECT * FROM (t1 CROSS JOIN t2) JOIN t3 ON 1
```

我们将这个规则称为 `table_reference_list_parens`。

一个 `table_factor` 可以是一个 `single_table`、一个 `subquery`、一个 `derived_table`、一个 `joined_table` 或自定义的 `table_reference_list_parens`，每一个都可以被任意数量的括号包围。这会导致语法上的歧义，因为 `table_factor` 本身也可以被括号包围。

我们通过设计语法来解决这个问题：规定 `table_factor` 本身不能有括号，但它的所有子情况各自拥有自己的括号规则，比如 `single_table_parens`、`joined_table_parens` 和 `table_reference_list_parens`。这样虽然看起来有些繁琐，但语法是无歧义的，并且不会产生移进 / 归约冲突（shift / reduce conflicts）。

## 通用表逻辑（general table）

`table_reference_list` 是在 DQL 语句的 `FROM` 子句、`UPDATE` 语句、`DELETE` 语句中使用的表名的列表；`table_reference_list` 是 `table_reference` 的列表。

| 水杉解析器语义组名称          | 语义组含义                                                   | 返回值类型        | MySQL 语义组名称              |
| ----------------------------- | ------------------------------------------------------------ | ----------------- | ----------------------------- |
| `table_reference_list`        | 在 DQL 和 DML 语句中的表元素的列表                           | `List[ast.Table]` | `table_reference_list`        |
| `table_reference`             | 在 DQL 和 DML 语句中的表元素                                 | `ast.Table`       | `table_reference`             |
| `esc_table_reference`         | 不兼容 ODBC 语法的表元素                                     | `ast.Table`       | `esc_table_reference`         |
| `table_factor`                | 单个表元素（包含任意层括号的 single_table、derived_table、joined_table_parens、table_reference_list_parens、table_function） | `ast.Table`       | `table_factor`                |
| `table_reference_list_parens` | 包含任意层括号的在 DQL 和 DML 语句中的表元素的列表           | `List[ast.Table]` | `table_reference_list_parens` |

## 单表（single table）

| 水杉解析器语义组名称  | 语义组含义                                       | 返回值类型        | MySQL 语义组名称      |
| --------------------- | ------------------------------------------------ | ----------------- | --------------------- |
| `single_table_parens` | 包含任意层嵌套括号的、通过表明标识符定义的单个表 | `ast.SingleTable` | `single_table_parens` |
| `single_table`        | 通过表名标识符定义的单个表                       | `ast.SingleTable` | `single_table`        |

## 关联表（joined table）

| 水杉解析器语义组名称  | 语义组含义                   | 返回值类型         | MySQL 语义组名称      |
| --------------------- | ---------------------------- | ------------------ | --------------------- |
| `joined_table`        | 关联表                       | `ast.Table`        | `joined_table`        |
| `joined_table_parens` | 包含大于等于一层括号的关联表 | `ast.Table`        | `joined_table_parens` |
| `natural_join_type`   | 自然连接的关键字             | `ast.EnumJoinType` | `natural_join_type`   |
| `inner_join_type`     | 内连接的关键字               | `ast.EnumJoinType` | `inner_join_type`     |
| `outer_join_type`     | 外关联的关键字               | `ast.EnumJoinType` | `outer_join_type`     |
| `opt_keyword_inner`   | 可选的 `INNER` 关键字        | -                  | `opt_inner`           |
| `opt_keyword_outer`   | 可选的 `OUTER` 关键字        | -                  | `opt_outer`           |

## 派生表（derived table）

| 水杉解析器语义组名称 | 语义组含义 | 返回值类型         | MySQL 语义组名称 |
| -------------------- | ---------- | ------------------ | ---------------- |
| `derived_table`      | 派生表     | `ast.DerivedTable` | `derived_table`  |

## 生成表函数（table function）

| 水杉解析器语义组名称        | 语义组含义                           | 返回值类型                      | MySQL 语义组名称 |
| --------------------------- | ------------------------------------ | ------------------------------- | ---------------- |
| `json_table_column_type`    | `JSON_TABLE` 函数中的字段类型        | `ast.JsonTableColumnType`       | `jt_column_type` |
| `json_table_column`         | `JSON_TABLE` 函数中的字段            | `ast.JsonTableColumnBase`       | `jt_column`      |
| `json_table_column_list`    | `JSON_TABLE` 函数中的字段的列表      | `List[ast.JsonTableColumnBase]` | `columns_list`   |
| `json_table_columns_clause` | `JSON_TABLE` 函数中的 `COLUMNS` 子句 | `List[ast.JsonTableColumnBase]` | `columns_clause` |
| `table_function`            | 生成表函数                           | `ast.TableFunctionJsonTable`    | `table_function` |

# 表达式（expression）

#### 一般表达式（general expression）

| 水杉解析器语义组名称           | 语义组含义                                       | 返回值类型                 | MySQL 语义组名称                                     |
| ------------------------------ | ------------------------------------------------ | -------------------------- | ---------------------------------------------------- |
| `operator_compare`             | 比较运算符                                       | `ast.EnumOperatorCompare`  | `comp_op`                                            |
| `simple_expr`                  | 简单表达式                                       | `ast.Expression`           | `simple_expr`                                        |
| `binary_expr`                  | 二元表达式                                       | `ast.Expression`           | `bit_expr`                                           |
| `predicate_expr`               | 谓语表达式                                       | `ast.Expression`           | `predicate`                                          |
| `bool_expr`                    | 布尔表达式                                       | `ast.Expression`           | `bool_pri`<br />`all_or_any`【包含】                 |
| `expr`                         | 一般表达式                                       | `ast.Expression`           | `expr`<br />`grouping_expr`                          |
| `opt_expr`                     | 可选的一般表达式                                 | `ast.Expression`           | `opt_expr`                                           |
| `opt_paren_expr_list`          | 可选的嵌套括号内可选的逗号分隔的一般表达式列表   | `List[ast.Expression]`     | `opt_paren_expr_list`                                |
| `opt_expr_list`                | 可选的逗号分隔的一般表达式列表                   | `List[ast.Expression]`     | `opt_expr_list`                                      |
| `expr_list`                    | 逗号分隔的一般表达式列表                         | `List[ast.Expression]`     | `expr_list`<br />`group_list`                        |
| `udf_expr`                     | UDF 表达式（自定义函数中的参数）                 | `ast.UdfExpression`        | `udf_expr`                                           |
| `udf_expr_list`                | 逗号分隔的 UDF 表达式的列表                      | `List[ast.UdfExpression]`  | `udf_expr_list`                                      |
| `opt_udf_expr_list`            | 可选的逗号分隔的 UDF 表达式的列表                | `List[ast.UdfExpression]`  | `opt_udf_expr_list`                                  |
| `match_column_list`            | `MATCH` 函数的列名的列表                         | `List[ast.Ident]`          | `ident_list_arg`                                     |
| `opt_in_natural_language_mode` | 全文本索引可选的 `IN NATURAL LANGUAGE MODE` 选项 | `ast.FulltextOption`       | `opt_natural_language_mode`                          |
| `opt_with_query_expansion`     | 全文本索引可选的 `WITH QUERY EXPANSION` 选项     | `ast.FulltextOption`       | `opt_query_expansion`                                |
| `fulltext_options`             | 全文本索引的选项                                 | `ast.FulltextOption`       | `fulltext_options`                                   |
| `opt_keyword_array`            | 可选的 `ARRAY` 关键字                            | `bool`                     | `opt_array_cast`                                     |
| `opt_keyword_interval`         | 可选的 `INTERVAL` 关键字                         | `bool`                     | `opt_interval`                                       |
| `when_list`                    | `CASE` 结构中的 `WHEN` 条件的列表                | `List[ast.WhenItem]`       | `when_list`                                          |
| `opt_else`                     | `CASE` 结构中可选的 `ELSE` 子句                  | `Optional[ast.Expression]` | `opt_else`                                           |
| `opt_expr_or_default_list`     | 可选的一般表达式或 `DEFAULT` 关键字的列表        | `List[ast.Expression]`     | `opt_values`                                         |
| `expr_or_default_list`         | 一般表达式或 `DEFAULT` 关键字的列表              | `List[ast.Expression]`     | `values`                                             |
| `expr_or_default`              | 一般表达式或 `DEFAULT` 关键字                    | `ast.Expression`           | `expr_or_default`                                    |
| `subquery`                     | 子查询表达式                                     | `ast.SubQuery`             | `row_subquery`<br />`table_subquery`<br />`subquery` |

#### 聚集函数表达式（sum function expression）

| 水杉解析器语义组名称 | 语义组含义                            | 返回值类型                    | MySQL 语义组名称                                             |
| -------------------- | ------------------------------------- | ----------------------------- | ------------------------------------------------------------ |
| `sum_expr`           | 聚集函数的表达式                      | `ast.Expression`              | `set_function_specification`<br />`sum_expr`【超集】<br />`grouping_operation`【超集】 |
| `in_sum_expr`        | 聚集函数的参数                        | `ast.Expression`              | `in_sum_expr`                                                |
| `opt_distinct`       | 可选的 `DISTINCT` 关键字              | `bool`                        | `opt_distinct`                                               |
| `opt_separator`      | 可选的 `SEPARATOR` 关键字引导的分隔符 | `Optional[ast.StringLiteral]` | `opt_gconcat_separator`                                      |

#### 窗口函数表达式（window function expression）

| 水杉解析器语义组名称         | 语义组含义                                                   | 返回值类型            | MySQL 语义组名称                                  |
| ---------------------------- | ------------------------------------------------------------ | --------------------- | ------------------------------------------------- |
| `stable_integer`             | 在执行过程中为常量的整数（字面值、参数占位符或用户变量）     | `ast.Param`           | `stable_integer`<br />`param_or_var`【超集】      |
| `opt_from_first_or_last`     | `NTH_VALUE` 窗口函数中的 `FROM FIRST` 子句或 `FROM LAST` 子句 | `ast.FromFirstOrLast` | `opt_from_first_last`                             |
| `opt_null_treatment`         | 窗口函数中指定 NULL 值处理策略的 `RESPECT NULLS` 或 `IGNORE NULLS` 子句 | `ast.NullTreatment`   | `opt_null_treatment`                              |
| `opt_lead_or_lag_info`       | LEAD 和 LAG 窗口函数中偏移量及默认值信息                     | `ast.LeadOrLagInfo`   | `opt_lead_lag_info`<br />`opt_ll_default`【包含】 |
| `window_function_expression` | 窗口函数表达式                                               | `ast.FuncWindowBase`  | `window_func_call`                                |

#### 普通函数表达式（function expression）

包括如下 4 种语义组：

- 关键字函数：函数名称为官方 SQL 2003 关键字，因为函数名是一个官方保留字，所以解析器中需要有专门的语法规则，不会产生任何潜在的冲突。
- 非关键字函数：函数名称为非保留关键字，因为函数名不是官方保留字，所以需要专门的语法规则，以避免与语言的其他部分产生不兼容的问题。一个函数出现在这里，要不是出于对其他 SQL 语法兼容的考虑，要不是出于类型推导的需要。
- 冲突风险函数：函数名称为非保留关键字，因为使用了常规的语法形式且该非保留关键字在文法的其他部分也有使用，所以需要专门的语法规则来处理。
- 常规函数：函数名称不是关键字，通常不会对语言引入副作用。

| 水杉解析器语义组名称  | 语义组含义                                 | 返回值类型               | MySQL 语义组名称                                             |
| --------------------- | ------------------------------------------ | ------------------------ | ------------------------------------------------------------ |
| `function_expression` | 函数表达式                                 | `ast.FunctionExpression` | `function_call_keyword`【超集】<br />`function_call_nonkeyword`【超集】<br />`function_call_conflict`【超集】<br />`geometry_function`【超集】<br />`function_call_generic`【超集】 |
| `now_expression`      | `NOW` 关键字及精度                         | `ast.FunctionExpression` | `now`                                                        |
| `date_time_type`      | 时间类型（`DATE`、`TIME` 或者 `DATETIME`） | `ast.DateTimeType`       | `date_time_type`                                             |

#### 运算符表达式（operator expression）

运算符表达式的备选规则均包含在一般表达式的语义组中。

#### 近似表达式（app expression）

在其他特定场景下使用的近似表达式。

# 基础元素（basic）

除 `base` 中的抽象节点外，不继承其他任何节点。

#### 固定的枚举类型（fixed enum）

| 水杉解析器语义组名称    | 语义组类型                                             | 返回值类型                  | MySQL 语义组名称       |
| ----------------------- | ------------------------------------------------------ | --------------------------- | ---------------------- |
| `opt_drop_restrict`     | 可选的 `DROP` 语句中 `RESTRICT` 选项的枚举值           | `ast.EnumDropRestrict`      | `opt_restrict`         |
| `opt_show_command_type` | 可选的 `SHOW` 语句命令类型的枚举值                     | `ast.EnumShowCommandType`   | `opt_show_cmd_type`    |
| `opt_repair_type_list`  | 可选的 `REPAIR` 语句命令类型的枚举值的列表             | `ast.EnumRepairType`        | `opt_mi_repair_types`  |
| `repair_type_list`      | `REPAIR` 语句命令类型的枚举值的列表                    | `ast.EnumRepairType`        | `mi_repair_types`      |
| `repair_type`           | `REPAIR` 语句命令类型的枚举值                          | `ast.EnumRepairType`        | `mi_repair_type`       |
| `opt_check_type_list`   | 可选的 `CHECK` 语句命令类型的枚举值的列表              | `ast.EnumCheckType`         | `opt_mi_check_types`   |
| `check_type_list`       | `CHECK` 语句命令类型的枚举值的列表                     | `ast.EnumCheckType`         | `mi_check_types`       |
| `check_type`            | `CHECK` 语句命令类型的枚举值                           | `ast.EnumCheckType`         | `mi_check_type`        |
| `opt_checksum_type`     | 可选的 `CHECKSUM` 语句命令类型的枚举值                 | `ast.EnumChecksumType`      | `opt_checksum_type`    |
| `opt_profile_type_list` | 可选的 `SHOW PROFILE` 语句中性能分析指标的枚举值的列表 | `ast.EnumProfileType`       | `opt_profile_defs`     |
| `profile_type_list`     | `SHOW PROFILE` 语句中性能分析指标的枚举值列表          | `ast.EnumProfileType`       | `profile_defs`         |
| `profile_type`          | `SHOW PROFILE` 语句中性能分析指标的枚举值              | `ast.EnumProfileType`       | `profile_def`          |
| `opt_variable_type`     | 可选的变量类型的枚举值                                 | `ast.EnumVariableType`      | `opt_var_type`         |
| `install_option_type`   | `INSTALL` 语句的安装选项的枚举值                       | `ast.EnumInstallOptionType` | `install_option_type`  |
| `kill_option_type`      | `KILL` 语句的选项的枚举值                              | `ast.EnumKillOptionType`    | `kill_option`          |
| `lock_option_type`      | `LOCK` 语句的锁定选项的枚举值                          | `ast.EnumLockOptionType`    | `lock_option`          |
| `opt_open_ssl_type`     | SSL 选项的枚举值                                       | `EnumOpenSslType`           | `opt_ssl`              |
| `opt_chain_type`        | `CHAIN` 选项的枚举值                                   | `EnumChainType`             | `opt_chain`            |
| `opt_release_type`      | `RELEASE` 选项的枚举值                                 | `EnumReleaseType`           | `opt_release`          |
| `resource_group_type`   | 资源组类型的枚举值                                     | `EnumResourceGroupType`     | `resource_group_types` |

#### 固定的词语组合（fixed word）

| 水杉解析器语义组名称             | 语义组类型                                                   | 返回值类型 | MySQL 语义组名称         |
| -------------------------------- | ------------------------------------------------------------ | ---------- | ------------------------ |
| `opt_keyword_of`                 | 可选的 `OPT` 关键字                                          | -          | `opt_of`                 |
| `opt_keyword_all`                | 可选的 `ALL` 关键字                                          | -          | `opt_all`                |
| `opt_keyword_into`               | 可选的 `INTO` 关键字                                         | -          | `opt_INTO`               |
| `opt_keyword_default`            | 可选的 `DEFAULT` 关键字                                      | -          | `opt_default`            |
| `opt_keyword_storage`            | 可选的 `STORAGE` 关键字                                      | -          | `opt_storage`            |
| `opt_keyword_temporary`          | 可选的 `TEMPORARY` 关键字                                    | `bool`     | `opt_temporary`          |
| `opt_keyword_extended`           | 可选的 `EXTENDED` 关键字                                     | `bool`     | `opt_extended`           |
| `opt_keyword_if_not_exists`      | 可选的 `IF NOT EXISTS` 关键字                                | `bool`     | `opt_if_not_exists`      |
| `opt_keyword_if_exists`          | 可选的 `IF EXISTS` 关键字                                    | `bool`     | `if_exists`              |
| `opt_keyword_force`              | 可选的 `FORCE` 关键字                                        | `bool`     | `opt_force`              |
| `opt_keyword_full`               | 可选的 `FULL` 关键字                                         | `bool`     | `opt_full`               |
| `opt_keyword_work`               | 可选的 `WORK` 关键字                                         | `bool`     | `opt_work`               |
| `opt_keyword_no_write_to_binlog` | 可选的 `NO_WRITE_TO_BINLOG` 关键字或 `LOCAL` 关键字          | `bool`     | `opt_no_write_to_binlog` |
| `opt_keyword_table`              | 可选的 `TABLE` 关键字                                        | -          | `opt_table`              |
| `keyword_describe_or_explain`    | `DESCRIBE` 关键字或 `EXPLAIN` 关键字                         | -          | `describe_command`       |
| `keyword_table_or_tables`        | `TABLE` 关键字或 `TABLES` 关键字                             | -          | `table_or_tables`        |
| `keyword_master_or_binary`       | `MASTER` 关键字或 `BINARY` 关键字                            | -          | `master_or_binary`       |
| `keyword_from_or_in`             | `FROM` 关键字或 `IN` 关键字                                  | -          | `from_or_in`             |
| `keyword_keys_or_index`          | `KEYS`、`INDEX` 或 `INDEXES` 关键字                          | -          | `keys_or_index`          |
| `keyword_replica_or_slave`       | `REPLICA` 或 `SLAVE` 关键字                                  | -          | `replica`                |
| `opt_braces`                     | 可选的空括号                                                 | -          | `optional_braces`        |
| `opt_comma`                      | 可选的逗号                                                   | -          | `opt_comma`              |
| `keyword_charset`                | `CHARSET` 关键字或 `CHAR SET` 关键字                         | -          | `character_set`          |
| `keyword_nchar`                  | `NCHAR` 关键字或 `NATIONAL CHAR` 关键字（兼容的 `NCHAR` 类型名称） | -          | `nchar`                  |
| `keyword_varchar`                | `CHAR VARYING` 关键字或 `VARCHAR` 关键字（兼容的 `VARCHAR` 类型名称） | -          | `varchar`                |
| `keyword_nvarchar`               | `NVARCHAR` 关键字、`NATIONAL VARCHAR` 关键字、`Ncharacter_setCHAR VARCHAR` 关键字、`NATIONAL CHAR VARYING` 关键字或 `NCHAR VARYING` 关键字（兼容的 `NVARCHAR` 类型名称） | -          | `nvarchar`               |
| `opt_equal`                      | 可选的 `=` 运算符或 `:=` 运算符                              | -          | `opt_equal`              |
| `equal`                          | `=` 运算符或 `:=` 运算符                                     | -          | `equal`                  |

## 标识符（ident）

| 水杉解析器语义组名称                                   | 语义组类型                                                   | 返回值类型             | MySQL 语义组名称                                             |
| ------------------------------------------------------ | ------------------------------------------------------------ | ---------------------- | ------------------------------------------------------------ |
| `ident_sys`                                            | 不是保留字或非保留关键字的标识符                             | `ast.Ident`            | `IDENT_sys`                                                  |
| `ident_keywords_unambiguous`（MySQL）                  | 非保留关键字，可以在任何位置用作未见引号的标识符，而不会引入语法冲突 | `ast.Ident`            | `ident_keywords_unambiguous`                                 |
| `ident_keywords_ambiguous_1_roles_and_labels`（MySQL） | 非保留关键字，不能用作角色名称（role name）和存储过程标签名称（SP label name） | `ast.Ident`            | `ident_keywords_ambiguous_1_roles_and_labels`                |
| `ident_keywords_ambiguous_2_labels`（MySQL）           | 非保留关键字，不能用作存储过程标签名称（SP label name）      | `ast.Ident`            | `ident_keywords_ambiguous_2_labels`                          |
| `ident_keywords_ambiguous_3_roles`（MySQL）            | 非保留关键字，不能用作角色名称（role name）                  | `ast.Ident`            | `ident_keywords_ambiguous_3_roles`                           |
| `ident_keywords_ambiguous_4_system_variables`（MySQL） | 非保留关键字，不能用作 SET 语句中赋值操作左侧的变量名以及变量前缀 | `ast.Ident`            | `ident_keywords_ambiguous_4_system_variables`                |
| `ident_general_keyword`（MySQL）                       | 非保留关键字，在一般场景下可以直接使用                       | `ast.Ident`            | `ident_keyword`                                              |
| `ident_label_keyword`（MySQL）                         | 非保留关键字，可以用作存储过程标签名称（label name）         | `ast.Ident`            | `label_keyword`                                              |
| `ident_role_keyword`（MySQL）                          | 非保留关键字，可以用作角色名称（role name）                  | `ast.Ident`            | `role_keyword`                                               |
| `ident_variable_keyword`（MySQL）                      | 非保留关键字，可以作为 SET 语句中赋值操作左侧的变量名以及变量前缀 | `ast.Ident`            | `lvalue_keyword`                                             |
| `opt_ident_list`                                       | 可选的单个标识符（`ident`）的列表                            | `List[str]`            | `opt_name_list`                                              |
| `ident_list`                                           | 单个标识符（`ident`）的列表                                  | `List[str]`            | `simple_ident_list`<br />`ident_string_list`<br />`using_list`<br />`reference_list`<br />`name_list` |
| `ident`（MySQL）                                       | 单个标识符（`ident`）                                        | `ast.Ident`            | `ident`<br />`schema`<br />`window_name`                     |
| `opt_ident_list_parens`                                | 可选的括号嵌套的单个标识符（`ident`）的列表                  | `List[str]`            | `opt_derived_column_list`<br />`opt_ref_list`                |
| `label_ident`（MySQL）                                 | 表示存储过程名称的标识符                                     | `ast.Ident`            | `label_ident`                                                |
| `role_ident`（MySQL）                                  | 表示角色的标识符                                             | `ast.Ident`            | `role_ident`                                                 |
| `variable_identifier`                                  | 变量名标识符                                                 | `ast.Identifier`       | `lvalue_variable`                                            |
| `variable_ident`（MySQL）                              | 表示变量名或变量名前缀的标识符                               | `ast.Ident`            | `lvalue_ident`                                               |
| `ident_2`                                              | 点分隔的两个标识符（`ident.ident`）                          | `ast.Ident`            | `simple_ident_q`【部分】                                     |
| `ident_3`                                              | 点分隔的三个标识符（`ident.ident.ident`）                    | `ast.Ident`            | `simple_ident_q`【部分】                                     |
| `opt_identifier_list`                                  | 可选的通用标识符的列表                                       | `List[ast.Identifier]` | `opt_table_list`                                             |
| `identifier_list`                                      | 通用标识符的列表                                             | `List[ast.Identifier]` | `table_list`                                                 |
| `identifier`                                           | 通用标识符（`ident` 或 `ident.ident`）                       | `ast.Identifier`       | `table_ident`<br />`sp_name`                                 |
| `table_ident_opt_wild_list`                            | 表标识符及可选的 `.*` 的列表                                 | `List[ast.Identifier]` | `table_alias_ref_list`                                       |
| `table_ident_opt_wild`                                 | 表标识符及可选的 `.*`                                        | `ast.Identifier`       | `table_ident_opt_wild`                                       |
| `opt_wild`                                             | 可选的 `.*`                                                  | -                      | `opt_wild`                                                   |
| `simple_ident`                                         | 通用标识符（`ident` 或 `ident.ident` 或 `ident.ident.ident`） | `ast.Expression`       | `simple_ident`<br />`simple_ident_nospvar`<br />`insert_column` |
| `simple_ident_list`                                    | 逗号分隔的通用通配符的列表                                   | `List[ast.Expression]` | `ident_list`<br />`insert_columns`                           |
| `opt_ident`                                            | 可选的单个标识符                                             | `Optional[str]`        | `opt_existing_window_name`<br />`opt_ident`                  |

## 字符集名称（charset）

| 水杉解析器语义组名称 | 语义组含义                               | 返回值类型              | MySQL 语义组名称                                             |
| -------------------- | ---------------------------------------- | ----------------------- | ------------------------------------------------------------ |
| `charset_ascii`      | ASCII 相关字符集名称关键字               | `ast.CharsetTypeEnum`   | `ascii`                                                      |
| `charset_unicode`    | UNICODE 相关字符集名称关键字             | `ast.CharsetTypeEnum`   | `unicode`                                                    |
| `charset_name`       | 字符集（排序规则）名称或 `BINARY` 关键字 | `ast.Charset`           | `charset_name`<br />`old_or_new_charset_name`<br />`collation_name` |
| `opt_charset`        | 可选的指定字符集信息                     | `ast.Charset`           | `opt_charset_with_opt_binary`                                |
| `opt_collate`        | 指定比较和排序规则                       | `Optional[ast.Charset]` | `opt_collate`                                                |

## 字面值（literal）

| 水杉解析器语义组名称       | 语义组含义                                                   | 返回值类型                | MySQL 语义组名称                                             |
| -------------------------- | ------------------------------------------------------------ | ------------------------- | ------------------------------------------------------------ |
| `text_literal_sys_list`    | 字符串字面值的列表                                           | `List[str]`               | `TEXT_STRING_sys_list`                                       |
| `text_literal_sys`         | 字符串字面值（不包括 Unicode 字符串）                        | `ast.StringLiteral`       | `TEXT_STRING_sys`<br />`TEXT_STRING_literal`<br />`TEXT_STRING_filesystem`<br />`TEXT_STRING_password`<br />`TEXT_STRING_validated`<br />`TEXT_STRING_sys_nonewline`<br />`filter_wild_db_table_string`<br />`json_attribute` |
| `int_literal`              | 整数字面值                                                   | `ast.IntLiteral`          | `int64_literal`                                              |
| `int_literal_or_hex`       | 整数字面值或十六进制字面值                                   | `ast.IntLiteral`          | `real_ulong_num`<br />`real_ulonglong_num`                   |
| `paren_int_literal_or_hex` | 包含外层括号的整数字面值或十六进制字面值                     | `ast.IntLiteral`          | `ws_num_codepoints`                                          |
| `num_literal`              | 数值字面值（包含整数、浮点数和小数字面值）                   | `ast.NumberLiteral`       | `NUM_literal`<br />`ulonglong_num`                           |
| `num_literal_or_hex`       | 数值字面值或十六进制字面值                                   | `ast.NumberLiteral`       | `ulong_num`                                                  |
| `temporal_literal`         | 时间字面值                                                   | `ast.TemporalLiteral`     | `temporal_literal`                                           |
| `literal`                  | 非空字面值（包括数值、时间、布尔、真值、假值、十六进制、二进制字面值） | `ast.Literal`             | `literal`                                                    |
| `null_literal`             | 空值字面值                                                   | `ast.Literal`             | `null_as_literal`                                            |
| `literal_or_null`          | 可为空字面值                                                 | `ast.Literal`             | `literal_or_null`                                            |
| `text_literal`             | 字符串字面值                                                 | `ast.StringLiteral`       | `text_literal`                                               |
| `text_string`              | 字符串、二进制、十六进制字面值                               | `ast.StringLiteral`       | `text_string`                                                |
| `text_string_list`         | 逗号分隔的字符串、二进制、十六进制字面值的列表               | `List[ast.StringLiteral]` | `string_list`                                                |
| `signed_literal`           | 非空字面值或有符号的数值字面值                               | `ast.Literal`             | `signed_literal`                                             |
| `signed_literal_or_null`   | 可为空字面值或有符号的数值字面值                             | `ast.Literal`             | `signed_literal_or_null`                                     |
| `ident_or_text`            | 标识符或字符串字面值表示的名称                               | `ast.Expression`          | `ident_or_text`【部分】                                      |
| `size_number`              | 磁盘大小的数值                                               | `ast.Expression`          | `size_number`                                                |
| `role_name_list`           | 角色名称的列表                                               | `List[ast.RoleName]`      | `role_list`                                                  |
| `role_name`                | 角色名称                                                     | `ast.RoleName`            | `role`                                                       |
| `role_ident_or_text`       | 标识符或字符串字面值表示的角色名                             | `str`                     | `role_ident_or_text`                                         |
| `user_name_list`           | 用户名称的列表                                               | `List[ast.UserName]`      | `user_list`                                                  |
| `user_name`                | 用户名称                                                     | `ast.UserName`            | `user`                                                       |
| `explicit_user_name`       | 用户名称（不匹配 `CURRENT_USER` 关键字）                     | `ast.UserName`            | `user_ident_or_text`                                         |

## 参数（param）

| 水杉解析器语义组名称 | 语义组含义 | 返回值类型  | MySQL 语义组名称 |
| -------------------- | ---------- | ----------- | ---------------- |
| `param_marker`       | 参数占位符 | `ast.Param` | `param_marker`   |

## 变量（variable）

| 水杉解析器语义组名称          | 语义组含义                 | 返回值类型                   | MySQL 语义组名称                                |
| ----------------------------- | -------------------------- | ---------------------------- | ----------------------------------------------- |
| `variable_name`               | 用户变量或系统变量的变量名 | `str`                        | `ident_or_text`                                 |
| `user_variable_list`          | 用户变量的列表             | `List[UserVariable]`         | `execute_var_list`                              |
| `user_variable`               | 用户变量                   | `UserVariable`               | `execute_var_ident`（对应 `'@' ident_or_text`） |
| `user_or_local_variable_list` | 用户变量或本地变量的列表   | `List[ast.Variable]`         | `select_var_list`                               |
| `user_or_local_variable`      | 用户变量或本地变量         | `ast.Variable`               | `select_var_ident`                              |
| `system_variable_type`        | 系统变量类型               | `ast.EnumSystemVariableType` | `opt_rvalue_system_variable_type`               |
| `system_variable`             | 系统变量                   | `ast.SystemVariable`         | `rvalue_system_variable`【包含】                |
| `system_or_user_variable`     | 系统变量或用户变量         | `ast.Variable`               | `rvalue_system_or_user_variable`                |
| `user_variable_assignment`    | 用户变量赋值语句           | `ast.UserVariableAssignment` | `in_expression_user_variable_assignment`        |

## 时间单位类型（time_unit）

| 水杉解析器语义组名称 | 语义组含义                            | 返回值类型         | MySQL 语义组名称      |
| -------------------- | ------------------------------------- | ------------------ | --------------------- |
| `time_unit`          | 时间单位关键字                        | `ast.TimeUnitEnum` | `interval_time_stamp` |
| `interval_time_unit` | 时间单位关键字（INTERVAL 中的关键字） | `ast.TimeUnitEnum` | `interval`            |

# 其他处理逻辑

## 转移到词法解析层实现的 MySQL 语义组

- `or`：在水杉解析器中直接使用 `KEYWORD_OR` 终结符。
  - `OR_SYM`：一般场景下的 `OR` 关键字
  - `OR2_SYM`：配置了 `MODE_PIPES_AS_CONCAT` 模式的 `OR` 关键字（如果配置，则直接在词法解析层进行替换）
- `and`：在水杉解析器中直接使用 `KEYWORD_AND` 终结符。
  - `AND_SYM`：一般场景下的 `AND` 关键字
  - `AND_AND_SYM`：一般场景下的 `&&` 运算符（MySQL 会发出待消失语法警告）
- `not`：在水杉解析器中直接使用 `KEYWORD_NOT` 终结符。
  - `NOT_SYM`：一般场景下的 `NOT` 关键字
  - `NOT2_SYM`：配置了 `MODE_HIGH_NOT_PRECEDENCE` 模式的 `NOT` 关键字（如果配置，则直接在词法解析层进行替换）
- MySQL 在词法解析层将 `EXPLAIN` 映射为 `DESCRIBE` 终结符（在 `lex.h` 文件中），而我们将这个等价逻辑放在语法解析层中实现。

## 查询层级

水杉 SQL 支持的查询表达式的等级如下：

- 初级查询（query primary）
- 中级查询（query expression body）：在初级查询的基础上，包含 `UNION`、`EXCEPT` 或 `INTERSECT`；同时，也支持嵌套括号的查询表达式
- 高级查询（query expression rare）：在中级查询的基础上，包含 `WITH`、`ORDER BY` 和 `LIMIT` 子句
- 查询表达式（query expression）：在高级查询的基础上，包含锁指定子句
- `SELECT` 语句：在高级查询的基础上，额外包含锁指定子句和 `INTO` 子句

## 不兼容 MySQL 的语法

- 不允许在 `SELECT` 语句的最外层添加 `INTO` 子句，仅允许在`FROM` 子句前添加 `INTO` 子句。
