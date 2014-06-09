#!/usr/bin/env python

import bz2
import gzip
import tarfile
import zipfile

from .main import HAS_LZMA
if HAS_LZMA:
    import lzma
