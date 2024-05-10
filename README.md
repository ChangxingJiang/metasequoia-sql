# metasequoia-sql

SQL 语法解析器，包含词法树解析（`lexical` 模块）、语法树解析（`core` 模块）和语法树分析（`analyzer` 模块）功能。

自 0.6.0 版本起，对外暴露的 API 将支持向前兼容。

## 安装方法

```bash
pip install metasequoia-sql
```

## 使用方法

### 词法树解析

将 SQL 语句解析为一个抽象词法树节点的列表：

```python
from metasequoia_sql import FSMMachine
FSMMachine.parse("your sql")
```

### 语法树解析

将 SQL 语句解析为一个抽象语法树，支持一次性解析多个 SQL 语句，支持解析 SQL 语句中的某个语法元素：

```python
from metasequoia_sql import *

statements = SQLParser.parse_statements("your sql file")
```

### 语法树分析：数据血缘分析

分析 INSERT 语句的数据血缘。数据血缘分析需要依赖元数据，所以需要根据你的数据源继承 `CreateTableStatementGetter` 类并提供给数据血缘分析器。

```python
from metasequoia_sql import *
from metasequoia_sql.analyzer import CreateTableStatementGetter
from metasequoia_sql.analyzer.data_linage.table_lineage_analyzer import TableLineageAnalyzer

table_lineage_analyzer = TableLineageAnalyzer(CreateTableStatementGetter(...))
for statement in SQLParser.parse_statements("your sql file"):
    if isinstance(statement, ASTInsertSelectStatement):
        result = table_lineage_analyzer.get_insert_table_lineage(statement)
```

## 实现原理

将词法分析与句法分析分离，先对解析 SQL 语句生成抽象词法树，然后解析抽象词法树生成抽象语法树。

在词法分析中，使用有限状态自动机进行解析。

在语法分析中，根据语法结构确定可能得元素类型后进行解析。

## 参与贡献

### 已知问题

- MySQL 中，使用连续的 `!` 符号的场景

参考文档：https://www.alibabacloud.com/help/zh/maxcompute/user-guide/insert-or-update-data-into-a-table-or-a-static-partition?spm=a2c63.p38356.0.0.637d7109wr3nC3

### 提交前自检

pylint 检查：在 Pull Request 时会自动执行检查。

```bash
pylint --max-line-length=120 metasequoia_sql
```

单元测试覆盖率检查：

```bash
# 将 metasequoia-sql 文件夹添加到 PYTHONPATH，并在 metasequoia-sql 文件夹下执行
coverage run .\scripts\tests\test_main.py
coverage report  # 生成文字报告
coverage html  # 生成 HTML 报告
```

## 修改记录

#### 0.3.0 > 0.4.0

新增：

- 分析器框架 & 基本分析器 & 数据血缘分析器
- 插件框架 & MyBatis 插件

优化：

- 优化词法分析节点，调整模块名，调整文件结构，将节点改为不可变
- 统一标识符引号的相关逻辑
- 兼容建表语句的索引包含 `COMMENT`、`KEY_BLOCK_SIZE` 的逻辑
- 兼容建表语句的外键中包含 `ON DELETE CASCADE` 的逻辑
- 兼容 Hive 建表语句

修复：

- 无法解析 MySQL 建表语句索引使用 USING 子句的 Bug
- 在 `INSERT INTO` 语句中未指定列报错的 Bug
- 各种原因导致解析后的 SQL 与原始 SQL 不一致的 Bug

#### 0.2.0 > 0.3.0

新增：

- 重构词法解析和语法解析以支持插件开发
- SET 语句的解析逻辑
- LATERAL VIEW 子句的解析逻辑

优化：

- core.objects 将语法节点重构为 dataclasses 类型
- 含 WITH 表达式的上游表解析逻辑
- core.parser 中的方法兼容字符串类型的 TokenScanner 类型
- 整理单元测试逻辑
- 代码质量提升
- core.objects 中将 get_used_column_list 和 get_used_table_list 改为抽象方法
- 支持 DB2 的 CURRENT DATE、CURRENT TIME、CURRENT TIMESTAMP 语法
- 增加 TokenScanner 未解析完成的发现机制
- 支持窗口函数的 ROWS 子句

#### 0.1.0 > 0.2.0

新增：

- `INSERT` 语句解析逻辑
- 一次性解析多条 SQL 语句

优化：

- 统一 `CREATE TABLE` 解析逻辑（使用 `TokenScanner`，改造节点对象，改造解析逻辑，改造 Hive 源码生成逻辑）
- 整理 objects 的节点和 parse 中的方法，清理多余对象，优化引用路径
- 统一 TokenScanner 使用方法

修复：

- `WITH` 语句解析报错的 Bug 修复
- Hive 建表语句的类型包含参数的 Bug 修复

##### 0.1.0

- 新增 SELECT 语句解析逻辑
- Bug 修复：移除在 Hive 建表语句末尾的分号

##### 0.0.1

- 新增 CREATE TABLE 语句解析逻辑