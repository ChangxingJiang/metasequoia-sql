引用样例：https://github.com/OctopusLian/SQL-Basic-Tutorial







# 语句层级

在解析 `SELECT` 语句时，我们希望将 `SELECT` 语句整体解析为 `SQLSelectStatement` 类，并支持插入、更新、删除子句的功能。

为了提高各子句在 `UPDATE`、`DELETE` 等语句中的复用性，我们将语句拆分为子句层级的对象。

在设计上，要求：

- 不允许语句层级的对象之间相互引用
- 在语句层级的对象中，只直接引用子句层级的对象

## SELECT（`SQLSelectStatement`）

`SELECT` 表达式，包含 一个 `DISTINCT` 标识，一个 `SELECT` 子句，零个或一个 `FROM` 子句，零个或一个 `JOIN` 子句，零个或一个 `WHERE` 子句，零个或一个 `GROUP BY` 子句，零个或一个 `HAVING` 子句，零个或一个 `ORDER BY` 子句，零个或一个 `LIMIT` 子句。具体如下：

| 属性名             | 类型                         | 含义            |
| ------------------ | ---------------------------- | --------------- |
| `_select_clause`   | `SQLSelectClause`            | `SELECT` 子句   |
| `_from_clause`     | `Optional[SQLFromClause]`    | `FROM` 子句     |
| `_join_clause`     | `Optional[SQLJoinClause]`    | `JOIN` 子句     |
| `_where_clause`    | `Optional[SQLWhereClause]`   | `WHERE` 子句    |
| `_group_by_clause` | `Optional[SQLGroupByClause]` | `GROUP BY` 子句 |
| `_having_clause`   | `Optional[SQLHavingCaluse]`  | `HAVING` 子句   |
| `_order_by_clause` | `Optional[SQLOrderByClause]` | `ORDER BY` 子句 |
| `_limit_clause`    | `Optional[SQLLimitClause]`   | `LIMIT` 子句    |

样例如下：

```sql
SELECT {列表达式}, {列表达式}, {通配符表达式}
FROM {表表达式}, {表表达式}
LEFT JOIN {表表达式} {关联表达式}
WHERE {条件表达式}
GROUP BY {列表达式}, {列表达式}
HAVING {条件表达式}
ORDER BY {列表达式}, {列表达式}
LIMIT {限制记录数} OFFSET {偏移记录数}
```

**TODO**｜支持 `LATERAL VIEW` 子句（`SQLLateralViewCluatse`）

# 子句层级

在不同子句中，有一些内部元素是相同的，为了能够复用这些元素的对象和解析逻辑，我们对每一个子句进行元素拆分，拆分为表达式层级。

在设计上，要求：

- 不允许子句层级的对象之间相互引用
- 在语句层级的对象中，只直接引用表达式层级的对象

各个子句涉及的表达式如下：

| 子句类型           | 列表达式 | 通配符表达式 | 表表达式 | 关联表达式 | 条件表达式 | 一般表达式 |
| ------------------ | -------- | ------------ | -------- | ---------- | ---------- | ---------- |
| `SQLSelectClause`  | 是       | 是           |          |            |            |            |
| `SQLFromClause`    |          |              | 是       |            |            |            |
| `SQLJoinClause`    |          |              | 是       | 是         |            |            |
| `SQLWhereClause`   |          |              |          |            | 是         |            |
| `SQLGroupByClause` |          |              |          |            |            | 是         |
| `SQLHavingClause`  |          |              |          |            | 是         |            |
| `SQLOrderByClause` |          |              |          |            |            | 是         |
| `SQLLimitClause`   |          |              |          |            |            |            |

## `SELECT` 子句（`SQLSelectClause`）

`SELECT` 子句，包含一个或多个有序的列表达式或通配符表达式。具体如下：

| 属性名      | 类型                                                      | 含义                                                         |
| ----------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| `_distinct` | `bool`                                                    | 是否 `DISTINCT` 的布尔值                                     |
| `_columns`  | `List[Union[SQLColumnExpression, SQLWildcardExpression]]` | 每一个 SELECT 的字段（包含别名信息），表表达式或通配符表达式的列表。 |

样例如下：

```sql
SELECT {列表达式}, {列表达式}, {通配符表达式}
```

## `FROM` 子句（`SQLFromClause`）

`FROM` 子句，包含一个或多个有序的表表达式。

| 属性名    | 类型                       | 含义                                   |
| --------- | -------------------------- | -------------------------------------- |
| `_tables` | `List[SQLTableExpression]` | 表名（包含别名信息），表表达式的列表。 |

样例如下：

```sql
FROM {表表达式}, {表表达式}
```

## `JOIN` 子句（`SQLJoinClause`）

`JOIN` 子句，包含关联类型，一个表表达式，一个关联表达式。

| 属性名       | 类型                 | 类型包含元素           |
| ------------ | -------------------- | ---------------------- |
| `_join_type` | `SQLJoinType`        | 关联类型的枚举类       |
| `_table`     | `SQLTableExpression` | 关联表，表表达式。     |
| `_join_rule` | `SQLJoinExpression`  | 关联方法，关联表达式。 |

样例如下：

```sql
{关联类型} JOIN {表表达式} ON {关联表达式}
```

```sql
{关联类型} JOIN {表表达式} {关联表达式(USING)}
```

## `WHERE` 子句（`SQLWhereClause`）

`WHERE` 子句，包含一个条件表达式。

| 属性名       | 类型                     | 含义                                              |
| ------------ | ------------------------ | ------------------------------------------------- |
| `_condition` | `SQLConditionExpression` | 条件表达式，其中包含 `AND`、`OR` 等复杂组合关系。 |

样例如下：

```sql
WHERE {条件表达式}
```

## `GROUP BY` 子句（`SQLGroupByClause`）

`GROUP BY` 子句，包含一个或多个有序的一般表达式。

| 属性名     | 类型                         | 含义             |
| ---------- | ---------------------------- | ---------------- |
| `_columns` | `List[SQLGeneralExpression]` | 一般表达式的列表 |

样例如下：

```sql
GROUP BY {一般表达式}, {一般表达式}
```

## `HAVING` 子句（`SQLHavingClause`）

`HAVING` 子句，包含一个条件表达式。

| 属性名       | 类型                     | 含义                                              |
| ------------ | ------------------------ | ------------------------------------------------- |
| `_condition` | `SQLConditionExpression` | 条件表达式，其中包含 `AND`、`OR` 等复杂组合关系。 |

样例如下：

```sql
HAVING {条件表达式}
```

## `ORDER BY` 子句（`SQLOrderByClause`）

`ORDER BY` 子句，包含一个或多个有序的一般表达式。

| 属性名     | 类型                                  | 含义             |
| ---------- | ------------------------------------- | ---------------- |
| `_columns` | `List[Tuple[SQLGeneralExpression, ]]` | 一般表达式的列表 |

样例如下：

```sql
ORDER BY {一般表达式}, {一般表达式}
```

## `LIMIT` 子句（`SQLLimitClause`）

`LIMIT` 子句，包含限制记录数和偏移记录数。

| 属性名    | 类型  | 含义       |
| --------- | ----- | ---------- |
| `_limit`  | `int` | 限制记录数 |
| `_offset` | `int` | 偏移记录数 |

样例如下：

```sql
LIMIT {限制记录数} OFFSET {偏移记录数}
```

```sql
LIMIT {偏移记录数}, {限制记录数}
```

# 表达式层级

在不同的表达式中，共用的基础元素是相同的，且表达式之间存在互相引用。

在设计上，要求：

- 表达式层级对象之间允许相互引用
- 表达式层级对象可以只能引用表达式层级的对象

在子句层级，共涉及了如下 6 种表达式对象：列表达式、通配符表达式、表表达式、关联表达式、条件表达式、一般表达式。

## 列表达式（`SQLColumnExpression`）

列表达式，仅在 `SELECT` 子句中使用，为 `SELECT` 查找的字段清单，包含一个一般表达式和零个或一个别名表达式。

| 属性名    | 类型                           | 含义       |
| --------- | ------------------------------ | ---------- |
| `_column` | `SQLGeneralExpression`         | 一般表达式 |
| `_alias`  | `Optional[SQLAliasExpression]` | 别名表达式 |

样例如下：

```sql
{一般表达式} AS {别名表达式}
```

```sql
{一般表达式} {别名表达式}
```

```sql
{一般表达式}
```

## 表表达式（`SQLTableExpression`）

表表达式即表名和别名的组合，仅出现在 `FROM` 和 `JOIN` 关键字之后，包含一个一般表达式和零个或一个别名表达式。

| 属性名   | 类型                           | 含义       |
| -------- | ------------------------------ | ---------- |
| `_table` | `SQLTableNameExpression`       | 一般表达式 |
| `_alias` | `Optional[SQLAliasExpression]` | 别名表达式 |

样例如下：

```sql
{表名表达式} AS {别名表达式}
```

```sql
{表名表达式} {别名表达式}
```

```sql
{表名表达式}
```

## 通配符表达式（`SQLWildcardExpression`）

通配符表达式，即 SELECT 子句中使用的 `*`，因为其使用场景与列表达式有明显区别，所以将其拆分出来，其中不会包含其他表达式。

样例如下：

```sql
*
```

## 关联表达式（`SQLJoinExpression`）

关联表达式有两种类型，分别是使用 `ON` 关键字的和使用 `USING` 函数的。这两种关联表达式都继承自关联表达式类，以期实现相同的接口。以上两种表达式类均为 `SQLJoinExpression` 的子类。

### `ON` 关联表达式（`SQLJoinOnExpression`）

| 属性名       | 类型                     | 含义                                              |
| ------------ | ------------------------ | ------------------------------------------------- |
| `_condition` | `SQLConditionExpression` | 条件表达式，其中包含 `AND`、`OR` 等复杂组合关系。 |

样例：

```sql
ON {条件表达式}
```

### `USING` 关联表达式（`SQLJoinUsingExpression`）

| 属性名            | 类型                    | 含义                                        |
| ----------------- | ----------------------- | ------------------------------------------- |
| `_using_function` | `SQLFunctionExpression` | 函数表达式，包含 `USING` 函数和里面的参数。 |

样例：

```sql
{函数表达式}
```

## 条件表达式（`SQLConditionExpression`）

条件表达式，包含在同一个层级下，用 AND 或 OR 条件关联多个布尔表达式。如果存在插入语，则插入语的类型也需要为条件表达式（`SQLConditionExpression`）。

因此，条件表达式中包含的元素仅有条件表达式、布尔表达式、逻辑运算符。

| 属性名      | 类型                                                         | 含义                               |
| ----------- | ------------------------------------------------------------ | ---------------------------------- |
| `_elements` | `List[Union[SQLConditionExpression, SQLBoolExpression, SQLLogicalOperator]]` | 条件表达式、布尔表达式、逻辑运算符 |

样例：

```sql
{布尔表达式} AND ({布尔表达式} OR {布尔表达式})
```

## 别名表达式（`SQLAlisaExpression`）

别名表达式，为字段名或表名的表名的别名部分，即 `AS` 关键字之后的部分， `AS` 关键字可能被省略。其中不会包含其他表达式。

| 属性名  | 类型  | 含义       |
| ------- | ----- | ---------- |
| `_name` | `str` | 别名名称。 |

样例：

```sql
{别名名称}
```

## 布尔值表达式（`SQLBoolExpression`）

布尔值表达式分为两种类型，一种是使用比较运算符的，一种是使用 `BETWEEN ... AND ...` 关键字的。以上两个类均为 `SQLBoolExpression` 的子类。

### 比较运算符布尔值表达式（`SQLBoolCompareExpression`）

使用比较运算符的关联表达式，其中包含一个比较运算符、一个运算符前的表达式和一个运算符后的表达式。

| 属性名      | 类型                   | 含义                           |
| ----------- | ---------------------- | ------------------------------ |
| `_operator` | `SQLCompareOperator`   | 比较运算符                     |
| `_before`   | `SQLGeneralExpression` | 一般表达式。运算符之前的部分。 |
| `_after`    | `SQLGeneralExpression` | 一般表达式。运算符之后的部分。 |

样例：

```sql
{一般表达式} {比较运算符} {一般表达式}
```

### `BETWEEN` 布尔值表达式（`SQLBoolBetweenExpression`）

使用 `BETWEEN ... AND ...` 关键字的关联表达式。包含 `BETWEEN` 关键字和 `AND` 关键字之间的一般表达式，和 `AND` 关键字之后的一般表达式。

| 属性名        | 类型                   | 含义                                              |
| ------------- | ---------------------- | ------------------------------------------------- |
| `_from_value` | `SQLGeneralExpression` | 一般表达式。`BETWEEN` 关键字和 `AND` 关键字之间。 |
| `_to_value`   | `SQLGeneralExpression` | 一般表达式。`AND` 关键字之后。                    |

样例：

```sql
{一般表达式} BETWEEN {一般表达式} TO {一般表达式}
```

## 表名表达式（`SQLTableNameExpression`）

表名表达式，包含一个表名字符串，零个或一个库名字符串。

| 属性名    | 类型            | 含义         |
| --------- | --------------- | ------------ |
| `_schema` | `Optional[str]` | 库名字符串。 |
| `_table`  | `str`           | 表名字符串。 |

样例：

```sql
{库名字符串}.{表名字符串}
```

```sql
{表名字符串}
```

## 一般表达式（`SQLGeneralExpression`）

在关联表达式、条件表达式、布尔值表达式、函数表达式中，均用到了一般表达式。

一般表达式可以是如下表达式的一种：函数表达式、`CASE` 表达式、窗口表达式、计算表达式、列名表达式、字面值。这 6 个类均为 `SQLGeneralExpression` 的子类。

### 计算表达式（`SQLComputeExpression`）

计算表达式是一个多项式，需要通过判断下一个元素是否为计算运算符，来判断自己的解析是否结束。

计算表达式的定义是在同一个层级下，用计算运算符（`+`、`-`、`*`、`/`）和一般表达式组成的语句。

| 属性名      | 类型                                                         | 含义                       |
| ----------- | ------------------------------------------------------------ | -------------------------- |
| `_elements` | `List[Union[SQLGeneralExpression, SQLPlus, SQLSubtract, SQLMultiple, SQLDivide]]` | 一般表达式、加减乘除的列表 |

样例：

```sql
{一般表达式(单项式)} {计算运算符} {一般表达式(单项式)}
```

### `CASE` 表达式（`SQLCaseExpression`）

`CASE` 表达式是一个单项式，能够明确了解当前表达式是否结束，包含多个 `WHEN`、`THEN` 的组合，以及一个 `ELSE` 值。

| 属性名        | 类型                                                      | 含义                          |
| ------------- | --------------------------------------------------------- | ----------------------------- |
| `_cases`      | `List[Tuple[SQLGeneralExpression, SQLGeneralExpression]]` | `WHEN` 和 `THEN` 的组合的列表 |
| `_else_value` | `SQLGeneralExpression`                                    | `ELSE` 值                     |

样例：

```sql
CASE
    WHEN {语句/元素} THEN {语句/元素}
    ELSE {语句/元素}
END
```

### 窗口表达式（`SQLWindowExpression`）

窗口表达式是一个单项式，能够明确了解当前表达式是否结束，包含一个窗口函数、一个 `PARTITION BY` 语句和一个 `ORDER BY` 语句。

| 属性名             | 类型                             | 含义                   |
| ------------------ | -------------------------------- | ---------------------- |
| `_window_function` | `SQLFunctionExpression`          | 窗口函数的函数表达式。 |
| `_partition_by`    | `Optional[SQLGeneralExpression]` | `PARTITION BY` 语句。  |
| `_order_by`        | `Optional[SQLGeneralExpression]` | `ORDER BY` 语句。      |

样例：

```sql
{函数表达式} OVER (PARTITION BY {语句/元素} ORDER BY {语句/元素} BETWEEN {} AND {})
```

### 函数表达式（`SQLFunctionExpression`）

函数表达式是一个单项式，能够明确了解当前表达式是否结束，包含一个函数名，零个、一个或多个函数参数的一般表达式。

| 属性名           | 类型                         | 含义                           |
| ---------------- | ---------------------------- | ------------------------------ |
| `_schema_name`   | `Optional[str]`              | 函数名所属的 schema。          |
| `_function_name` | `str`                        | 函数名字符串。                 |
| `_params`        | `List[SQLGeneralExpression]` | 一般表达式的列表。函数的参数。 |

样例：

```sql
{函数名的schema}.{函数名}({一般表达式}, {一般表达式})
```

```sql
{函数名}({一般表达式}, {一般表达式})
```

### 列名表达式（`SQLColumnNameExpression`）

列名表达式是一个单项式，能够明确了解当前表达式是否结束，包含一个列名字符串，零个或一个表名字符串。

| 属性名    | 类型            | 含义         |
| --------- | --------------- | ------------ |
| `_table`  | `Optional[str]` | 表名字符串。 |
| `_column` | `str`           | 列名字符串。 |

样例：

```sql
{表名字符串}.{列名字符串}
```

```sql
{列名字符串}
```

### 字面值表达式（`SQLLiteralExpression`）

字面值表达式是一个单项式，能够明确了解当前表达式是否结束，包含一个指定类型的字面值。

| 属性名   | 类型         | 含义             |
| -------- | ------------ | ---------------- |
| `_value` | `SQLLiteral` | 制定类型的字面值 |

## 基础元素（Basic Element）

### 计算运算符（`SQLComputeOperator`）

计算运算符，在计算表达式中被使用，具体包含加法运算符、减法运算符、乘法运算符、除法运算符 4 种运算符，这 4 个类均为 `SQLComputeOperator` 的子类。

- `SQLPlus`：加法运算符
- `SQLSubtract`：减法运算符
- `SQLMultiple`：乘法运算符
- `SQLDivide`：除法运算符

### 比较运算符（`SQLCompareOperator`）

比较运算符，在布尔值表达式中被使用，具体包含不等于、小于、小等于、大于、大于等于 5 种运算符，这 5 个类均为 `SQLCompareOperator` 的子类。

- `SQLNotEqualTo`：不等于运算符
- `SQLLessThan`：小于运算符
- `SQLLessThanOrEqual`：小于等于运算符
- `SQLGreaterThan`：大于运算符
- `SQLGreaterThanOrEqual`：大于等于运算符

### 字面值（`SQLLiteral`）

字面值，在字面值表达式中被使用，具体包含整型、浮点型、字符串、十六机制、布尔值、位值、空值，这 7 个类均为 `SQLLiteral` 的子类。

- `SQLLiteralInteger`：整型字面值
- `SQLLiteralFloat`：浮点型字面值
- `SQLLiteralString`：字符串型字面值
- `SQLLiteralHex`：十六进制型字面值
- `SQLLiteralBool`：布尔型字面值
- `SQLLiteralBit`：位值型字面值
- `SQLLiteralNull`：空值的字面值

### 逻辑运算符（`SQLLogicalOperator`）

逻辑运算符，用于连接布尔值表达式，在条件表达式中被使用。具体包含 `AND` 运算符、`OR` 运算符和 `NOT` 运算符，这 3 个类均为 `SQLLogicalOperator` 的子类。

- `SQLAndOperator`：逻辑 `AND` 运算符
- `SQLOrOperator`：逻辑 `OR` 运算符
- `SQLNotOperator`：逻辑 `NOT` 运算符
