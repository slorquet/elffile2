#!/usr/bin/make -f
#
# Copyright © 2010 - 2011, 2013 K Richard Pixley
#
# See LICENSE for details.
#
# Time-stamp: <30-Jun-2013 19:50:42 PDT by rich@noir.com>

default: all
unames := $(shell uname -s)

packagename := elffile

venvsuffix := 

pyver := 2.7
vpython := python${pyver}

ifeq (${unames},Darwin)
virtualenv := /Library/Frameworks/Python.framework/Versions/${pyver}/bin/virtualenv
else
ifeq (${unames},Linux)
virtualenv := virtualenv -p ${vpython}
else
$(error Unrecognized system)
endif
endif

venvbase := ${packagename}-dev
venv := ${venvbase}-${pyver}
pythonbin := ${venv}/bin
python := ${pythonbin}/python

activate := . ${pythonbin}/activate
setuppy := ${activate} && python setup.py
pypitest := -r https://testpypi.python.org/pypi

.PHONY: ve
ve: ${python}
${python}:
	${virtualenv} --no-site-packages ${venv}
	${activate} && pip install coding

clean: clean_docs
	rm -rf ${venvbase}* .stamp-virtualenv .stamp-apt build \
		dist ${packagename}.egg-info *.pyc apidocs *.egg *~

.PHONY: check
check: develop ${nose_egg}
	${setuppy} nosetests

sdist_format := bztar

.PHONY: sdist
sdist: ${python}
	${setuppy} sdist --formats=${sdist_format}

.PHONY: bdist
bdist: ${python}
	${setuppy} bdist

.PHONY: develop
develop: ${venv}/lib/${vpython}/site-packages/${packagename}.egg-link

${venv}/lib/${vpython}/site-packages/${packagename}.egg-link: ${python} ${coding_egg} ${nose_egg}
	${setuppy} --version 
	${setuppy} lint
	${setuppy} develop

.PHONY: bdist_upload
bdist_upload: ${python} 
	${setuppy} bdist_egg upload ${pypitest}

.PHONY: sdist_upload
sdist_upload: ${python}
	${setuppy} sdist --formats=${sdist_format} upload ${pypitest}

.PHONY: register
register: ${python}
	${setuppy} $@ ${pypitest}

.PHONY: bdist_egg
bdist_egg: ${python}
	${setuppy} $@

doctrigger = docs/build/html/index.html

.PHONY: docs
docs: ${doctrigger}
clean_docs:; (cd docs && $(MAKE) clean)

${doctrigger}: docs/source/index.rst ${packagename}.py
	${setuppy} build_sphinx
	#(cd docs && $(MAKE) html)

.PHONY: lint
lint: ${python}
	${setuppy} $@

.PHONY: build_sphinx
build_sphinx: ${python}
	${setuppy} $@

.PHONY: install
install: ${python}
	${setuppy} $@

.PHONY: nosetests
nosetests: develop ${nose_egg}
	${setuppy} $@

.PHONY: test
test: ${python}
	${setuppy} $@

.PHONY: docs_upload upload_docs
upload_docs docs_upload: ${doctrigger}
	${setuppy} upload_docs ${pypitest}

supported_versions := \
	2.6 \
	2.7 \
	3.0 \
	3.1 \
	3.2 \
	3.3 \

bigcheck: ${supported_versions:%=bigcheck-%}
bigcheck-%:; $(MAKE) pyver=$* check

bigupload: register sdist_upload ${supported_versions:%=bigupload-%} docs_upload
bigupload-%:; $(MAKE) pyver=$* bdist_upload
