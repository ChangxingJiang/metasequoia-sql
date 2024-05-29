# metasequoia-sql

metasequoia-sql 是一款注重性能的 SQL 语法的解析和分析器，适用于 SQL 的格式化、执行和分析场景，致力于打造性能最高的 Python 版 SQL 解析器。具有如下 3 个主要特性：

- 词法解析器与语法解析器相互独立，支持插件开发
- 使用单一状态机实现词法解析，避免大量正则表达式的复杂逻辑
- 除包含并列关系的节点外（例如 `ORDER BY` 多个字段），抽象语法树为完全的、根据计算优先级嵌套的一元和二元表达式结构

metasequoia-sql 包含词法树解析（`lexical` 模块）、语法树解析（`core` 模块）和语法树分析（`analyzer` 模块）等主要功能。

自 0.6.0 版本起，metasequoia-sql 的 public 方法 API 将尽可能支持向前兼容。

## 安装方法

```bash
pip install metasequoia-sql
```

## 使用方法

### 词法解析

单纯的词法解析，可以应用于 SQL 语句格式化等场景。

将 SQL 语句解析为一个词法节点的列表（demo_101），节点中包含对应的源代码（`source` 属性）以及节点标签（`marks` 属性）。

```python
from metasequoia_sql import FSMMachine

amt_tree = FSMMachine.parse("SELECT column1, '2' FROM table_1")
for node in amt_tree:
    print(node)
```

对于有括号的 SQL 语句，会将括号生成一个 `AMTParenthesis` 类型节点，该节点包含一个 `PARENTHESIS`
标记，括号中的词法节点会被添加到括号节点的 `children` 属性中（demo_102）。

```python
from metasequoia_sql import FSMMachine

amt_tree = FSMMachine.parse("SELECT column1, (column2 + 1) * 2 FROM table_1")
for node in amt_tree:
    print(node)
```

### 语法解析

将 SQL 语句解析为一个抽象语法树，返回抽象语法树的根节点。

词法解析支持一次性解析一个语句（demo_201）：

```python
from metasequoia_sql import SQLParser

statement = SQLParser.parse_select_statement("SELECT column1, '2' FROM table_1")
print(statement)
```

也支持一次性解析多个语句（demo_202）：

```python
from metasequoia_sql import SQLParser

statements = SQLParser.parse_statements("SELECT column1 FROM table_1; SELECT column2 FROM table_2")
for statement in statements:
    print(statement)
```

此外，也可以解析语句中的某个部分（demo_203）：

```python
from metasequoia_sql import SQLParser

expression = SQLParser.parse_logical_and_level_expression("(`column1` > 2) AND (`column2` > 1)")
print(expression)
```

### 应用样例：数据血缘分析

通过基于语法解析器的数据血缘分析工具，可以实现对 SQL 语句的分析。例如：

分析 INSERT 语句的数据血缘。数据血缘分析需要依赖元数据，所以需要根据你的数据源继承 `CreateTableStatementGetter`
类并提供给数据血缘分析器（demo_301）：

```python
from metasequoia_sql import *
from metasequoia_sql.analyzer import CreateTableStatementGetter
from metasequoia_sql.analyzer.data_linage.table_lineage_analyzer import TableLineageAnalyzer

table_lineage_analyzer = TableLineageAnalyzer(CreateTableStatementGetter(...))
for statement in SQLParser.parse_statements("your sql file"):
    if isinstance(statement, ASTInsertSelectStatement):
        result = table_lineage_analyzer.get_insert_table_lineage(statement)
```

### 插件样例：MyBatis 插件（暂未完善）

通过重写了语法解析器和词法解析器的插件，可以实现对特殊 SQL 语法的解析。例如：

对 MyBatis 语法进行解析（demo_302）：

```python
from metasequoia_sql.plugins.mybaitis import SQLParserMyBatis

statements = SQLParserMyBatis.parse_statements("SELECT column_1 FROM Shohin "
                                               "WHERE #{column_2} > 500 "
                                               "GROUP BY #{column_3}")
for statement in statements:
    print(statement)
```

### 工具样例：SQL on OTS（暂未发布）

通过基于语法解析器的工具，可以实现一些实现 SQL 执行的工具。

## 性能比较

- 测试样本：4482 个脚本，共 19880057 字节（18.96 MB）的 SQL 语句。
- 测试 Python环境：Python 3.10
- 测试 CPU：Intel(R) Core(TM) i7-10510U CPU @ 1.80GHz

|                 | 解析时间     | 平均解析速度       |
|-----------------|----------|--------------|
| metasequoia-sql | 65.28 秒  | 297.4 KB / s |
| sqlglot         | 182.74 秒 | 106.2 KB / s |

## 基本特性

- 词法解析器与句法解析器分离
- 使用单一、独立的状态机实现词法解析
- 除了逻辑并列的场景外，抽象语法树为完全的嵌套二元表达式

## 参与贡献

单元测试当前不会自动检查）：

运行 `scripts/test/test_main.py` 脚本。如果有新增功能，也需要新增对应的单元测试。

pylint 代码质量检查（在 Pull Request 时自动检查）：

```bash
pylint --max-line-length=120 metasequoia_sql
```

单元测试覆盖率检查（当前不会自动检查）：

```bash
# 将 metasequoia-sql 文件夹添加到 PYTHONPATH，并在 metasequoia-sql 文件夹下执行
coverage run .\scripts\tests\test_main.py
coverage report  # 生成文字报告
coverage html  # 生成 HTML 报告
```

## 版本更新记录

[文档地址](https://github.com/ChangxingJiang/metasequoia-sql/blob/main/docs/%E7%89%88%E6%9C%AC%E6%9B%B4%E6%96%B0%E8%AE%B0%E5%BD%95.md)
