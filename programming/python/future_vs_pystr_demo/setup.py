import setuptools
import sysconfig

if __name__ == "__main__":
    setuptools.setup(
        name="pystr_demo",
        version="0.1",
        description="Comparison matrix demo for PyStr from py3c.",
        author="Enji Cooper",
        author_email="yaneurabeya@gmail.com",
        requires=["future", "six"],
        install_requires=["py3c"],
        packages=setuptools.find_packages(),
        ext_modules=[
            setuptools.Extension(
                name="pystr_demo.c_ext",
                sources=["srcs/check_c_ext.c"],
            )
        ],
    )
