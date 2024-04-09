# sql-tree：SQL 解析器

## 安装方法

```bash
pip install metasequoia-sql
```

## 使用方法

### 词法分析

对 SQL 语句进行句法分析，将 SQL 语句中的每个部分拆分为一个抽象语法树节点（详见 demo_1）：

```python
from metasequoia_sql.ast.functions import parse_as_statements

root = parse_as_statements("your sql")
```

### 句法分析

对 SQL 语句进行语法分析，将 SQL 语句转化为对应可操作的对象（详见 demo_2）：

```python
from metasequoia_sql.parser.common import parse_create_table_statement
from metasequoia_sql.common.token_scanner import build_token_scanner

statement = parse_create_table_statement(build_token_scanner("your sql"))
```

### 翻译工具

将 MySQL 的 CREATE TABLE 语句转换为 Hive 的 CREATE TABLE 语句：

```python
from metasequoia_sql.parser.common import parse_create_table_statement
from metasequoia_sql.translate import *
from metasequoia_sql.common.token_scanner import build_token_scanner

statement = parse_create_table_statement(build_token_scanner("your sql"))
```

## 实现原理

**SQL 解析原理**：将词法分析与句法分析分离，对所有 SQL 语句进行词法分析，然后对不同的 SQL 语句类型使用不同的句法分析方法。

**不同 DataSource 的 SQL 语句转换方法**： 先从特定 DataSource 的 SQL 转化为包含所有数据库特性的 FullStatement，然后再从
FullStatement 转化为另一个 DataSource 的 SQl。通过这样的处理，可以避免开发网状结构的转换器，而只需要开发星星转换器即可。

- `ast`：词法分析（主要使用有限状态自动机实现）
- `common`：遍历器工具
- `objects`：SQL语句对象
- `parser`：SQL语句解析器
- `translate`：翻译器

### 词法分析

字面值类型：[参考文档](https://deepinout.com/mysql/mysql-top-articles-mysql/1694052463_j_mysql-literals.html)

- `ASTLiteralString`：字符串字面值

### 句法分析

#### 节点层级

单项式级别（`SQLMonomial`）：在当前层级，仅包含一个元素或两个相互依存的元素，其中不允许包含任何计算符。但是需要注意的是，函数调用虽然是单项式级别，但它可能包含一个或多个多项式级别的子节点。

- `SQLFunction`：函数调用。包含参数插入语。
- `SQLColumnType`：DDL 中的字段类型，是 `SQLFunction` 的子类。可以是类型名称或函数调用（类型的注释）。因为在其他场景下，类型名称均不允许单独使用，所以在这里额外处理。
- `SQLVariable`：变量引用。不包含插入语。例如 `CURRENT_DATE` 等。
- `SQLLiteral`：字面值。没有依赖的列名。
- 计算运算符
  - `SQLPlus`：
- `SQLCompareOperator`：比较运算符。

- `SQLColumnName`：列名。
- `SQLTableName`：表名。

多项式级别（`SQLPolynomial`）：

- `SQLCaseExpression`：CASE 语句。包含一个完整的 CASE 语句。
- `SQLSimpleExpression`：基础表达式。包含计算运算符的多项式，但在当前层级不包含别名、比较运算符。
- `SQLColumnExpression`：字段表达式。包含计算运算符和别名的多项式，但在当前层级不包含比较运算符。
- `SQLSoloConditionExpression`：单独比较表达式。包含计算运算符和一个比较运算符。
- `SQLMultiConditionExpression`：组合比较表达式。即使用 OR 或 JOIN 进行组合的单独比较表达式。单独比较表达式也是一种组合比较表达式
- `SQLBetweenExpression`：Between 语句。包含一个基础表达式及 BETWEEN ... AND ... 语句。在使用上等价于比较表达式。
- `SQLWindowExpression`：窗口表达式。包含一个完整的窗口语句，但不包含别名。在使用上等价于基础表达式。

子句级别（`SQLClause`）：

- `SQLFromClause`：FROM 子句。包含多个表名和别名的组合。
- `SQLJoinClause`：JOIN 子句。包含一个表名、一个别名，以及一个与它对应的 ON 语句或 USING 函数。
- `SQLWhereClause`：WHERE 子句。包含一个组合比较表达式。
- `SQLGroupByClause`：GROUP BY 子句。包含多个分组字段（基础表达式）。
- `SQLHavingClause`：HAVING 子句。包含一个组合比较表达式。
- `SQLOrderByClause`：ORDER BY 子句。包含多个排序字段（基础表达式）。
- `SQLLimitClause`：LIMIT 子句。包含一个开始位置和一个数量。
- `SQLLateralViewCluatse`：LATERAL VIEW 子句。

语句级别（`SQLStatement`）：

- `SQLCreateTableStatement`：CREATE TABLE 语句
- `SQLSelectStatement`：SELECT 语句

联合级别（`SQLUnion`）：

- `SQLUnionClause`：UNION 语句。包含多个 SELECT 语句。
- `SQLUnionALLClause`：UNION ALL 语句。包含多个 SELECT 语句。

## 已知的不兼容

- DB2 的 `CURRENT DATE` 的语法

## 修改记录

#### 0.1.0 > 0.1.1

新增：
- `INSERT` 语句解析逻辑
- 一次性解析多条 SQL 语句

优化：
- 统一 `CREATE TABLE` 解析逻辑（使用 `TokenScanner`，改造节点对象，改造解析逻辑，改造 Hive 源码生成逻辑）
- 清理多余对象
- TokenScanner 使用方法

修复：
- `WITH` 语句解析报错的 Bug 修复

##### 0.1.0

- 新增 SELECT 语句解析逻辑
- Bug 修复：移除在 Hive 建表语句末尾的分号

##### 0.0.1

- 新增 CREATE TABLE 语句解析逻辑