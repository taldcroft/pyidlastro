#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst

# Use "distribute" - the setuptools fork that supports python 3.
from distribute_setup import use_setuptools
use_setuptools()

import glob
from setuptools import setup, find_packages

from astropy import setup_helpers
from astropy.version_helper import get_git_devstr, generate_version_py

# Set affiliated package-specific settings
PACKAGENAME = 'pyidlastro'
DESCRIPTION = 'Python ports of IDL astronomy library routines'
LONG_DESCRIPTION = pyidlastro.__doc__
AUTHOR = 'Tom Aldcroft'
AUTHOR_EMAIL = 'taldcroft@gmail.com'
LICENSE = 'BSD'
URL = 'http://astropy.org'

#version should be PEP386 compatible (http://www.python.org/dev/peps/pep-0386)
version = '0.0.dev'

# Indicates if this version is a release version
release = 'dev' not in version

# Adjust the compiler in case the default on this platform is to use a
# broken one.
setup_helpers.adjust_compiler()

# Indicate that we are in building mode
setup_helpers.set_build_mode()

if not release:
    version += get_git_devstr(False)
generate_version_py(PACKAGENAME, version, release,
                    setup_helpers.get_debug_option())

# Use the find_packages tool to locate all packages and modules
packagenames = find_packages()

# Treat everything in scripts except README.rst as a script to be installed
scripts = glob.glob('scripts/*')
if 'scripts/README.rst' in scripts:
    scripts.remove('scripts/README.rst')

# Check that Numpy is installed.
# NOTE: We cannot use setuptools/distribute/packaging to handle this
# dependency for us, since some of the subpackages need to be able to
# access numpy at build time, and they are configured before
# setuptools has a chance to check and resolve the dependency.
setup_helpers.check_numpy()

# This dictionary stores the command classes used in setup below
cmdclassd = {'test': setup_helpers.setup_test_command(PACKAGENAME)}

# Additional C extensions that are not Cython-based should be added here.
extensions = []

# A dictionary to keep track of all package data to install
package_data = {PACKAGENAME: ['data/*']}

# A dictionary to keep track of extra packagedir mappings
package_dirs = {}

# Update extensions, package_data, packagenames and package_dirs from
# any sub-packages that define their own extension modules and package
# data.  See the docstring for setup_helpers.update_package_files for
# more details.
setup_helpers.update_package_files(PACKAGENAME, extensions, package_data,
                                   packagenames, package_dirs)

if setup_helpers.HAVE_CYTHON and not release:
    from Cython.Distutils import build_ext
    # Builds Cython->C if in dev mode and Cython is present
    cmdclassd['build_ext'] = build_ext

if setup_helpers.AstropyBuildSphinx is not None:
    cmdclassd['build_sphinx'] = setup_helpers.AstropyBuildSphinx


setup(name=PACKAGENAME,
      version=version,
      description=DESCRIPTION,
      packages=packagenames,
      package_data=package_data,
      package_dir=package_dirs,
      ext_modules=extensions,
      scripts=scripts,
      requires=['astropy'],
      install_requires=['astropy'],
      provides=[PACKAGENAME],
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      url=URL,
      long_description=LONG_DESCRIPTION,
      cmdclass=cmdclassd,
      zip_safe=False,
      use_2to3=True
      )
