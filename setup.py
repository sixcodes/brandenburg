# Standard library imports
from os import path

# Third party imports
from setuptools import find_packages, setup  # Always prefer setuptools over distutils

here = path.abspath(path.dirname(__file__))

setup(
    name="brandenburg",
    version="0.2.0",
    description="Data bridge API",
    long_description="",
    url="https://github.com/sixcodes/brandenburg",
    # Author details
    author="Jesué Junior",
    author_email="opensource@sixcodes.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    test_suite="tests",
    install_requires=[],
    entry_points={},
)
