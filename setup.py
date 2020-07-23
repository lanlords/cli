# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="HelloWorld",
    version="1.0",
    description="CLI to manage Lanlords infrastructure",
    long_description=readme,
    url="https://github.com/lanlords/cli",
    license=license,
    install_requires=["click"],
    entry_points="""
        [console_scripts]
        hello=hello:cli
    """,
)
