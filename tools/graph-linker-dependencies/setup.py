#!/usr/bin/env python3

import platform
import sys
from setuptools import find_packages
from setuptools import setup


osname = platform.system().lower()
if osname not in "freebsd":
    sys.exit("This package only works on FreeBSD.")

GLD = "graph_linker_dependencies"

setup(
    name="graph_linker_dependencies",
    version="0.1",
    description="Tool for graphing FreeBSD linker dependencies.",
    author="Enji Cooper",
    author_email="yaneurabeya@gmail.com",
    url="https://github.com/ngie-eign/scratch",
    include_package_data=True,
    packages=find_packages(where="src"),
    package_data={f"{GLD}": ["templates/*.pyt"]},
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            f"create_link_dependency_graph={GLD}.create_link_dependency_graph:main"
        ]
    },
    requirements=["jinja2"],
)
