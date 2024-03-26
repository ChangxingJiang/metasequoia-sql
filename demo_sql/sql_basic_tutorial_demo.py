"""
引用来自 https://github.com/OctopusLian/SQL-Basic-Tutorial 仓库的样例 SQL
"""

CH01_1 = """
CREATE DATABASE Shop;
"""

CH01_2 = """
CREATE TABLE Shohin
(shohin_id     CHAR(4)      NOT NULL,
 shohin_mei    VARCHAR(100) NOT NULL,
 shohin_bunrui VARCHAR(32)  NOT NULL,
 hanbai_tanka  INTEGER ,
 shiire_tanka  INTEGER ,
 torokubi      DATE ,
 PRIMARY KEY (shohin_id));
"""

CH01_3 = """
DROP TABLE Shohin;
"""

# PostgreSQL
CH01_4_T1 = """
ALTER TABLE Shohin ADD COLUMN shohin_mei_kana VARCHAR(100);
"""

# Oracle
CH01_4_T2 = """
ALTER TABLE Shohin ADD (shohin_mei_kana VARCHAR2(100));
"""

# SqlServer
CH01_4_T3 = """
ALTER TABLE Shohin ADD shohin_mei_kana VARCHAR(100);
"""

# Oracle
CH01_5_T1 = """
ALTER TABLE Shohin DROP (shohin_mei_kana);
"""

# SqlServer
CH01_5_T2 = """
ALTER TABLE Shohin DROP COLUMN shohin_mei_kana;
"""

# MySQL
CH01_6_T1 = """
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

# Oracle
CH01_6_T2 = """
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

# SqlServer
CH01_6_T3 = """
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

# DB2
CH01_7_T1 = """
RENAME TABLE Sohin TO Shohin;
"""

# MySQL
CH01_7_T2 = """
RENAME TABLE Sohin to Shohin;
"""

# Oracle + PostgreSQL
CH01_A_T3 = """
ALTER TABLE Sohin RENAME TO Shohin;
"""

# SqlServer
CH01_A_T4 = """
sp_rename 'Sohin', 'Shohin';
"""

CH02_1 = """
SELECT shohin_id, shohin_mei, shiire_tanka
  FROM Shohin;
"""

CH02_2 = """
SELECT *
  FROM Shohin;
"""

CH02_3 = """
SELECT shohin_id, shohin_mei, shohin_bunrui, hanbai_tanka,
       shiire_tanka, torokubi
  FROM Shohin;
"""

CH02_4 = """
SELECT shohin_id    AS id,
       shohin_mei   AS namae,
       shiire_tanka AS tanka
  FROM Shohin;
"""

CH02_5 = """
SELECT shohin_id    AS "商品编号",
       shohin_mei   AS "商品名称",
       shiire_tanka AS "进货单价"
  FROM Shohin;
"""

CH02_6 = """
SELECT '商品' AS mojiretsu, 38 AS kazu, '2009-02-24' AS hizuke,
       shohin_id, shohin_mei
  FROM Shohin;
"""

CH02_7 = """
SELECT DISTINCT shohin_bunrui
  FROM Shohin;
"""

CH02_8 = """
SELECT DISTINCT shiire_tanka
  FROM Shohin;
"""

CH02_9 = """
SELECT DISTINCT shohin_bunrui, torokubi
  FROM Shohin;
"""

CH02_10 = """
SELECT shohin_mei, shohin_bunrui
  FROM Shohin
 WHERE shohin_bunrui = '衣服';
"""

CH02_11 = """
SELECT shohin_mei
  FROM Shohin
 WHERE shohin_bunrui = '衣服';
"""

CH02_13 = """
-- 本SELECT语句会从结果中删除重复行。
SELECT DISTINCT shohin_id, shiire_tanka
  FROM Shohin;
"""

CH02_14 = """
/* 本SELECT语句，
   会从结果中删除重复行。*/
SELECT DISTINCT shohin_id, shiire_tanka
  FROM Shohin;
"""

CH02_15 = """
SELECT DISTINCT shohin_id, shiire_tanka
-- 本SELECT语句会从结果中删除重复行。
  FROM Shohin;
"""

CH02_16 = """
SELECT DISTINCT shohin_id, shiire_tanka
/* 本SELECT语句,
   会从结果中删除重复行。*/
  FROM Shohin;
"""

CH02_17 = """
SELECT shohin_mei, hanbai_tanka,
       hanbai_tanka * 2 AS "hanbai_tanka_x2"
  FROM Shohin;
"""
