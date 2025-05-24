"""
词法解析 Demo

<AMTSingle source="SELECT" marks=>
<AMTSingle source="column1" marks=NAME>
<AMTSingle source="," marks=>
<AMTParenthesis children=[<AMTSingle source="column2" marks=NAME>, <AMTSingle source="+" marks=>, <AMTSingle source="1" marks=LITERAL|LITERAL_INT>] marks=PARENTHESIS>
<AMTSingle source="*" marks=>
<AMTSingle source="2" marks=LITERAL|LITERAL_INT>
<AMTSingle source="FROM" marks=>
<AMTSingle source="table_1" marks=NAME>
"""

from metasequoia_sql_old import FSMMachine

amt_tree = FSMMachine.parse("SELECT column1, (column2 + 1) * 2 FROM table_1")
for node in amt_tree:
    print(node)
