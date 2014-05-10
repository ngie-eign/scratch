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

from .util import (
    mkdir_p,
    rm,
)


def decompress(decompress_callback, srcfile, destdir, keep=True):
    mkdir_p(destdir)

    path_without_ext = os.path.splitext(srcfile)[0]
    destfile = os.path.join(destdir, os.path.basename(path_without_ext))
    with tempfile.NamedTemporaryFile(delete=False, dir=destdir) as tmpfile:
        try:
            decompress_callback(srcfile, tmpfile.name)
            rm(destfile)
            shutil.move(tmpfile.name, destfile)
        except:
            os.remove(tmpfile.name)
            raise

    if not keep:
        os.remove(srcfile)


def extract(extract_callback, srcfile, destdir, keep=True):
    mkdir_p(destdir)

    old_cwd = os.getcwd()
    temporary_directory = os.path.abspath(tempfile.mkdtemp(dir=destdir))
    try:
        extract_callback(srcfile, temporary_directory)
        os.chdir(temporary_directory)
        try:
            for path in os.listdir('.'):
                destpath = os.path.join('..', os.path.basename(path))
                rm(destpath)
                if os.path.isdir(path):
                    shutil.move(path, destpath)
                else:
                    os.rename(path, destpath)
        finally:
            os.chdir(old_cwd)
    finally:
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


def decompress_lzma(*args, **kwargs):
    decompress(decompress_lzma_callback, *args, **kwargs)


def decompress_lzma_callback(srcfile, destfile):
    with lzma.open(srcfile) as fd:
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
    decompressors.update({
        '.lzma': decompress_lzma,
        '.xz': decompress_lzma,
    })

    extractors.update({
        '.tar.xz': extract_tar,
    })
