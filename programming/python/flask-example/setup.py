#!/usr/bin/env python
#
# Python egg installer script for the frontend server
#
# @author Enji Cooper

#import glob
import os
#from stat import ST_MODE
from setuptools import setup, find_packages
#from distutils import log
#from distutils.command.install import install
import sys
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), 'frontend'))
import frontend as frontend

"""
class Install(install):
    def run(self):
        install.run(self)
        data_files = []
        for prefix, paths in self.distribution.data_files:
            data_files.extend(map(lambda path: \
                                  os.path.join(self.root + prefix,
                                               os.path.basename(path)),
                              paths))
        for file in self.get_outputs():
            if file not in data_files:
                continue
            if self.dry_run:
                log.info("changing mode of %s", file)
            else:
                mode = ((os.stat(file)[ST_MODE]) | 0555) & 07777
                log.info("changing mode of %s to %o", file, mode)
                os.chmod(file, mode)
"""

setup(
        #cmdclass={
        #    'install': Install,
        #},
        #data_files=[
        #    ('/etc/init.d', glob.glob('init.d/*')),
        #    ('/usr/local/bin/${package_name}', glob.glob('daemon/*')),
        #],
        name="Frontend server",
        version=frontend.__version__,
        description="Frontend server",
        author="Enji Cooper",
        author_email="dev@null",
        maintainer="Enji Cooper",
        maintainer_email="dev@null",
        packages=find_packages(exclude=['*test*']),
        license=frontend.__license__,
        platforms="Posix; Mac OS X",
        url="http://dev.null/",
        install_requires=['flask==0.10.1'],
)
