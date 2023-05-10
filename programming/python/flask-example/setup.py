#!/usr/bin/env python
#
# Python egg installer script for the frontend server
#
# @author Enji Cooper

from __future__ import absolute_import

import os
import sys
from setuptools import find_packages
from setuptools import setup

sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), "frontend"))

import frontend

setup(
    name="Frontend server",
    version=frontend.__version__,
    description="Frontend server",
    author="Enji Cooper",
    author_email="dev@null",
    maintainer="Enji Cooper",
    maintainer_email="dev@null",
    packages=find_packages(exclude=["*test*"]),
    license=frontend.__license__,
    platforms="Posix; Mac OS X",
    url="http://dev.null/",
    install_requires=["flask~=2.0"],
)
