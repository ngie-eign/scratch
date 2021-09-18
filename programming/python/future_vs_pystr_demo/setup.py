import os.path
import setuptools
import site
import sys
import sysconfig


try:
    prefix = os.path.commonprefix([site.getsitepackages()[-1], sys.executable])
except AttributeError:
    prefix = site.PREFIXES[-1]
site_includedir = os.path.join(prefix, "include", "site", "python{}".format(sysconfig.get_python_version()))


if __name__ == "__main__":
    setuptools.setup(
        name="pystr_demo",
        version="0.1",
        description="Comparison matrix demo for PyStr from py3c.",
        author="Enji Cooper",
        author_email="yaneurabeya@gmail.com",
        requires=["future", "six"],
        build_requires=["py3c"],
        ext_modules=[
            setuptools.Extension(
                include_dirs=[site_includedir],
                name="pystr_demo_c_ext",
                sources=["srcs/check_c_ext.c"],
            )
        ],
    )
