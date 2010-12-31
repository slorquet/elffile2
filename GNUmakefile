#!/usr/bin/make -f
#
# Copyright 2010 K. Richard Pixley.
# See LICENSE for details.
#
# Time-stamp: <30-Dec-2010 19:17:03 PST by rich@noir.com>

# FIXME: is there a way to force dependencies to be installed before
# building through distutils/setuptools/distribute?  Akin to "apt-get
# build-dep".

default: all
unamem := $(shell uname -m)
unames := $(shell uname -s)

packagename := elffile

#venvopts := --distribute
venvsuffix := 

ifeq (${unames},Darwin)
pyver := 2.7
virtualenv := /Library/Frameworks/Python.framework/Versions/${pyver}/bin/virtualenv
#virtualenv := /usr/local/bin/virtualenv-${pyver}
else
ifeq (${unames},Linux)
pyver := 2.6
virtualenv := virtualenv
else
$(error Unrecognized system)
endif
endif

vpython := python${pyver}
#virtualenv := virtualenv5

venv := ${packagename}-dev
pythonbin := ${venv}/bin
python := ${pythonbin}/python

activate := . ${pythonbin}/activate
setuppy := ${activate} && python setup.py

nose_egg := ${venv}/lib/${vpython}/site-packages/nose-1.0.0-py${pyver}.egg
sphinx_egg := ${venv}/lib/${vpython}/site-packages/Sphinx-1.0.5-py${pyver}.egg
coding_egg := ${venv}/lib/${vpython}/site-packages/coding-0.001-py${pyver}.egg

ve = ${python} ${nose_egg} ${sphinx_egg}

all: develop

nose: ${nose_egg}
${nose_egg}: ${python}
	: ${python}
	: ${nose_egg}
	${pythonbin}/easy_install -U nose

sphinx: ${sphinx_egg}
${sphinx_egg}: ${python}
	${pythonbin}/easy_install -U sphinx

coding: ${coding_egg}
${coding_egg}: ${python}
	${pythonbin}/easy_install -U coding

.PHONY: ve
ve: ${python}
${python}: #.stamp-virtualenv
	${virtualenv} -p ${vpython} --no-site-packages ${venvopts} ${venv}
	${activate} && python distribute_setup.py

.stamp-virtualenv: #.stamp-apt:
	#sudo apt-get install --yes ${DEBIANS}
	touch $@-new && mv $@-new $@

clean: clean_docs
	rm -rf ${venv} .stamp-virtualenv .stamp-apt build dist ${packagename}.egg-info ${packagename}/*.pyc apidocs *.egg *.pyc distribute-*.tar.gz

.PHONY: check
check: ${python} ${nose_egg}
	#${activate} && nosetests
	${setuppy} nosetests

.PHONY: sdist
sdist: ${ve}
	${setuppy} sdist

.PHONY: bdist
bdist: ${ve}
	${setuppy} bdist

.PHONY: develop
develop: ${venv}/lib/${vpython}/site-packages/${packagename}.egg-link

${venv}/lib/${vpython}/site-packages/${packagename}.egg-link: ${python} ${coding_egg} ${nose_egg}
	${setuppy} develop

.PHONY: bdist_upload
bdist_upload: ${python} 
	${setuppy} bdist_egg upload

.PHONY: sdist_upload
sdist_upload: ${ve}
	${setuppy} sdist upload

.PHONY: register
register: ${python}
	${setuppy} $@

.PHONY: bdist_egg
bdist_egg: ${ve}
	${setuppy} $@

doctrigger = docs/build/html/index.html

.PHONY: docs
docs: ${doctrigger} develop
clean_docs:; (cd docs && $(MAKE) clean)

${doctrigger}: ${sphinx_egg} docs/source/index.rst ${packagename}.py docs/source/conf.py
	(cd docs && $(MAKE) html)

.PHONY: install
install: ${python}
	${setuppy} $@

.PHONY: nosetests
nosetests: develop ${nose_egg}
	${setuppy} $@

.PHONY: test
test: ${python}
	${setuppy} $@

.PHONY: upload_docs
upload_docs: ${doctrigger} 
	${setuppy} $@
