"""
《MySQL 必知必会》样例 SQL
"""

DEMO_MYSQL_MCC_15_2_3_1 = """
SELECT prod_name, vend_name, prod_price, quantity
FROM orderitems, products, vendors
WHERE products.vend_id = vendors.vend_id
  AND orderitems.prod_id = products.prod_id
  AND order_num = 20005;
"""
