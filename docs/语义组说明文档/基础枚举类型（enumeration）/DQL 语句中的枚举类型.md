##### 比较运算符

| 水杉解析器语义组名称 | 语义组含义 | 返回值类型            | MySQL 语义组名称 |
| -------------------- | ---------- | --------------------- | ---------------- |
| `compare_operator`   | 比较运算符 | `EnumCompareOperator` | `comp_op`        |

##### 全文索引的选项

| 水杉解析器语义组名称           | 语义组含义                                     | 返回值类型           | MySQL 语义组名称            |
| ------------------------------ | ---------------------------------------------- | -------------------- | --------------------------- |
| `fulltext_options`             | 全文索引的选项                                 | `EnumFulltextOption` | `fulltext_options`          |
| `opt_in_natural_language_mode` | 全文索引可选的 `IN NATURAL LANGUAGE MODE` 选项 | `EnumFulltextOption` | `opt_natural_language_mode` |
| `opt_with_query_expansion`     | 全文索引可选的 `WITH QUERY EXPANSION` 选项     | `EnumFulltextOption` | `opt_query_expansion`       |
