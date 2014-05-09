#!/usr/bin/env python
"""
A generalized decompressor/extractor script

This is useful in cases when bsdtar/libarchive isn't present as it
automatically determines the appropriate format for extracting files.

Originally written against Python 2.7.5.

...moduleauthor: Garrett Cooper
...date: May 2014
"""

import sys

if sys.version_info < (2, 7):
    sys.exit('This script is only supported on 2.7+')

import bz2
import gzip
try:
    import lzma
    HAS_LZMA = True
except ImportError:
    HAS_LZMA = False
import os
import shutil
import tarfile
import tempfile
import zipfile


def rm(path):
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except:
            os.remove(path)


def decompress(decompress_callback, srcfile, destdir, keep=True):
    if not os.path.isdir(destdir):
        os.makedirs(destdir)

    path_without_ext = os.path.splitext(srcfile)[0]
    destfile = os.path.join(destdir, os.path.basename(path_without_ext))
    with tempfile.NamedTemporaryFile(delete=False, dir=destdir) as tmpfile:
        try:
            decompress_callback(srcfile, tmpfile.name)
            rm(destfile)
            shutil.move(tmpfile.name, destfile)
        except Exception as e:
            rm(tmpfile.name)

    if not keep:
        os.remove(srcfile)


def extract(extract_callback, srcfile, destdir, keep=True):
    if not os.path.isdir(destdir):
        os.makedirs(destdir)
    temporary_directory = os.path.abspath(tempfile.mkdtemp(dir=destdir))
    old_cwd = os.getcwd()
    try:
        extract_callback(srcfile, temporary_directory)
        os.chdir(temporary_directory)
        for path in os.listdir('.'):
            destpath = os.path.join('..', os.path.basename(path))
            rm(destpath)
            if os.path.isdir(path):
                shutil.move(path, destpath)
            else:
                os.rename(path, destpath)
    finally:
        os.chdir(old_cwd)
        shutil.rmtree(temporary_directory)

    if not keep:
        os.remove(srcfile)


def decompress_bz2(*args, **kwargs):
    decompress(decompress_bz2_callback, *args, **kwargs)


def decompress_bz2_callback(srcfile, destfile):
    fd = bz2.BZ2File(srcfile)
    try:
        with open(destfile, 'w+b') as destfd:
            destfd.write(fd.read())
    finally:
        fd.close()


def decompress_gz(*args, **kwargs):
    decompress(decompress_gz_callback, *args, **kwargs)


def decompress_gz_callback(srcfile, destfile):
    with gzip.open(srcfile) as fd:
        with open(destfile, 'w+b') as destfd:
            destfd.write(fd.read())


def extract_tar(*args, **kwargs):
    extract(extract_tar_callback, *args, **kwargs)


def extract_tar_callback(srcfile, destdir):
    with tarfile.open(srcfile, 'r', errorlevel=1) as tf:
        tf.extractall(destdir)


def extract_zip(*args, **kwargs):
    extract(extract_zip_callback, *args, **kwargs)


def extract_zip_callback(srcfile, destdir):
    with zipfile.ZipFile(srcfile, 'r') as zf:
        zf.extractall(destdir)


decompressors = {
    '.bz2': decompress_bz2,
    '.gz': decompress_gz,
}


extractors = {
    '.tar': extract_tar,
    '.tar.bz2': extract_tar,
    '.tbz2': extract_tar,
    '.tgz': extract_tar,
    '.tar.gz': extract_tar,
    '.zip': extract_zip,
}


if HAS_LZMA:

    def decompress_lzma(*args, **kwargs):
        decompress(decompress_lzma_callback, *args, **kwargs)

    def decompress_lzma_callback(srcfile, destfile):
        with lzma.open(srcfile) as fd:
            with open(destfile, 'w+b') as destfd:
                destfd.write(fd.read())

    decompressors.update({
        '.lzma': decompress_lzma,
        '.xz': decompress_lzma,
    })
    extractors.update({
        '.tar.xz': extract_tar,
    })


def main(argv=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--keep', action='store_true')

    parser.add_argument('filename')
    parser.add_argument('destdir')

    args = parser.parse_args()

    filename = args.filename
    rest, ext = os.path.splitext(filename)

    for extractor in [extractor for ext, extractor in extractors.items()
                      if filename.endswith(ext)]:
        extractor(filename, args.destdir, keep=args.keep)
        sys.exit(0)

    for decompressor in [decompressor for ext, decompressor in
                         decompressors.items()
                         if filename.endswith(ext)]:
        decompressor(filename, args.destdir, keep=args.keep)
        sys.exit(0)

    sys.exit('Unsupported file: %s' % (filename, ))


if __name__ == '__main__':
    main()
