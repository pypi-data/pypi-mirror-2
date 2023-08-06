#
# Copyright (c) 2006-2011, Prometheus Research, LLC
# See `LICENSE` for license information, `AUTHORS` for the list of authors.
#

# The setup script for HTSQL; requires setuptools to run.
#
# Type `python setup.py install` to install HTSQL, or see `INSTALL`
# for the list of prerequisites and detailed installation instructions.

from setuptools import setup, find_packages
import os.path

# We use the merged content of `README`, `INSTALL`, and `NEWS` as the
# long description of the package.

root = os.path.dirname(__file__)
README = open(os.path.join(root, 'README')).read()
INSTALL = open(os.path.join(root, 'INSTALL')).read()
NEWS = open(os.path.join(root, 'NEWS')).read()

# The distutils parameters are defined here.  Do not forget to update
# the `__version__` attribute in `src/htsql/__init__.py` and `version`
# and `release` attributes in `doc/conf.py` any time the `VERSION`
# parameter is updated here.

NAME = "HTSQL"
VERSION = "2.1.0rc1"
DESCRIPTION = "Query language for the accidental programmer"
LONG_DESCRIPTION = "\n".join([README, INSTALL, NEWS])
AUTHOR = "Clark C. Evans and Kirill Simonov; Prometheus Research, LLC"
AUTHOR_EMAIL = "cce@clarkevans.com"
LICENSE = "Free To Use But Restricted"
PLATFORMS = "Any"
URL = "http://htsql.org/"
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Intended Audience :: Science/Research",        
    "License :: Free To Use But Restricted",
    "License :: Other/Proprietary License",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.5",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: SQL",
    "Topic :: Database :: Front-Ends",
    "Topic :: Internet :: WWW/HTTP :: WSGI",
    "Topic :: Software Development :: Libraries",
]
KEYWORDS = "sql http uri relational database"
PACKAGES = find_packages('src')
PACKAGE_DIR = {'': 'src'}
INCLUDE_PACKAGE_DATA = True
ZIP_SAFE = False
ENTRY_POINTS = {
    'console_scripts': ['htsql-ctl = htsql.ctl:main'],
    'htsql.addons': [
        'htsql.core = htsql.export:HTSQL_CORE',
        'engine.sqlite = htsql_sqlite.export:ENGINE_SQLITE',
        'engine.pgsql = htsql_pgsql.export:ENGINE_PGSQL',
        'engine.postgres = htsql_pgsql.export:ENGINE_PGSQL',
        'engine.mysql = htsql_mysql.export:ENGINE_MYSQL',
        'engine.oracle = htsql_oracle.export:ENGINE_ORACLE',
        'engine.mssql = htsql_mssql.export:ENGINE_MSSQL',
        'tweak.pgsql.timeout'
            ' = htsql_tweak.pgsql_timeout.export:TWEAK_PGSQL_TIMEOUT',
        'tweak.autolimit = htsql_tweak.autolimit.export:TWEAK_AUTOLIMIT',
        'tweak.schema = htsql_tweak.schema.export:TWEAK_SCHEMA',
        'tweak.cors = htsql_tweak.cors.export:TWEAK_CORS',
        'tweak.pgsql.catalog'
            ' = htsql_tweak.pgsql_catalog.export:TWEAK_PGSQL_CATALOG',
        'tweak.pgsql.view'
            ' = htsql_tweak.pgsql_view.export:TWEAK_PGSQL_VIEW',
        'tweak.pgsql.inet'
            ' = htsql_tweak.pgsql_inet.export:TWEAK_PGSQL_INET',
    ],
}
INSTALL_REQUIRES = [
    'setuptools>=0.6c9',
    'pyyaml>=3.07',
#    'psycopg2>=2.0.10',
#    'MySQL-python>=1.2.2',
#    'cx_Oracle>=5.0',
#    'pymssql>=1.0.2',
]

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      platforms=PLATFORMS,
      url=URL,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      packages=PACKAGES,
      package_dir=PACKAGE_DIR,
      include_package_data=INCLUDE_PACKAGE_DATA,
      zip_safe=ZIP_SAFE,
      entry_points=ENTRY_POINTS,
      install_requires=INSTALL_REQUIRES,
)


