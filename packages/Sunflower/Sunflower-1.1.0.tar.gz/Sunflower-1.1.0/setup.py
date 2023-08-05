#!/usr/bin/env python

"""Sunflower: model transcription factor binding to DNA

Sunflower models the simultaneous binding of transcription factors to
DNA. It uses a hidden Markov model that resembles a sunflower.
"""

__version__ = "1.1.0"

# Copyright 2007-2009 Michael M. Hoffman <hoffman+software@ebi.ac.uk>

import sys

# required for from __future__ import division, with_statement
assert sys.version_info >= (2, 5, 1)

import os
from subprocess import check_call

from ez_setup import use_setuptools
use_setuptools()

from setuptools import Extension, find_packages, setup
from setuptools.command.install import install

# provide a missing setuptools feature
class NumpyExtension(Extension):
    def __init__(self, *args, **kwargs):
        Extension.__init__(self, *args, **kwargs)

        self._include_dirs = self.include_dirs
        del self.include_dirs # restore overwritten property

    # warning: Extension is a classic class so it's not really read-only
    @property
    def include_dirs(self):
        from numpy import get_include

        return self._include_dirs + [get_include()]

doclines = __doc__.splitlines()
name, short_description = doclines[0].split(": ")
long_description = "\n".join(doclines[2:])

url = "http://www.ebi.ac.uk/~hoffman/software/%s/" % name.lower()
download_url = "%s%s-%s.tar.gz" % (url, name, __version__)

classifiers = ["Development Status :: 2 - Pre-Alpha",
               "Environment :: Console",
               "Intended Audience :: Science/Research",
               "License :: Other/Proprietary License",
               "Natural Language :: English",
               "Operating System :: POSIX :: Linux",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering :: Bio-Informatics"]

# XXX: sql driver should have [sql] at the end so it is only loaded sometimes
entry_points = """
[console_scripts]
h5attr = sunflower.h5attr:main
h5cat = sunflower.h5cat:main
pwm2sfl = sunflower.pwm2sfl:main
sunrecompose = sunflower.recompose:main
sunflower = sunflower.simulator:main
sunreport = sunflower.report:main
sunsplit = sunflower.split:main

[sunflower.drivers]
DEFAULT = sunflower.driver.hdf5:HDF5Driver
hdf5 = sunflower.driver.hdf5:HDF5Driver
sql = sunflower.driver.sql:SQLDriver
tabdelim = sunflower.driver.tabdelim:TabDelimDriver
"""

ext_modules = [NumpyExtension("_fwd_bwd",
                              ["src/_fwd_bwd.pyx", "src/fwd_bwd.c"])]

setup_requires = ["numpy>=1.0.3"]
install_requires = ["path>=2.2", "tables>=2.0.dev",
                    "textinput>=0.1.1", "setuptools>=0.6c9"] + setup_requires

extras_require = dict(distributed=["Poly>=0.1.1"],
                      develop=["Pyrex>=0.9.5.1a"],
                      sql=["docsql"])

# XXX: remove these when the upstream packages are updated to fix these issues
dependency_links = ["http://pypi.python.org/packages/source/p/path.py/path-2.2.zip"]

# XXX: test new setuptools does not require this?
# this is a workaround of the fact that setuptools doesn't install
# things that are in setup_requires even if they are also in
# install_requires
class SubprocessEasyInstall(install):
    def run(self):
        install.run(self)

        args = [sys.executable, "-m", "easy_install"] + setup_requires
        check_call(args)

if __name__ == "__main__":
    setup(name=name,
          version=__version__,
          description=short_description,
          author="Michael Hoffman",
          author_email="hoffman+%s@ebi.ac.uk" % name.lower(),
          url=url,
          download_url=download_url,
          license="all rights reserved",
          classifiers=classifiers,
          long_description=long_description,
          dependency_links=dependency_links,
          setup_requires=setup_requires,
          install_requires=install_requires,
          extras_require=extras_require,
          zip_safe=False,

          # XXX: this should be based off of __file__ instead
          packages=find_packages("."),
          ext_package="sunflower",
          ext_modules=ext_modules,
          include_package_data=True,
          entry_points=entry_points,
    #      cmdclass=dict(install=SubprocessEasyInstall)
          )
