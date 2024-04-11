from metasequoia_sql.common import build_token_scanner
from metasequoia_sql.objects import DataSource
from metasequoia_sql.parser.expression import parse_create_table_statement

if __name__ == "__main__":
    statement = parse_create_table_statement(build_token_scanner("""
CREATE TABLE `manual_annotation` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `video_id` varchar(20) NOT NULL COMMENT '视频ID(B站ID)',
  `video_name` varchar(300) NOT NULL COMMENT '视频名称',
  `video_deleted` tinyint(1) unsigned zerofill NOT NULL DEFAULT '0' COMMENT '视频是否已被删除：0没有删除，1已删除',
  `author_id` bigint unsigned DEFAULT NULL COMMENT '视频作者ID',
  `author_name` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频作者名称（仅标注作用）',
  `series_id` bigint DEFAULT NULL COMMENT '视频所属系列ID',
  `series_name` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频所属系列名称（仅标注作用）',
  `video_index_in_series` int DEFAULT NULL COMMENT '视频在所属系列中的序号',
  `video_name_in_series` varchar(300) DEFAULT NULL COMMENT '视频在所属系列中的名称',
  `event_label_1` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频内容讲解事件的第1级标签',
  `event_label_2` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频内容讲解的历史第2级标签',
  `event_label_3` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频内容讲解的历史第3级标签',
  `event_label_4` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '视频内容讲解的历史第4级标签',
  `start_date` varchar(12) DEFAULT NULL COMMENT '视频内容讲解的开始时间(公元前用BC前缀)',
  `end_date` varchar(12) DEFAULT NULL COMMENT '视频内容讲解的结束时间(公元前用BC前缀)',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_company_id` (`video_id`),
  KEY `index_author_id` (`author_id`),
  KEY `index_area_name` (`event_label_1`),
  KEY `index_start_date` (`start_date`),
  KEY `index_series_id` (`series_id`),
  FULLTEXT KEY `fulltext_video_name` (`video_name`)
) ENGINE=InnoDB AUTO_INCREMENT=659 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Bilibili历史类视频'"""))
    print(statement.source(DataSource.HIVE))
