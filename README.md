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
from metasequoia_sql.parser.mysql_parser import parse_mysql_create_table_statement

statement = parse_mysql_create_table_statement("your sql")
```

### 翻译工具

将 MySQL 的 CREATE TABLE 语句转换为 Hive 的 CREATE TABLE 语句：

```python
from metasequoia_sql.parser.mysql_parser import parse_mysql_create_table_statement
from metasequoia_sql.translate import *

statement = ddl_create_table_statement_to_hive(
    ddl_create_table_statement_from_mysql(parse_mysql_create_table_statement("your sql")))
```

## 实现原理

**SQL 解析原理**：将词法分析与句法分析分离，对所有 SQL 语句进行词法分析，然后对不同的 SQL 语句类型使用不同的句法分析方法。

**不同 DataSource 的 SQL 语句转换方法**： 先从特定 DataSource 的 SQL 转化为包含所有数据库特性的 FullStatement，然后再从
FullStatement 转化为另一个 DataSource 的 SQl。通过这样的处理，可以避免开发网状结构的转换器，而只需要开发星星转换器即可。

## 修改记录

##### 0.0.2

- 词法分析模块
    - 将直接遍历字符串，改为使用 TextScanner 遍历器
    - 将在栈中添加不同元素，该为使用 ASTBuilder 构造中节点
    - 将通过变量维护各个状态并向状态栈中直接添加元素，改为使用 AstParseContext 管理匹配上下文状态
    - 新增等于、计算运算符和比较运算符节点类型
    - 支持包含多个表达式的字符串
- 句法分析模块
    - CREATE TABLE 相关的句法解析节点属性
    - 移除在 Hive 建表语句末尾的分号

##### 0.0.1

- 初始化