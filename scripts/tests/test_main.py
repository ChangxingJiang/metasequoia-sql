"""
当前文件的依赖（仅测试场景需要，故不需要添加到 requirements.txt 中）：
pip install coverage
"""

import os
import unittest

# 获取测试文件所在目录
test_dir = os.path.dirname(os.path.realpath(__file__))

# 测试用例加载器，添加discover方法以支持模式匹配
loader = unittest.TestLoader()
suite = loader.discover(test_dir, pattern='test_*.py')

# 执行测试用例
runner = unittest.TextTestRunner()
runner.run(suite)
