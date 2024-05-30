from distutils.core import setup

from setuptools import find_packages

with open("README.md", "r", encoding="UTF-8") as file:
    long_description = file.read()

setup(
    name="metasequoia-sql",
    version="0.6.0",
    description="metasequoia-sql 是一款注重性能的 SQL 语法的解析和分析器，适用于 SQL 的格式化、执行和分析场景，致力于打造性能最高的 Python 版 SQL 解析器。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="changxing",
    author_email="1278729001@qq.com",
    url="https://github.com/ChangxingJiang/metasequoia-sql",
    install_requires=[],
    license="MIT License",
    packages=[package for package in find_packages() if package.startswith("metasequoia_sql")],
    platforms=["all"],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries"
    ]
)
