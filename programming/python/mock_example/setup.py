#!/usr/bin/env python

from setuptools import setup

setup(
    name="fizzbuzz",
    version="0.1",
    description="Example fizzbuzz app",
    author="Enji Cooper",
    author_email="yaneurabeya@gmail.com",
    packages=["fizzbuzz"],
    package_dir={
        "fizzbuzz": "src",
        "fizzbuzz.tests": "tests",
    },
    entry_points={"console_scripts": ["fizzbuzz=fizzbuzz.__main__:main"]},
    install_requires=[
        "future",
        "typing;python_version<'3'",
    ],
    test_suite="fizzbuzz.tests",
    tests_require=[
        "mock;python_version<'3'",
    ]
)
