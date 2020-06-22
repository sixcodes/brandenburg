from codecs import open  # To use a consistent encoding
from os import path

from setuptools import find_packages, setup  # Always prefer setuptools over distutils

here = path.abspath(path.dirname(__file__))

setup(
    name="brandenburg",
    version="0.1.0",
    description="Data Gate Project",
    long_description="",
    url="https://github.com/sixcodes/brandenburg",
    author="Jesué Junior",
    author_email="jesuesousa@gmail.com",
    license="BSD-3",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    test_suite="tests",
    install_requires=[],
)
