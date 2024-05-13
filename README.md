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

<!--参考文档：https://www.alibabacloud.com/help/zh/maxcompute/user-guide/insert-or-update-data-into-a-table-or-a-static-partition?spm=a2c63.p38356.0.0.637d7109wr3nC3 -->

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

## 版本更新记录

