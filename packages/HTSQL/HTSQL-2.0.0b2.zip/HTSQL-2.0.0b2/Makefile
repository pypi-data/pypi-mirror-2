# This makefile provides various build, installation and testing tasks.

.PHONY: default build install develop doc dist windist pypi \
	test cleanup train train-ctl train-sqlite train-pgsql purge-test


# Load configuration variables from `Makefile.env`.  There is a sample
# file `Makefile.env.sample`; copy it to `Makefile.env` and edit it
# to match your configuration.
-include Makefile.env


#
# The default task.
#

# Display the list of available targets.
default:
	@echo "Run 'make <target>', where <target> is one of:"
	@echo
	@echo "  *** Building and Installation ***"
	@echo "  build: to build the HTSQL packages"
	@echo "  install: to install the HTSQL packages"
	@echo "  develop: to install the HTSQL packages in the development mode"
	@echo "  doc: to build the HTSQL documentation"
	@echo "  dist: to build a source and an EGG distribution"
	@echo "  pypi: to register and upload the package to PyPI"
	@echo
	@echo "  *** Regression Testing ***"
	@echo "  test: to run HTSQL regression tests"
	@echo "  cleanup: to drop users and databases deployed by regression tests"
	@echo "  train: to run all HTSQL tests in the train mode"
	@echo "  train-ctl: to run tests for htsql-ctl routines in the train mode"
	@echo "  train-sqlite: to run SQLite-specific tests in the train mode"
	@echo "  train-pgsql: to run PostgreSQL-specific tests in the train mode"
	@echo "  purge-test: to purge state test output data"
	@echo
	@echo "  *** Shell and Server ***"
	@echo "  shell-sqlite: to start an HTSQL shell on the SQLite test database"
	@echo "  shell-pgsql: to start an HTSQL shell on the PostgreSQL test database"
	@echo "  serve-sqlite: to start an HTTP server on the SQLite test database"
	@echo "  serve-pgsql: to start an HTTP server on the PostgreSQL test database"
	@echo


#
# Building and installation tasks.
#

# Build the HTSQL packages.
build:
	python setup.py build

# Install the HTSQL packages.
install:
	python setup.py install

# Install the HTSQL packages in the development mode.
develop:
	python setup.py develop

# Build the HTSQL documentation.
doc:
	sphinx-build -b html doc build/doc

# Build a source and an EGG distributions.
# FIXME: include HTML documentation; `dist_dir` is broken for `--bdist-deb`.
# Note that `bdist_deb` requires `stdeb` package.
dist:
	rm -rf build
	python setup.py sdist
	python setup.py bdist_egg
	#python setup.py --command-packages=stdeb.command bdist_deb 

# Register and upload the package to PyPI.
# FIXME: include HTML documentation.
pypi:
	rm -rf build
	python setup.py register sdist bdist_egg upload

#
# Regression testing tasks.
#

# Run HTSQL regression tests.
test:
	htsql-ctl regress -i test/regress.yaml -q

# Drop any users and databases deployed by the regression tests.
cleanup:
	htsql-ctl regress -i test/regress.yaml -q cleanup-pgsql cleanup-sqlite

# Run HTSQL regression tests in the train mode.
train:
	htsql-ctl regress -i test/regress.yaml --train

# Run regression tests for htsql-ctl routines in the train mode.
train-ctl:
	htsql-ctl regress -i test/regress.yaml --train ctl

# Run SQLite-specific regression tests in the train mode.
train-sqlite:
	htsql-ctl regress -i test/regress.yaml --train sqlite

# Run PostgreSQL-specific regression tests in the train mode.
train-pgsql:
	htsql-ctl regress -i test/regress.yaml --train pgsql

# Purge stale output records from HTSQL regression tests.
purge-test:
	htsql-ctl regress -i test/regress.yaml -q --train --purge


#
# Shell and server tasks.
#

# The connection URI for regression databases.
SQLITE_REGRESS_DB?=sqlite:///build/regress/regress-sqlite/htsql_regress.sqlite
PGSQL_ADDRESS?=${PGSQL_HOST}$(if ${PGSQL_PORT},:${PGSQL_PORT})
PGSQL_REGRESS_DB?=pgsql://htsql_regress:secret@${PGSQL_ADDRESS}/htsql_regress

# The HTTP server address.
HTSQL_HOST?=localhost
HTSQL_PORT?=8080

# Start an HTSQL shell on the SQLite regression database.
shell-sqlite:
	htsql-ctl shell ${SQLITE_REGRESS_DB}

# Start an HTSQL shell on the PostgreSQL regression database.
shell-pgsql:
	htsql-ctl shell ${PGSQL_REGRESS_DB}

# Start an HTTP/HTSQL server on the SQLite regression database.
serve-sqlite:
	htsql-ctl serve ${SQLITE_REGRESS_DB} ${HTSQL_HOST} ${HTSQL_PORT}

# Start an HTTP/HTSQL server on the PostgreSQL regression database.
serve-pgsql:
	htsql-ctl serve ${PGSQL_REGRESS_DB} ${HTSQL_HOST} ${HTSQL_PORT}


