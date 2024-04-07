"""
WITH 语句的 Demo

来自：https://blog.csdn.net/ChinaLiyq/article/details/131940087
"""

WD_01 = """
WITH temp_table AS (
    SELECT column1, column2
    FROM some_table
    WHERE column3 = 'value'
)

SELECT *
FROM temp_table
"""

WD_02 = """
WITH recursive_query AS (
    SELECT start_id, end_id, distance
    FROM some_table
    WHERE start_id = 1
    UNION ALL
    SELECT r.start_id, t.end_id, r.distance + t.distance
    FROM recursive_query r
    JOIN some_table t ON r.end_id = t.start_id
)
SELECT *
FROM recursive_query
"""

WD_03 = """
WITH temp_table1 AS (
    SELECT column1, column2
    FROM some_table
    WHERE column3 = 'value'
), temp_table2 AS (
    SELECT column4, column5
    FROM another_table
    WHERE column6 = 'value'
)
SELECT *
FROM temp_table1
JOIN temp_table2 ON temp_table1.column1 = temp_table2.column4
"""

WD_04 = """
WITH w1 AS (
select name, value from diction where code = 's_model'
), w2 AS (
select name,value from diction where code = 'd_model'
), w3 AS (
select project_name,id from project
)
select w3.project_name, t1.device_name, t1.device_sn, t1.update_time,t1.device_model,t1.device_type from device t1
left join project_device pd on t1.id = pd.device_id
join w3 on w3.id = pd.project_id
where t1.device_type in (1,2);
"""

WD_05 = """
WITH w1 AS (
    SELECT name, value FROM diction WHERE code = 's_model'
)
SELECT w1.name, t1.device_type, t1.device_model
FROM device t1
JOIN w1 ON t1.device_model = w1.value
WHERE t1.device_type = 1;
"""

WD_06 = """
WITH 
    w1 AS (
        SELECT name, value FROM diction WHERE code = 's_model'
    ),
    w2 AS (
        SELECT name, value FROM diction WHERE code = 'd_model'
    )
SELECT w1.name, t1.device_type, t1.device_model
FROM device t1
JOIN w1 ON t1.device_model = w1.value
WHERE t1.device_type = 1
UNION
SELECT w2.name, t1.device_type, t1.device_model
FROM device t1
JOIN w2 ON t1.device_model = w2.value
WHERE t1.device_type = 2;
"""
