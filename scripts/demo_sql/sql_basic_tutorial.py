"""
引用来自 https://github.com/OctopusLian/SQL-Basic-Tutorial 仓库的样例 SQL，在该仓库中，对样例 SQL 的描述如下：

《SQL基础教程》：仓库代码源于《SQL基础教程》上的代码和课后练习
├── Ch01 //数据库和SQL
├── Ch02  //查询基础
├── Ch03  //聚合与排序
├── Ch04  //数据更新
├── Ch05  //复杂查询
├── Ch06  //函数、谓词、CASE表达式
├── Ch07  //集合运算
└── Ch08  //SQL高级处理
"""

SBT_CH01_01 = """
CREATE DATABASE Shop;
"""

SBT_CH01_02 = """
CREATE TABLE Shohin
(shohin_id     CHAR(4)      NOT NULL,
 shohin_mei    VARCHAR(100) NOT NULL,
 shohin_bunrui VARCHAR(32)  NOT NULL,
 hanbai_tanka  INTEGER ,
 shiire_tanka  INTEGER ,
 torokubi      DATE ,
 PRIMARY KEY (shohin_id));
"""

SBT_CH01_03 = """
DROP TABLE Shohin;
"""

SBT_CH01_04_POSTGRESQL = """
ALTER TABLE Shohin ADD COLUMN shohin_mei_kana VARCHAR(100);
"""

SBT_CH01_04_ORACLE = """
ALTER TABLE Shohin ADD (shohin_mei_kana VARCHAR2(100));
"""

SBT_CH01_04_SQLSERVER = """
ALTER TABLE Shohin ADD shohin_mei_kana VARCHAR(100);
"""

SBT_CH01_05_ORACLE = """
ALTER TABLE Shohin DROP (shohin_mei_kana);
"""

SBT_CH01_05_SQLSERVER = """
ALTER TABLE Shohin DROP COLUMN shohin_mei_kana;
"""

SBT_CH01_06_MYSQL = """
START TRANSACTION;

INSERT INTO Shohin VALUES ('0001', 'T恤' ,'衣服', 1000, 500, '2009-09-20');
INSERT INTO Shohin VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11');
INSERT INTO Shohin VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL);
INSERT INTO Shohin VALUES ('0004', '菜刀', '厨房用具', 3000, 2800, '2009-09-20');
INSERT INTO Shohin VALUES ('0005', '高压锅', '厨房用具', 6800, 5000, '2009-01-15');
INSERT INTO Shohin VALUES ('0006', '叉子', '厨房用具', 500, NULL, '2009-09-20');
INSERT INTO Shohin VALUES ('0007', '擦菜板', '厨房用具', 880, 790, '2008-04-28');
INSERT INTO Shohin VALUES ('0008', '圆珠笔', '办公用品', 100, NULL, '2009-11-11');

COMMIT;
"""

SBT_CH01_06_ORACLE = """
INSERT INTO Shohin VALUES ('0001', 'T恤' ,'衣服', 1000, 500, '2009-09-20');
INSERT INTO Shohin VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11');
INSERT INTO Shohin VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL);
INSERT INTO Shohin VALUES ('0004', '菜刀', '厨房用具', 3000, 2800, '2009-09-20');
INSERT INTO Shohin VALUES ('0005', '高压锅', '厨房用具', 6800, 5000, '2009-01-15');
INSERT INTO Shohin VALUES ('0006', '叉子', '厨房用具', 500, NULL, '2009-09-20');
INSERT INTO Shohin VALUES ('0007', '擦菜板', '厨房用具', 880, 790, '2008-04-28');
INSERT INTO Shohin VALUES ('0008', '圆珠笔', '办公用品', 100, NULL, '2009-11-11');

COMMIT;
"""

SBT_CH01_06_SQLSERVER = """
BEGIN TRANSACTION;

INSERT INTO Shohin VALUES ('0001', 'T恤' ,'衣服', 1000, 500, '2009-09-20');
INSERT INTO Shohin VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11');
INSERT INTO Shohin VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL);
INSERT INTO Shohin VALUES ('0004', '菜刀', '厨房用具', 3000, 2800, '2009-09-20');
INSERT INTO Shohin VALUES ('0005', '高压锅', '厨房用具', 6800, 5000, '2009-01-15');
INSERT INTO Shohin VALUES ('0006', '叉子', '厨房用具', 500, NULL, '2009-09-20');
INSERT INTO Shohin VALUES ('0007', '擦菜板', '厨房用具', 880, 790, '2008-04-28');
INSERT INTO Shohin VALUES ('0008', '圆珠笔', '办公用品', 100, NULL, '2009-11-11');

COMMIT;
"""

SBT_CH01_07_DB2 = """
RENAME TABLE Sohin TO Shohin;
"""

SBT_CH01_07_MYSQL = """
RENAME TABLE Sohin to Shohin;
"""

SBT_CH01_A_ORACLE = """
ALTER TABLE Sohin RENAME TO Shohin;
"""

SBT_CH01_A_T4_SQLSERVER = """
sp_rename 'Sohin', 'Shohin';
"""

SBT_CH02_01 = """
SELECT shohin_id, shohin_mei, shiire_tanka
  FROM Shohin;
"""

SBT_CH02_02 = """
SELECT *
  FROM Shohin;
"""

SBT_CH02_03 = """
SELECT shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka,
       shiire_tanka, torokubi
  FROM Shohin;
"""

SBT_CH02_04 = """
SELECT shohin_id    AS id,
       shohin_mei   AS namae,
       shiire_tanka AS tanka
  FROM Shohin;
"""

SBT_CH02_05 = """
SELECT shohin_id    AS "商品编号",
       shohin_mei   AS "商品名称",
       shiire_tanka AS "进货单价"
  FROM Shohin;
"""

SBT_CH02_06 = """
SELECT '商品' AS mojiretsu, 38 AS kazu, '2009-02-24' AS hizuke,
       shohin_id, shohin_mei
  FROM Shohin;
"""

SBT_CH02_07 = """
SELECT DISTINCT shohin_bunrui
  FROM Shohin;
"""

SBT_CH02_08 = """
SELECT DISTINCT shiire_tanka
  FROM Shohin;
"""

SBT_CH02_09 = """
SELECT DISTINCT shohin_bunrui, torokubi
  FROM Shohin;
"""

SBT_CH02_10 = """
SELECT shohin_mei, shohin_bunrui
  FROM Shohin
 WHERE shohin_bunrui = '衣服';
"""

SBT_CH02_11 = """
SELECT shohin_mei
  FROM Shohin
 WHERE shohin_bunrui = '衣服';
"""

SBT_CH02_13 = """
-- 本SELECT语句会从结果中删除重复行。
SELECT DISTINCT shohin_id, shiire_tanka
  FROM Shohin;
"""

SBT_CH02_14 = """
/* 本SELECT语句，
   会从结果中删除重复行。*/
SELECT DISTINCT shohin_id, shiire_tanka
  FROM Shohin;
"""

SBT_CH02_15 = """
SELECT DISTINCT shohin_id, shiire_tanka
-- 本SELECT语句会从结果中删除重复行。
  FROM Shohin;
"""

SBT_CH02_16 = """
SELECT DISTINCT shohin_id, shiire_tanka
/* 本SELECT语句,
   会从结果中删除重复行。*/
  FROM Shohin;
"""

SBT_CH02_17 = """
SELECT shohin_mei, hanbai_tanka,
       hanbai_tanka * 2 AS "hanbai_tanka_x2"
  FROM Shohin;
"""

SBT_CH02_18 = """
SELECT shohin_mei, shohin_bunrui
  FROM Shohin
 WHERE hanbai_tanka = 500;
"""

SBT_CH02_19 = """
SELECT shohin_mei, shohin_bunrui
  FROM Shohin
 WHERE hanbai_tanka <> 500;
"""

SBT_CH02_20 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka
  FROM Shohin
 WHERE hanbai_tanka >= 1000;
"""

SBT_CH02_21 = """
SELECT shohin_mei, shohin_bunrui, torokubi
  FROM Shohin
 WHERE torokubi < '2009-09-27';
"""

SBT_CH02_22 = """
SELECT shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
 WHERE hanbai_tanka - shiire_tanka >= 500;
"""

SBT_CH02_23_MYSQL = """
-- DDL：创建表
CREATE TABLE Chars
(chr CHAR(3) NOT NULL,
PRIMARY KEY (chr));

-- DML：插入数据
START TRANSACTION;

INSERT INTO Chars VALUES ('1');
INSERT INTO Chars VALUES ('2');
INSERT INTO Chars VALUES ('3');
INSERT INTO Chars VALUES ('10');
INSERT INTO Chars VALUES ('11');
INSERT INTO Chars VALUES ('222');

COMMIT;
"""

SBT_CH02_23_ORACLE = """
-- DDL：创建表
CREATE TABLE Chars
(chr CHAR(3) NOT NULL,
PRIMARY KEY (chr));

-- DML：插入数据

INSERT INTO Chars VALUES ('1');
INSERT INTO Chars VALUES ('2');
INSERT INTO Chars VALUES ('3');
INSERT INTO Chars VALUES ('10');
INSERT INTO Chars VALUES ('11');
INSERT INTO Chars VALUES ('222');

COMMIT;
"""

SBT_CH02_23_SQLSERVER = """
-- DDL：创建表
CREATE TABLE Chars
(chr CHAR(3) NOT NULL,
PRIMARY KEY (chr));

-- DML：插入数据
BEGIN TRANSACTION;

INSERT INTO Chars VALUES ('1');
INSERT INTO Chars VALUES ('2');
INSERT INTO Chars VALUES ('3');
INSERT INTO Chars VALUES ('10');
INSERT INTO Chars VALUES ('11');
INSERT INTO Chars VALUES ('222');

COMMIT;
"""

SBT_CH02_24 = """
SELECT chr
  FROM Chars
 WHERE chr > '2';
"""

SBT_CH02_25 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka = 2800;
"""

SBT_CH02_26 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka <> 2800;
"""

SBT_CH02_27 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka = NULL;
"""

SBT_CH02_28 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka IS NULL;
"""

SBT_CH02_29 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka IS NOT NULL;
"""

SBT_CH02_A_DB2 = """
SELECT (100 + 200) * 3 AS keisan FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH02_A_ORACLE = """
SELECT (100 + 200) * 3 AS keisan FROM DUAL;
"""

SBT_CH02_A_SQLSERVER = """
SELECT (100 + 200) * 3 AS keisan;
"""

SBT_CH02_30 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka
  FROM Shohin
 WHERE hanbai_tanka >= 1000;
"""

SBT_CH02_31 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka
  FROM Shohin
 WHERE NOT hanbai_tanka >= 1000;
"""

SBT_CH02_32 = """
SELECT shohin_mei, shohin_bunrui
  FROM Shohin
 WHERE hanbai_tanka < 1000;
"""

SBT_CH02_33 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shohin_bunrui = '厨房用具'
   AND hanbai_tanka >= 3000;
"""

SBT_CH02_34 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shohin_bunrui = '厨房用具'
    OR hanbai_tanka >= 3000;
"""

SBT_CH02_35 = """
SELECT shohin_mei, shohin_bunrui, torokubi
  FROM Shohin
 WHERE shohin_bunrui = '办公用品'
   AND torokubi = '2009-09-11'
    OR torokubi = '2009-09-20';
"""

SBT_CH02_36 = """
SELECT shohin_mei, shohin_bunrui, torokubi
  FROM Shohin
 WHERE shohin_bunrui = '办公用品'
   AND (   torokubi = '2009-09-11'
        OR torokubi = '2009-09-20');
"""

SBT_CH03_01 = """
SELECT COUNT(*)
  FROM Shohin;
"""

SBT_CH03_02 = """
SELECT COUNT(shiire_tanka)
  FROM Shohin;
"""

SBT_CH03_03 = """
CREATE TABLE NullTbl
(col_1 INTEGER);

INSERT INTO NullTbl VALUES (NULL);
INSERT INTO NullTbl VALUES (NULL);
INSERT INTO NullTbl VALUES (NULL);

SELECT COUNT(*), COUNT(col_1)
  FROM NullTbl;
"""

SBT_CH03_04 = """
SELECT SUM(hanbai_tanka)
  FROM Shohin;
"""

SBT_CH03_05 = """
SELECT SUM(hanbai_tanka), SUM(shiire_tanka)
  FROM Shohin;
"""

SBT_CH03_06 = """
SELECT AVG(hanbai_tanka)
  FROM Shohin;
"""

SBT_CH03_07 = """
SELECT AVG(hanbai_tanka), AVG(shiire_tanka)
  FROM Shohin;
"""

SBT_CH03_08 = """
SELECT MAX(hanbai_tanka), MIN(shiire_tanka)
  FROM Shohin;
"""

SBT_CH03_09 = """
SELECT MAX(torokubi), MIN(torokubi)
  FROM Shohin;
"""

SBT_CH03_10 = """
SELECT COUNT(DISTINCT shohin_bunrui)
  FROM Shohin;
"""

SBT_CH03_11 = """
SELECT DISTINCT COUNT(shohin_bunrui)
  FROM Shohin;
"""

SBT_CH03_12 = """
SELECT SUM(hanbai_tanka), SUM(DISTINCT hanbai_tanka)
  FROM Shohin;
"""

SBT_CH03_13 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH03_14 = """
SELECT shiire_tanka, COUNT(*)
  FROM Shohin
 GROUP BY shiire_tanka;
"""

SBT_CH03_15 = """
SELECT shiire_tanka, COUNT(*)
  FROM Shohin
 WHERE shohin_bunrui = '衣服'
 GROUP BY shiire_tanka;
"""

SBT_CH03_16 = """
SELECT shohin_mei, shiire_tanka, COUNT(*)
  FROM Shohin
 GROUP BY shiire_tanka;
"""

SBT_CH03_17 = """
SELECT shohin_bunrui AS sb, COUNT(*)
  FROM Shohin
 GROUP BY sb;
"""

SBT_CH03_18 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH03_19 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 WHERE COUNT(*) = 2
 GROUP BY shohin_bunrui;
"""

SBT_CH03_A_1 = """
-- 使用DISTINCT的情况
SELECT DISTINCT shohin_bunrui
  FROM Shohin;
"""

SBT_CH03_A_2 = """
-- 使用GROUP BY的情况
SELECT shohin_bunrui
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH03_20 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui
HAVING COUNT(*) = 2;
"""

SBT_CH03_21 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH03_22 = """
SELECT shohin_bunrui, AVG(hanbai_tanka)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH03_23 = """
SELECT shohin_bunrui, AVG(hanbai_tanka)
  FROM Shohin
 GROUP BY shohin_bunrui
HAVING AVG(hanbai_tanka) >= 2500;
"""

SBT_CH03_24 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui
HAVING shohin_mei = '圆珠笔';
"""

SBT_CH03_25 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui
HAVING shohin_bunrui = '衣服';
"""

SBT_CH03_26 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
WHERE shohin_bunrui = '衣服'
 GROUP BY shohin_bunrui;
"""

SBT_CH03_27 = """
SELECT shohin_id, shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin;
"""

SBT_CH03_28 = """
SELECT shohin_id, shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
ORDER BY hanbai_tanka;
"""

SBT_CH03_29 = """
SELECT shohin_id, shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
ORDER BY hanbai_tanka DESC;
"""

SBT_CH03_30 = """
SELECT shohin_id, shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
ORDER BY hanbai_tanka, shohin_id;
"""

SBT_CH03_31 = """
SELECT shohin_id, shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
ORDER BY shiire_tanka;
"""

SBT_CH03_32 = """
SELECT shohin_id AS id, shohin_mei, hanbai_tanka AS ht, shiire_tanka
  FROM Shohin
ORDER BY ht, id;
"""

SBT_CH03_33 = """
SELECT shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
ORDER BY shohin_id;
"""

SBT_CH03_34 = """
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui
ORDER BY COUNT(*);
"""

SBT_CH03_35_1 = """
-- 通过列明指定
SELECT shohin_id, shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
ORDER BY hanbai_tanka DESC, shohin_id;
"""

SBT_CH03_35_2 = """
-- 通过列编号指定
SELECT shohin_id, shohin_mei, hanbai_tanka, shiire_tanka
  FROM Shohin
ORDER BY 3 DESC, 1;
"""

SBT_CH04_01 = """
CREATE TABLE ShohinIns
(shohin_id     CHAR(4)      NOT NULL,
 shohin_mei    VARCHAR(100) NOT NULL,
 shohin_bunrui VARCHAR(32)  NOT NULL,
 hanbai_tanka  INTEGER      DEFAULT 0,
 shiire_tanka  INTEGER      ,
 torokubi      DATE         ,
 PRIMARY KEY (shohin_id));
"""

SBT_CH04_02 = """
INSERT INTO ShohinIns (shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi) VALUES ('0001', 'T恤' ,'衣服', 1000, 500, '2009-09-20');
"""

SBT_CH04_03_1 = """
-- 使用列清单
INSERT INTO ShohinIns (shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi) VALUES ('0005', '高压锅', '厨房用具', 6800, 5000, '2009-01-15');
"""

SBT_CH04_03_2 = """
-- 不使用列清单
INSERT INTO ShohinIns VALUES ('0005', '高压锅', '厨房用具', 6800, 5000, '2009-01-15');
"""

SBT_CH04_04 = """
INSERT INTO ShohinIns (shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi) VALUES ('0006', '叉子', '厨房用具', 500, NULL, '2009-09-20');
"""

SBT_CH04_06 = """
INSERT INTO ShohinIns (shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi) VALUES ('0007', '擦菜板', '厨房用具', DEFAULT, 790, '2009-04-28');
"""

SBT_CH04_07 = """
INSERT INTO ShohinIns (shohin_id, shohin_mei, shohin_bunrui, shiire_tanka, torokubi) VALUES ('0007', '擦菜板', '厨房用具', 790, '2009-04-28');
"""

SBT_CH04_08_1 = """
-- 省略shiire_tanka列（无约束）：默认插入NULL
INSERT INTO ShohinIns (shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, torokubi) VALUES ('0008', '圆珠笔', '办公用品', 100, '2009-11-11');
"""

SBT_CH04_08_2 = """
-- 省略shohin_mei列（NOT NULL约束）：错误
INSERT INTO ShohinIns (shohin_id, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi) VALUES ('0009', '办公用品', 1000, 500, '2009-12-12');
"""

SBT_CH04_09 = """
-- 插入数据用的复制商品表
CREATE TABLE ShohinCopy
(shohin_id     CHAR(4)      NOT NULL,
 shohin_mei    VARCHAR(100) NOT NULL,
 shohin_bunrui VARCHAR(32)  NOT NULL,
 hanbai_tanka  INTEGER      ,
 shiire_tanka  INTEGER      ,
 torokubi      DATE         ,
 PRIMARY KEY (shohin_id));
"""

SBT_CH04_10 = """
-- 将商品表中的数据复制到复制商品表中
INSERT INTO ShohinCopy (shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi)
SELECT shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi
  FROM Shohin;
"""

SBT_CH04_11 = """
-- 根据商品种类进行汇总用表
CREATE TABLE ShohinBunrui
(shohin_bunrui VARCHAR(32)  NOT NULL,
 sum_hanbai_tanka  INTEGER      ,
 sum_shiire_tanka  INTEGER      ,
 PRIMARY KEY (shohin_bunrui));
"""

SBT_CH04_12 = """
INSERT INTO ShohinBunrui (shohin_bunrui, sum_hanbai_tanka, sum_shiire_tanka)
SELECT shohin_bunrui, SUM(hanbai_tanka), SUM(shiire_tanka)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH04_A_ORACLE = """
-- Oracle中的多行INSERT
INSERT ALL INTO ShohinIns VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11')
           INTO ShohinIns VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL)
           INTO ShohinIns VALUES ('0004', '菜刀', '厨房用具', 3000, 2800, '2009-09-20')
SELECT * FROM DUAL;
"""

SBT_CH04_A_SQLSERVER = """
-- 多行INSERT（Oracle之外）
INSERT INTO ShohinIns VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11'),
                             ('0003', '运动T恤', '衣服', 4000, 2800, NULL),
                             ('0004', '菜刀', '厨房用具', 3000, 2800, '2009-09-20');
"""

SBT_CH04_13 = """
DELETE FROM Shohin;
"""

SBT_CH04_14 = """
DELETE FROM Shohin
 WHERE hanbai_tanka >= 4000;
"""

SBT_CH04_15 = """
UPDATE Shohin
   SET torokubi = '2009-10-10';
"""

SBT_CH04_16 = """
UPDATE Shohin
   SET hanbai_tanka = hanbai_tanka * 10
 WHERE shohin_bunrui = '厨房用具';
"""

SBT_CH04_17 = """
UPDATE Shohin
   SET torokubi = NULL
 WHERE shohin_id = '0008';
"""

SBT_CH04_18_1 = """
-- 1次UPDATE只更新1列
UPDATE Shohin
   SET hanbai_tanka = hanbai_tanka * 10
 WHERE shohin_bunrui = '厨房用具';
"""

SBT_CH04_18_2 = """
UPDATE Shohin
   SET shiire_tanka = shiire_tanka / 2
 WHERE shohin_bunrui = '厨房用具';
"""

SBT_CH04_19 = """
-- 使用逗号对列进行分隔排列
UPDATE Shohin
   SET hanbai_tanka = hanbai_tanka * 10,
       shiire_tanka = shiire_tanka / 2
 WHERE shohin_bunrui = '厨房用具';
"""

SBT_CH04_20 = """
-- 将列用小括号括起来的列表形式
UPDATE Shohin
   SET (hanbai_tanka, shiire_tanka) = (hanbai_tanka * 10, shiire_tanka / 2)
 WHERE shohin_bunrui = '厨房用具';
"""

SBT_CH04_21_MYSQL = """
START TRANSACTION;

    -- 运动T恤的销售单价下调1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka - 1000
     WHERE shohin_mei = '运动T恤';

    -- T恤的销售单价上浮1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka + 1000
     WHERE shohin_mei = 'T恤';

COMMIT;
"""

SBT_CH04_21_ORACLE = """
    -- 运动T恤的销售单价下调1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka - 1000
     WHERE shohin_mei = '运动T恤';

    -- T恤的销售单价上浮1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka + 1000
     WHERE shohin_mei = 'T恤';

COMMIT;
"""

SBT_CH04_21_SQLSERVER = """
BEGIN TRANSACTION;

    -- 运动T恤的销售单价下调1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka - 1000
     WHERE shohin_mei = '运动T恤';

    -- T恤的销售单价上浮1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka + 1000
     WHERE shohin_mei = 'T恤';

COMMIT;
"""

SBT_CH04_22_MYSQL = """
START TRANSACTION;

    -- 运动T恤的销售单价下调1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka - 1000
     WHERE shohin_mei = '运动T恤';

    -- T恤的销售单价上浮1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka + 1000
     WHERE shohin_mei = 'T恤';

ROLLBACK;
"""

SBT_CH04_22_ORACLE = """
    -- 运动T恤的销售单价下调1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka - 1000
     WHERE shohin_mei = '运动T恤';

    -- T恤的销售单价上浮1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka + 1000
     WHERE shohin_mei = 'T恤';

ROLLBACK;
"""

SBT_CH04_22_SQLSERVER = """
BEGIN TRANSACTION;

    -- 运动T恤的销售单价下调1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka - 1000
     WHERE shohin_mei = '运动T恤';

    -- T恤的销售单价上浮1000日元
    UPDATE Shohin
       SET hanbai_tanka = hanbai_tanka + 1000
     WHERE shohin_mei = 'T恤';

ROLLBACK;
"""

SBT_CH05_01 = """
SELECT shohin_bunrui, SUM(hanbai_tanka), SUM(shiire_tanka)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH05_02 = """
CREATE VIEW ShohinSum (shohin_bunrui, cnt_shohin)
AS
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH05_03 = """
SELECT shohin_bunrui, cnt_shohin
  FROM ShohinSum;
"""

SBT_CH05_04 = """
CREATE VIEW ShohinSumJim (shohin_bunrui, cnt_shohin)
AS
SELECT shohin_bunrui, cnt_shohin
  FROM ShohinSum
 WHERE shohin_bunrui = '办公用品';

-- 确认创建好的视图
SELECT shohin_bunrui, cnt_shohin
  FROM ShohinSumJim;
"""

SBT_CH05_05 = """
CREATE VIEW ShohinJim (shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka, shiire_tanka, torokubi)
AS 
SELECT *
  FROM Shohin
 WHERE shohin_bunrui = '办公用品';
"""

SBT_CH05_06 = """
INSERT INTO ShohinJim VALUES ('0009', '印章', '办公用品', 95, 10, '2009-11-30');
"""

SBT_CH05_07 = """
DROP VIEW ShohinSum;
"""

SBT_CH05_A_POSTGRESQL = """
CREATE OR REPLACE RULE insert_rule
AS ON INSERT
TO  ShohinJim DO INSTEAD
INSERT INTO Shohin VALUES (
           new.shohin_id, 
           new.shohin_mei, 
           new.shohin_bunrui, 
           new.hanbai_tanka, 
           new.shiire_tanka, 
           new.torokubi);
"""

SBT_CH05_B = """
-- 删除商品编号为0009的印章
DELETE FROM Shohin WHERE shohin_id = '0009';
"""

SBT_CH05_08 = """
-- 根据商品分类统计商品数量的视图
CREATE VIEW ShohinSum (shohin_bunrui, cnt_shohin)
AS
SELECT shohin_bunrui, COUNT(*)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH05_09_ORACLE = """
-- 在FROM子句中直接书写定义视图的SELECT语句
SELECT shohin_bunrui, cnt_shohin
  FROM (SELECT shohin_bunrui, COUNT(*) AS cnt_shohin
          FROM Shohin
         GROUP BY shohin_bunrui) ShohinSum;
"""

SBT_CH05_09_SQLSERVER = """
-- 在FROM子句中直接书写定义视图的SELECT语句
SELECT shohin_bunrui, cnt_shohin
  FROM (SELECT shohin_bunrui, COUNT(*) AS cnt_shohin
          FROM Shohin
         GROUP BY shohin_bunrui) AS ShohinSum;
"""

SBT_CH05_10_ORACLE = """
SELECT shohin_bunrui, cnt_shohin
  FROM (SELECT *
          FROM (SELECT shohin_bunrui, COUNT(*) AS cnt_shohin
                  FROM Shohin
                 GROUP BY shohin_bunrui) ShohinSum
         WHERE cnt_shohin = 4) ShohinSum2;
"""

SBT_CH05_10_SQLSERVER = """
SELECT shohin_bunrui, cnt_shohin
  FROM (SELECT *
          FROM (SELECT shohin_bunrui, COUNT(*) AS cnt_shohin
                  FROM Shohin
                 GROUP BY shohin_bunrui) AS ShohinSum
         WHERE cnt_shohin = 4) AS ShohinSum2;
"""

SBT_CH05_11 = """
SELECT AVG(hanbai_tanka)
  FROM Shohin;
"""

SBT_CH05_12 = """
SELECT shohin_id, shohin_mei, hanbai_tanka
  FROM Shohin
 WHERE hanbai_tanka > (SELECT AVG(hanbai_tanka)
                         FROM Shohin);
"""

SBT_CH05_13 = """
SELECT shohin_id, 
       shohin_mei, 
       hanbai_tanka,
       (SELECT AVG(hanbai_tanka)
          FROM Shohin) AS avg_tanka
  FROM Shohin;
"""

SBT_CH05_14 = """
SELECT shohin_bunrui, AVG(hanbai_tanka)
  FROM Shohin
 GROUP BY shohin_bunrui
HAVING AVG(hanbai_tanka) > (SELECT AVG(hanbai_tanka)
                              FROM Shohin);
"""

SBT_CH05_15 = """
SELECT AVG(hanbai_tanka)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH05_16_ORACLE = """
SELECT shohin_bunrui, shohin_mei, hanbai_tanka
  FROM Shohin S1
 WHERE hanbai_tanka > (SELECT AVG(hanbai_tanka)
                         FROM Shohin S2
                        WHERE S1.shohin_bunrui = S2.shohin_bunrui
                        GROUP BY shohin_bunrui);
"""

SBT_CH05_16_SQLSERVER = """
SELECT shohin_bunrui, shohin_mei, hanbai_tanka
  FROM Shohin AS S1
 WHERE hanbai_tanka > (SELECT AVG(hanbai_tanka)
                         FROM Shohin AS S2
                        WHERE S1.shohin_bunrui = S2.shohin_bunrui
                        GROUP BY shohin_bunrui);
"""

SBT_CH06_01 = """
-- DDL：创建表
CREATE TABLE SampleMath
(m  NUMERIC (10,3),
 n  INTEGER,
 p  INTEGER);

-- DML：插入数据
START TRANSACTION;

INSERT INTO SampleMath(m, n, p) VALUES (500,  0,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (-180, 0,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, NULL, NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 7,    3);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 5,    2);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 4,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (8,    NULL, 3);
INSERT INTO SampleMath(m, n, p) VALUES (2.27, 1,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (5.555,2,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 1,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (8.76, NULL, NULL);

COMMIT;


-- 确认表中的内容
SELECT * FROM SampleMath;
"""

SBT_CH06_01_ORACLE = """
-- DDL：创建表
CREATE TABLE SampleMath
(m  NUMERIC (10,3),
 n  INTEGER,
 p  INTEGER);

-- DML：插入数据

INSERT INTO SampleMath(m, n, p) VALUES (500,  0,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (-180, 0,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, NULL, NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 7,    3);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 5,    2);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 4,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (8,    NULL, 3);
INSERT INTO SampleMath(m, n, p) VALUES (2.27, 1,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (5.555,2,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 1,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (8.76, NULL, NULL);

COMMIT;


-- 确认表中的内容
SELECT * FROM SampleMath;
"""

SBT_CH06_01_SQLSERVER = """
-- DDL：创建表
CREATE TABLE SampleMath
(m  NUMERIC (10,3),
 n  INTEGER,
 p  INTEGER);

-- DML：插入数据
BEGIN TRANSACTION;

INSERT INTO SampleMath(m, n, p) VALUES (500,  0,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (-180, 0,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, NULL, NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 7,    3);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 5,    2);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 4,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (8,    NULL, 3);
INSERT INTO SampleMath(m, n, p) VALUES (2.27, 1,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (5.555,2,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (NULL, 1,    NULL);
INSERT INTO SampleMath(m, n, p) VALUES (8.76, NULL, NULL);

COMMIT;


-- 确认表中的内容
SELECT * FROM SampleMath;
"""

SBT_CH06_02 = """
SELECT m,
       ABS(m) AS abs_col
  FROM SampleMath;
"""

SBT_CH06_03_ORACLE = """
SELECT n, p,
       MOD(n, p) AS mod_col
  FROM SampleMath;
"""

SBT_CH06_03_SQLSERVER = """
SELECT n, p,
       n % p AS mod_col
  FROM SampleMath;
"""

SBT_CH06_04 = """
SELECT m, n,
       ROUND(m, n) AS round_col
  FROM SampleMath;
"""

SBT_CH06_05_MYSQL = """
-- DDL：创建表
CREATE TABLE SampleStr
(str1  VARCHAR(40),
 str2  VARCHAR(40),
 str3  VARCHAR(40));

-- DML：插入数据
START TRANSACTION;

INSERT INTO SampleStr (str1, str2, str3) VALUES ('opx',	        'rt'	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abc'	,	'def'	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('山田'	,	'太郎'  ,	'是我');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('aaa'	,	NULL    ,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES (NULL	,	'xyz',	        NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('@!#$%',	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('ABC'	,	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('aBC'	,	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abc太郎',	'abc'	,	'ABC');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abcdefabc',   'abc'	,	'ABC');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('micmic',	      'i',        'I');

COMMIT;


-- 确认表中的内容
SELECT * FROM SampleStr;
"""

SBT_CH06_05_ORACLE = """
-- DDL：创建表
CREATE TABLE SampleStr
(str1  VARCHAR(40),
 str2  VARCHAR(40),
 str3  VARCHAR(40));

-- DML：插入数据

INSERT INTO SampleStr (str1, str2, str3) VALUES ('opx',	        'rt'	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abc'	,	'def'	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('山田'	,	'太郎'  ,	'是我');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('aaa'	,	NULL    ,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES (NULL	,	'xyz',	        NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('@!#$%',	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('ABC'	,	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('aBC'	,	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abc太郎',	'abc'	,	'ABC');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abcdefabc',   'abc'	,	'ABC');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('micmic',	      'i',        'I');

COMMIT;


-- 确认表中的内容
SELECT * FROM SampleStr;
"""

SBT_CH06_05_SQLSERVER = """
-- DDL：创建表
CREATE TABLE SampleStr
(str1  VARCHAR(40),
 str2  VARCHAR(40),
 str3  VARCHAR(40));

-- DML：插入数据
BEGIN TRANSACTION;

INSERT INTO SampleStr (str1, str2, str3) VALUES ('opx',	        'rt'	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abc'	,	'def'	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('山田'	,	'太郎'  ,	'是我');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('aaa'	,	NULL    ,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES (NULL	,	'xyz',	        NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('@!#$%',	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('ABC'	,	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('aBC'	,	NULL	,	NULL);
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abc太郎',	'abc'	,	'ABC');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('abcdefabc',   'abc'	,	'ABC');
INSERT INTO SampleStr (str1, str2, str3) VALUES ('micmic',	      'i',        'I');;

COMMIT;


-- 确认表中的内容
SELECT * FROM SampleStr;
"""

SBT_CH06_06_MYSQL = """
SELECT str1, str2,
       CONCAT(str1, str2) AS str_concat
  FROM SampleStr;
"""

SBT_CH06_06_ORACLE = """
SELECT str1, str2,
       str1 || str2 AS str_concat
  FROM SampleStr;
"""

SBT_CH06_06_SQLSERVER = """
SELECT str1, str2,
       str1 + str2 AS str_concat
  FROM SampleStr;
"""

SBT_CH06_7_SQLSERVER = """
SELECT str1, str2, str3,
       str1 + str2 + str3 AS str_concat
  FROM SampleStr;
"""

SBT_CH06_07_MYSQL = """
SELECT str1, str2, str3,
       CONCAT(str1, str2, str3) AS str_concat
  FROM SampleStr;
"""

SBT_CH06_07_ORACLE = """
SELECT str1, str2, str3,
       str1 || str2 || str3 AS str_concat
  FROM SampleStr
 WHERE str1 = '山田';
"""

SBT_CH06_08_ORACLE = """
SELECT str1,
       LENGTH(str1) AS len_str
  FROM SampleStr;
"""

SBT_CH06_08_SQLSERVER = """
SELECT str1,
       LEN(str1) AS len_str
  FROM SampleStr;
"""

SBT_CH06_09 = """
SELECT str1,
       LOWER(str1) AS low_str
  FROM SampleStr
 WHERE str1 IN ('ABC', 'aBC', 'abc', '山田');
"""

SBT_CH06_10 = """
SELECT str1, str2, str3,
       REPLACE(str1, str2, str3) AS rep_str
  FROM SampleStr;
"""

SBT_CH06_11_ORACLE = """
SELECT str1,
       SUBSTR(str1, 3, 2) AS sub_str
  FROM SampleStr;
"""

SBT_CH06_11_POSTGRESQL = """
SELECT str1,
       SUBSTRING(str1 FROM 3 FOR 2) AS sub_str
  FROM SampleStr;
"""

SBT_CH06_11_SQLSERVER = """
SELECT str1,
       SUBSTRING(str1, 3, 2) AS sub_str
  FROM SampleStr;
"""

SBT_CH06_12 = """
SELECT str1,
       UPPER(str1) AS up_str
  FROM SampleStr
 WHERE str1 IN ('ABC', 'aBC', 'abc', '山田');
"""

SBT_CH06_13_DB2 = """
/* CURRENT和TIME之间由半角空格隔开，
   指定临时表SYSIBM.SYSDUMMY1 */
SELECT CURRENT DATE
  FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH06_13_ORACLE = """
-- 指定临时表（DUAL）
SELECT CURRENT_DATE
  FROM DUAL;
"""

SBT_CH06_13_POSTGRESQL = """
SELECT CURRENT_DATE;
"""

SBT_CH06_13_SQLSERVER = """
-- 使用CAST将CURRENT_TIMESTAMP转换为日期类型
SELECT CAST(CURRENT_TIMESTAMP AS DATE) AS CUR_DATE;
"""

SBT_CH06_14_DB2 = """
/* CURRENT和TIME之间由半角空格隔开，
   指定临时表SYSIBM.SYSDUMMY1 */
SELECT CURRENT TIMESTAMP
  FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH06_14_ORACLE = """
-- 指定临时表（DUAL）
SELECT CURRENT_TIMESTAMP
  FROM DUAL;
"""

SBT_CH06_14_POSTGRESQL = """
SELECT CURRENT_TIME;
"""

SBT_CH06_14_SQLSERVER = """
-- 使用CAST将CURRENT_TIMESTAMP转换为日期类型
SELECT CAST(CURRENT_TIMESTAMP AS TIME) AS CUR_TIME;
"""

SBT_CH06_15_DB2 = """
/* CURRENT和TIME之间由半角空格隔开，
   指定临时表SYSIBM.SYSDUMMY1 */
SELECT CURRENT TIMESTAMP
  FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH06_15_ORACLE = """
-- 指定临时表（DUAL）
SELECT CURRENT_TIMESTAMP
  FROM DUAL;
"""

SBT_CH06_15_SQLSERVER = """
SELECT CURRENT_TIMESTAMP;
"""

SBT_CH06_16_DB2 = """
SELECT CURRENT TIMESTAMP,
       EXTRACT(YEAR   FROM CURRENT TIMESTAMP) AS year,
       EXTRACT(MONTH  FROM CURRENT TIMESTAMP) AS month,
       EXTRACT(DAY    FROM CURRENT TIMESTAMP) AS day,
       EXTRACT(HOUR   FROM CURRENT TIMESTAMP) AS hour,
       EXTRACT(MINUTE FROM CURRENT TIMESTAMP) AS minute,
       EXTRACT(SECOND FROM CURRENT TIMESTAMP) AS second
  FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH06_16_ORACLE = """
SELECT CURRENT_TIMESTAMP,
       EXTRACT(YEAR   FROM CURRENT_TIMESTAMP) AS year,
       EXTRACT(MONTH  FROM CURRENT_TIMESTAMP) AS month,
       EXTRACT(DAY    FROM CURRENT_TIMESTAMP) AS day,
       EXTRACT(HOUR   FROM CURRENT_TIMESTAMP) AS hour,
       EXTRACT(MINUTE FROM CURRENT_TIMESTAMP) AS minute,
       EXTRACT(SECOND FROM CURRENT_TIMESTAMP) AS second
FROM DUAL;
"""

SBT_CH06_16_POSTGRESQL = """
SELECT CURRENT_TIMESTAMP,
       EXTRACT(YEAR   FROM CURRENT_TIMESTAMP) AS year,
       EXTRACT(MONTH  FROM CURRENT_TIMESTAMP) AS month,
       EXTRACT(DAY    FROM CURRENT_TIMESTAMP) AS day,
       EXTRACT(HOUR   FROM CURRENT_TIMESTAMP) AS hour,
       EXTRACT(MINUTE FROM CURRENT_TIMESTAMP) AS minute,
       EXTRACT(SECOND FROM CURRENT_TIMESTAMP) AS second;
"""

SBT_CH06_16_SQLSERVER = """
SELECT CURRENT_TIMESTAMP,
       DATEPART(YEAR   , CURRENT_TIMESTAMP) AS year,
       DATEPART(MONTH  , CURRENT_TIMESTAMP) AS month,
       DATEPART(DAY    , CURRENT_TIMESTAMP) AS day,
       DATEPART(HOUR   , CURRENT_TIMESTAMP) AS hour,
       DATEPART(MINUTE , CURRENT_TIMESTAMP) AS minute,
       DATEPART(SECOND , CURRENT_TIMESTAMP) AS second;
"""

SBT_CH06_17_DB2 = """
SELECT CAST('0001' AS INTEGER) AS int_col
  FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH06_17_MYSQL = """
SELECT CAST('0001' AS SIGNED INTEGER) AS int_col;
"""

SBT_CH06_17_ORACLE = """
SELECT CAST('0001' AS INTEGER) AS int_col
  FROM DUAL;
"""

SBT_CH06_17_SQLSERVER = """
SELECT CAST('0001' AS INTEGER) AS int_col
  FROM DUAL;
"""

SBT_CH06_18_DB2 = """
SELECT CAST('2009-12-14' AS DATE) AS date_col FROM
  SYSIBM.SYSDUMMY1;
"""

SBT_CH06_18_ORACLE = """
SELECT CAST('2009-12-14' AS DATE) AS date_col
  FROM DUAL;
"""

SBT_CH06_18_SQLSERVER = """
SELECT CAST('2009-12-14' AS DATE) AS date_col;
"""

SBT_CH06_19_DB2 = """
SELECT COALESCE(NULL, 1)           AS col_1,
       COALESCE(NULL, 'test', NULL)       AS col_2,
       COALESCE(NULL, NULL, '2009-11-01') AS col_3
  FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH06_19_ORACLE = """
SELECT COALESCE(NULL, 1)           AS col_1,
       COALESCE(NULL, 'test', NULL)       AS col_2,
       COALESCE(NULL, NULL, '2009-11-01') AS col_3
  FROM SYSIBM.SYSDUMMY1;
"""

SBT_CH06_19_SQLSERVER = """
SELECT COALESCE(NULL, 1)                  AS col_1,
       COALESCE(NULL, 'test', NULL)       AS col_2,
       COALESCE(NULL, NULL, '2009-11-01') AS col_3;
"""

SBT_CH06_20 = """
SELECT COALESCE(str2, 'taNULL')
  FROM SampleStr;
"""

SBT_CH06_21_MYSQL = """
-- DDL：创建表
CREATE TABLE SampleLike
( strcol VARCHAR(6) NOT NULL,
  PRIMARY KEY (strcol));

-- DML：插入数据
START TRANSACTION;

INSERT INTO SampleLike (strcol) VALUES ('abcddd');
INSERT INTO SampleLike (strcol) VALUES ('dddabc');
INSERT INTO SampleLike (strcol) VALUES ('abdddc');
INSERT INTO SampleLike (strcol) VALUES ('abcdd');
INSERT INTO SampleLike (strcol) VALUES ('ddabc');
INSERT INTO SampleLike (strcol) VALUES ('abddc');

COMMIT;
"""

SBT_CH06_21_ORACLE = """
-- DDL：创建表
CREATE TABLE SampleLike
( strcol VARCHAR(6) NOT NULL,
  PRIMARY KEY (strcol));

-- DML：插入数据

INSERT INTO SampleLike (strcol) VALUES ('abcddd');
INSERT INTO SampleLike (strcol) VALUES ('dddabc');
INSERT INTO SampleLike (strcol) VALUES ('abdddc');
INSERT INTO SampleLike (strcol) VALUES ('abcdd');
INSERT INTO SampleLike (strcol) VALUES ('ddabc');
INSERT INTO SampleLike (strcol) VALUES ('abddc');

COMMIT;
"""

SBT_CH06_21_SQLSERVER = """
-- DDL：创建表
CREATE TABLE SampleLike
( strcol VARCHAR(6) NOT NULL,
  PRIMARY KEY (strcol));

-- DML：插入数据
BEGIN TRANSACTION;

INSERT INTO SampleLike (strcol) VALUES ('abcddd');
INSERT INTO SampleLike (strcol) VALUES ('dddabc');
INSERT INTO SampleLike (strcol) VALUES ('abdddc');
INSERT INTO SampleLike (strcol) VALUES ('abcdd');
INSERT INTO SampleLike (strcol) VALUES ('ddabc');
INSERT INTO SampleLike (strcol) VALUES ('abddc');

COMMIT;
"""

SBT_CH06_22 = """
SELECT *
  FROM SampleLike
 WHERE strcol LIKE 'ddd%';
"""

SBT_CH06_23 = """
SELECT *
  FROM SampleLike
 WHERE strcol LIKE '%ddd%';
"""

SBT_CH06_24 = """
SELECT *
  FROM SampleLike
 WHERE strcol LIKE '%ddd';
"""

SBT_CH06_25 = """
SELECT *
  FROM SampleLike
 WHERE strcol LIKE 'abc__';
"""

SBT_CH06_26 = """
SELECT *
  FROM SampleLike
 WHERE strcol LIKE 'abc___';
"""

SBT_CH06_27 = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin
 WHERE hanbai_tanka BETWEEN 100 AND 1000;
"""

SBT_CH06_28 = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin
 WHERE hanbai_tanka > 100 
   AND hanbai_tanka < 1000;
"""

SBT_CH06_29 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka IS NULL;
"""

SBT_CH06_30 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka IS NOT NULL;
"""

SBT_CH06_31 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka =  320
    OR shiire_tanka =  500
    OR shiire_tanka = 5000;
"""

SBT_CH06_32 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka IN (320, 500, 5000);
"""

SBT_CH06_33 = """
SELECT shohin_mei, shiire_tanka
  FROM Shohin
 WHERE shiire_tanka NOT IN (320, 500, 5000);
"""

SBT_CH06_34 = """
CREATE TABLE TenpoShohin
(tenpo_id  CHAR(4)       NOT NULL,
 tenpo_mei  VARCHAR(200) NOT NULL,
 shohin_id CHAR(4)       NOT NULL,
 suryo     INTEGER       NOT NULL,
 PRIMARY KEY (tenpo_id, shohin_id));
"""

SBT_CH06_35_MYSQL = """
START TRANSACTION;

INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0001',	30);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0002',	50);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0003',	15);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0002',	30);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0003',	120);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0004',	20);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0006',	10);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0007',	40);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0003',	20);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0004',	50);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0006',	90);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0007',	70);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000D',	'福冈',		'0001',	100);

COMMIT;
"""

SBT_CH06_35_ORACLE = """

INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0001',	30);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0002',	50);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0003',	15);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0002',	30);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0003',	120);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0004',	20);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0006',	10);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0007',	40);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0003',	20);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0004',	50);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0006',	90);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0007',	70);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000D',	'福冈',		'0001',	100);

COMMIT;
"""

SBT_CH06_35_SQLSERVER = """
BEGIN TRANSACTION;

INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0001',	30);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0002',	50);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000A',	'东京',		'0003',	15);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0002',	30);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0003',	120);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0004',	20);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0006',	10);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000B',	'名古屋',	'0007',	40);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0003',	20);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0004',	50);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0006',	90);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000C',	'大阪',		'0007',	70);
INSERT INTO TenpoShohin (tenpo_id, tenpo_mei, shohin_id, suryo) VALUES ('000D',	'福冈',		'0001',	100);

COMMIT;
"""

SBT_CH06_36 = """
-- 取得在大阪店销售的商品的销售单价
SELECT shohin_mei, hanbai_tanka
  FROM Shohin
 WHERE shohin_id IN (SELECT shohin_id 
                       FROM TenpoShohin
                      WHERE tenpo_id = '000C');
"""

SBT_CH06_37 = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin
 WHERE shohin_id NOT IN (SELECT shohin_id 
                           FROM TenpoShohin
                          WHERE tenpo_id = '000A');
"""

SBT_CH06_38_ORACLE = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin S
 WHERE EXISTS (SELECT *
                 FROM TenpoShohin TS
                WHERE TS.tenpo_id = '000C'
                  AND TS.shohin_id = S.shohin_id);
"""

SBT_CH06_38_SQLSERVER = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin AS S
 WHERE EXISTS (SELECT *
                 FROM TenpoShohin AS TS
                WHERE TS.tenpo_id = '000C'
                  AND TS.shohin_id = S.shohin_id);
"""

SBT_CH06_39_ORACLE = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin S
 WHERE EXISTS (SELECT 1 -- 这里可以书写恰当的常数
                 FROM TenpoShohin TS
                WHERE TS.tenpo_id = '000C'
                  AND TS.shohin_id = S.shohin_id);
"""

SBT_CH06_39_SQLSERVER = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin AS S
 WHERE EXISTS (SELECT 1 -- 这里可以书写恰当的常数
                 FROM TenpoShohin AS TS
                WHERE TS.tenpo_id = '000C'
                  AND TS.shohin_id = S.shohin_id);
"""

SBT_CH06_40_ORACLE = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin S
 WHERE NOT EXISTS (SELECT *
                     FROM TenpoShohin TS
                    WHERE TS.tenpo_id = '000A'
                      AND TS.shohin_id = S.shohin_id);
"""

SBT_CH06_40_SQLSERVER = """
SELECT shohin_mei, hanbai_tanka
  FROM Shohin AS S
 WHERE NOT EXISTS (SELECT *
                     FROM TenpoShohin AS TS
                    WHERE TS.tenpo_id = '000A'
                      AND TS.shohin_id = S.shohin_id);
"""

SBT_CH06_41 = """
SELECT shohin_mei,
       CASE WHEN shohin_bunrui = '衣服'         THEN 'A：' || shohin_bunrui
            WHEN shohin_bunrui = '办公用品'     THEN 'B：' || shohin_bunrui
            WHEN shohin_bunrui = '厨房用具' THEN 'C：' || shohin_bunrui
            ELSE NULL
       END AS abc_shohin_bunrui
  FROM Shohin;
"""

SBT_CH06_43 = """
-- 对按照商品种类得到的销售单价合计值进行行列转换
SELECT SUM(CASE WHEN shohin_bunrui = '衣服'         THEN hanbai_tanka ELSE 0 END) AS sum_tanka_ihuku,
       SUM(CASE WHEN shohin_bunrui = '厨房用具' THEN hanbai_tanka ELSE 0 END) AS sum_tanka_kitchen,
       SUM(CASE WHEN shohin_bunrui = '办公用品'     THEN hanbai_tanka ELSE 0 END) AS sum_tanka_jimu
  FROM Shohin;
"""

SBT_CH06_A = """
-- 使用简单CASE表达式的情况
SELECT shohin_mei,
       CASE shohin_bunrui
            WHEN '衣服'         THEN 'A：' || shohin_bunrui
            WHEN '办公用品'     THEN 'B：' || shohin_bunrui
            WHEN '厨房用具' THEN 'C：' || shohin_bunrui
            ELSE NULL
        END AS abc_shohin_bunrui
  FROM Shohin;
"""

SBT_CH06_B_MYSQL = """
-- MySQL中使用IF代替CASE表达式
SELECT  shohin_mei,
        IF( IF( IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL)
            	    IS NULL AND shohin_bunrui = '办公用品', CONCAT('B：', shohin_bunrui), 
            	IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL))
                    IS NULL AND shohin_bunrui = '厨房用具', CONCAT('C：', shohin_bunrui), 
                    IF( IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL)
            	    IS NULL AND shohin_bunrui = '办公用品', CONCAT('B：', shohin_bunrui), 
            	IF(shohin_bunrui = '衣服',  CONCAT('A：', shohin_bunrui), NULL))) AS abc_shohin_bunrui
  FROM Shohin;
"""

SBT_CH06_B_ORACLE = """
-- Oracle中使用DECODE代替CASE表达式
SELECT  shohin_mei,
        DECODE(shohin_bunrui, '衣服',         'A：' || shohin_bunrui,
                              '办公用品',     'B：' || shohin_bunrui,
                              '厨房用具', 'C：' || shohin_bunrui,
               NULL) AS abc_shohin_bunrui
  FROM Shohin;
"""

SBT_CH07_01 = """
CREATE TABLE Shohin2
(shohin_id     CHAR(4)      NOT NULL,
 shohin_mei    VARCHAR(100) NOT NULL,
 shohin_bunrui VARCHAR(32)  NOT NULL,
 hanbai_tanka  INTEGER      ,
 shiire_tanka  INTEGER      ,
 torokubi      DATE         ,
 PRIMARY KEY (shohin_id));
"""

SBT_CH07_02_MYSQL = """
START TRANSACTION;

INSERT INTO Shohin2 VALUES ('0001', 'T恤', '衣服', 1000, 500, '2009-09-20');
INSERT INTO Shohin2 VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11');
INSERT INTO Shohin2 VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL);
INSERT INTO Shohin2 VALUES ('0009', '手套', '衣服', 800, 500, NULL);
INSERT INTO Shohin2 VALUES ('0010', '水壶', '厨房用具', 2000, 1700, '2009-09-20');

COMMIT;
"""

SBT_CH07_02_ORACLE = """
INSERT INTO Shohin2 VALUES ('0001', 'T恤', '衣服', 1000, 500, '2009-09-20');
INSERT INTO Shohin2 VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11');
INSERT INTO Shohin2 VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL);
INSERT INTO Shohin2 VALUES ('0009', '手套', '衣服', 800, 500, NULL);
INSERT INTO Shohin2 VALUES ('0010', '水壶', '厨房用具', 2000, 1700, '2009-09-20');

COMMIT;
"""

SBT_CH07_02_SQLSERVER = """
BEGIN TRANSACTION;

INSERT INTO Shohin2 VALUES ('0001', 'T恤', '衣服', 1000, 500, '2009-09-20');
INSERT INTO Shohin2 VALUES ('0002', '打孔器', '办公用品', 500, 320, '2009-09-11');
INSERT INTO Shohin2 VALUES ('0003', '运动T恤', '衣服', 4000, 2800, NULL);
INSERT INTO Shohin2 VALUES ('0009', '手套', '衣服', 800, 500, NULL);
INSERT INTO Shohin2 VALUES ('0010', '水壶', '厨房用具', 2000, 1700, '2009-09-20');

COMMIT;
"""

SBT_CH07_03 = """
SELECT shohin_id, shohin_mei
  FROM Shohin
UNION
SELECT shohin_id, shohin_mei
  FROM Shohin2;
"""

SBT_CH07_04 = """
SELECT shohin_id, shohin_mei
  FROM Shohin
 WHERE shohin_bunrui = '厨房用具'
UNION
SELECT shohin_id, shohin_mei
  FROM Shohin2
 WHERE shohin_bunrui = '厨房用具'
ORDER BY shohin_id;
"""

SBT_CH07_05 = """
SELECT shohin_id, shohin_mei
  FROM Shohin
UNION ALL
SELECT shohin_id, shohin_mei
  FROM Shohin2;
"""

SBT_CH07_06 = """
SELECT shohin_id, shohin_mei
  FROM Shohin
INTERSECT
SELECT shohin_id, shohin_mei
  FROM Shohin2
ORDER BY shohin_id;
"""

SBT_CH07_07_ORACLE = """
-- Oracle中不使用EXCEPT而使用MINUS
SELECT shohin_id, shohin_mei
  FROM Shohin
MINUS
SELECT shohin_id, shohin_mei
  FROM Shohin2
ORDER BY shohin_id;
"""

SBT_CH07_07_SQLSERVER = """
SELECT shohin_id, shohin_mei
  FROM Shohin
EXCEPT
SELECT shohin_id, shohin_mei
  FROM Shohin2
ORDER BY shohin_id;
"""

SBT_CH07_08_ORACLE = """
-- 从Shohin2的记录中删除Shohin的记录
SELECT shohin_id, shohin_mei
  FROM Shohin2
MINUS
SELECT shohin_id, shohin_mei
  FROM Shohin
ORDER BY shohin_id;
"""

SBT_CH07_08_SQLSERVER = """
-- 从Shohin2的记录中删除Shohin的记录
SELECT shohin_id, shohin_mei
  FROM Shohin2
EXCEPT
SELECT shohin_id, shohin_mei
  FROM Shohin
ORDER BY shohin_id;
"""

SBT_CH07_09_ORACLE = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM TenpoShohin TS INNER JOIN Shohin S
    ON TS.shohin_id = S.shohin_id;
"""

SBT_CH07_09_SQLSERVER = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM TenpoShohin AS TS INNER JOIN Shohin AS S
    ON TS.shohin_id = S.shohin_id;
"""

SBT_CH07_10_ORACLE = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM TenpoShohin TS INNER JOIN Shohin S
    ON TS.shohin_id = S.shohin_id
 WHERE TS.tenpo_id = '000A';
"""

SBT_CH07_10_SQLSERVER = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM TenpoShohin AS TS INNER JOIN Shohin AS S
    ON TS.shohin_id = S.shohin_id
 WHERE TS.tenpo_id = '000A';
"""

SBT_CH07_11_ORACLE = """
SELECT TS.tenpo_id, TS.tenpo_mei, S.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM TenpoShohin TS RIGHT OUTER JOIN Shohin S
    ON TS.shohin_id = S.shohin_id;
"""

SBT_CH07_11_SQLSERVER = """
SELECT TS.tenpo_id, TS.tenpo_mei, S.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM TenpoShohin AS TS RIGHT OUTER JOIN Shohin AS S
    ON TS.shohin_id = S.shohin_id;
"""

SBT_CH07_12_ORACLE = """
SELECT TS.tenpo_id, TS.tenpo_mei, S.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM Shohin S LEFT OUTER JOIN TenpoShohin TS
    ON TS.shohin_id = S.shohin_id;
"""

SBT_CH07_12_SQLSERVER = """
SELECT TS.tenpo_id, TS.tenpo_mei, S.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM Shohin AS S LEFT OUTER JOIN TenpoShohin AS TS
    ON TS.shohin_id = S.shohin_id;
"""

SBT_CH07_13_MYSQL = """
-- DDL：创建表
CREATE TABLE ZaikoShohin
( souko_id		CHAR(4)      NOT NULL,
  shohin_id     CHAR(4)      NOT NULL,
  zaiko_suryo	INTEGER      NOT NULL,
  PRIMARY KEY (souko_id, shohin_id));

-- DML：插入数据
START TRANSACTION;

INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0001',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0002',	120);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0003',	200);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0004',	3);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0005',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0006',	99);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0007',	999);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0008',	200);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0001',	10);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0002',	25);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0003',	34);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0004',	19);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0005',	99);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0006',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0007',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0008',	18);

COMMIT;
"""

SBT_CH07_13_ORACLE = """
-- DDL：创建表
CREATE TABLE ZaikoShohin
( souko_id		CHAR(4)      NOT NULL,
  shohin_id     CHAR(4)      NOT NULL,
  zaiko_suryo	INTEGER      NOT NULL,
  PRIMARY KEY (souko_id, shohin_id));

-- DML：插入数据

INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0001',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0002',	120);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0003',	200);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0004',	3);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0005',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0006',	99);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0007',	999);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0008',	200);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0001',	10);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0002',	25);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0003',	34);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0004',	19);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0005',	99);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0006',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0007',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0008',	18);

COMMIT;
"""

SBT_CH07_13_SQLSERVER = """
-- DDL：创建表
CREATE TABLE ZaikoShohin
( souko_id		CHAR(4)      NOT NULL,
  shohin_id     CHAR(4)      NOT NULL,
  zaiko_suryo	INTEGER      NOT NULL,
  PRIMARY KEY (souko_id, shohin_id));

-- DML：插入数据
BEGIN TRANSACTION;

INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0001',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0002',	120);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0003',	200);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0004',	3);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0005',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0006',	99);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0007',	999);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S001',	'0008',	200);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0001',	10);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0002',	25);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0003',	34);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0004',	19);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0005',	99);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0006',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0007',	0);
INSERT INTO ZaikoShohin (souko_id, shohin_id, zaiko_suryo) VALUES ('S002',	'0008',	18);

COMMIT;
"""

SBT_CH07_14_ORACLE = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei, S.hanbai_tanka, ZS.zaiko_suryo
  FROM TenpoShohin TS INNER JOIN Shohin S
    ON TS.shohin_id = S.shohin_id
          INNER JOIN ZaikoShohin ZS
             ON TS.shohin_id = ZS.shohin_id
 WHERE ZS.souko_id = 'S001';
"""

SBT_CH07_14_SQLSERVER = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei, S.hanbai_tanka, ZS.zaiko_suryo
  FROM TenpoShohin AS TS INNER JOIN Shohin AS S
    ON TS.shohin_id = S.shohin_id
               INNER JOIN ZaikoShohin AS ZS
                   ON TS.shohin_id = ZS.shohin_id
WHERE ZS.souko_id = 'S001';
"""

SBT_CH07_15_ORACLE = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei
  FROM TenpoShohin TS CROSS JOIN Shohin S;
"""

SBT_CH07_15_SQLSERVER = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei
  FROM TenpoShohin AS TS CROSS JOIN Shohin AS S;
"""

SBT_CH07_16 = """
SELECT TS.tenpo_id, TS.tenpo_mei, TS.shohin_id, S.shohin_mei, S.hanbai_tanka
  FROM TenpoShohin TS, Shohin S
 WHERE TS.shohin_id = S.shohin_id
   AND TS.tenpo_id = '000A';
"""
SBT_CH07_A_MYSQL = """
-- DDL：创建表
CREATE TABLE Skills 
(skill VARCHAR(32),
 PRIMARY KEY(skill));

CREATE TABLE EmpSkills 
(emp   VARCHAR(32), 
 skill VARCHAR(32),
 PRIMARY KEY(emp, skill));

-- DML：插入数据
START TRANSACTION;

INSERT INTO Skills VALUES('Oracle');
INSERT INTO Skills VALUES('UNIX');
INSERT INTO Skills VALUES('Java');

INSERT INTO EmpSkills VALUES('相田', 'Oracle');
INSERT INTO EmpSkills VALUES('相田', 'UNIX');
INSERT INTO EmpSkills VALUES('相田', 'Java');
INSERT INTO EmpSkills VALUES('相田', 'C#');
INSERT INTO EmpSkills VALUES('神崎', 'Oracle');
INSERT INTO EmpSkills VALUES('神崎', 'UNIX');
INSERT INTO EmpSkills VALUES('神崎', 'Java');
INSERT INTO EmpSkills VALUES('平井', 'UNIX');
INSERT INTO EmpSkills VALUES('平井', 'Oracle');
INSERT INTO EmpSkills VALUES('平井', 'PHP');
INSERT INTO EmpSkills VALUES('平井', 'Perl');
INSERT INTO EmpSkills VALUES('平井', 'C++');
INSERT INTO EmpSkills VALUES('若田部', 'Perl');
INSERT INTO EmpSkills VALUES('渡来', 'Oracle');

COMMIT;
"""

SBT_CH07_A_ORACLE = """
-- DDL：创建表
CREATE TABLE Skills 
(skill VARCHAR(32),
 PRIMARY KEY(skill));

CREATE TABLE EmpSkills 
(emp   VARCHAR(32), 
 skill VARCHAR(32),
 PRIMARY KEY(emp, skill));

-- DML：插入数据

INSERT INTO Skills VALUES('Oracle');
INSERT INTO Skills VALUES('UNIX');
INSERT INTO Skills VALUES('Java');

INSERT INTO EmpSkills VALUES('相田', 'Oracle');
INSERT INTO EmpSkills VALUES('相田', 'UNIX');
INSERT INTO EmpSkills VALUES('相田', 'Java');
INSERT INTO EmpSkills VALUES('相田', 'C#');
INSERT INTO EmpSkills VALUES('神崎', 'Oracle');
INSERT INTO EmpSkills VALUES('神崎', 'UNIX');
INSERT INTO EmpSkills VALUES('神崎', 'Java');
INSERT INTO EmpSkills VALUES('平井', 'UNIX');
INSERT INTO EmpSkills VALUES('平井', 'Oracle');
INSERT INTO EmpSkills VALUES('平井', 'PHP');
INSERT INTO EmpSkills VALUES('平井', 'Perl');
INSERT INTO EmpSkills VALUES('平井', 'C++');
INSERT INTO EmpSkills VALUES('若田部', 'Perl');
INSERT INTO EmpSkills VALUES('渡来', 'Oracle');

COMMIT;
"""

SBT_CH07_A_SQLSERVER = """
-- DDL：创建表
CREATE TABLE Skills 
(skill VARCHAR(32),
 PRIMARY KEY(skill));

CREATE TABLE EmpSkills 
(emp   VARCHAR(32), 
 skill VARCHAR(32),
 PRIMARY KEY(emp, skill));

-- DML：插入数据
BEGIN TRANSACTION;

INSERT INTO Skills VALUES('Oracle');
INSERT INTO Skills VALUES('UNIX');
INSERT INTO Skills VALUES('Java');

INSERT INTO EmpSkills VALUES('相田', 'Oracle');
INSERT INTO EmpSkills VALUES('相田', 'UNIX');
INSERT INTO EmpSkills VALUES('相田', 'Java');
INSERT INTO EmpSkills VALUES('相田', 'C#');
INSERT INTO EmpSkills VALUES('神崎', 'Oracle');
INSERT INTO EmpSkills VALUES('神崎', 'UNIX');
INSERT INTO EmpSkills VALUES('神崎', 'Java');
INSERT INTO EmpSkills VALUES('平井', 'UNIX');
INSERT INTO EmpSkills VALUES('平井', 'Oracle');
INSERT INTO EmpSkills VALUES('平井', 'PHP');
INSERT INTO EmpSkills VALUES('平井', 'Perl');
INSERT INTO EmpSkills VALUES('平井', 'C++');
INSERT INTO EmpSkills VALUES('若田部', 'Perl');
INSERT INTO EmpSkills VALUES('渡来', 'Oracle');

COMMIT;
"""

SBT_CH07_B = """
SELECT DISTINCT emp
  FROM EmpSkills ES1
 WHERE NOT EXISTS
        (SELECT skill
           FROM Skills
         EXCEPT
         SELECT skill
           FROM EmpSkills ES2
          WHERE ES1.emp = ES2.emp);
"""

SBT_CH08_01 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka,
       RANK () OVER (PARTITION BY shohin_bunrui
                         ORDER BY hanbai_tanka) AS ranking
  FROM Shohin;
"""

SBT_CH08_02 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka, 
       RANK () OVER (ORDER BY hanbai_tanka) AS ranking
  FROM Shohin;
"""

SBT_CH08_03 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka, 
       RANK () OVER (ORDER BY hanbai_tanka) AS ranking,
       DENSE_RANK () OVER (ORDER BY hanbai_tanka) AS dense_ranking,
       ROW_NUMBER () OVER (ORDER BY hanbai_tanka) AS row_num
 FROM Shohin;
"""

SBT_CH08_04 = """
SELECT shohin_id, shohin_mei, hanbai_tanka,
       SUM (hanbai_tanka) OVER (ORDER BY shohin_id) AS current_sum
  FROM Shohin;
"""

SBT_CH08_05 = """
SELECT shohin_id, shohin_mei, hanbai_tanka,
       AVG (hanbai_tanka) OVER (ORDER BY shohin_id) AS current_avg
  FROM Shohin;
"""

SBT_CH08_06 = """
SELECT shohin_id, shohin_mei, hanbai_tanka,
       AVG (hanbai_tanka) OVER (ORDER BY shohin_id
                                ROWS 2 PRECEDING) AS moving_avg
  FROM Shohin;
"""

SBT_CH08_07 = """
SELECT shohin_id, shohin_mei, hanbai_tanka,
       AVG (hanbai_tanka) OVER (ORDER BY shohin_id
                                ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) AS moving_avg
  FROM Shohin;
"""

SBT_CH08_08 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka, 
       RANK () OVER (ORDER BY hanbai_tanka) AS ranking
  FROM Shohin;
"""

SBT_CH08_09 = """
SELECT shohin_mei, shohin_bunrui, hanbai_tanka, 
       RANK () OVER (ORDER BY hanbai_tanka) AS ranking
  FROM Shohin
 ORDER BY ranking;
"""

SBT_CH08_10 = """
SELECT shohin_bunrui, SUM(hanbai_tanka)
  FROM Shohin
 GROUP BY shohin_bunrui;
"""

SBT_CH08_11 = """
SELECT '合计' AS shohin_bunrui, SUM(hanbai_tanka)
  FROM Shohin
UNION ALL
SELECT shohin_bunrui, SUM(hanbai_tanka)
  FROM Shohin
GROUP BY shohin_bunrui;
"""

SBT_CH08_12_MYSQL = """
SELECT shohin_bunrui, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY shohin_bunrui WITH ROLLUP;
"""

SBT_CH08_12_ORACLE = """
SELECT shohin_bunrui, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY ROLLUP(shohin_bunrui);
"""

SBT_CH08_13 = """
SELECT shohin_bunrui, torokubi, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY shohin_bunrui, torokubi;
"""

SBT_CH08_14_MYSQL = """
SELECT shohin_bunrui, torokubi, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY shohin_bunrui, torokubi WITH ROLLUP;
"""

SBT_CH08_14_ORACLE = """
SELECT shohin_bunrui, torokubi, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY ROLLUP(shohin_bunrui, torokubi);
"""

SBT_CH08_15 = """
SELECT GROUPING(shohin_bunrui) AS shohin_bunrui, 
            GROUPING(torokubi) AS torokubi, SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY ROLLUP(shohin_bunrui, torokubi);
"""

SBT_CH08_16 = """
SELECT CASE WHEN GROUPING(shohin_bunrui) = 1
            THEN '商品种类 合计'
            ELSE shohin_bunrui END AS shohin_bunrui,
       CASE WHEN GROUPING(torokubi) = 1
            THEN '登记日期 合计'
            ELSE CAST(torokubi AS VARCHAR(16)) END AS torokubi,
       SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY ROLLUP(shohin_bunrui, torokubi);
"""

SBT_CH08_17 = """
SELECT CASE WHEN GROUPING(shohin_bunrui) = 1
            THEN '商品种类 合计'
            ELSE shohin_bunrui END AS shohin_bunrui,
       CASE WHEN GROUPING(torokubi) = 1
            THEN '登记日期 合计'
            ELSE CAST(torokubi AS VARCHAR(16)) END AS torokubi,
       SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY CUBE(shohin_bunrui, torokubi);
"""

SBT_CH08_18 = """
SELECT CASE WHEN GROUPING(shohin_bunrui) = 1
            THEN '商品种类 合计'
            ELSE shohin_bunrui END AS shohin_bunrui,
       CASE WHEN GROUPING(torokubi) = 1
            THEN '登记日期 合计'
            ELSE CAST(torokubi AS VARCHAR(16)) END AS torokubi,
       SUM(hanbai_tanka) AS sum_tanka
  FROM Shohin
 GROUP BY GROUPING SETS (shohin_bunrui, torokubi);
"""


