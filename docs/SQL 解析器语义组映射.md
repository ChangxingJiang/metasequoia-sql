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

| 水杉解析器语义组名称  | 语义组类型                | 返回值类型            | MySQL 语义组名称                                            |
| --------------------- | ------------------------- | --------------------- | ----------------------------------------------------------- |
| `start_entry`         | 入口语义组                | `Optional[Statement]` | `start_entry`                                               |
| `sql_statement_entry` | 标准 SQL 语句的入口语义组 | `Optional[Statement]` | `sql_statement`                                             |
| `sql_statement`       | 标准 SQL 语句             | `Statement`           | `simple_statement_or_begin`<br />`simple_statement`【超集】 |
| `opt_end_of_input`    | 可选的输入流结束符        | -                     | `opt_end_of_input`                                          |

# 语句（statement）

#### ALTER DATABASE 语句（alter database statement）

| 水杉解析器语义组名称       | 语义组类型            | 返回值类型               | MySQL 语义组名称      |
| -------------------------- | --------------------- | ------------------------ | --------------------- |
| `alter_database_statement` | `ALTER DATABASE` 语句 | `AlterDatabaseStatement` | `alter_database_stmt` |

#### ALTER EVENT 语句（alter event statement）

| 水杉解析器语义组名称    | 语义组类型         | 返回值类型            | MySQL 语义组名称   |
| ----------------------- | ------------------ | --------------------- | ------------------ |
| `alter_event_statement` | `ALTER EVENT` 语句 | `AlterEventStatement` | `alter_event_stmt` |

#### ALTER FUNCTION 语句（alter function statement）

| 水杉解析器语义组名称       | 语义组类型            | 返回值类型               | MySQL 语义组名称      |
| -------------------------- | --------------------- | ------------------------ | --------------------- |
| `alter_function_statement` | `ALTER FUNCTION` 语句 | `AlterFunctionStatement` | `alter_function_stmt` |

#### ALTER INSTANCE 语句（alter instance statement）

| 水杉解析器语义组名称       | 语义组类型            | 返回值类型               | MySQL 语义组名称        |
| -------------------------- | --------------------- | ------------------------ | ----------------------- |
| `alter_instance_statement` | `ALTER INSTANCE` 语句 | `AlterInstanceStatement` | `alter_instance_stmt`   |
| `alter_instance_action`    | `ALTER INSTANCE` 操作 | `AlterInstanceAction`    | `alter_instance_action` |

#### ALTER LOGFILE 语句（alter logfile statement）

| 水杉解析器语义组名称                  | 语义组类型                            | 返回值类型              | MySQL 语义组名称                  |
| ------------------------------------- | ------------------------------------- | ----------------------- | --------------------------------- |
| `alter_logfile_statement`             | `ALTER LOGFILE` 语句                  | `AlterLogfileStatement` | `alter_logfile_stmt`              |
| `opt_alter_logfile_group_option_list` | 可选的 `ALTER LOGFILE` 语句选项的列表 | `List[DdlOption]`       | `opt_alter_logfile_group_options` |
| `alter_logfile_group_option_list`     | `ALTER LOGFILE` 语句选项的列表        | `List[DdlOption]`       | `alter_logfile_group_option_list` |
| `alter_logfile_group_option`          | `ALTER LOGFILE` 语句的选项            | `DdlOption`             | `alter_logfile_group_option`      |

#### ALTER PROCEDURE 语句（alter procedure statement）

| 水杉解析器语义组名称        | 语义组类型             | 返回值类型                | MySQL 语义组名称       |
| --------------------------- | ---------------------- | ------------------------- | ---------------------- |
| `alter_procedure_statement` | `ALTER PROCEDURE` 语句 | `AlterProcedureStatement` | `alter_procedure_stmt` |

#### ALTER RESOURCE GROUP 语句（alter resource group statement）

| 水杉解析器语义组名称             | 语义组类型                  | 返回值类型                    | MySQL 语义组名称            |
| -------------------------------- | --------------------------- | ----------------------------- | --------------------------- |
| `alter_resource_group_statement` | `ALTER RESOURCE GROUP` 语句 | `AlterResourceGroupStatement` | `alter_resource_group_stmt` |

#### ALTER SERVER 语句（alter server statement）

| 水杉解析器语义组名称     | 语义组类型          | 返回值类型             | MySQL 语义组名称    |
| ------------------------ | ------------------- | ---------------------- | ------------------- |
| `alter_server_statement` | `ALTER SERVER` 语句 | `AlterServerStatement` | `alter_server_stmt` |

#### ALTER TABLE 语句（alter table statement）

| 水杉解析器语义组名称    | 语义组类型         | 返回值类型            | MySQL 语义组名称   |
| ----------------------- | ------------------ | --------------------- | ------------------ |
| `alter_table_statement` | `ALTER TABLE` 语句 | `AlterTableStatement` | `alter_table_stmt` |

#### ALTER TABLESPACE 语句（alter tablespace statement）

| 水杉解析器语义组名称               | 语义组类型                           | 返回值类型                 | MySQL 语义组名称               |
| ---------------------------------- | ------------------------------------ | -------------------------- | ------------------------------ |
| `alter_tablespace_statement`       | `ALTER TABLESPACE` 语句              | `AlterTablespaceStatement` | `alter_tablespace_stmt`        |
| `opt_alter_tablespace_option_list` | 可选的 `ALTER TABLESPACE` 选项的列表 | `List[DdlOption]`          | `opt_alter_tablespace_options` |
| `alter_tablespace_option_list`     | `ALTER TABLESPACE` 的选项的列表      | `List[DdlOption]`          | `alter_tablespace_option_list` |
| `alter_tablespace_option`          | `ALTER TABLESPACE` 的选项            | `DdlOption`                | `alter_tablespace_option`      |

#### ALTER UNDO TABLESPACE 语句（alter undo tablespace statement）

| 水杉解析器语义组名称              | 语义组类型                   | 返回值类型                     | MySQL 语义组名称             |
| --------------------------------- | ---------------------------- | ------------------------------ | ---------------------------- |
| `alter_undo_tablespace_statement` | `ALTER UNDO TABLESPACE` 语句 | `AlterUndoTablespaceStatement` | `alter_undo_tablespace_stmt` |

#### ALTER VIEW 语句（alter view statement）

| 水杉解析器语义组名称   | 语义组类型        | 返回值类型           | MySQL 语义组名称                                             |
| ---------------------- | ----------------- | -------------------- | ------------------------------------------------------------ |
| `alter_view_statement` | `ALTER VIEW` 语句 | `AlterViewStatement` | `alter_view_stmt`<br />`view_tail`【包含】<br />`view_query_block`【包含】 |

#### ANALYZE TABLE 语句（analyze table statement）

| 水杉解析器语义组名称         | 语义组类型           | 返回值类型              | MySQL 语义组名称             |
| ---------------------------- | -------------------- | ----------------------- | ---------------------------- |
| `analyze_table_statement`    | `ANALYZE TABLE` 语句 | `AnalyzeTableStatement` | `analyze_table_stmt`         |
| `opt_histogram`              | 可选的直方图参数     | `Histogram`             | `opt_histogram`              |
| `opt_histogram_update_param` | 直方图的更新参数     | `HistogramUpdateParam`  | `opt_histogram_update_param` |

#### BEGIN 语句（begin statement）

| 水杉解析器语义组名称 | 语义组类型   | 返回值类型       | MySQL 语义组名称 |
| -------------------- | ------------ | ---------------- | ---------------- |
| `begin_statement`    | `BEGIN` 语句 | `BeginStatement` | `begin_stmt`     |

#### BINLOG 语句（binlog statement）

| 水杉解析器语义组名称 | 语义组类型    | 返回值类型        | MySQL 语义组名称      |
| -------------------- | ------------- | ----------------- | --------------------- |
| `binlog_statement`   | `BINLOG` 语句 | `BinlogStatement` | `binlog_base64_event` |

#### CALL 语句（call statement）

| 水杉解析器语义组名称        | 语义组类型          | 返回值类型        | MySQL 语义组名称            |
| --------------------------- | ------------------- | ----------------- | --------------------------- |
| `change_statement`          | `CHANGE` 语句       | `ChangeStatement` | `change`                    |
| `change_replication_source` | `CHANGE` 复制源类型 | -                 | `change_replication_source` |

#### CHANGE 语句（change statement）

| 水杉解析器语义组名称 | 语义组类型  | 返回值类型      | MySQL 语义组名称 |
| -------------------- | ----------- | --------------- | ---------------- |
| `call_statement`     | `CALL` 语句 | `CallStatement` | `call_stmt`      |

#### CHECK TABLE 语句（check table statement）

| 水杉解析器语义组名称    | 语义组类型         | 返回值类型            | MySQL 语义组名称   |
| ----------------------- | ------------------ | --------------------- | ------------------ |
| `check_table_statement` | `CHECK TABLE` 语句 | `CheckTableStatement` | `check_table_stmt` |

#### CHECKSUM 语句（checksum statement）

| 水杉解析器语义组名称 | 语义组类型      | 返回值类型          | MySQL 语义组名称 |
| -------------------- | --------------- | ------------------- | ---------------- |
| `checksum_statement` | `CHECKSUM` 语句 | `ChecksumStatement` | `checksum`       |

#### CLONE 语句（clone statement）

| 水杉解析器语义组名称 | 语义组类型                                | 返回值类型       | MySQL 语义组名称  |
| -------------------- | ----------------------------------------- | ---------------- | ----------------- |
| `clone_statement`    | `CLONE` 语句                              | `CloneStatement` | `clone_stmt`      |
| `opt_datadir_ssl`    | `CLONE` 语句的临时数据目录和 SSL 选项信息 | `TempDatadirSsl` | `opt_datadir_ssl` |

#### COMMIT 语句（commit statement）

| 水杉解析器语义组名称 | 语义组类型    | 返回值类型        | MySQL 语义组名称 |
| -------------------- | ------------- | ----------------- | ---------------- |
| `commit_statement`   | `COMMIT` 语句 | `CommitStatement` | `commit`         |

#### CREATE DATABASE 语句（create database statement）

| 水杉解析器语义组名称        | 语义组类型             | 返回值类型                | MySQL 语义组名称 |
| --------------------------- | ---------------------- | ------------------------- | ---------------- |
| `create_database_statement` | `CREATE DATABASE` 语句 | `CreateDatabaseStatement` | `create`【部分】 |

#### CREATE INDEX 语句（create index statement）

| 水杉解析器语义组名称     | 语义组类型             | 返回值类型        | MySQL 语义组名称    |
| ------------------------ | ---------------------- | ----------------- | ------------------- |
| `create_index_statement` | `CREATE INDEX` 语句    | `CreateIndexStmt` | `create_index_stmt` |
| `opt_keyword_unique`     | 可选的 `UNIQUE` 关键字 | `EnumIndexType`   | `opt_unique`        |

#### CREATE RESOURCE GROUP 语句（create resource group statement）

| 水杉解析器语义组名称              | 语义组类型                   | 返回值类型                     | MySQL 语义组名称             |
| --------------------------------- | ---------------------------- | ------------------------------ | ---------------------------- |
| `create_resource_group_statement` | `CREATE RESOURCE GROUP` 语句 | `CreateResourceGroupStatement` | `create_resource_group_stmt` |

#### CREATE ROLE 语句（create role statement）

| 水杉解析器语义组名称    | 语义组类型         | 返回值类型            | MySQL 语义组名称   |
| ----------------------- | ------------------ | --------------------- | ------------------ |
| `create_role_statement` | `CREATE ROLE` 语句 | `CreateRoleStatement` | `create_role_stmt` |

#### CREATE SRS 语句（create srs statement）

| 水杉解析器语义组名称     | 语义组类型          | 返回值类型           | MySQL 语义组名称  |
| ------------------------ | ------------------- | -------------------- | ----------------- |
| `create_srs_statement`   | `CREATE SRS` 语句   | `CreateSrsStatement` | `create_srs_stmt` |
| `opt_srs_attribute_list` | 可选的 SRS 属性列表 | `List[SrsAttribute]` | `srs_attributes`  |
| `srs_attribute_list`     | SRS 属性列表        | `List[SrsAttribute]` |                   |
| `srs_attribute`          | SRS 属性            | `SrsAttribute`       |                   |

#### CREATE TABLE 语句（create table statement）

| 水杉解析器语义组名称         | 语义组类型                                 | 返回值类型              | MySQL 语义组名称               |
| ---------------------------- | ------------------------------------------ | ----------------------- | ------------------------------ |
| `create_table_statement`     | `CREATE TABLE` 语句                        | `CreateTableStatement`  | `create_table_stmt`            |
| `opt_create_table_option_1`  | `CREATE TABLE` 的选项（第 1 层）           | `TempCreateTableOption` | `opt_create_table_options_etc` |
| `opt_create_table_option_2`  | `CREATE TABLE` 的选项（第 2 层）           | `TempCreateTableOption` | `opt_create_partitioning_etc`  |
| `opt_create_table_option_3`  | `CREATE TABLE` 的选项（第 3 层）           | `TempCreateTableOption` | `opt_duplicate_as_qe`          |
| `as_create_query_expression` | 可选择是否包含前置 `AS` 关键字的查询表达式 | `QueryExpression`       | `as_create_query_expression`   |

#### CREATE UNDO TABLESPACE 语句（create undo tablespace statement）

| 水杉解析器语义组名称               | 语义组类型                    | 返回值类型                      | MySQL 语义组名称 |
| ---------------------------------- | ----------------------------- | ------------------------------- | ---------------- |
| `create_undo_tablespace_statement` | `CREATE UNDO TABLESPACE` 语句 | `CreateUndoTablespaceStatement` | `create`【部分】 |

#### CREATE VIEW 语句（create view statement）

| 水杉解析器语义组名称    | 语义组类型         | 返回值类型            | MySQL 语义组名称                                             |
| ----------------------- | ------------------ | --------------------- | ------------------------------------------------------------ |
| `create_view_statement` | `CREATE VIEW` 语句 | `CreateViewStatement` | `create`【部分】<br />`view_tail`【包含】<br />`view_query_block`【包含】<br />`view_replace_or_algorithm`【包含】 |

将 `create` 语义组中的备选规则 `CREATE view_or_trigger_or_sp_or_event`，以及 `view_or_trigger_or_sp_or_event` 语义组、`definer_tail` 语义和 `no_definer_tail` 语义组拆分为各个不同的 `CREATE` 语句单独的语义组。

#### DEALLOCATE 语句（deallocate statement）

| 水杉解析器语义组名称   | 语义组类型        | 返回值类型            | MySQL 语义组名称 |
| ---------------------- | ----------------- | --------------------- | ---------------- |
| `deallocate_statement` | `DEALLOCATE` 语句 | `DeallocateStatement` | `deallocate`     |

#### DELETE 语句（delete statement）

| 水杉解析器语义组名称 | 语义组类型    | 返回值类型        | MySQL 语义组名称 |
| -------------------- | ------------- | ----------------- | ---------------- |
| `delete_statement`   | `DELETE` 语句 | `DeleteStatement` | `delete_stmt`    |

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

| 水杉解析器语义组名称             | 语义组类型                           | 返回值类型                    | MySQL 语义组名称            |
| -------------------------------- | ------------------------------------ | ----------------------------- | --------------------------- |
| `drop_database_statement`        | `DROP DATABASE` 语句                 | `DropDatabaseStatement`       | `drop_database_stmt`        |
| `drop_event_statement`           | `DROP EVENT` 语句                    | `DropEventStatement`          | `drop_event_stmt`           |
| `drop_function_statement`        | `DROP FUNCTION` 语句                 | `DropFunctionStatement`       | `drop_function_stmt`        |
| `drop_index_statement`           | `DROP INDEX` 语句                    | `DropIndexStatement`          | `drop_index_stmt`           |
| `drop_logfile_statement`         | `DROP LOGFILE` 语句                  | `DropLogfileStatement`        | `drop_logfile_stmt`         |
| `drop_procedure_statement`       | `DROP PROCEDURE` 语句                | `DropProcedureStatement`      | `drop_procedure_stmt`       |
| `drop_resource_group_statement`  | `DROP RESOURCE GROUP` 语句           | `DropResourceGroupStatement`  | `drop_resource_group_stmt`  |
| `drop_role_statement`            | `DROP ROLE` 语句                     | `DropRoleStatement`           | `drop_role_stmt`            |
| `drop_server_statement`          | `DROP SERVER` 语句                   | `DropServerStatement`         | `drop_server_stmt`          |
| `drop_srs_statement`             | `DROP SPATIAL REFERENCE SYSTEM` 语句 | `DropSrsStatement`            | `drop_srs_stmt`             |
| `drop_tablespace_statement`      | `DROP TABLESPACE` 语句               | `DropTablespaceStatement`     | `drop_tablespace_stmt`      |
| `drop_undo_tablespace_statement` | `DROP UNDO TABLESPACE` 语句          | `DropUndoTablespaceStatement` | `drop_undo_tablespace_stmt` |
| `drop_table_statement`           | `DROP TABLE` 语句                    | `DropTableStatement`          | `drop_table_stmt`           |
| `drop_trigger_statement`         | `DROP TRIGGER` 语句                  | `DropTriggerStatement`        | `drop_trigger_stmt`         |
| `drop_user_statement`            | `DROP USER` 语句                     | `DropUserStatement`           | `drop_user_stmt`            |
| `drop_view_statement`            | `DROP VIEW` 语句                     | `DropViewStatement`           | `drop_view_stmt`            |

#### EXECUTE 语句（execute statement）

| 水杉解析器语义组名称 | 语义组类型                    | 返回值类型           | MySQL 语义组名称 |
| -------------------- | ----------------------------- | -------------------- | ---------------- |
| `execute_statement`  | `EXECUTE` 语句                | `ExecuteStatement`   | `execute`        |
| `execute_using`      | `EXECUTE` 语句的 `USING` 子句 | `List[UserVariable]` | `execute_using`  |

#### EXPLAIN 语句（explain statement）

| 水杉解析器语义组名称     | 语义组类型                                     | 返回值类型               | MySQL 语义组名称                               |
| ------------------------ | ---------------------------------------------- | ------------------------ | ---------------------------------------------- |
| `explain_statement`      | `EXPLAIN` 语句                                 | `ExplainStatement`       | `explain_stmt`<br />`explainable_stmt`【包含】 |
| `opt_explain_options`    | 可选的 `EXPLAIN` 分析选项                      | `ExplainOptions`         | `opt_explain_options`                          |
| `opt_explain_format`     | 可选的 `FORMAT` 引导的指定分析结果格式子句     | `Optional[str]`          | `opt_explain_format`                           |
| `opt_explain_into`       | 可选的 `INTO` 引导的指定分析结果写入变量子句   | `Optional[UserVariable]` | `opt_explain_into`                             |
| `opt_explain_for_schema` | 可选的 `FOR DATABASE` 引导的指定分析数据库子句 | `Optional[str]`          | `opt_explain_for_schema`                       |

#### FLUSH 语句（flush statement）

| 水杉解析器语义组名称 | 语义组类型   | 返回值类型       | MySQL 语义组名称                     |
| -------------------- | ------------ | ---------------- | ------------------------------------ |
| `flush_statement`    | `FLUSH` 语句 | `FlushStatement` | `flush`<br />`flush_options`【包含】 |

#### GET DIAGNOSTICS 语句（get diagnostics statement）

| 水杉解析器语义组名称          | 语义组类型             | 返回值类型                       | MySQL 语义组名称              |
| ----------------------------- | ---------------------- | -------------------------------- | ----------------------------- |
| `get_diagnostics_statement`   | `GET DIAGNOSTICS` 语句 | `GetDiagnosticsStatement`        | `get_diagnostics`             |
| `diagnostics_information`     | 诊断信息               | `DiagnosticsInformation`         | `diagnostics_information`     |
| `statement_information`       | 语句诊断信息项的列表   | `List[StatementInformationItem]` | `statement_information`       |
| `statement_information_item`  | 语句诊断信息项         | `StatementInformationItem`       | `statement_information_item`  |
| `condition_information`       | 条件诊断信息项的列表   | `List[ConditionInformationItem]` | `condition_information`       |
| `condition_information_item`  | 条件诊断信息项         | `ConditionInformationItem`       | `condition_information_item`  |
| `simple_target_specification` | 指定的诊断目标         | `Expression`                     | `simple_target_specification` |

#### GRANT 语句和 REVOKE 语句（grant and revoke statement）

| 水杉解析器语义组名称     | 语义组类型               | 返回值类型              | MySQL 语义组名称         |
| ------------------------ | ------------------------ | ----------------------- | ------------------------ |
| `grant_statement`        | `GRANT` 语句             | `GrantStatement`        | `grant`                  |
| `revoke_statement`       | `REVOKE` 语句            | `RevokeStatement`       | `revoke`                 |
| `role_or_privilege_list` | 角色或权限列表           | `List[RoleOrPrivilege]` | `role_or_privilege_list` |
| `role_or_privilege`      | 角色或权限               | `RoleOrPrivilege`       | `role_or_privilege`      |
| `opt_with_roles`         | 可选的 `WITH ROLES` 子句 | `WithRole`              | `opt_with_roles`         |
| `opt_except_role_list`   | 可选的排除角色列表       | `List[RoleName]`        | `opt_except_role_list`   |
| `opt_grant_as`           | 可选的 `GRANT AS` 子句   | `Optional[UserName]`    | `opt_grant_as`           |
| `grant_identifier`       | `GRANT` 语句中的标识符   | `GrantIdentifier`       | `grant_ident`            |

#### GROUP REPLICATION 语句（group replication statement）

| 水杉解析器语义组名称                      | 语义组类型                                  | 返回值类型                          | MySQL 语义组名称                      |
| ----------------------------------------- | ------------------------------------------- | ----------------------------------- | ------------------------------------- |
| `group_replication_statement`             | `GROUP REPLICATION` 语句                    | `GroupReplicationStatement`         | `group_replication`                   |
| `opt_group_replication_start_option_list` | 可选的 `GROUP REPLICATION START` 选项的列表 | `List[GroupReplicationStartOption]` | `opt_group_replication_start_options` |
| `group_replication_start_option_list`     | `GROUP REPLICATION START` 选项的列表        | `List[GroupReplicationStartOption]` | `group_replication_start_options`     |
| `group_replication_start_option`          | `GROUP REPLICATION START` 的选项            | `GroupReplicationStartOption`       | `group_replication_start_option`      |
| `group_replication_user`                  | `GROUP REPLICATION` 的 `USER` 选项          | `GroupReplicationUser`              | `group_replication_user`              |
| `group_replication_password`              | `GROUP REPLICATION` 的 `PASSWORD` 选项      | `GroupReplicationPassword`          | `group_replication_password`          |
| `group_replication_plugin_auth`           | `GROUP REPLICATION` 的插件认证选项          | `group_replication_plugin_auth`     | `group_replication_plugin_auth`       |

#### HANDLER 语句（handler statement）

| 水杉解析器语义组名称 | 语义组类型     | 返回值类型         | MySQL 语义组名称 |
| -------------------- | -------------- | ------------------ | ---------------- |
| `handler_statement`  | `HANDLER` 语句 | `HandlerStatement` | `handler_stmt`   |

#### HELP 语句（help statement）

| 水杉解析器语义组名称 | 语义组类型  | 返回值类型      | MySQL 语义组名称 |
| -------------------- | ----------- | --------------- | ---------------- |
| `help_statement`     | `HELP` 语句 | `HelpStatement` | `help`           |

#### IMPORT TABLE 语句（import table statement）

| 水杉解析器语义组名称     | 语义组类型          | 返回值类型             | MySQL 语义组名称 |
| ------------------------ | ------------------- | ---------------------- | ---------------- |
| `import_table_statement` | `IMPORT TABLE` 语句 | `ImportTableStatement` | `insert_stmt`    |

#### INSERT 语句和 REPLACE 语句（insert or replace statement）

| 水杉解析器语义组名称      | 语义组类型                                        | 返回值类型                 | MySQL 语义组名称          |
| ------------------------- | ------------------------------------------------- | -------------------------- | ------------------------- |
| `insert_statement`        | `INSERT` 语句                                     | `InsertOrReplaceStatement` | `insert_stmt`             |
| `replace_statement`       | `REPLACE` 语句                                    | `InsertOrReplaceStatement` | `replace_stmt`            |
| `insert_from_constructor` | 通过值列表构造的多行数据                          | `TempInsertColumnAndValue` | `insert_from_constructor` |
| `insert_values`           | `VALUE` 或 `VALUES` 关键字引导的多行数据          | `List[RowValue]`           | `insert_values`           |
| `keyword_value_or_values` | `VALUE` 关键字或 `VALUES` 关键字                  | -                          | `value_or_values`         |
| `row_value_list`          | `INSERT` 和 `REPLACE` 语句中的行数据的列表        | `List[RowValue]`           | `values_list`             |
| `row_value`               | `INSERT` 和 `REPLACE` 语句中的行数据              | `RowValue`                 | `row_value`               |
| `insert_from_query`       | 通过查询构造的多行数据                            | `TempInsertColumnAndQuery` | `insert_query_expression` |
| `opt_insert_alias`        | `INSERT` 语句中 `AS` 关键字引导的表别名和字段别名 | `TempInsertAlias`          | `opt_values_reference`    |
| `opt_insert_update_list`  | 可选的 `ON DUPLICATE KEY UPDATE` 子句             | `List[UpdateElement]`      | `opt_insert_update_list`  |

#### INSTALL 语句和 UNINSTALL 语句（install and uninstall statement）

| 水杉解析器语义组名称         | 语义组类型                                   | 返回值类型              | MySQL 语义组名称             |
| ---------------------------- | -------------------------------------------- | ----------------------- | ---------------------------- |
| `install_set_rvalue`         | `INSTALL` 语句的 `SET` 子句中的右值          | `Expression`            | `install_set_rvalue`         |
| `install_set_value`          | `INSTALL` 语句的 `SET` 子句中的单个值        | `InstallSetValue`       | `install_set_value`          |
| `install_set_value_list`     | `INSTALL` 语句的 `SET` 子句中值的列表        | `List[InstallSetValue]` | `install_set_value_list`     |
| `opt_install_set_value_list` | 可选的 `INSTALL` 语句的 `SET` 子句中值的列表 | `List[InstallSetValue]` | `opt_install_set_value_list` |
| `install_statement`          | `INSTALL` 语句                               | `InstallStatement`      | `install_stmt`               |
| `uninstall_statement`        | `UNINSTALL` 语句                             | `UninstallStatement`    | `uninstall`                  |

#### KILL 语句（kill statement）

| 水杉解析器语义组名称 | 语义组类型  | 返回值类型      | MySQL 语义组名称 |
| -------------------- | ----------- | --------------- | ---------------- |
| `kill_statement`     | `KILL` 语句 | `KillStatement` | `kill`           |

#### LOAD 语句（load statement）

| 水杉解析器语义组名称         | 语义组类型               | 返回值类型                 | MySQL 语义组名称             |
| ---------------------------- | ------------------------ | -------------------------- | ---------------------------- |
| `load_statement`             | `LOAD` 语句              | `LoadStatement`            | `load_stmt`                  |
| `opt_source_count`           | 可选的数据源计数         | `int`                      | `opt_source_count`           |
| `opt_xml_rows_identified_by` | 可选的 XML 行标识符      | `Optional[str]`            | `opt_xml_rows_identified_by` |
| `opt_ignore_lines`           | 可选的忽略行数           | `int`                      | `opt_ignore_lines`           |
| `opt_field_or_var_spec`      | 可选的字段或变量的列表   | `List[Expression]`         | `opt_field_or_var_spec`      |
| `fields_or_vars`             | 字段或变量的列表         | `List[Expression]`         | `fields_or_vars`             |
| `field_or_var`               | 字段或变量               | `Expression`               | `field_or_var`               |
| `opt_load_data_set_spec`     | 可选的 LOAD 数据设置列表 | `List[LoadDataSetElement]` | `opt_load_data_set_spec`     |
| `load_data_set_list`         | LOAD 数据设置列表        | `List[LoadDataSetElement]` | `load_data_set_list`         |
| `load_data_set_elem`         | LOAD 数据设置元素        | `LoadDataSetElement`       | `load_data_set_elem`         |
| `opt_load_parallel`          | 可选的并行加载选项       | `int`                      | `opt_load_parallel`          |
| `opt_load_memory`            | 可选的内存选项           | `int`                      | `opt_load_memory`            |
| `opt_load_algorithm`         | 可选的算法选项           | `bool`                     | `opt_load_algorithm`         |

#### LOCK 语句和 UNLOCK 语句（lock and unlock statement）

| 水杉解析器语义组名称 | 语义组类型             | 返回值类型        | MySQL 语义组名称  |
| -------------------- | ---------------------- | ----------------- | ----------------- |
| `lock_statement`     | `LOCK` 语句            | `LockStatement`   | `lock`            |
| `unlock_statement`   | `UNLOCK` 语句          | `UnlockStatement` | `unlock`          |
| `table_lock_list`    | 单个表的锁定信息的列表 | `List[TableLock]` | `table_lock_list` |
| `table_lock`         | 单个表的锁定信息       | `TableLock`       | `table_lock`      |

#### OPTIMIZE TABLE 语句（optimize table statement）

| 水杉解析器语义组名称       | 语义组类型            | 返回值类型               | MySQL 语义组名称      |
| -------------------------- | --------------------- | ------------------------ | --------------------- |
| `optimize_table_statement` | `OPTIMIZE TABLE` 语句 | `OptimizeTableStatement` | `optimize_table_stmt` |

#### PURGE 语句（purge statement）

| 水杉解析器语义组名称 | 语义组类型   | 返回值类型       | MySQL 语义组名称                     |
| -------------------- | ------------ | ---------------- | ------------------------------------ |
| `purge_statement`    | `PURGE` 语句 | `PurgeStatement` | `purge`<br />`purge_options`【包含】 |
| `purge_option`       | `PURGE` 选项 | `PurgeOption`    | `purge_option`                       |

#### PREPARE 语句（prepare）

| 水杉解析器语义组名称 | 语义组类型                         | 返回值类型                           | MySQL 语义组名称 |
| -------------------- | ---------------------------------- | ------------------------------------ | ---------------- |
| `prepare_statement`  | `PREPARE` 语句                     | `PrepareStatement`                   | `prepare`        |
| `prepare_source`     | `PREPARE` 语句的 `FROM` 子句中的值 | `Union[StringLiteral, UserVariable]` | `prepare_src`    |

#### RELEASE 语句（release statement）

| 水杉解析器语义组名称 | 语义组类型     | 返回值类型         | MySQL 语义组名称 |
| -------------------- | -------------- | ------------------ | ---------------- |
| `release_statement`  | `RELEASE` 语句 | `ReleaseStatement` | `release`        |

#### RENAME 语句（rename statement）

| 水杉解析器语义组名称 | 语义组类型                          | 返回值类型                            | MySQL 语义组名称      |
| -------------------- | ----------------------------------- | ------------------------------------- | --------------------- |
| `rename_statement`   | `RENAME` 语句                       | `RenameStatement`                     | `rename`              |
| `rename_user_list`   | `RENAME` 语句中的用户重命名对的列表 | `List[Tuple[UserName, UserName]]`     | `rename_list`         |
| `rename_table_list`  | `RENAME` 语句中的表重命名对的列表   | `List[Tuple[Identifier, Identifier]]` | `table_to_table_list` |
| `rename_table_item`  | `RENAME` 语句中的表重命名对         | `Tuple[Identifier, Identifier]`       | `table_to_table`      |

#### REPAIR TABLE 语句（repair table statement）

| 水杉解析器语义组名称     | 语义组类型          | 返回值类型             | MySQL 语义组名称    |
| ------------------------ | ------------------- | ---------------------- | ------------------- |
| `repair_table_statement` | `REPAIR TABLE` 语句 | `RepairTableStatement` | `repair_table_stmt` |

#### RESET 语句（reset statement）

| 水杉解析器语义组名称   | 语义组类型          | 返回值类型          | MySQL 语义组名称                           |
| ---------------------- | ------------------- | ------------------- | ------------------------------------------ |
| `reset_statement`      | `RESET` 语句        | `ResetStatement`    | `reset`<br />`opt_if_exists_ident`【包含】 |
| `reset_options`        | `RESET` 选项列表    | `List[ResetOption]` | `reset_options`                            |
| `reset_option`         | `RESET` 单个选项    | `ResetOption`       | `reset_option`                             |
| `source_reset_options` | `SOURCE RESET` 选项 | `Optional[int]`     | `source_reset_options`                     |

#### RESTART 语句（restart statement）

| 水杉解析器语义组名称 | 语义组类型     | 返回值类型         | MySQL 语义组名称      |
| -------------------- | -------------- | ------------------ | --------------------- |
| `restart_statement`  | `RESTART` 语句 | `RestartStatement` | `restart_server_stmt` |

#### ROLLBACK 语句（rollback statement）

| 水杉解析器语义组名称 | 语义组类型      | 返回值类型          | MySQL 语义组名称 |
| -------------------- | --------------- | ------------------- | ---------------- |
| `rollback_statement` | `ROLLBACK` 语句 | `RollbackStatement` | `rollback`       |

#### SAVEPOINT 语句（savepoint statement）

| 水杉解析器语义组名称  | 语义组类型       | 返回值类型           | MySQL 语义组名称 |
| --------------------- | ---------------- | -------------------- | ---------------- |
| `savepoint_statement` | `SAVEPOINT` 语句 | `SavepointStatement` | `savepoint`      |

#### SELECT 语句（select statement）

| 水杉解析器语义组名称      | 语义组类型                                                   | 返回值类型              | MySQL 语义组名称                                     |
| ------------------------- | ------------------------------------------------------------ | ----------------------- | ---------------------------------------------------- |
| `simple_query`            | 简单查询（包括查询选项、查询字段表达式、`INTO` 子句、`FROM` 子句、`WHERE` 子句、`GROUP BY` 子句、`HAVING` 子句、`WINDOW` 子句和 `QUALIFY` 子句） | `SimpleQuery`           | `query_specification`                                |
| `opt_select_option_list`  | 可选的查询选项的列表                                         | `SelectOption`          | `select_options`                                     |
| `select_option_list`      | 查询选项的列表                                               | `SelectOption`          | `select_option_list`                                 |
| `select_option`           | 查询选项                                                     | `SelectOption`          | `select_option`<br />`query_spec_option`【超集】     |
| `select_item_list`        | `SELECT` 子句中的查询字段表达式的列表                        | `List[Expression]`      | `select_item_list`                                   |
| `select_item`             | `SELECT` 子句中的查询字段表达式                              | `Expression`            | `select_item`                                        |
| `table_wild`              | 表中所有字段的通配符                                         | `TableWild`             | `table_wild`                                         |
| `table_value_constructor` | 通过值列表构造的查询                                         | `TableValueConstructor` | `table_value_constructor`                            |
| `row_value_explicit_list` | `ROW` 关键字引导的值列表的列表                               | `List[Row]`             | `values_row_list`                                    |
| `row_value_explicit`      | `ROW` 关键字引导的值列表                                     | `Row`                   | `row_value_explicit`                                 |
| `explicit_table`          | 明确指定表的查询                                             | `ExplicitTable`         | `explicit_table`                                     |
| `query_primary`           | 初级查询（简单查询、通过值列表构造的查询或明确指定表的查询） | `Query`                 | `query_primary`                                      |
| `query_expression_body`   | 中级查询（在初级查询的基础上，包含 `UNION`、`EXCEPT` 或 `INTERSECT`） | `Query`                 | `query_expression_body`                              |
| `union_option`            | 联合类型                                                     | `UnionOption`           | `union_option`                                       |
| `query_expression_bare`   | 高级查询（在中级查询的基础上，包含 `WITH`、`ORDER BY` 和 `LIMIT` 子句） | `QueryExpression`       | `query_expression`                                   |
| `query_expression`        | 查询表达式（在高级查询的基础上，包含可选的锁指定子句）       | `QueryExpression`       | `query_expression_with_opt_locking_clauses`          |
| `query_expression_parens` | 嵌套任意层括号的查询表达式                                   | `QueryExpression`       | `query_expression_parens`                            |
| `select_statement`        | `SELECT` 语句                                                | `SelectStatement`       | `select_stmt`<br />`select_stmt_with_into`【不兼容】 |

#### SET RESOURCE GROUP 语句（set resource group statement）

| 水杉解析器语义组名称           | 语义组类型                | 返回值类型                  | MySQL 语义组名称                               |
| ------------------------------ | ------------------------- | --------------------------- | ---------------------------------------------- |
| `set_resource_group_statement` | `SET RESOURCE GROUP` 语句 | `SetResourceGroupStatement` | `set_resource_group_stmt`                      |
| `thread_id_list`               | 线程 ID 列表              | `List[int]`                 | `thread_id_list_options`<br />`thread_id_list` |

#### SET ROLE 语句（set role statement）

| 水杉解析器语义组名称 | 语义组类型      | 返回值类型         | MySQL 语义组名称 |
| -------------------- | --------------- | ------------------ | ---------------- |
| `set_role_statement` | `SET ROLE` 语句 | `SetRoleStatement` | `set_role_stmt`  |

#### SHOW 语句（show statement）

| 水杉解析器语义组名称               | 语义组类型                                     | 返回值类型                     | MySQL 语义组名称              |
| ---------------------------------- | ---------------------------------------------- | ------------------------------ | ----------------------------- |
| `show_binary_log_status_statement` | `SHOW BINARY LOG STATUS` 语句                  | `ShowBinaryLogStatusStatement` | `show_binary_log_status_stmt` |
| `show_binary_logs_statement`       | `SHOW BINARY LOGS` 语句                        | `ShowBinaryLogsStatement`      | `show_binary_logs_stmt`       |
| `show_binlog_events_statement`     | `SHOW BINLOG EVENTS` 语句                      | `ShowBinlogEventsStatement`    | `show_binlog_events_stmt`     |
| `show_char_set_statement`          | `SHOW CHAR SET` 语句                           | `ShowCharSetStatement`         | `show_character_set_stmt`     |
| `show_collation_statement`         | `SHOW COLLATION` 语句                          | `ShowCollationStatement`       | `show_collation_stmt`         |
| `show_columns_statement`           | `SHOW COLUMNS` 语句                            | `ShowColumnsStatement`         | `show_columns_stmt`           |
| `show_count_errors_statement`      | `SHOW COUNT ERRORS` 语句                       | `ShowCountErrorsStatement`     | `show_count_errors_stmt`      |
| `show_count_warnings_statement`    | `SHOW COUNT WARNINGS` 语句                     | `ShowCountWarningsStatement`   | `show_count_warnings_stmt`    |
| `show_create_database_stmt`        | `SHOW CREATE DATABASE` 语句                    | `ShowCreateDatabaseStatement`  | `show_create_database_stmt`   |
| `show_create_event_statement`      | `SHOW CREATE EVENT` 语句                       | `ShowCreateEventStatement`     | `show_create_event_stmt`      |
| `show_create_function_statement`   | `SHOW CREATE FUNCTION` 语句                    | `ShowCreateFunctionStatement`  | `show_create_function_stmt`   |
| `show_create_procedure_statement`  | `SHOW CREATE PROCEDURE` 语句                   | `ShowCreateProcedureStatement` | `show_create_procedure_stmt`  |
| `show_create_table_statement`      | `SHOW CREATE TABLE` 语句                       | `ShowCreateTableStatement`     | `show_create_table_stmt`      |
| `show_create_trigger_statement`    | `SHOW CREATE TRIGGER` 语句                     | `ShowCreateTriggerStatement`   | `show_create_trigger_stmt`    |
| `show_create_user_statement`       | `SHOW CREATE USER` 语句                        | `ShowCreateUserStatement`      | `show_create_user_stmt`       |
| `show_create_view_statement`       | `SHOW CREATE VIEW` 语句                        | `ShowCreateViewStatement`      | `show_create_view_stmt`       |
| `show_databases_statement`         | `SHOW DATABASES` 语句                          | `ShowDatabasesStatement`       | `show_databases_stmt`         |
| `show_engine_logs_statement`       | `SHOW ENGINE LOGS` 语句                        | `ShowEngineLogsStatement`      | `show_engine_logs_stmt`       |
| `show_engine_mutex_stmt`           | `SHOW ENGINE MUTEX` 语句                       | `ShowEngineMutexStatement`     | `show_engine_mutex_stmt`      |
| `show_engine_status_stmt`          | `SHOW ENGINE STATUS` 语句                      | `ShowEngineStatusStatement`    | `show_engine_status_stmt`     |
| `show_engines_statement`           | `SHOW ENGINES` 语句                            | `ShowEnginesStatement`         | `show_engines_stmt`           |
| `show_errors_statement`            | `SHOW ERRORS` 语句                             | `ShowErrorsStatement`          | `show_errors_stmt`            |
| `show_events_statement`            | `SHOW EVENTS` 语句                             | `ShowEventsStatement`          | `show_events_stmt`            |
| `show_function_code_statement`     | `SHOW FUNCTION CODE` 语句                      | `ShowFunctionCodeStatement`    | `show_function_code_stmt`     |
| `show_function_status_statement`   | `SHOW FUNCTION STATUS` 语句                    | `ShowFunctionStatusStatement`  | `show_function_status_stmt`   |
| `show_grants_statement`            | `SHOW GRANTS` 语句                             | `ShowEnginesStatement`         | `show_grants_stmt`            |
| `show_keys_statement`              | `SHOW KEYS` 语句                               | `ShowKeysStatement`            | `show_keys_stmt`              |
| `show_master_status_statement`     | `SHOW MASTER STATUS` 语句                      | `ShowMasterStatusStatement`    | `show_master_status_stmt`     |
| `show_open_tables_statement`       | `SHOW OPEN TABLES` 语句                        | `ShowOpenTablesStatement`      | `show_open_tables_stmt`       |
| `show_parse_tree_statement`        | `SHOW PARSE TREE` 语句                         | `ShowParseTreeStatement`       | `show_parse_tree_stmt`        |
| `show_plugins_statement`           | `SHOW PLUGINS` 语句                            | `ShowPluginsStatement`         | `show_plugins_stmt`           |
| `show_privileges_statement`        | `SHOW PRIVILEGES` 语句                         | `ShowPrivilegesStatement`      | `show_privileges_stmt`        |
| `show_procedure_code_statement`    | `SHOW PROCEDURE CODE` 语句                     | `ShowProcedureCodeStatement`   | `show_procedure_code_stmt`    |
| `show_procedure_status_statement`  | `SHOW PROCEDURE STATUS` 语句                   | `ShowProcedureStatusStatement` | `show_procedure_status_stmt`  |
| `show_processlist_statement`       | `SHOW PROCESSLIST` 语句                        | `ShowProcesslistStatement`     | `show_processlist_stmt`       |
| `show_profile_statement`           | `SHOW PROFILE` 语句                            | `ShowProfileStatement`         | `show_profile_stmt`           |
| `show_profiles_statement`          | `SHOW PROFILES` 语句                           | `ShowProfilesStatement`        | `show_profiles_stmt`          |
| `show_relaylog_events_statement`   | `SHOW RELAYLOG EVENTS` 语句                    | `ShowRelaylogEventsStatement`  | `show_relaylog_events_stmt`   |
| `show_replica_status_statement`    | `SHOW REPLICA STATUS` 语句                     | `ShowReplicaStatusStatement`   | `show_replica_status_stmt`    |
| `show_replicas_statement`          | `SHOW REPLICAS` 语句                           | `ShowReplicasStatement`        | `show_replicas_stmt`          |
| `show_status_statement`            | `SHOW STATUS` 语句                             | `ShowStatusStatement`          | `show_status_stmt`            |
| `show_table_status_statement`      | `SHOW TABLE STATUS` 语句                       | `ShowTableStatusStatement`     | `show_table_status_stmt`      |
| `show_tables_statement`            | `SHOW TABLES` 语句                             | `ShowTablesStatement`          | `show_tables_stmt`            |
| `show_triggers_statement`          | `SHOW TRIGGERS` 语句                           | `ShowTriggersStatement`        | `show_triggers_stmt`          |
| `show_warnings_statement`          | `SHOW WARNINGS` 语句                           | `ShowWarningsStatement`        | `show_variables_stmt`         |
| `show_variables_statement`         | `SHOW VARIABLES` 语句                          | `ShowVariablesStatement`       | `show_warnings_stmt`          |
| `opt_binlog_in`                    | 可选的 `IN` 关键字引导的指定文件名子句         | `Optional[str]`                | `opt_binlog_in`               |
| `opt_binlog_from`                  | 可选的 `FROM` 关键字引导指定位事件开始位置子句 | `Optional[int]`                | `binlog_from`                 |
| `opt_wild_or_where`                | 可选的通配符或 `WHERE` 子句                    | `TempWildOrWhere`              | `opt_wild_or_where`           |
| `opt_show_schema`                  | `SHOW` 语句中可选的数据库名称                  | `Optional[str]`                | `opt_db`                      |
| `engine_name_or_all`               | 引擎名称或 `ALL` 关键字                        | `Optional[str]`                | `engine_or_all`               |
| `opt_for_query`                    | 可选的 `FOR QUERY` 引导的线程 ID               | `Optional[int]`                | `opt_for_query`               |
| `opt_for_channel`                  | 可选的 `FOR CHANNEL` 引导的通道名              | `Optional[str]`                | `opt_channel`                 |

#### SHUTDOWN 语句（shutdown statement）

| 水杉解析器语义组名称 | 语义组类型      | 返回值类型          | MySQL 语义组名称 |
| -------------------- | --------------- | ------------------- | ---------------- |
| `shutdown_statement` | `SHUTDOWN` 语句 | `ShutdownStatement` | `shutdown_stmt`  |

#### SIGNAL 语句和 RESIGNAL 语句（signal and resignal statement）

| 水杉解析器语义组名称           | 语义组类型                                                   | 返回值类型                       | MySQL 语义组名称                              |
| ------------------------------ | ------------------------------------------------------------ | -------------------------------- | --------------------------------------------- |
| `signal_statement`             | `SIGNAL` 语句                                                | `SignalStatement`                | `signal_stmt`                                 |
| `resignal_statement`           | `RESIGNAL` 语句                                              | `ResignalStatement`              | `resignal_stmt`                               |
| `opt_signal_value`             | `RESIGNAL` 语句中可选的信号值                                | `Optional[Union[str, SqlState]]` | `opt_signal_value`                            |
| `signal_value`                 | `SIGNAL` 和 `RESIGNAL` 语句中的信号值                        | `Union[str, SqlState]`           | `signal_value`                                |
| `opt_set_signal_information`   | `SIGNAL` 和 `RESIGNAL` 语句中可选的 `SET` 关键字引导的信号项子句 | `List[SignalInformation]`        | `opt_set_signal_information`                  |
| `signal_information_item_list` | `SIGNAL` 和 `RESIGNAL` 语句中的信息项列表                    | `List[SignalInformation]`        | `signal_information_item_list`                |
| `signal_allowed_expr`          | `SIGNAL` 和 `RESIGNAL` 语句中信息项的值允许的表达式          | `Expression`                     | `signal_allowed_expr`<br />`condition_number` |

#### START TRANSACTION 语句（start transaction statement）

| 水杉解析器语义组名称                 | 语义组类型               | 返回值类型                  | MySQL 语义组名称                    |
| ------------------------------------ | ------------------------ | --------------------------- | ----------------------------------- |
| `start_transaction_statement`        | `START TRANSACTION` 语句 | `StartTransactionStatement` | `start`                             |
| `opt_start_transaction_options_list` | 可选的事务选项的列表     | `StartTransactionOption`    | `opt_start_transaction_option_list` |
| `start_transaction_options_list`     | 事务选项的列表           | `StartTransactionOption`    | `start_transaction_option_list`     |
| `start_transaction_options`          | 事务选项                 | `StartTransactionOption`    | `start_transaction_option`          |

#### STOP REPLICA 语句（stop replica statement）

| 水杉解析器语义组名称     | 语义组类型          | 返回值类型             | MySQL 语义组名称         |
| ------------------------ | ------------------- | ---------------------- | ------------------------ |
| `stop_replica_statement` | `STOP REPLICA` 语句 | `StopReplicaStatement` | `stop_replica_statement` |

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

#### USE 语句（use statement）

| 水杉解析器语义组名称 | 语义组类型 | 返回值类型     | MySQL 语义组名称 |
| -------------------- | ---------- | -------------- | ---------------- |
| `use_statement`      | `USE` 语句 | `UseStatement` | `use`            |

#### XA 语句（xa statement）

| 水杉解析器语义组名称 | 语义组类型    | 返回值类型    | MySQL 语义组名称 |
| -------------------- | ------------- | ------------- | ---------------- |
| `xa_statement`       | XA 事务语句   | `XaStatement` | `xa`             |
| `xid`                | XA 事务标识符 | `XaId`        | `xid`            |

# 子句（clause）

#### DEFINER 子句（definer clause）

指定定义者子句。

| 水杉解析器语义组名称 | 语义组类型                        | 返回值类型           | MySQL 语义组名称                                             |
| -------------------- | --------------------------------- | -------------------- | ------------------------------------------------------------ |
| `opt_definer_clause` | 可选的指定定义者的 `DEFINER` 子句 | `Optional[UserName]` | `definer_opt`<br />`no_definer`【子集】<br />`definer`【子集】 |

#### FROM 子句（from clause）

| 水杉解析器语义组名称 | 语义组类型         | 返回值类型    | MySQL 语义组名称                         |
| -------------------- | ------------------ | ------------- | ---------------------------------------- |
| `opt_from_clause`    | 可选的 `FROM` 子句 | `List[Table]` | `opt_from_clause`                        |
| `from_clause`        | `FROM` 子句        | `List[Table]` | `from_clause`<br />`from_tables`【包含】 |

#### GROUP BY 子句（group by clause）

| 水杉解析器语义组名称  | 语义组类型                          | 返回值类型                | MySQL 语义组名称   |
| --------------------- | ----------------------------------- | ------------------------- | ------------------ |
| `opt_group_by_clause` | 可选的 `GROUP BY` 子句              | `Optional[GroupByClause]` | `opt_group_clause` |
| `olap_opt`            | `GROUP BY` 子句中的分组统计信息规则 | `EnumOlapOpt`             | `olap_opt`         |

#### HAVING 子句（having clause）

| 水杉解析器语义组名称 | 语义组类型           | 返回值类型             | MySQL 语义组名称    |
| -------------------- | -------------------- | ---------------------- | ------------------- |
| `opt_having_clause`  | 可选的 `HAVING` 子句 | `Optional[Expression]` | `opt_having_clause` |

#### 索引指定子句（index hint clause）

| 水杉解析器语义组名称     | 语义组类型                         | 返回值类型          | MySQL 语义组名称                                 |
| ------------------------ | ---------------------------------- | ------------------- | ------------------------------------------------ |
| `index_hint_for`         | 索引指定子句中的索引用途           | `EnumIndexHintFor`  | `index_hint_clause`                              |
| `index_hint_type`        | 索引指定子句中指定类型             | `EnumIndexHintType` | `index_hint_type`                                |
| `hint_key_name`          | 索引指定子句中的索引名称           | `str`               | `key_usage_element`                              |
| `hint_key_name_list`     | 索引指定子句中的索引名称的列表     | `List[str]`         | `key_usage_list`                                 |
| `opt_hint_key_name_list` | 索引指定子句中可选的索引名称的列表 | `List[str]`         | `opt_key_usage_list`                             |
| `index_hint`             | 索引指定子句                       | `IndexHint`         | `index_hint_definition`                          |
| `index_hint_list`        | 索引指定子句的列表                 | `List[IndexHint]`   | `index_hints_list`                               |
| `opt_index_hint_list`    | 可选的索引指定子句的列表           | `List[IndexHint]`   | `opt_index_hints_list`<br />`opt_key_definition` |

#### INTO 子句（into clause）

| 水杉解析器语义组名称    | 语义组类型                                         | 返回值类型        | MySQL 语义组名称        |
| ----------------------- | -------------------------------------------------- | ----------------- | ----------------------- |
| `opt_into_clause`       | 可选的 `INTO` 子句                                 | `IntoClauseBase`  | `into_clause`【超集】   |
| `into_destination`      | `INTO` 子句中的写入目标                            | `IntoClauseBase`  | `into_destination`      |
| `opt_load_data_charset` | 可选的 `INTO` 子句和 `LOAD` 语句中指定字符集的子句 | `Charset`         | `opt_load_data_charset` |
| `opt_field_term`        | 可选的 `COLUMNS` 引导的外部文件字段格式选项的列表  | `FileFieldOption` | `opt_field_term`        |
| `field_term_list`       | 外部文件字段格式选项的列表                         | `FileFieldOption` | `field_term_list`       |
| `field_term`            | 外部文件字段格式选项                               | `FileFieldOption` | `field_term`            |
| `opt_line_term`         | 可选的 `LINES` 引导的外部文件行格式选项的列表      | `FileLineOption`  | `opt_line_term`         |
| `line_term_list`        | 外部文件行格式选项的列表                           | `FileLineOption`  | `line_term_list`        |
| `line_term`             | 外部文件行格式选项                                 | `FileLineOption`  | `line_term`             |

#### LIMIT 子句（limit clause）

| 水杉解析器语义组名称      | 语义组类型                                  | 返回值类型              | MySQL 语义组名称                            |
| ------------------------- | ------------------------------------------- | ----------------------- | ------------------------------------------- |
| `opt_limit_clause`        | 可选的 `LIMIT` 子句                         | `Optional[LimitClause]` | `opt_limit_clause`                          |
| `limit_clause`            | `LIMIT` 子句                                | `LimitClause`           | `limit_clause`<br />`limit_options`【超集】 |
| `opt_simple_limit_clause` | 可选的简单 `LIMIT` 子句（不支持指定偏移量） | `Optional[LimitClause]` | `opt_simple_limit`                          |
| `limit_option`            | `LIMIT` 子句中的数量                        | `Expression`            | `limit_option`                              |

#### 锁指定子句（locking clause）

| 水杉解析器语义组名称    | 语义组类型                                            | 返回值类型            | MySQL 语义组名称                                         |
| ----------------------- | ----------------------------------------------------- | --------------------- | -------------------------------------------------------- |
| `locking_clause_list`   | 锁指定子句的列表                                      | `List[LockingClause]` | `locking_clause_list`                                    |
| `locking_clause`        | 锁指定子句                                            | `LockingClause`       | `locking_clause`<br />`table_locking_list`【包含】       |
| `lock_strength`         | 指定锁类型的关键字（`UPDATE` 或 `SHARE`）             | `LockStrength`        | `lock_strength`                                          |
| `opt_locked_row_action` | 可选的指定锁行为的关键字（`SKIP LOCKED` 或 `NOWAIT`） | `LockedRowAction`     | `opt_locked_row_action`<br />`locked_row_action`【超集】 |

#### ORDER BY 子句（order by clause）

| 水杉解析器语义组名称  | 语义组类型                                  | 返回值类型                | MySQL 语义组名称                                             |
| --------------------- | ------------------------------------------- | ------------------------- | ------------------------------------------------------------ |
| `order_direction`     | 指定排序方向的 `ASC` 或 `DESC` 关键字       | `EnumOrderDirection`      | `ordering_direction`                                         |
| `opt_order_direction` | 可选的指定排序方向的 `ASC` 或 `DESC` 关键字 | `EnumOrderDirection`      | `opt_ordering_direction`                                     |
| `order_expr`          | 指定排序条件及方向的表达式                  | `OrderExpression`         | `order_expr`                                                 |
| `order_by_list`       | 指定排序条件及方向的表达式的列表            | `OrderClause`             | `order_list`<br />`gorder_list`                              |
| `opt_order_by_clause` | 可选的 `ORDER BY` 子句                      | `Optional[OrderByClause]` | `opt_order_clause`<br />`order_clause`<br />`opt_window_order_by_clause`<br />`opt_gorder_clause` |

#### OVER 子句（over clause）

| 水杉解析器语义组名称      | 语义组类型                                             | 返回值类型                | MySQL 语义组名称                                             |
| ------------------------- | ------------------------------------------------------ | ------------------------- | ------------------------------------------------------------ |
| `window_border_type`      | 窗口的边界类型                                         | `WindowBorderTypeEnum`    | `window_frame_units`                                         |
| `opt_window_exclude`      | 窗口函数中可选的 `EXCLUDE` 子句                        | `WindowExclusionTypeEnum` | `opt_window_frame_exclusion`                                 |
| `window_frame_start`      | 窗口开始边界                                           | `WindowBorder`            | `window_frame_start`                                         |
| `window_frame_bound`      | 窗口开始边界或窗口结束边界                             | `WindowBorder`            | `window_frame_bound`                                         |
| `window_frame_extent`     | 窗口的开始和结束边界                                   | `WindowBorders`           | `window_frame_extent`<br />`window_frame_between`            |
| `opt_window_frame_clause` | 窗口框架（包括边界类型、边界值、排除值）               | `WindowFrame`             | `opt_window_frame_clause`                                    |
| `window_name_or_spec`     | `OVER` 关键字引导的窗口子句（不含 `OVER` 关键字）      | `Window`                  | `window_name_or_spec`<br />`window_spec`<br />`window_spec_details` |
| `windowing_clause`        | `OVER` 关键字引导的窗口子句（含 `OVER` 关键字）        | `Window`                  | `windowing_clause`                                           |
| `opt_windowing_clause`    | 可选的 `OVER` 关键字引导的窗口子句（含 `OVER` 关键字） | `Window`                  | `opt_windowing_clause`                                       |

#### PARTITION 子句（partition clause）

用于 DQL 语句中的表子句、`INSERT` 语句、`REPLACE` 语句、`DELETE` 语句和 `LOAD` 语句，指定使用的分区列表。

| 水杉解析器语义组名称   | 语义组类型              | 返回值类型                   | MySQL 语义组名称    |
| ---------------------- | ----------------------- | ---------------------------- | ------------------- |
| `opt_partition_clause` | 可选的 `PARTITION` 子句 | `Optional[List[Expression]]` | `opt_use_partition` |
| `partition_clause`     | `PARTITION` 子句        | `List[Expression]`           | `use_partition`     |

#### 窗口函数中的 PARTITION BY 子句（window partition by clause）

用于窗口函数中的 `OVER` 子句，指定窗口分区规则。

| 水杉解析器语义组名称      | 语义组类型                 | 返回值类型         | MySQL 语义组名称       |
| ------------------------- | -------------------------- | ------------------ | ---------------------- |
| `opt_partition_by_clause` | 可选的 `PARTITION BY` 子句 | `List[Expression]` | `opt_partition_clause` |

#### QUALIFY 子句（qualify clause）

| 水杉解析器语义组名称 | 语义组类型            | 返回值类型             | MySQL 语义组名称     |
| -------------------- | --------------------- | ---------------------- | -------------------- |
| `opt_qualify_clause` | 可选的 `QUALIFY` 子句 | `Optional[Expression]` | `opt_qualify_clause` |

#### REQUIRE 子句（require clause）

| 水杉解析器语义组名称   | 语义组类型         | 返回值类型                 | MySQL 语义组名称       |
| ---------------------- | ------------------ | -------------------------- | ---------------------- |
| `require_clause`       | `REQUIRE` 子句     | `Optional[RequireClause]`  | `require_clause`       |
| `require_list`         | `REQUIRE` 列表     | `List[RequireListElement]` | `require_list`         |
| `require_list_element` | `REQUIRE` 列表元素 | `RequireListElement`       | `require_list_element` |

#### WHERE 子句（where clause）

| 水杉解析器语义组名称 | 语义组类型          | 返回值类型             | MySQL 语义组名称   |
| -------------------- | ------------------- | ---------------------- | ------------------ |
| `opt_where_clause`   | 可选的 `WHERE` 子句 | `Optional[Expression]` | `opt_where_clause` |
| `where_clause`       | `WHERE` 子句        | `Expression`           | `where_clause`     |

#### WINDOW 子句（window clause）

| 水杉解析器语义组名称     | 语义组类型           | 返回值类型               | MySQL 语义组名称                                             |
| ------------------------ | -------------------- | ------------------------ | ------------------------------------------------------------ |
| `opt_window_clause`      | 可选的 `WINDOW` 子句 | `Optional[List[Window]]` | `opt_window_clause`                                          |
| `window_definition_list` | 窗口定义子句的列表   | `List[Window]`           | `window_definition_list`                                     |
| `window_definition`      | 窗口定义子句         | `Window`                 | `window_definition`<br />`window_spec`【包含】<br />`window_spec_details`【包含】 |

#### WITH 子句（with clause）

| 水杉解析器语义组名称 | 语义组类型              | 返回值类型             | MySQL 语义组名称    |
| -------------------- | ----------------------- | ---------------------- | ------------------- |
| `opt_with_clause`    | 可选的 `WITH` 子句      | `Optional[WithClause]` | `opt_with_clause`   |
| `with_clause`        | `WITH` 子句             | `WithClause`           | `with_clause`       |
| `with_table_list`    | `WITH` 子句中的表的列表 | `List[WithTable]`      | `with_list`         |
| `with_table`         | `WITH` 子句中的表       | `WithTable`            | `common_table_expr` |

#### DDL 中的 PARTITION BY 子句（ddl partition by clause）

| 水杉解析器语义组名称               | 语义组类型                                           | 返回值类型                     | MySQL 语义组名称                                             |
| ---------------------------------- | ---------------------------------------------------- | ------------------------------ | ------------------------------------------------------------ |
| `ddl_partition_by_clause`          | DDL 中的 `PARTITION BY` 子句                         | `DdlPartitionByClause`         | `partition_clause`                                           |
| `partition_type_definition`        | DDL 的分区类型定义子句                               | `PartitionTypeDefinition`      | `part_type_def`                                              |
| `opt_key_algorithm`                | 可选的 `ALGORITHM` 关键字引导的指定分区算法子句      | `Optional[IntLiteral]`         | `opt_key_algo`                                               |
| `opt_keyword_linear`               | 可选的 `linear` 关键字                               | -                              | `opt_linear`                                                 |
| `opt_num_partitions`               | 可选的 `PARTITIONS` 关键字引导的指定分区数量子句     | `Optional[int]`                | `opt_num_parts`                                              |
| `opt_subpartition_type_definition` | 可选的子分区的类型定义子句                           | `SubPartitionTypeDefinition`   | `opt_sub_part`                                               |
| `opt_num_subpartitions`            | 可选的 `SUBPARTITION` 关键字引导的指定子分区数量子句 | `Optional[int]`                | `opt_num_subparts`                                           |
| `opt_partition_definition_list`    | 可选的括号嵌套的分区定义子句的列表                   | `List[PartitionDefinition]`    | `opt_part_defs`                                              |
| `partition_definition_list`        | 分区定义子句的列表                                   | `List[PartitionDefinition]`    | `part_def_list`                                              |
| `partition_definition`             | 分区定义子句                                         | `PartitionDefinition`          | `part_definition`                                            |
| `opt_partition_values`             | 可选的 `VALUES` 关键字引导的分区值列表子句           | `Optional[PartitionValues]`    | `opt_part_values`<br />`part_func_max`【包含】<br />`part_values_in`【包含】 |
| `partition_value_list_parens_list` | “括号嵌套的分区值的列表” 的列表                      | `List[List[PartitionValue]]`   | `part_value_list`                                            |
| `partition_value_list_parens`      | 括号嵌套的分区值的列表                               | `List[PartitionValue]`         | `part_value_item_list_paren`                                 |
| `partition_value_list`             | 分区值的列表                                         | `List[PartitionValue]`         | `part_value_item_list`                                       |
| `partition_value`                  | 分区值                                               | `PartitionValue`               | `part_value_item`                                            |
| `opt_subpartition_definition_list` | 可选的括号嵌套的定义子分区子句的列表                 | `List[SubPartitionDefinition]` | `opt_sub_partition`                                          |
| `subpartition_definition_list`     | 定义子分区子句的列表                                 | `List[SubPartitionDefinition]` | `sub_part_list`                                              |
| `subpartition_definition`          | 定义子分区子句                                       | `SubPartitionDefinition`       | `sub_part_definition`                                        |
| `opt_partition_option_list`        | 可选的分区配置选项的列表                             | `List[PartitionOption]`        | `opt_part_options`                                           |
| `partition_option_list`            | 分区配置选项的列表                                   | `List[PartitionOption]`        | `part_option_list`                                           |
| `partition_option`                 | 分区配置选项                                         | `PartitionOption`              | `part_option`                                                |

# 短语（pharse）

#### DDL 选项（ddl option）

| 水杉解析器语义组名称                       | 语义组含义                                              | 返回值类型                           | MySQL 语义组名称                                          |
| ------------------------------------------ | ------------------------------------------------------- | ------------------------------------ | --------------------------------------------------------- |
| `create_table_option_list`                 | 逗号或空格分隔的 `CREATE TABLE` 语句中的表属性的列表    | `List[DdlOption]`                    | `create_table_options`                                    |
| `create_table_option_list_space_separated` | 空格分隔的 `CREATE TABLE` 语句中的表属性的列表          | `List[DdlOption]`                    | `create_table_options_space_separated`                    |
| `create_table_option`                      | `CREATE TABLE` 语句中的表选项                           | `DdlOption`                          | `create_table_option`                                     |
| `opt_create_database_option_list`          | 可选的 `CREATE DATABASE` 语句中的数据库选项列表         | `List[DdlOption]`                    | `opt_create_database_options`                             |
| `create_database_option_list`              | `CREATE DATABASE` 语句中的数据库选项列表                | `List[DdlOption]`                    | `create_database_option_list`                             |
| `create_database_option`                   | `CREATE DATABASE` 语句中的数据库选项                    | `DdlOption`                          | `create_database_option`                                  |
| `alter_database_option_list`               | `ALTER DATABASE` 语句中的数据库选项列表                 | `List[DdlOption]`                    | `alter_database_option_list`                              |
| `alter_database_option`                    | `ALTER DATABASE` 语句中的数据库选项                     | `DdlOption`                          | `alter_database_option`                                   |
| `ternary_option_value`                     | 整数字面值、十六进制字面值或 `DEFAULT` 关键字           | `Expression`                         | `ternary_option`                                          |
| `ddl_option_default_charset`               | 指定默认字符集的数据库选项或表选项                      | `DdlOptionDefaultCharset`            | `default_charset`                                         |
| `ddl_option_default_collate`               | 指定默认排序规则的数据库选项或表选项                    | `DdlOptionDefaultCollate`            | `default_collation`                                       |
| `ddl_option_default_encryption`            | 指定默认加密的数据库选项                                | `DdlOptionDefaultEncryption`         | `default_encryption`                                      |
| `ddl_option_autoextend_size`               | 指定表空间每次自动扩展的大小属性                        | `DdlOptionAutoextendSize`            | `option_autoextend_size`<br />`ts_option_autoextend_size` |
| `opt_drop_tablespace_option_list`          | 可选的 `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表 | `List[DdlOption]`                    | `opt_drop_ts_options`                                     |
| `drop_tablespace_option_list`              | `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表        | `List[DdlOption]`                    | `drop_ts_option_list`                                     |
| `drop_tablespace_option`                   | `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项              | `DdlOption`                          | `drop_ts_option`                                          |
| `opt_drop_undo_tablespace_option_list`     | 可选的 `UNDO TABLESPACE` 的选项的列表                   | `List[DdlOption]`                    | `opt_undo_tablespace_options`                             |
| `drop_undo_tablespace_option_list`         | `UNDO TABLESPACE` 的选项的列表                          | `List[DdlOption]`                    | `undo_tablespace_option_list`                             |
| `drop_undo_tablespace_option`              | `UNDO TABLESPACE` 的选项                                | `DdlOption`                          | `undo_tablespace_option`                                  |
| `opt_create_tablespace_option_list`        | 可选的 `CREATE TABLESPACE` 的选项的列表                 | `List[DdlOption]`                    | `opt_tablespace_options`                                  |
| `create_tablespace_option_list`            | `CREATE TABLESPACE` 的选项的列表                        | `List[DdlOption]`                    | `tablespace_option_list`                                  |
| `create_tablespace_option`                 | `CREATE TABLESPACE` 的选项                              | `DdlOption`                          | `tablespace_option`                                       |
| `opt_create_logfile_option_list`           | 可选的 `CREATE LOGFILE` 的选项的列表                    | `List[DdlOption]`                    | `opt_logfile_group_options`                               |
| `create_logfile_option_list`               | `CREATE LOGFILE` 的选项的列表                           | `List[DdlOption]`                    | `logfile_group_option_list`                               |
| `create_logfile_option`                    | `CREATE LOGFILE` 的选项                                 | `DdlOption`                          | `logfile_group_option`                                    |
| `ddl_option_engine`                        | ALTER 选项：`ENGINE`                                    | `DdlOptionEngine`                    | `ts_option_engine`                                        |
| `ddl_option_wait`                          | ALTER 选项：`WAIT` 或 `NO_WAIT`                         | `DdlOptionWait`                      | `ts_option_wait`                                          |
| `ddl_option_initial_size`                  | 指定表空间初始大小的属性                                | `DdlOptionInitialSize`               | `ts_option_initial_size`                                  |
| `ddl_option_max_size`                      | 指定表空间最大大小的属性                                | `DdlOptionMaxSize`                   | `ts_option_max_size`                                      |
| `ddl_option_tablespace_encryption`         | 指定表空间加密属性                                      | `DdlOptionTablespaceEncryption`      | `ts_option_encryption`                                    |
| `ddl_option_tablespace_engine_attribute`   | 指定表空间引擎属性                                      | `DdlOptionTablespaceEngineAttribute` | `ts_option_engine_attribute`                              |
| `ddl_option_extent_size`                   | 指定表空间段初始空间大小的属性                          | `DdlOptionExtentSize`                | `ts_option_extent_size`                                   |
| `ddl_option_undo_buffer_size`              | 指定表空间的 UNDO 日志缓冲区大小的属性                  | `DdlOptionUndoBufferSize`            | `ts_option_undo_buffer_size`                              |
| `ddl_option_redo_buffer_size`              | 指定表空间的 REDO 日志缓冲区大小的属性                  | `DdlOptionRedoBufferSize`            | `ts_option_redo_buffer_size`                              |
| `ddl_option_nodegroup`                     | 指定表空间的节点组属性                                  | `DdlOptionNodeGroup`                 | `ts_option_nodegroup`                                     |
| `ddl_option_comment`                       | 指定注释                                                | `DdlOptionComment`                   | `ts_option_comment`                                       |
| `ddl_option_file_block_size`               | 指定表空间文件块大小                                    | `DdlOptionFileBlockSize`             | `ts_option_file_block_size`                               |

`drop_undo_tablespace_option` 语义组与 `alter_option_engine` 语义组一致，但考虑可拓展性保留单独的 `drop_undo_tablespace_option` 语义组。

#### 字段类型（field type）

| 水杉解析器语义组名称       | 语义组含义                                                   | 返回值类型        | MySQL 语义组名称                                 |
| -------------------------- | ------------------------------------------------------------ | ----------------- | ------------------------------------------------ |
| `field_type_param_1`       | 括号中的 1 个字段类型参数                                    | `FieldTypeParams` | `field_length`<br />`type_datetime_precision`    |
| `opt_field_type_param_1`   | 可选的括号中的 1 个字段类型参数                              | `FieldTypeParams` | `opt_field_length`<br />`standard_float_options` |
| `field_type_param_2`       | 括号中的 2 个字段类型参数                                    | `FieldTypeParams` | `precision`                                      |
| `opt_field_type_param_2`   | 可选的括号中的 2 个字段类型参数                              | `FieldTypeParams` | `opt_precision`                                  |
| `opt_field_type_param_0_1` | 可选的括号中的 0 个或 1 个字段类型参数                       | `FieldTypeParams` | `func_datetime_precision`                        |
| `opt_field_type_param_1_2` | 可选的括号中的 1 个或 2 个字段类型参数                       | `FieldTypeParams` | `float_options`                                  |
| `cast_type`                | `CAST` 函数、`CONVERT` 函数以及 `JSON_VALUE` 函数中指定的返回值类型 | `CastType`        | `cast_type`                                      |
| `opt_returning_type`       | `JSON_VALUE` 函数中可选的返回值类型                          | `CastType`        | `opt_returning_type`                             |
| `field_option`             | 单个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）           | `FieldOption`     | `field_option`                                   |
| `field_option_list`        | 多个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）           | `FieldOption`     | `field_opt_list`                                 |
| `opt_field_option_list`    | 可选的多个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）     | `FieldOption`     | `field_options`                                  |
| `field_type`               | DDL 语句中的字段类型                                         | `FieldType`       | `type`                                           |

#### DDL 表元素（ddl table element）

| 水杉解析器语义组名称                  | 语义组含义                                                   | 返回值类型                       | MySQL 语义组名称                                |
| ------------------------------------- | ------------------------------------------------------------ | -------------------------------- | ----------------------------------------------- |
| `table_element_list`                  | DDL 定义表中的元素的列表                                     | `List[TableElement]`             | `table_element_list`                            |
| `table_element`                       | DDL 定义表中的元素                                           | `TableElement`                   | `table_element`                                 |
| `column_definition`                   | DDL 的字段定义信息（含外键）                                 | `ColumnDefinition`               | `column_def`                                    |
| `field_definition`                    | DDL 的字段基本信息（不含外键约束）                           | `FieldDefinition`                | `field_def`                                     |
| `opt_generated_always`                | 可选的 `GENERATED ALWAYS` 关键字                             | `bool`                           | `opt_generated_always`                          |
| `opt_stored_attribute`                | 可选的 `VIRTUAL` 或 `STORED` 关键字                          | `EnumStoredAttribute`            | `opt_stored_attribute`                          |
| `opt_references_definition`           | 可选的 `REFERENCES` 关键字引导的指定外键约束子句             | `Optional[ReferencesDefinition]` | `opt_references`                                |
| `references_definition`               | `REFERENCES` 关键字引导的指定外键约束子句                    | `ReferencesDefinition`           | `references`                                    |
| `opt_match_clause`                    | 外键约束中可选的 `MATCH` 子句                                | `EnumReferenceMatch`             | `opt_match_clause`                              |
| `opt_on_update_on_delete`             | `REFERENCES` 指定外键约束子句中的 `ON UPDATE` 和 `ON DELETE` 子句 | `TempOnUpdateOnDelete`           | `opt_on_update_delete`                          |
| `reference_action_option`             | `REFERENCE` 子句中指定外键变化时行为的选项                   | `EnumReferenceActionOption`      | `delete_option`                                 |
| `index_definition`                    | DDL 的索引定义信息                                           | `TableElement`                   | `table_constraint_def`                          |
| `opt_index_name_and_type`             | 可选的索引名称和索引数据结构                                 | `TempIndexNameAndType`           | `opt_index_name_and_type`                       |
| `index_key_definition_list`           | 索引字段定义的列表                                           | `List[IndexKeyDefinition]`       | `key_list`                                      |
| `index_key_definition`                | 索引字段定义                                                 | `IndexKeyDefinition`             | `key_part`                                      |
| `index_key_definition_with_expr_list` | 包含使用表达式的索引字段定义的列表                           | `List[IndexKeyDefinition]`       | `key_list_with_expression`                      |
| `index_key_definition_with_expr`      | 包含使用表达式的索引字段定义                                 | `IndexKeyDefinition`             | `key_part_with_expression`                      |
| `constraint_index_type`               | 约束类索引类型（主键索引或唯一索引）                         | `EnumIndexType`                  | `constraint_key_type`                           |
| `opt_keyword_key_or_index`            | 可选的 `KEY` 或 `INDEX` 关键字                               | -                                | `opt_key_or_index`                              |
| `keyword_key_or_index`                | `KEY` 或 `INDEX` 关键字                                      | -                                | `key_or_index`                                  |
| `keyword_keys_or_index`               | `KEYS`、`INDEX` 或 `INDEXES` 关键字                          | -                                |                                                 |
| `opt_constraint_enforcement`          | 可选的 `ENFORCED`、`NOT ENFORCED` 关键字                     | `Optional[bool]`                 | `opt_constraint_enforcement`                    |
| `constraint_enforcement`              | `ENFORCED`、`NOT ENFORCED` 关键字                            | `bool`                           | `constraint_enforcement`<br />`opt_not`【包含】 |

#### DDL 字段属性（ddl column attribute）

| 水杉解析器语义组名称        | 语义组含义                               | 返回值类型              | MySQL 语义组名称                                             |
| --------------------------- | ---------------------------------------- | ----------------------- | ------------------------------------------------------------ |
| `opt_column_attribute_list` | 可选的 DDL 字段属性的列表                | `List[ColumnAttribute]` | `opt_column_attribute_list`                                  |
| `column_attribute_list`     | DDL 字段属性的列表                       | `List[ColumnAttribute]` | `column_attribute_list`                                      |
| `column_attribute`          | DDL 字段属性                             | `ColumnAttribute`       | `column_attribute`<br />`opt_keyword_primary`【包含】<br />`constraint_enforcement`【包含】 |
| `now_or_signed_literal`     | `NOW` 关键字或数值字面值                 | `Expression`            | `now_or_signed_literal`                                      |
| `column_format`             | DDL 字段存储格式的枚举                   | `EnumColumnFormat`      | `column_format`                                              |
| `storage_media`             | DDL 字段存储介质的枚举                   | `EnumStorageMedia`      | `storage_media`                                              |
| `opt_constraint_name`       | 可选的 `CONSTRAINT` 关键字引导的约束名称 | `Optional[str]`         | `opt_constraint_name`                                        |
| `check_constraint`          | 指定约束条件的 `CHECK` 子句              | `Expression`            | `check_constraint`                                           |

#### DDL 索引属性（ddl index attribute）

| 水杉解析器语义组名称                | 语义组含义                             | 返回值类型                          | MySQL 语义组名称             |
| ----------------------------------- | -------------------------------------- | ----------------------------------- | ---------------------------- |
| `opt_spatial_index_attribute_list`  | 可选的 `SPATIAL` 类型索引的属性的列表  | `List[IndexAttribute]`              | `opt_spatial_index_options`  |
| `spatial_index_attribute_list`      | `SPATIAL` 类型索引的属性的列表         | `List[IndexAttribute]`              | `spatial_index_options`      |
| `spatial_index_attribute`           | `SPATIAL` 类型索引的属性               | `IndexAttribute`                    | `spatial_index_option`       |
| `opt_fulltext_index_attribute_list` | 可选的 `FULLTEXT` 类型索引的属性的列表 | `List[IndexAttribute]`              | `opt_fulltext_index_options` |
| `fulltext_index_attribute_list`     | `FULLTEXT` 类型索引的属性的列表        | `List[IndexAttribute]`              | `fulltext_index_options`     |
| `fulltext_index_attribute`          | `FULLTEXT` 类型索引的属性              | `IndexAttribute`                    | `fulltext_index_option`      |
| `opt_normal_index_attribute_list`   | 可选的普通类型索引的属性的列表         | `List[IndexAttribute]`              | `opt_index_options`          |
| `normal_index_attribute_list`       | 普通类型索引的属性的列表               | `List[IndexAttribute]`              | `index_options`              |
| `normal_index_attribute`            | 普通类型索引的属性                     | `IndexAttribute`                    | `index_option`               |
| `common_index_attribute`            | 各索引类型通用的属性                   | `IndexAttribute`                    | `common_index_option`        |
| `opt_index_type_clause`             | 可选的指定索引数据结构类型的子句       | `Optional[IndexAttrUsingIndexType]` | `opt_index_type_clause`      |
| `index_type_clause`                 | 指定索引数据结构类型的子句             | `IndexAttrUsingIndexType`           | `index_type_clause`          |
| `index_structure_type`              | 索引数据结构类型                       | `EnumIndexStructureType`            | `index_type`                 |

`spatial_index_option` 语义组与 `common_index_attribute` 语义组逻辑一致，但为保证可拓展性将其拆分为两个语义组。

#### 别名（alias）

| 水杉解析器语义组名称 | 语义组含义                          | 返回值类型      | MySQL 语义组名称  |
| -------------------- | ----------------------------------- | --------------- | ----------------- |
| `opt_keyword_as`     | 可选的 `AS` 关键字                  | -               | `opt_as`          |
| `opt_select_alias`   | 可选的字段表达式和 UDF 表达式的别名 | `Optional[str]` | `select_alias`    |
| `opt_table_alias`    | 可选的表表达式的别名                | `Optional[str]` | `opt_table_alias` |

#### JSON 表选项（json table option）

| 水杉解析器语义组名称     | 语义组含义                          | 返回值类型           | MySQL 语义组名称                                             |
| ------------------------ | ----------------------------------- | -------------------- | ------------------------------------------------------------ |
| `json_on_response`       | Json 解析失败时的返回值             | `JsonOnResponse`     | `json_on_response`                                           |
| `json_on_empty`          | Json 解析遇到空值时的处理方法       | `JsonOnResponse`     | `on_empty`                                                   |
| `json_on_error`          | Json 解析遇到错误时的处理方法       | `JsonOnResponse`     | `on_error`                                                   |
| `json_on_empty_on_error` | Json 解析遇到空值或错误时的处理方法 | `JsonOnEmptyOnError` | `opt_on_empty_or_error`<br />`opt_on_empty_or_error_json_table` |

#### 时间间隔（time interval）

| 水杉解析器语义组名称 | 语义组含义     | 返回值类型     | MySQL 语义组名称                             |
| -------------------- | -------------- | -------------- | -------------------------------------------- |
| `time_interval`      | 时间间隔表达式 | `TimeInterval` | 无对应语义组（`INTERVAL_SYM expr interval`） |

#### DML 语句选项（dml option）

| 水杉解析器语义组名称       | 语义组含义                                                   | 返回值类型  | MySQL 语义组名称      |
| -------------------------- | ------------------------------------------------------------ | ----------- | --------------------- |
| `opt_keyword_ignore`       | 可选的 `IGNORE` 关键字                                       | `DmlOption` | `opt_ignore`          |
| `opt_keyword_low_priority` | 可选的 `LOW_PRIORITY` 关键字                                 | `DmlOption` | `opt_low_priority`    |
| `opt_delete_option_list`   | 可选的 `DELETE` 语句中的选项的列表                           | `DmlOption` | `opt_delete_options`  |
| `delete_option_list`       | `DELETE` 语句中的选项的列表                                  | `DmlOption` |                       |
| `delete_option`            | `DELETE` 语句中的选项（`quick`、`LOW_PRIORITY` 或 `IGNORE` 关键字） | `DmlOption` | `opt_delete_option`   |
| `opt_insert_option`        | 可选的 `INSERT` 语句中的选项                                 | `DmlOption` | `insert_lock_option`  |
| `opt_replace_option`       | 可选的 `REPLACE` 语句中的选项                                | `DmlOption` | `replace_lock_option` |

#### 重复值处理规则（on duplicate）

| 水杉解析器语义组名称 | 语义组含义                                              | 返回值类型    | MySQL 语义组名称 |
| -------------------- | ------------------------------------------------------- | ------------- | ---------------- |
| `opt_on_duplicate`   | 可选的指定重复值处理规则的 `REPLACE` 或 `IGNORE` 关键字 | `OnDuplicate` | `opt_duplicate`  |
| `on_duplicate`       | 指定重复值处理规则的 `REPLACE` 或 `IGNORE` 关键字       | `OnDuplicate` | `duplicate`      |

#### DDL 修改表选项（ddl alter option）

核心是 `alter_command_modifier_list` 语义组。

| 水杉解析器语义组名称                  | 语义组含义                                                   | 返回值类型                  | MySQL 语义组名称                                             |
| ------------------------------------- | ------------------------------------------------------------ | --------------------------- | ------------------------------------------------------------ |
| `alter_command_modifier_list`         | `ALTER` 命令的修饰选项的列表                                 | `TempAlterOptionList`       | `alter_commands_modifier_list`                               |
| `alter_command_modifier`              | `ALTER` 命令的修饰选项                                       | `TempAlterOptionList`       | `alter_commands_modifier`                                    |
| `opt_alter_option_lock_and_algorithm` | 可选的任意顺序的 `ALGORITHM` 和 `LOCK` 修改表选项子句        | `TempAlterOptionList`       | `opt_index_lock_and_algorithm`                               |
| `alter_option_algorithm`              | DDL 修改表选项：`ALGORITHM`（创建索引时使用的算法或机制）    | `AlterAlgorithmOption`      | `alter_algorithm_option`<br />`alter_algorithm_option_value`【包含】 |
| `alter_option_lock`                   | DDL 修改表选项：`LOCK`（指定创建索引时对表施加的锁类型）     | `AlterLockOption`           | `alter_lock_option`<br />`alter_lock_option_value`【包含】   |
| `opt_alter_option_with_validation`    | 可选的 DDL 修改表选项：`WITH VALIDATION` 或 `WITHOUT VALIDATION` | `AlterOptionWithValidation` | `opt_with_validation`                                        |
| `alter_option_with_validation`        | DDL 修改表选项：`WITH VALIDATION` 或 `WITHOUT VALIDATION`    | `AlterOptionWithValidation` | `with_validation`                                            |

#### CPU 范围（cpu range）

| 水杉解析器语义组名称           | 语义组含义                                       | 返回值类型       | MySQL 语义组名称               |
| ------------------------------ | ------------------------------------------------ | ---------------- | ------------------------------ |
| `opt_resource_group_vcpu_list` | `VCPU` 关键字引导的指定 CPU 编号或范围列表的等式 | `List[CpuRange]` | `opt_resource_group_vcpu_list` |
| `cpu_num_or_range_list`        | CPU 编号或范围的列表                             | `List[CpuRange]` | `vcpu_range_spec_list`         |
| `cpu_num_or_range`             | CPU 编号或范围                                   | `CpuRange`       | `vcpu_num_or_range`            |

#### SQL 状态（sql state）

| 水杉解析器语义组名称 | 语义组含义 | 返回值类型 | MySQL 语义组名称 |
| -------------------- | ---------- | ---------- | ---------------- |
| `sql_state`          | SQL 状态   | `SqlState` | `sqlstate`       |

#### 线程优先级（thread priority）

| 水杉解析器语义组名称  | 语义组含义                 | 返回值类型       | MySQL 语义组名称              |
| --------------------- | -------------------------- | ---------------- | ----------------------------- |
| `opt_thread_priority` | 可选的线程优先级           | `ThreadPriority` | `opt_resource_group_priority` |
| `signed_int_num`      | 正整数字面值或负整数字面值 | `int`            | `signed_num`                  |

#### 函数选项（function option）

| 水杉解析器语义组名称          | 语义组含义                                                   | 返回值类型             | MySQL 语义组名称                    |
| ----------------------------- | ------------------------------------------------------------ | ---------------------- | ----------------------------------- |
| `alter_function_option_list`  | `ALTER FUNCTION` 和 `ALTER PROCEDURE` 语句中的函数选项的列表 | `List[FunctionOption]` | `sp_a_chistics`                     |
| `alter_function_option`       | `ALTER FUNCTION` 和 `ALTER PROCEDURE` 语句中的函数选项       | `FunctionOption`       | `sp_chistic`<br />`sp_suid`【子集】 |
| `create_function_option_list` | `CREATE FUNCTION` 和 `CREATE PROCEDURE` 语句中的函数选项的列表 | `List[FunctionOption]` | `sp_c_chistics`                     |
| `create_function_option`      | `CREATE FUNCTION` 和 `CREATE PROCEDURE` 语句中的函数选项     | `FunctionOption`       | `sp_c_chistic`                      |

#### 处理命令（process command）

`EVENT` 语句和 `TRIGGER` 语句中使用的处理命令。

| 水杉解析器语义组名称                     | 语义组含义                           | 返回值类型                           | MySQL 语义组名称                                             |
| ---------------------------------------- | ------------------------------------ | ------------------------------------ | ------------------------------------------------------------ |
| `process_command_list`                   | 分号分隔的处理命令的列表             | `List[ProcessCommand]`               | `sp_proc_stmts1`<br />`sp_proc_stmts`                        |
| `opt_do_process_command`                 | 可选的 `DO` 关键字引导的处理命令     | `Optional[ProcessCommand]`           | `opt_ev_sql_stmt`                                            |
| `process_command`                        | 处理命令                             | `ProcessCommand`                     | `sp_proc_stmt`<br />`ev_sql_stmt_inner`<br />`ev_sql_stmt`   |
| `process_command_statement`              | 处理命令：执行语句                   | `ProcessCommandStatement`            | `sp_proc_stmt_statement`                                     |
| `process_command_return`                 | 处理命令：返回表达式结果             | `ProcessCommandReturn`               | `sp_proc_stmt_return`                                        |
| `process_command_if`                     | 处理命令：`IF` 语句                  | `ProcessCommandIf`                   | `sp_proc_stmt_if`<br />`sp_if`【包含】                       |
| `process_command_opt_elseif_list`        | 处理命令中可选的 `ELSEIF` 子句的列表 | `List[ProcessCommandConditionTuple]` | `sp_elseifs`【部分】                                         |
| `process_command_elseif_list`            | 处理命令中的 `ELSEIF` 子句的列表     | `List[ProcessCommandConditionTuple]` | `sp_elseifs`【部分】                                         |
| `process_command_elseif`                 | 处理命令中的 `ELSEIF` 子句           | `ProcessCommandConditionTuple`       | `sp_elseifs`【部分】                                         |
| `process_command_opt_else`               | 处理命令中可选的 `ELSE` 子句         | `Optional[List[ProcessCommand]]`     | `else_clause_opt`                                            |
| `process_command_case`                   | 处理命令：`CASE` 语句                | `ProcessCommandCase`                 | `case_stmt_specification`<br />`simple_case_stmt`【子集】<br />`searched_case_stmt`【子集】 |
| `process_command_when_clause_list`       | 处理命令中的 `WHEN` 子句的列表       | `List[ProcessCommandConditionTuple]` | `simple_when_clause_list`<br />`searched_when_clause_list`   |
| `process_command_when_clause`            | 处理命令中的 `WHEN` 子句             | `ProcessCommandConditionTuple`       | `simple_when_clause`<br />`searched_when_clause`             |
| `process_command_handler_condition_list` | 处理命令中的处理器条件值的列表       | `List[ProcessCommandConditionValue]` | `sp_hcond_list`                                              |
| `process_command_declare_list`           | 处理命令的声明表达式的列表           | `List[ProcessCommandDeclare]`        | `sp_decls`                                                   |
| `process_command_declare`                | 处理命令的声明表达式                 | `ProcessCommandDeclare`              | `sp_decl`                                                    |
| `process_command_handler_condition`      | 处理命令中的处理器条件值             | `ProcessCommandConditionValue`       | `sp_hcond`<br />`sp_hcond_element`                           |
| `process_command_condition`              | 处理命令中的条件值                   | `ProcessCommandConditionValue`       | `sp_cond`                                                    |
| `process_command_labeled_block`          | 处理命令：带标签的代码块             | `ProcessCommandLabeledBlock`         | `sp_labeled_block`                                           |
| `process_command_unlabeled_block`        | 处理命令：不带标签的代码块           | `ProcessCommandUnlabeledBlock`       | `sp_unlabeled_block`                                         |
| `process_command_block`                  | 处理命令中的代码块内容               | `ProcessCommandBlock`                | `sp_block_content`                                           |
| `process_command_labeled_control`        | 处理命令：带标签的控制语句           | `ProcessCommandLabeledControl`       | `sp_labeled_control`                                         |
| `process_command_unlabeled_control`      | 处理命令：不带标签的控制语句         | `ProcessCommand`                     | `sp_proc_stmt_unlabeled`<br />`sp_unlabeled_control`         |
| `process_command_leave`                  | 处理命令：`LEAVE` 语句               | `ProcessCommandLeave`                | `sp_proc_stmt_leave`                                         |
| `process_command_iterate`                | 处理命令：`ITERATE` 语句             | `ProcessCommandIterate`              | `sp_proc_stmt_iterate`                                       |
| `process_command_open`                   | 处理命令：`OPEN` 游标语句            | `ProcessCommandOpen`                 | `sp_proc_stmt_open`                                          |
| `process_command_fetch`                  | 处理命令：`FETCH` 游标语句           | `ProcessCommandFetch`                | `sp_proc_stmt_fetch`                                         |
| `process_command_close`                  | 处理命令：`CLOSE` 游标语句           | `ProcessCommandClose`                | `sp_proc_stmt_close`                                         |

#### 事件调度时间（schedule time）

| 水杉解析器语义组名称   | 语义组含义                              | 返回值类型               | MySQL 语义组名称                                |
| ---------------------- | --------------------------------------- | ------------------------ | ----------------------------------------------- |
| `opt_on_schedule_time` | 可选的 `ON SCHEDULE` 引导的事件调度时间 | `Optional[ScheduleTime]` |                                                 |
| `on_schedule_time`     | `ON SCHEDULE` 引导的事件调度时间        | `ScheduleTime`           | （对应 `ON_SYM SCHEDULE_SYM ev_schedule_time`） |
| `schedule_time`        | 事件调度时间                            | `ScheduleTime`           | `ev_schedule_time`                              |
| `opt_schedule_starts`  | 可选的事件开始时间                      | `Optional[Expression]`   | `ev_starts`                                     |
| `opt_schedule_ends`    | 可选的事件结束时间                      | `Optional[Expression]`   | `ev_ends`                                       |

#### 事件属性（event attribute）

| 水杉解析器语义组名称 | 语义组含义       | 返回值类型             | MySQL 语义组名称   |
| -------------------- | ---------------- | ---------------------- | ------------------ |
| `opt_event_rename`   | 可选的事件重命名 | `Optional[Identifier]` | `opt_ev_rename_to` |
| `opt_event_comment`  | 可选的事件注释   | `Optional[str]`        | `opt_ev_comment`   |

#### 修改命令（alter command）

| 水杉解析器语义组名称            | 语义组含义                                            | 返回值类型                                          | MySQL 语义组名称                                   |
| ------------------------------- | ----------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------- |
| `opt_alter_table_actions`       | 可选的包含窗口相关修改命令的修改命令的列表            | `List[Union[AlterCommand, AlterOption, DdlOption]]` | `opt_alter_table_actions`                          |
| `standalone_alter_table_action` | `ALTER` 命令的修饰选项的列表和独立的 `ALTER` 修改命令 | `List[Union[AlterCommand, AlterOption, DdlOption]]` | `standalone_alter_table_action`                    |
| `opt_alter_command_list`        | 可选的修改命令的列表                                  | `List[Union[AlterCommand, AlterOption, DdlOption]]` | `opt_alter_command_list`<br />`alter_list`【子集】 |
| `alter_command_list`            | 修改命令的列表                                        | `List[Union[AlterCommand, AlterOption, DdlOption]]` |                                                    |
| `alter_command`                 | 单个修改命令                                          | `List[Union[AlterCommand, AlterOption, DdlOption]]` |                                                    |
| `standalone_alter_commands`     | 独立的 `ALTER` 修改命令                               | `AlterCommand`                                      | `standalone_alter_commands`                        |
| `alter_list_item`               | `ALTER TABLE` 修改命令                                | `AlterCommand`                                      | `alter_list_item`                                  |
| `alter_table_partition_options` | 窗口相关的修改命令                                    | `AlterCommand`                                      | `alter_table_partition_options`                    |
| `all_or_alt_part_name_list`     | `ALL` 关键字或指定分区名称列表                        | `Optional[List[str]]`                               | `all_or_alt_part_name_list`                        |
| `opt_place`                     | 可选的变更字段插入位置                                | `AlterPlace`                                        | `opt_place`                                        |
| `alter_order_expr_list`         | `ALTER` 排序表达式的列表                              | `List[OrderExpression]`                             | `alter_order_list`                                 |
| `alter_order_expr`              | `ALTER` 排序表达式                                    | `OrderExpression`                                   | `alter_order_item`                                 |

#### 日志文件撤销文件（undofile）

| 水杉解析器语义组名称 | 语义组含义           | 返回值类型 | MySQL 语义组名称 |
| -------------------- | -------------------- | ---------- | ---------------- |
| `undofile`           | 日志文件撤销文件名称 | `str`      | `lg_undofile`    |

#### 表空间数据文件（datafile）

| 水杉解析器语义组名称 | 语义组含义         | 返回值类型 | MySQL 语义组名称 |
| -------------------- | ------------------ | ---------- | ---------------- |
| `datafile`           | 表空间数据文件名称 | `str`      | `ts_datafile`    |

#### 服务器选项（server option）

| 水杉解析器语义组名称  | 语义组含义       | 返回值类型           | MySQL 语义组名称      |
| --------------------- | ---------------- | -------------------- | --------------------- |
| `server_options_list` | 服务器选项的列表 | `List[ServerOption]` | `server_options_list` |
| `server_option`       | 服务器选项       | `ServerOption`       | `server_option`       |

#### 身份认证（identification）

| 水杉解析器语义组名称                        | 语义组含义                       | 返回值类型                             | MySQL 语义组名称                            |
| ------------------------------------------- | -------------------------------- | -------------------------------------- | ------------------------------------------- |
| `identification`                            | 身份认证（选择具体的认证方式）   | `Identification`                       | `identification`                            |
| `identified_by_password`                    | 使用密码进行身份认证             | `IdentifiedByPassword`                 | `identified_by_password`                    |
| `identified_by_random_password`             | 使用随机密码进行身份认证         | `IdentifiedByRandomPassword`           | `identified_by_random_password`             |
| `identified_with_plugin`                    | 使用插件进行身份认证             | `IdentifiedWithPlugin`                 | `identified_with_plugin`                    |
| `identified_with_plugin_as_auth`            | 使用插件和认证字符串进行身份认证 | `IdentifiedWithPluginAsAuth`           | `identified_with_plugin_as_auth`            |
| `identified_with_plugin_by_password`        | 使用插件和密码进行身份认证       | `IdentifiedWithPluginByPassword`       | `identified_with_plugin_by_password`        |
| `identified_with_plugin_by_random_password` | 使用插件和随机密码进行身份认证   | `IdentifiedWithPluginByRandomPassword` | `identified_with_plugin_by_random_password` |

#### 复制源定义（source definition）

| 水杉解析器语义组名称 | 语义组含义                | 返回值类型               | MySQL 语义组名称                             |
| -------------------- | ------------------------- | ------------------------ | -------------------------------------------- |
| `source_def_list`    | 复制源定义的列表          | `List[SourceDefinition]` | `source_defs`                                |
| `source_def`         | 复制源定义                | `SourceDefinition`       | `source_def`                                 |
| `source_file_def`    | 源文件定义                | `SourceFileDefinition`   | `source_file_def`                            |
| `assign_gtids_type`  | 分配 GTIDs 给匿名事务定义 | `AssignGidsDefinition`   | `assign_gtids_to_anonymous_transactions_def` |

#### 过滤器定义（filter definition）

| 水杉解析器语义组名称      | 语义组含义         | 返回值类型               | MySQL 语义组名称          |
| ------------------------- | ------------------ | ------------------------ | ------------------------- |
| `filter_def_list`         | 过滤器定义的列表   | `List[FilterDefinition]` | `filter_defs`             |
| `filter_def`              | 过滤器定义         | `FilterDefinition`       | `filter_def`              |
| `opt_filter_db_pair_list` | 可选的数据库对列表 | `List[Tuple[str, str]]`  | `opt_filter_db_pair_list` |
| `filter_db_pair_list`     | 数据库对列表       | `List[Tuple[str, str]]`  | `filter_db_pair_list`     |

#### 连接选项（connect option）

| 水杉解析器语义组名称      | 语义组含义         | 返回值类型            | MySQL 语义组名称      |
| ------------------------- | ------------------ | --------------------- | --------------------- |
| `opt_connect_option_list` | 可选的连接选项列表 | `List[ConnectOption]` | `connect_options`     |
| `connect_option_list`     | 连接选项的列表     | `List[ConnectOption]` | `connect_option_list` |
| `connect_option`          | 连接选项           | `ConnectOption`       | `connect_option`      |

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

#### 通用表逻辑（general table）

`table_reference_list` 是在 DQL 语句的 `FROM` 子句、`UPDATE` 语句、`DELETE` 语句中使用的表名的列表；`table_reference_list` 是 `table_reference` 的列表。

| 水杉解析器语义组名称          | 语义组含义                                                   | 返回值类型    | MySQL 语义组名称              |
| ----------------------------- | ------------------------------------------------------------ | ------------- | ----------------------------- |
| `table_reference_list`        | 在 DQL 和 DML 语句中的表元素的列表                           | `List[Table]` | `table_reference_list`        |
| `table_reference`             | 在 DQL 和 DML 语句中的表元素                                 | `Table`       | `table_reference`             |
| `esc_table_reference`         | 不兼容 ODBC 语法的表元素                                     | `Table`       | `esc_table_reference`         |
| `table_factor`                | 单个表元素（包含任意层括号的 single_table、derived_table、joined_table_parens、table_reference_list_parens、table_function） | `Table`       | `table_factor`                |
| `table_reference_list_parens` | 包含任意层括号的在 DQL 和 DML 语句中的表元素的列表           | `List[Table]` | `table_reference_list_parens` |

#### 单表（single table）

| 水杉解析器语义组名称  | 语义组含义                                       | 返回值类型    | MySQL 语义组名称      |
| --------------------- | ------------------------------------------------ | ------------- | --------------------- |
| `single_table_parens` | 包含任意层嵌套括号的、通过表明标识符定义的单个表 | `SingleTable` | `single_table_parens` |
| `single_table`        | 通过表名标识符定义的单个表                       | `SingleTable` | `single_table`        |

#### 关联表（joined table）

| 水杉解析器语义组名称  | 语义组含义                   | 返回值类型     | MySQL 语义组名称      |
| --------------------- | ---------------------------- | -------------- | --------------------- |
| `joined_table`        | 关联表                       | `Table`        | `joined_table`        |
| `joined_table_parens` | 包含大于等于一层括号的关联表 | `Table`        | `joined_table_parens` |
| `natural_join_type`   | 自然连接的关键字             | `EnumJoinType` | `natural_join_type`   |
| `inner_join_type`     | 内连接的关键字               | `EnumJoinType` | `inner_join_type`     |
| `outer_join_type`     | 外关联的关键字               | `EnumJoinType` | `outer_join_type`     |
| `opt_keyword_inner`   | 可选的 `INNER` 关键字        | -              | `opt_inner`           |
| `opt_keyword_outer`   | 可选的 `OUTER` 关键字        | -              | `opt_outer`           |

#### 派生表（derived table）

| 水杉解析器语义组名称 | 语义组含义 | 返回值类型     | MySQL 语义组名称 |
| -------------------- | ---------- | -------------- | ---------------- |
| `derived_table`      | 派生表     | `DerivedTable` | `derived_table`  |

#### 生成表函数（table function）

| 水杉解析器语义组名称        | 语义组含义                           | 返回值类型                  | MySQL 语义组名称 |
| --------------------------- | ------------------------------------ | --------------------------- | ---------------- |
| `json_table_column_type`    | `JSON_TABLE` 函数中的字段类型        | `JsonTableColumnType`       | `jt_column_type` |
| `json_table_column`         | `JSON_TABLE` 函数中的字段            | `JsonTableColumnBase`       | `jt_column`      |
| `json_table_column_list`    | `JSON_TABLE` 函数中的字段的列表      | `List[JsonTableColumnBase]` | `columns_list`   |
| `json_table_columns_clause` | `JSON_TABLE` 函数中的 `COLUMNS` 子句 | `List[JsonTableColumnBase]` | `columns_clause` |
| `table_function`            | 生成表函数                           | `TableFunctionJsonTable`    | `table_function` |

# 表达式（expression）

#### 一般表达式（general expression）

| 水杉解析器语义组名称           | 语义组含义                                       | 返回值类型             | MySQL 语义组名称                                     |
| ------------------------------ | ------------------------------------------------ | ---------------------- | ---------------------------------------------------- |
| `operator_compare`             | 比较运算符                                       | `EnumOperatorCompare`  | `comp_op`                                            |
| `simple_expr`                  | 简单表达式                                       | `Expression`           | `simple_expr`                                        |
| `binary_expr`                  | 二元表达式                                       | `Expression`           | `bit_expr`                                           |
| `predicate_expr`               | 谓语表达式                                       | `Expression`           | `predicate`                                          |
| `bool_expr`                    | 布尔表达式                                       | `Expression`           | `bool_pri`<br />`all_or_any`【包含】                 |
| `expr`                         | 一般表达式                                       | `Expression`           | `expr`<br />`grouping_expr`                          |
| `opt_expr`                     | 可选的一般表达式                                 | `Expression`           | `opt_expr`                                           |
| `opt_paren_expr_list`          | 可选的嵌套括号内可选的逗号分隔的一般表达式列表   | `List[Expression]`     | `opt_paren_expr_list`                                |
| `opt_expr_list`                | 可选的逗号分隔的一般表达式列表                   | `List[Expression]`     | `opt_expr_list`                                      |
| `expr_list`                    | 逗号分隔的一般表达式列表                         | `List[Expression]`     | `expr_list`<br />`group_list`                        |
| `udf_expr`                     | UDF 表达式（自定义函数中的参数）                 | `UdfExpression`        | `udf_expr`                                           |
| `udf_expr_list`                | 逗号分隔的 UDF 表达式的列表                      | `List[UdfExpression]`  | `udf_expr_list`                                      |
| `opt_udf_expr_list`            | 可选的逗号分隔的 UDF 表达式的列表                | `List[UdfExpression]`  | `opt_udf_expr_list`                                  |
| `match_column_list`            | `MATCH` 函数的列名的列表                         | `List[Ident]`          | `ident_list_arg`                                     |
| `opt_in_natural_language_mode` | 全文本索引可选的 `IN NATURAL LANGUAGE MODE` 选项 | `FulltextOption`       | `opt_natural_language_mode`                          |
| `opt_with_query_expansion`     | 全文本索引可选的 `WITH QUERY EXPANSION` 选项     | `FulltextOption`       | `opt_query_expansion`                                |
| `fulltext_options`             | 全文本索引的选项                                 | `FulltextOption`       | `fulltext_options`                                   |
| `opt_keyword_array`            | 可选的 `ARRAY` 关键字                            | `bool`                 | `opt_array_cast`                                     |
| `opt_keyword_interval`         | 可选的 `INTERVAL` 关键字                         | `bool`                 | `opt_interval`                                       |
| `when_list`                    | `CASE` 结构中的 `WHEN` 条件的列表                | `List[WhenItem]`       | `when_list`                                          |
| `opt_else`                     | `CASE` 结构中可选的 `ELSE` 子句                  | `Optional[Expression]` | `opt_else`                                           |
| `opt_expr_or_default_list`     | 可选的一般表达式或 `DEFAULT` 关键字的列表        | `List[Expression]`     | `opt_values`                                         |
| `expr_or_default_list`         | 一般表达式或 `DEFAULT` 关键字的列表              | `List[Expression]`     | `values`                                             |
| `expr_or_default`              | 一般表达式或 `DEFAULT` 关键字                    | `Expression`           | `expr_or_default`                                    |
| `subquery`                     | 子查询表达式                                     | `SubQuery`             | `row_subquery`<br />`table_subquery`<br />`subquery` |
| `opt_default_expr`             | 可选的 `DEFAULT` 关键字引导的表达式              | `Optional[Expression]` | `sp_opt_default`                                     |

#### 聚集函数表达式（sum function expression）

| 水杉解析器语义组名称 | 语义组含义                            | 返回值类型                | MySQL 语义组名称                                             |
| -------------------- | ------------------------------------- | ------------------------- | ------------------------------------------------------------ |
| `sum_expr`           | 聚集函数的表达式                      | `Expression`              | `set_function_specification`<br />`sum_expr`【超集】<br />`grouping_operation`【超集】 |
| `in_sum_expr`        | 聚集函数的参数                        | `Expression`              | `in_sum_expr`                                                |
| `opt_distinct`       | 可选的 `DISTINCT` 关键字              | `bool`                    | `opt_distinct`                                               |
| `opt_separator`      | 可选的 `SEPARATOR` 关键字引导的分隔符 | `Optional[StringLiteral]` | `opt_gconcat_separator`                                      |

#### 窗口函数表达式（window function expression）

| 水杉解析器语义组名称         | 语义组含义                                                   | 返回值类型        | MySQL 语义组名称                                  |
| ---------------------------- | ------------------------------------------------------------ | ----------------- | ------------------------------------------------- |
| `stable_integer`             | 在执行过程中为常量的整数（字面值、参数占位符或用户变量）     | `Param`           | `stable_integer`<br />`param_or_var`【超集】      |
| `opt_from_first_or_last`     | `NTH_VALUE` 窗口函数中的 `FROM FIRST` 子句或 `FROM LAST` 子句 | `FromFirstOrLast` | `opt_from_first_last`                             |
| `opt_null_treatment`         | 窗口函数中指定 NULL 值处理策略的 `RESPECT NULLS` 或 `IGNORE NULLS` 子句 | `NullTreatment`   | `opt_null_treatment`                              |
| `opt_lead_or_lag_info`       | LEAD 和 LAG 窗口函数中偏移量及默认值信息                     | `LeadOrLagInfo`   | `opt_lead_lag_info`<br />`opt_ll_default`【包含】 |
| `window_function_expression` | 窗口函数表达式                                               | `FuncWindowBase`  | `window_func_call`                                |

#### 普通函数表达式（function expression）

包括如下 4 种语义组：

- 关键字函数：函数名称为官方 SQL 2003 关键字，因为函数名是一个官方保留字，所以解析器中需要有专门的语法规则，不会产生任何潜在的冲突。
- 非关键字函数：函数名称为非保留关键字，因为函数名不是官方保留字，所以需要专门的语法规则，以避免与语言的其他部分产生不兼容的问题。一个函数出现在这里，要不是出于对其他 SQL 语法兼容的考虑，要不是出于类型推导的需要。
- 冲突风险函数：函数名称为非保留关键字，因为使用了常规的语法形式且该非保留关键字在文法的其他部分也有使用，所以需要专门的语法规则来处理。
- 常规函数：函数名称不是关键字，通常不会对语言引入副作用。

| 水杉解析器语义组名称  | 语义组含义                                 | 返回值类型           | MySQL 语义组名称                                             |
| --------------------- | ------------------------------------------ | -------------------- | ------------------------------------------------------------ |
| `function_expression` | 函数表达式                                 | `FunctionExpression` | `function_call_keyword`【超集】<br />`function_call_nonkeyword`【超集】<br />`function_call_conflict`【超集】<br />`geometry_function`【超集】<br />`function_call_generic`【超集】 |
| `now_expression`      | `NOW` 关键字及精度                         | `FunctionExpression` | `now`                                                        |
| `date_time_type`      | 时间类型（`DATE`、`TIME` 或者 `DATETIME`） | `DateTimeType`       | `date_time_type`                                             |

#### 运算符表达式（operator expression）

运算符表达式的备选规则均包含在一般表达式的语义组中。

#### 近似表达式（app expression）

在其他特定场景下使用的近似表达式。

# 基础元素（basic）

除 `base` 中的抽象节点外，不继承其他任何节点。

#### 固定的枚举类型（fixed enum）

| 水杉解析器语义组名称           | 语义组类型                                             | 返回值类型                     | MySQL 语义组名称                         |
| ------------------------------ | ------------------------------------------------------ | ------------------------------ | ---------------------------------------- |
| `opt_drop_restrict`            | 可选的 `DROP` 语句中 `RESTRICT` 选项的枚举值           | `EnumDropRestrict`             | `opt_restrict`                           |
| `opt_show_command_type`        | 可选的 `SHOW` 语句命令类型的枚举值                     | `EnumShowCommandType`          | `opt_show_cmd_type`                      |
| `opt_repair_type_list`         | 可选的 `REPAIR` 语句命令类型的枚举值的列表             | `EnumRepairType`               | `opt_mi_repair_types`                    |
| `repair_type_list`             | `REPAIR` 语句命令类型的枚举值的列表                    | `EnumRepairType`               | `mi_repair_types`                        |
| `repair_type`                  | `REPAIR` 语句命令类型的枚举值                          | `EnumRepairType`               | `mi_repair_type`                         |
| `opt_check_type_list`          | 可选的 `CHECK` 语句命令类型的枚举值的列表              | `EnumCheckType`                | `opt_mi_check_types`                     |
| `check_type_list`              | `CHECK` 语句命令类型的枚举值的列表                     | `EnumCheckType`                | `mi_check_types`                         |
| `check_type`                   | `CHECK` 语句命令类型的枚举值                           | `EnumCheckType`                | `mi_check_type`                          |
| `opt_checksum_type`            | 可选的 `CHECKSUM` 语句命令类型的枚举值                 | `EnumChecksumType`             | `opt_checksum_type`                      |
| `opt_profile_type_list`        | 可选的 `SHOW PROFILE` 语句中性能分析指标的枚举值的列表 | `EnumProfileType`              | `opt_profile_defs`                       |
| `profile_type_list`            | `SHOW PROFILE` 语句中性能分析指标的枚举值列表          | `EnumProfileType`              | `profile_defs`                           |
| `profile_type`                 | `SHOW PROFILE` 语句中性能分析指标的枚举值              | `EnumProfileType`              | `profile_def`                            |
| `opt_variable_type`            | 可选的变量类型的枚举值                                 | `EnumVariableType`             | `opt_var_type`                           |
| `install_option_type`          | `INSTALL` 语句的安装选项的枚举值                       | `EnumInstallOptionType`        | `install_option_type`                    |
| `kill_option_type`             | `KILL` 语句的选项的枚举值                              | `EnumKillOptionType`           | `kill_option`                            |
| `lock_option_type`             | `LOCK` 语句的锁定选项的枚举值                          | `EnumLockOptionType`           | `lock_option`                            |
| `opt_open_ssl_type`            | SSL 选项的枚举值                                       | `EnumOpenSslType`              | `opt_ssl`                                |
| `opt_chain_type`               | `CHAIN` 选项的枚举值                                   | `EnumChainType`                | `opt_chain`                              |
| `opt_release_type`             | `RELEASE` 选项的枚举值                                 | `EnumReleaseType`              | `opt_release`                            |
| `resource_group_type`          | 资源组类型的枚举值                                     | `EnumResourceGroupType`        | `resource_group_types`                   |
| `signal_condition_type`        | `SIGNAL` 和 `RESIGNAL` 语句中条件信息项名称的枚举值    | `EnumSignalConditionType`      | `signal_condition_information_item_name` |
| `flush_option_type_list`       | `FLUSH` 语句选项的枚举值的列表                         | `EnumFlushOptionType`          | `flush_options_list`                     |
| `flush_option_type`            | `FLUSH` 语句选项的枚举值                               | `EnumFlushOptionType`          | `flush_option`                           |
| `flush_lock_type`              | `FLUSH` 语句锁定选项的枚举值                           | `EnumFlushLockType`            | `opt_flush_lock`                         |
| `opt_acl_type`                 | 可选的 ACL 类型枚举值                                  | `EnumAclType`                  | `opt_acl_type`                           |
| `opt_join_or_resume`           | XA 事务中的 JOIN/RESUME 选项枚举值                     | `EnumXaJoinOrResume`           | `opt_join_or_resume`                     |
| `opt_suspend`                  | XA 事务中的 SUSPEND 选项枚举值                         | `EnumXaSuspend`                | `opt_suspend`                            |
| `opt_enable_disable`           | 资源组启用 / 禁用状态的枚举值                          | `EnumEnableDisable`            | `opt_resource_group_enable_disable`      |
| `opt_view_check_option`        | 可选的视图检查选项的枚举值                             | `EnumViewCheckOption`          | `view_check_option`                      |
| `opt_event_status_type`        | 可选的事件状态类型的枚举值                             | `EnumEventStatusType`          | `opt_ev_status`                          |
| `handler_type`                 | 处理器类型的枚举值                                     | `EnumHandlerType`              | `sp_handler_type`                        |
| `opt_event_completion_type`    | 可选的事件完成类型的枚举值                             | `EnumEventCompletionType`      | `opt_ev_on_completion`                   |
| `event_completion_type`        | 事件完成类型的枚举值                                   | `EnumEventCompletionType`      | `ev_on_completion`                       |
| `which_area`                   | 诊断区域的枚举值                                       | `EnumDiagnosticsAreaType`      | `which_area`                             |
| `statement_information_type`   | 语句诊断信息项名称的枚举值                             | `EnumStatementInformationType` | `statement_information_item_name`        |
| `condition_information_type`   | 条件诊断信息项名称的枚举值                             | `EnumConditionInformationType` | `condition_information_item_name`        |
| `row_format_type`              | 行格式类型的枚举值                                     | `EnumRowFormatType`            | `row_types`                              |
| `merge_insert_type`            | 向 MERGE 表插入数据的类型的枚举值                      | `EnumMergeInsertType`          | `merge_insert_types`                     |
| `undo_tablespace_state`        | `UNDO TABLESPACE` 状态的枚举值                         | `EnumUndoTablespaceState`      | `undo_tablespace_state`                  |
| `opt_view_algorithm_type`      | 可选的视图算法类型的枚举值                             | `EnumViewAlgorithmType`        |                                          |
| `view_algorithm_type`          | 视图算法类型的枚举值                                   | `EnumViewAlgorithmType`        | `view_algorithm`                         |
| `view_suid_type`               | 视图 SUID 类型的枚举值                                 | `EnumViewSuidType`             | `view_suid`                              |
| `opt_replica_thread_type_list` | 可选的副本线程选项的枚举值的列表                       | `EnumReplicaThreadType`        | `opt_replica_thread_option_list`         |
| `replica_thread_type_list`     | 副本线程选项的枚举值的列表                             | `EnumReplicaThreadType`        | `replica_thread_option_list`             |
| `replica_thread_type`          | 副本线程选项的枚举值                                   | `EnumReplicaThreadType`        | `replica_thread_option`                  |
| `data_or_xml`                  | `LOAD` 语句中数据类型的枚举值                          | `EnumDataType`                 | `data_or_xml`                            |
| `load_data_lock`               | `LOAD` 语句中锁定类型的枚举值                          | `EnumLoadDataLock`             | `load_data_lock`                         |
| `load_source_type`             | `LOAD` 语句中数据源类型的枚举值                        | `EnumLoadSourceType`           | `load_source_type`                       |
| `table_primary_key_check_type` | 表主键检查类型的枚举值                                 | `EnumTablePrimaryKeyCheckType` | `table_primary_key_check_def`            |
| `handler_scan_function`        | `HANDLER` 语句扫描函数的枚举值                         | `EnumHandlerScanFunction`      | `handler_scan_function`                  |
| `handler_rkey_function`        | `HANDLER` 语句索引键函数的枚举值                       | `EnumHandlerRkeyFunction`      | `handler_rkey_function`                  |
| `handler_rkey_mode`            | `HANDLER` 语句索引键模式的枚举值                       | `EnumHandlerRkeyMode`          | `handler_rkey_mode`                      |

#### 固定的词语组合（fixed word）

| 水杉解析器语义组名称                                         | 语义组类型                                                   | 返回值类型 | MySQL 语义组名称                                   |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ---------- | -------------------------------------------------- |
| `opt_keyword_of`                                             | 可选的 `OPT` 关键字                                          | -          | `opt_of`                                           |
| `opt_keyword_all`                                            | 可选的 `ALL` 关键字                                          | `bool`     | `opt_all`<br />`opt_replica_reset_options`         |
| `opt_keyword_into`                                           | 可选的 `INTO` 关键字                                         | -          | `opt_INTO`                                         |
| `opt_keyword_default`                                        | 可选的 `DEFAULT` 关键字                                      | -          | `opt_default`                                      |
| `opt_keyword_storage`                                        | 可选的 `STORAGE` 关键字                                      | -          | `opt_storage`                                      |
| `opt_keyword_temporary`                                      | 可选的 `TEMPORARY` 关键字                                    | `bool`     | `opt_temporary`                                    |
| `opt_keyword_extended`                                       | 可选的 `EXTENDED` 关键字                                     | `bool`     | `opt_extended`                                     |
| `opt_keyword_if_not_exists`                                  | 可选的 `IF NOT EXISTS` 关键字                                | `bool`     | `opt_if_not_exists`                                |
| `opt_keyword_if_exists`                                      | 可选的 `IF EXISTS` 关键字                                    | `bool`     | `if_exists`                                        |
| `opt_keyword_force`                                          | 可选的 `FORCE` 关键字                                        | `bool`     | `opt_force`                                        |
| `opt_keyword_full`                                           | 可选的 `FULL` 关键字                                         | `bool`     | `opt_full`                                         |
| `opt_keyword_work`                                           | 可选的 `WORK` 关键字                                         | `bool`     | `opt_work`                                         |
| `opt_keyword_no_write_to_binlog`                             | 可选的 `NO_WRITE_TO_BINLOG` 关键字或 `LOCAL` 关键字          | `bool`     | `opt_no_write_to_binlog`                           |
| `opt_keyword_table`                                          | 可选的 `TABLE` 关键字                                        | -          | `opt_table`                                        |
| `opt_keyword_savepoint`                                      | 可选的 `SAVEPOINT` 关键字                                    | -          | `opt_savepoint`                                    |
| `opt_keyword_value`                                          | 可选的 `VALUE` 关键字                                        | -          | `opt_value`                                        |
| `opt_keyword_privileges`                                     | 可选的 `PRIVILEGES` 关键字                                   | -          | `opt_privileges`                                   |
| `opt_keyword_with_admin_option`                              | 可选的 `WITH ADMIN OPTION` 关键字组合                        | -          | `opt_with_admin_option`                            |
| `opt_keyword_grant_option`                                   | 可选的 `WITH GRANT OPTION` 关键字组合                        | -          | `grant_options`<br />`opt_grant_option`            |
| `opt_keyword_ignore_unknown_user`                            | 可选的 `IGNORE UNKNOWN USER` 关键字组合                      | -          | `opt_ignore_unknown_user`                          |
| `opt_keyword_convert_xid`                                    | 可选的 `CONVERT XID` 关键字组合                              | `bool`     | `opt_convert_xid`                                  |
| `opt_keyword_one_phase`                                      | 可选的 `ONE PHASE` 关键字组合                                | `bool`     | `opt_one_phase`                                    |
| `opt_keyword_column`                                         | 可选的 `COLUMN` 关键字                                       | -          | `opt_column`                                       |
| `opt_keyword_on_replace`                                     | 可选的 `ON REPLACE` 关键字组合                               | `bool`     | `view_replace`                                     |
| `opt_keyword_from`                                           | 可选的 `FROM` 关键字                                         | -          | `opt_from_keyword`                                 |
| `opt_keyword_local`                                          | 可选的 `LOCAL` 关键字                                        | `bool`     | `opt_local`                                        |
| `opt_keyword_in_primary_key_order`                           | 可选的 `IN PRIMARY KEY ORDER` 关键字组合                     | `bool`     | `opt_source_order`                                 |
| `opt_keyword_and`                                            | 可选的 `AND` 关键字                                          | -          | `opt_and`                                          |
| `keyword_deallocate_or_drop`                                 | `DEALLOCATE` 关键字或 `DROP` 关键字                          | -          | `deallocate_or_drop`                               |
| `keyword_describe_or_explain`                                | `DESCRIBE` 关键字或 `EXPLAIN` 关键字                         | -          | `describe_command`                                 |
| `keyword_table_or_tables`                                    | `TABLE` 关键字或 `TABLES` 关键字                             | -          | `table_or_tables`                                  |
| `keyword_master_or_binary`                                   | `MASTER` 关键字或 `BINARY` 关键字                            | -          | `master_or_binary`                                 |
| `keyword_from_or_in`                                         | `FROM` 关键字或 `IN` 关键字                                  | -          | `from_or_in`                                       |
| `keyword_keys_or_index`                                      | `KEYS`、`INDEX` 或 `INDEXES` 关键字                          | -          | `keys_or_index`                                    |
| `keyword_replica_or_slave`                                   | `REPLICA` 或 `SLAVE` 关键字                                  | -          | `replica`                                          |
| `keyword_master_or_binary_logs_and_gtids`                    | `MASTER` 关键字或 `BINARY LOGS AND GTIDS` 关键字组合         | -          | `master_or_binary_logs_and_gtids`                  |
| `keyword_begin_or_start`                                     | `BEGIN` 关键字或 `START` 关键字                              | -          | `begin_or_start`                                   |
| `keyword_next_from_or_from`                                  | 可选的 `NEXT FROM` 或 `FROM` 关键字（用于 FETCH 语法中的噪声词） | -          | `sp_opt_fetch_noise`                               |
| `keyword_visible_or_invisible`                               | `VISIBLE` 关键字或 `INVISIBLE` 关键字                        | `bool`     | `visibility`                                       |
| `keyword_master_log_file_or_source_log_file`                 | `MASTER_LOG_FILE` 关键字或 `SOURCE_LOG_FILE` 关键字          | -          | `source_log_file`                                  |
| `keyword_master_log_pos_or_source_log_pos`                   | `MASTER_LOG_POS` 关键字或 `SOURCE_LOG_POS` 关键字            | -          | `source_log_pos`                                   |
| `keyword_lines_or_rows`                                      | `LINES` 关键字或 `ROWS` 关键字                               | -          | `lines_or_rows`                                    |
| `keyword_master_auto_position_or_source_auto_position`       | `MASTER_AUTO_POSITION` 关键字或 `SOURCE_AUTO_POSITION` 关键字 | -          | `change_replication_source_auto_position`          |
| `keyword_master_host_or_source_host`                         | `MASTER_HOST` 关键字或 `SOURCE_HOST` 关键字                  | -          | `change_replication_source_host`                   |
| `keyword_master_bind_or_source_bind`                         | `MASTER_BIND` 关键字或 `SOURCE_BIND` 关键字                  | -          | `change_replication_source_bind`                   |
| `change_replication_source_user`                             | `MASTER_USER` 关键字或 `SOURCE_USER` 关键字                  | -          | `change_replication_source_user`                   |
| `keyword_master_password_or_source_password`                 | `MASTER_PASSWORD` 关键字或 `SOURCE_PASSWORD` 关键字          | -          | `change_replication_source_password`               |
| `keyword_master_port_or_source_port`                         | `MASTER_PORT` 关键字或 `SOURCE_PORT` 关键字                  | -          | `change_replication_source_port`                   |
| `keyword_master_connect_retry_or_source_connect_retry`       | `MASTER_CONNECT_RETRY` 关键字或 `SOURCE_CONNECT_RETRY` 关键字 | -          | `change_replication_source_connect_retry`          |
| `keyword_master_retry_count_or_source_retry_count`           | `MASTER_RETRY_COUNT` 关键字或 `SOURCE_RETRY_COUNT` 关键字    | -          | `change_replication_source_retry_count`            |
| `keyword_master_delay_or_source_delay`                       | `MASTER_DELAY` 关键字或 `SOURCE_DELAY` 关键字                | -          | `change_replication_source_delay`                  |
| `keyword_master_ssl_or_source_ssl`                           | `MASTER_SSL` 关键字或 `SOURCE_SSL` 关键字                    | -          | `change_replication_source_ssl`                    |
| `keyword_master_ssl_ca_or_source_ssl_ca`                     | `MASTER_SSL_CA` 关键字或 `SOURCE_SSL_CA` 关键字              | -          | `change_replication_source_ssl_ca`                 |
| `keyword_master_ssl_capath_or_source_ssl_capath`             | `MASTER_SSL_CAPATH` 关键字或 `SOURCE_SSL_CAPATH` 关键字      | -          | `change_replication_source_ssl_capath`             |
| `keyword_master_ssl_cipher_or_source_ssl_cipher`             | `MASTER_SSL_CIPHER` 关键字或 `SOURCE_SSL_CIPHER` 关键字      | -          | `change_replication_source_ssl_cipher`             |
| `keyword_master_ssl_crl_or_source_ssl_crl`                   | `MASTER_SSL_CRL` 关键字或 `SOURCE_SSL_CRL` 关键字            | -          | `change_replication_source_ssl_crl`                |
| `keyword_master_ssl_crlpath_or_source_ssl_crlpath`           | `MASTER_SSL_CRLPATH` 关键字或 `SOURCE_SSL_CRLPATH` 关键字    | -          | `change_replication_source_ssl_crlpath`            |
| `keyword_master_ssl_key_or_source_ssl_key`                   | `MASTER_SSL_KEY` 关键字或 `SOURCE_SSL_KEY` 关键字            | -          | `change_replication_source_ssl_key`                |
| `keyword_master_ssl_verify_server_cert_or_source_ssl_verify_server_cert` | `MASTER_SSL_VERIFY_SERVER_CERT` 关键字或 `SOURCE_SSL_VERIFY_SERVER_CERT` 关键字 | -          | `change_replication_source_ssl_verify_server_cert` |
| `keyword_master_tls_version_or_source_tls_version`           | `MASTER_TLS_VERSION` 关键字或 `SOURCE_TLS_VERSION` 关键字    | -          | `change_replication_source_tls_version`            |
| `keyword_master_tls_ciphersuites_or_source_tls_ciphersuites` | `MASTER_TLS_CIPHERSUITES` 关键字或 `SOURCE_TLS_CIPHERSUITES` 关键字 | -          | `change_replication_source_tls_ciphersuites`       |
| `keyword_master_ssl_cert_or_source_ssl_cert`                 | `MASTER_SSL_CERT` 关键字或 `SOURCE_SSL_CERT` 关键字          | -          | `change_replication_source_ssl_cert`               |
| `keyword_master_public_key_path_or_source_public_key_path`   | `MASTER_PUBLIC_KEY_PATH` 关键字或 `SOURCE_PUBLIC_KEY_PATH` 关键字 | -          | `change_replication_source_public_key`             |
| `keyword_get_master_public_key_or_get_source_public_key`     | `GET_MASTER_PUBLIC_KEY` 关键字或 `GET_SOURCE_PUBLIC_KEY` 关键字 | -          | `change_replication_source_get_source_public_key`  |
| `keyword_master_heartbeat_period_or_source_heartbeat_period` | `MASTER_HEARTBEAT_PERIOD` 关键字或 `SOURCE_HEARTBEAT_PERIOD` 关键字 | -          | `change_replication_source_heartbeat_period`       |
| `keyword_master_compression_algorithm_or_source_compression_algorithm` | `MASTER_COMPRESSION_ALGORITHM` 关键字或 `SOURCE_COMPRESSION_ALGORITHM` 关键字 | -          | `change_replication_source_compression_algorithm`  |
| `keyword_master_zstd_compression_level_or_source_zstd_compression_level` | `MASTER_ZSTD_COMPRESSION_LEVEL` 关键字或 `SOURCE_ZSTD_COMPRESSION_LEVEL` 关键字 | -          | `change_replication_source_zstd_compression_level` |
| `opt_braces`                                                 | 可选的空括号                                                 | -          | `optional_braces`                                  |
| `opt_comma`                                                  | 可选的逗号                                                   | -          | `opt_comma`                                        |
| `keyword_charset`                                            | `CHARSET` 关键字或 `CHAR SET` 关键字                         | -          | `character_set`                                    |
| `keyword_nchar`                                              | `NCHAR` 关键字或 `NATIONAL CHAR` 关键字（兼容的 `NCHAR` 类型名称） | -          | `nchar`                                            |
| `keyword_varchar`                                            | `CHAR VARYING` 关键字或 `VARCHAR` 关键字（兼容的 `VARCHAR` 类型名称） | -          | `varchar`                                          |
| `keyword_nvarchar`                                           | `NVARCHAR` 关键字、`NATIONAL VARCHAR` 关键字、`Ncharacter_setCHAR VARCHAR` 关键字、`NATIONAL CHAR VARYING` 关键字或 `NCHAR VARYING` 关键字（兼容的 `NVARCHAR` 类型名称） | -          | `nvarchar`                                         |
| `opt_equal`                                                  | 可选的 `=` 运算符或 `:=` 运算符                              | -          | `opt_equal`                                        |
| `equal`                                                      | `=` 运算符或 `:=` 运算符                                     | -          | `equal`                                            |
| `opt_to_or_eq_or_as`                                         | `TO` 关键字、`=` 运算符或 `AS` 关键字                        | -          | `opt_to`                                           |

#### 标识符（ident）

| 水杉解析器语义组名称                                   | 语义组类型                                                   | 返回值类型         | MySQL 语义组名称                                             |
| ------------------------------------------------------ | ------------------------------------------------------------ | ------------------ | ------------------------------------------------------------ |
| `ident_sys`                                            | 不是保留字或非保留关键字的标识符                             | `Ident`            | `IDENT_sys`                                                  |
| `ident_keywords_unambiguous`（MySQL）                  | 非保留关键字，可以在任何位置用作未见引号的标识符，而不会引入语法冲突 | `Ident`            | `ident_keywords_unambiguous`                                 |
| `ident_keywords_ambiguous_1_roles_and_labels`（MySQL） | 非保留关键字，不能用作角色名称（role name）和存储过程标签名称（SP label name） | `Ident`            | `ident_keywords_ambiguous_1_roles_and_labels`                |
| `ident_keywords_ambiguous_2_labels`（MySQL）           | 非保留关键字，不能用作存储过程标签名称（SP label name）      | `Ident`            | `ident_keywords_ambiguous_2_labels`                          |
| `ident_keywords_ambiguous_3_roles`（MySQL）            | 非保留关键字，不能用作角色名称（role name）                  | `Ident`            | `ident_keywords_ambiguous_3_roles`                           |
| `ident_keywords_ambiguous_4_system_variables`（MySQL） | 非保留关键字，不能用作 SET 语句中赋值操作左侧的变量名以及变量前缀 | `Ident`            | `ident_keywords_ambiguous_4_system_variables`                |
| `ident_general_keyword`（MySQL）                       | 非保留关键字，在一般场景下可以直接使用                       | `Ident`            | `ident_keyword`                                              |
| `ident_label_keyword`（MySQL）                         | 非保留关键字，可以用作存储过程标签名称（label name）         | `Ident`            | `label_keyword`                                              |
| `ident_role_keyword`（MySQL）                          | 非保留关键字，可以用作角色名称（role name）                  | `Ident`            | `role_keyword`                                               |
| `ident_variable_keyword`（MySQL）                      | 非保留关键字，可以作为 SET 语句中赋值操作左侧的变量名以及变量前缀 | `Ident`            | `lvalue_keyword`                                             |
| `parens_opt_ident_list`                                | 括号框柱的可选的单个标识符（`ident`）的列表                  | `List[str]`        | `opt_filter_db_list`                                         |
| `opt_ident_list`                                       | 可选的单个标识符（`ident`）的列表                            | `List[str]`        | `opt_name_list`                                              |
| `ident_list`                                           | 单个标识符（`ident`）的列表                                  | `List[str]`        | `simple_ident_list`<br />`ident_string_list`<br />`using_list`<br />`reference_list`<br />`name_list`<br />`column_list`<br />`sp_fetch_list`<br />`sp_decl_idents`<br />`filter_db_list` |
| `ident`（MySQL）                                       | 单个标识符（`ident`）                                        | `Ident`            | `ident`<br />`schema`<br />`window_name`<br />`filter_db_ident` |
| `opt_ident_list_parens`                                | 可选的括号嵌套的单个标识符（`ident`）的列表                  | `List[str]`        | `opt_derived_column_list`<br />`opt_ref_list`<br />`opt_column_list` |
| `opt_label_ident`                                      | 可选的 label 标识符                                          | `Optional[str]`    | `sp_opt_label`                                               |
| `label_ident`（MySQL）                                 | 表示存储过程名称的标识符                                     | `Ident`            | `label_ident`                                                |
| `role_ident`（MySQL）                                  | 表示角色的标识符                                             | `Ident`            | `role_ident`                                                 |
| `variable_identifier`                                  | 变量名标识符                                                 | `Identifier`       | `lvalue_variable`                                            |
| `variable_ident`（MySQL）                              | 表示变量名或变量名前缀的标识符                               | `Ident`            | `lvalue_ident`                                               |
| `ident_2`                                              | 点分隔的两个标识符（`ident.ident`）                          | `Ident`            | `simple_ident_q`【部分】                                     |
| `ident_3`                                              | 点分隔的三个标识符（`ident.ident.ident`）                    | `Ident`            | `simple_ident_q`【部分】                                     |
| `opt_identifier_list`                                  | 可选的通用标识符的列表                                       | `List[Identifier]` | `opt_table_list`                                             |
| `identifier_list`                                      | 通用标识符的列表                                             | `List[Identifier]` | `table_list`                                                 |
| `identifier`                                           | 通用标识符（`ident` 或 `ident.ident`）                       | `Identifier`       | `table_ident`<br />`sp_name`                                 |
| `parens_opt_qualified_identifier_list`                 | 括号框柱的可选的完全限定的通用标识符的列表                   | `List[Identifier]` | `opt_filter_table_list`                                      |
| `opt_qualified_identifier_list`                        | 可选的完全限定的通用标识符的列表                             | `List[Identifier]` |                                                              |
| `qualified_identifier_list`                            | 完全限定的通用标识符的列表                                   | `List[Identifier]` | `filter_table_list`                                          |
| `qualified_identifier`                                 | 完全限定的通用标识符（`ident.ident`）                        | `Identifier`       | `filter_table_ident`                                         |
| `identifier_allow_default`                             | 允许 DEFAULT 前缀的标识符（`ident` 或 `ident.ident` 或 `DEFAULT.ident`） | `Identifier`       | `persisted_variable_ident`                                   |
| `table_ident_opt_wild_list`                            | 表标识符及可选的 `.*` 的列表                                 | `List[Identifier]` | `table_alias_ref_list`                                       |
| `table_ident_opt_wild`                                 | 表标识符及可选的 `.*`                                        | `Identifier`       | `table_ident_opt_wild`                                       |
| `opt_wild`                                             | 可选的 `.*`                                                  | -                  | `opt_wild`                                                   |
| `simple_ident`                                         | 通用标识符（`ident` 或 `ident.ident` 或 `ident.ident.ident`） | `Expression`       | `simple_ident`<br />`simple_ident_nospvar`<br />`insert_column` |
| `simple_ident_list`                                    | 逗号分隔的通用通配符的列表                                   | `List[Expression]` | `ident_list`<br />`insert_columns`                           |
| `opt_ident`                                            | 可选的单个标识符                                             | `Optional[str]`    | `opt_existing_window_name`<br />`opt_ident`<br />`ident_or_empty` |

#### 字符集名称（charset）

| 水杉解析器语义组名称 | 语义组含义                               | 返回值类型          | MySQL 语义组名称                                             |
| -------------------- | ---------------------------------------- | ------------------- | ------------------------------------------------------------ |
| `charset_ascii`      | ASCII 相关字符集名称关键字               | `CharsetTypeEnum`   | `ascii`                                                      |
| `charset_unicode`    | UNICODE 相关字符集名称关键字             | `CharsetTypeEnum`   | `unicode`                                                    |
| `charset_name`       | 字符集（排序规则）名称或 `BINARY` 关键字 | `Charset`           | `charset_name`<br />`old_or_new_charset_name`<br />`collation_name` |
| `opt_charset`        | 可选的指定字符集信息                     | `Charset`           | `opt_charset_with_opt_binary`                                |
| `opt_collate`        | 指定比较和排序规则                       | `Optional[Charset]` | `opt_collate`                                                |

#### 字面值（literal）

| 水杉解析器语义组名称               | 语义组含义                                                   | 返回值类型            | MySQL 语义组名称                                             |
| ---------------------------------- | ------------------------------------------------------------ | --------------------- | ------------------------------------------------------------ |
| `parens_opt_text_literal_sys_list` | 括号框柱的可选的字符串字面值的列表                           | `List[str]`           | `opt_filter_string_list`                                     |
| `opt_text_literal_sys_list`        | 可选的字符串字面值的列表                                     | `List[str]`           |                                                              |
| `text_literal_sys_list`            | 字符串字面值的列表                                           | `List[str]`           | `TEXT_STRING_sys_list`<br />`filter_string_list`             |
| `text_literal_or_hex`              | 字符串字面值或十六机制字符串                                 | `str`                 | `TEXT_STRING_hash`                                           |
| `text_literal_sys`                 | 字符串字面值（不包括 Unicode 字符串）                        | `StringLiteral`       | `TEXT_STRING_sys`<br />`TEXT_STRING_literal`<br />`TEXT_STRING_filesystem`<br />`TEXT_STRING_password`<br />`TEXT_STRING_validated`<br />`TEXT_STRING_sys_nonewline`<br />`filter_wild_db_table_string`<br />`json_attribute`<br />`filter_string` |
| `text_literal_sys_or_null`         | 字符串字面值或 `NULL` 关键字                                 | `Optional[str]`       | `source_tls_ciphersuites_def`                                |
| `int_literal`                      | 整数字面值                                                   | `IntLiteral`          | `int64_literal`                                              |
| `int_literal_or_hex`               | 整数字面值或十六进制字面值                                   | `IntLiteral`          | `real_ulong_num`<br />`real_ulonglong_num`                   |
| `paren_int_literal_or_hex`         | 包含外层括号的整数字面值或十六进制字面值                     | `IntLiteral`          | `ws_num_codepoints`                                          |
| `num_literal`                      | 数值字面值（包含整数、浮点数和小数字面值）                   | `NumberLiteral`       | `NUM_literal`<br />`ulonglong_num`                           |
| `opt_num_literal_or_hex_list`      | 可选的数值字面值或十六进制字面值的列表                       | `List[int]`           | `ignore_server_id_list`                                      |
| `num_literal_or_hex_list`          | 数值字面值或十六进制字面值的列表                             | `List[int]`           |                                                              |
| `num_literal_or_hex`               | 数值字面值或十六进制字面值                                   | `NumberLiteral`       | `ulong_num`<br />`ignore_server_id`                          |
| `temporal_literal`                 | 时间字面值                                                   | `TemporalLiteral`     | `temporal_literal`                                           |
| `literal`                          | 非空字面值（包括数值、时间、布尔、真值、假值、十六进制、二进制字面值） | `Literal`             | `literal`                                                    |
| `null_literal`                     | 空值字面值                                                   | `Literal`             | `null_as_literal`                                            |
| `literal_or_null`                  | 可为空字面值                                                 | `Literal`             | `literal_or_null`                                            |
| `text_literal`                     | 字符串字面值                                                 | `StringLiteral`       | `text_literal`                                               |
| `text_string`                      | 字符串、二进制、十六进制字面值                               | `StringLiteral`       | `text_string`                                                |
| `text_string_list`                 | 逗号分隔的字符串、二进制、十六进制字面值的列表               | `List[StringLiteral]` | `string_list`                                                |
| `signed_literal`                   | 非空字面值或有符号的数值字面值                               | `Literal`             | `signed_literal`                                             |
| `signed_literal_or_null`           | 可为空字面值或有符号的数值字面值                             | `Literal`             | `signed_literal_or_null`                                     |
| `ident_or_text`                    | 标识符或字符串字面值表示的名称                               | `Expression`          | `ident_or_text`【部分】                                      |
| `size_number`                      | 磁盘大小的数值                                               | `Expression`          | `size_number`                                                |
| `role_name_list`                   | 角色名称的列表                                               | `List[RoleName]`      | `role_list`                                                  |
| `role_name`                        | 角色名称                                                     | `RoleName`            | `role`                                                       |
| `role_ident_or_text`               | 标识符或字符串字面值表示的角色名                             | `str`                 | `role_ident_or_text`                                         |
| `user_name_list`                   | 用户名称的列表                                               | `List[UserName]`      | `user_list`                                                  |
| `user_name`                        | 用户名称                                                     | `UserName`            | `user`                                                       |
| `explicit_user_name_or_null`       | 用户名称（不匹配 `CURRENT_USER` 关键字）或 `NULL` 关键字     | `Optional[UserName]`  | `privilege_check_def`                                        |
| `explicit_user_name`               | 用户名称（不匹配 `CURRENT_USER` 关键字）                     | `UserName`            | `user_ident_or_text`                                         |

#### 参数（param）

| 水杉解析器语义组名称 | 语义组含义 | 返回值类型 | MySQL 语义组名称 |
| -------------------- | ---------- | ---------- | ---------------- |
| `param_marker`       | 参数占位符 | `Param`    | `param_marker`   |

#### 变量（variable）

| 水杉解析器语义组名称          | 语义组含义                 | 返回值类型               | MySQL 语义组名称                                |
| ----------------------------- | -------------------------- | ------------------------ | ----------------------------------------------- |
| `variable_name`               | 用户变量或系统变量的变量名 | `str`                    | `ident_or_text`                                 |
| `user_variable_list`          | 用户变量的列表             | `List[UserVariable]`     | `execute_var_list`                              |
| `user_variable`               | 用户变量                   | `UserVariable`           | `execute_var_ident`（对应 `'@' ident_or_text`） |
| `user_or_local_variable_list` | 用户变量或本地变量的列表   | `List[Variable]`         | `select_var_list`                               |
| `user_or_local_variable`      | 用户变量或本地变量         | `Variable`               | `select_var_ident`                              |
| `system_variable_type`        | 系统变量类型               | `EnumSystemVariableType` | `opt_rvalue_system_variable_type`               |
| `system_variable`             | 系统变量                   | `SystemVariable`         | `rvalue_system_variable`【包含】                |
| `system_or_user_variable`     | 系统变量或用户变量         | `Variable`               | `rvalue_system_or_user_variable`                |
| `user_variable_assignment`    | 用户变量赋值语句           | `UserVariableAssignment` | `in_expression_user_variable_assignment`        |

#### 时间单位类型（time_unit）

| 水杉解析器语义组名称 | 语义组含义                            | 返回值类型     | MySQL 语义组名称      |
| -------------------- | ------------------------------------- | -------------- | --------------------- |
| `time_unit`          | 时间单位关键字                        | `TimeUnitEnum` | `interval_time_stamp` |
| `interval_time_unit` | 时间单位关键字（INTERVAL 中的关键字） | `TimeUnitEnum` | `interval`            |

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
