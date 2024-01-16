# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="forticare",
    version="0.2.0",
    description="Fortinet FortiCare Python SDK",
    long_description=readme,
    author="Charles Prevot",
    author_email="charles.prevot@quib-it.com",
    url="https://github.com/cprevot93/forticare.git",
    license=license,
    packages=find_packages(exclude=("tests", "docs")),
)
