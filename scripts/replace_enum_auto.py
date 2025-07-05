#!/usr/bin/env python3
"""
自动替换terminal_type.py中的enum.auto()为递增的整数
"""
import re

def replace_enum_auto():
    # 读取文件
    with open('../metasequoia_sql/terminal/terminal_type.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 需要确定起始数字 - 从现有的最大数字开始
    lines = content.split('\n')
    max_num = 0
    for line in lines:
        # 查找类似 "KEYWORD_XXX = 数字" 的模式
        match = re.search(r'= (\d+)', line)
        if match:
            num = int(match.group(1))
            max_num = max(max_num, num)
    
    # 从max_num + 1开始替换
    current_num = max_num + 1
    
    # 简单地逐个替换第一个出现的enum.auto()
    while 'enum.auto()' in content:
        content = content.replace('enum.auto()', str(current_num), 1)
        current_num += 1
    
    # 写回文件
    with open('../metasequoia_sql/terminal/terminal_type.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已替换所有enum.auto()实例，数字从 {max_num + 1} 开始")

if __name__ == '__main__':
    replace_enum_auto() 