# metasequoia-sql

[![pypi Version](https://img.shields.io/pypi/v/metasequoia-sql.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/metasequoia-sql/)
[![Downloads](https://static.pepy.tech/personalized-badge/metasequoia-sql?period=total&units=none&left_color=grey&right_color=orange&left_text=Pip%20Downloads)](https://pepy.tech/project/metasequoia-sql)

水杉 SQL 解析器是一款致力于高性能的纯 Python 版开源 SQL 解析器，适用于语法检查、血缘分析等场景。

- 相较于其他纯 Python 的 SQL 解析器，性能极其优异
- 完美支持 MySQL 8.0 的全部语法，支持常见 Hive 方言
- 类型标注覆盖所有 AST 节点的所有属性
- 采用 Python 版本 YACC 定义 SQL 语法，通过水杉解析器生成器生成解析器代码
- 采用单一状态机实现词法解析
- 支持表达式解析、字段类型等语法元素解析

> 水杉系列解析器致力于打造高性能 Python 版编程语言的解析器，其他作品包括：
>
> - [metasequoia-parser](https://github.com/ChangxingJiang/metasequoia-parser)：解析器生成器
> - [metaequoia-shell](https://github.com/ChangxingJiang/metasequoia-shell)：Shell 解析器
> - [metasequoia-java](https://github.com/ChangxingJiang/metasequoia-java)：Java 解析器

## 安装方法

```bash
pip install metasequoia-sql
```

## 快速开始

将 SQL 语句解析为抽象语法树：

```python
from metasequoia_sql import LexFSM
from metasequoia_sql import parse

ast = parse(LexFSM("SELECT * FROM table_name"))
```

## 性能分析

- 待构造测试集进行测试，计划比较对象：sqlglot

## 参与贡献

提交 Pull Request 和 Issues 即可。

的代码格式化检查命令如下：

```shell
pylint --max-line-length=120 metasequoia_sql metasequoia_sql_grammar
```

如果存在 pylint 检查问题，可使用 /.cursur/template 中的提示词通过 Cursor 进行修复。

## 版本变化

- 1.0.0：重构词法解析和语法解析，将语法解析由 Python 实现的逻辑解析，替换为通过水杉解析器生成器生成。AST 语义组结构调整，不再向前兼容。
- 0.6.0：第一款稳定版本。
