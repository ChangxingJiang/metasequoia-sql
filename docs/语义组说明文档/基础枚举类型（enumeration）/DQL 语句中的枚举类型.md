##### 比较运算符

| 水杉解析器语义组名称 | 语义组含义 | 返回值类型            | MySQL 语义组名称 |
| -------------------- | ---------- | --------------------- | ---------------- |
| `compare_operator`   | 比较运算符 | `EnumCompareOperator` | `comp_op`        |

##### 全文索引的选项

| 水杉解析器语义组名称           | 语义组含义                                                   | 返回值类型           | MySQL 语义组名称            |
| ------------------------------ | ------------------------------------------------------------ | -------------------- | --------------------------- |
| `fulltext_options`             | 全文索引的选项                                               | `EnumFulltextOption` | `fulltext_options`          |
| `opt_in_natural_language_mode` | 全文索引可选的 `IN NATURAL LANGUAGE MODE` 选项               | `EnumFulltextOption` | `opt_natural_language_mode` |
| `opt_with_query_expansion`     | 全文索引可选的 `WITH QUERY EXPANSION` 选项                   | `EnumFulltextOption` | `opt_query_expansion`       |
| `opt_from_first_or_last`       | `NTH_VALUE` 窗口函数中的 `FROM FIRST` 子句或 `FROM LAST` 子句 | `FromFirstOrLast`    | `opt_from_first_last`       |

##### 窗口函数的窗口方向选项

| 水杉解析器语义组名称     | 语义组含义                                       | 返回值类型                  | MySQL 语义组名称      |
| ------------------------ | ------------------------------------------------ | --------------------------- | --------------------- |
| `opt_from_first_or_last` | `NTH_VALUE` 窗口函数中指定窗口方向的 `FROM` 子句 | `EnumFromFirstOrLastOption` | `opt_from_first_last` |

##### 窗口函数的 NULL 处理选项

| 水杉解析器语义组名称 | 语义组含义                                                   | 返回值类型                | MySQL 语义组名称     |
| -------------------- | ------------------------------------------------------------ | ------------------------- | -------------------- |
| `opt_null_treatment` | 窗口函数中指定 NULL 值处理策略的 `RESPECT NULLS` 或 `IGNORE NULLS` 子句 | `EnumNullTreatmentOption` | `opt_null_treatment` |

##### 排序方向类型

| 水杉解析器语义组名称  | 语义组类型                                  | 返回值类型               | MySQL 语义组名称         |
| --------------------- | ------------------------------------------- | ------------------------ | ------------------------ |
| `opt_order_direction` | 可选的指定排序方向的 `ASC` 或 `DESC` 关键字 | `EnumOrderDirectionType` | `opt_ordering_direction` |
| `order_direction`     | 指定排序方向的 `ASC` 或 `DESC` 关键字       | `EnumOrderDirectionType` | `ordering_direction`     |
