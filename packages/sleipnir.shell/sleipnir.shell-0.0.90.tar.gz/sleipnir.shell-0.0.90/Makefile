# -*- mode:makefile -*-
# Sleipnir - A solution for mass delivery of consumer products.
# Copyright (C) 2010, 2011 Carlos Martín <cmartin@liberalia.net>

# this makefile is based on the one founded into gpodder app.

PYTHON:=$(shell which python)
SHELLPATH:=$(PWD)/src/sleipnir/shell

PROJECT=$(shell export PYTHONPATH=${SHELLPATH}; ${PYTHON} -c "import constants; print constants.__namespace__")
VERSION=$(shell export PYTHONPATH=${SHELLPATH}; ${PYTHON} -c "import constants; print constants.__version__")
RELEASE=$(shell export PYTHONPATH=${SHELLPATH}; ${PYTHON} -c "import constants; print constants.__release__")
PKGNAME=$(shell export PYTHONPATH=${SHELLPATH}; ${PYTHON} -c "import constants; print constants.__appname__.lower()")
BINNAME=$(shell export PYTHONPATH=${SHELLPATH}; ${PYTHON} -c "import constants; print constants.__namespace__")


# Common directories
DESTDIR=/
RESOURCES_DIR=data
PO_DIR=$(RESOURCES_DIR)/po

# i10n suport
MESSAGESPOT=$(RESOURCES_DIR)/messages.pot
UIFILES=$(wildcard data/ui/desktop/*.ui)
UIFILES_H=$(subst .ui,.ui.h,$(UIFILES))
TRANSLATABLE_SOURCE=$(wildcard src/$(PROJECT)/*.py src/$(PROJECT)/lib/*.py)

# where's python
PYTHON=$(shell which python)
BINFILE=$(CURDIR)/src/$(PROJECT)/bin/$(BINNAME)
PYTHONPATH=$(PWD)/src/$(shell for EGG in `ls -d *.egg`; do TEMP=$$TEMP:$$PWD/$$EGG; done; echo $$TEMP)

all: help
help:
	@echo "make clean       - Get rid of scratch and byte files"
	@echo "make distclean   - Do a 'make clean' + remove 'dist/'"
	@echo "make headlink    - Print URL for the current Git head"
	@echo "make install     - Install on local system"
	@echo "make lint        - Check for coding standard violations & flakes"
	@echo "make messages    - Update messages.pot + .po files + .mo files"
	@echo "make release     - Create source tarball in 'dist/'"
	@echo "make releasetest - Run some tests before the release"
	@echo "make test        - Run $(PKGNAME) in local directory"
	@echo "make unittest    - Run doctests + unittests"

test:
	@echo -ne '\033]0;$(BINNAME)/QML console\007'
	-@COVERAGE=`which coverage 2>/dev/null`; 			 \
	[ -f $$COVERAGE ] && COVERAGE="$$COVERAGE run --branch --timid"; \
	echo $$COVERAGE `basename $(BINFILE)` --profile --verbose;	 \
	export PYTHONPATH=$(PYTHONPATH) && $$COVERAGE $(BINFILE) --profile --verbose

unittest:
	$(PYTHON) setup.py test

release: distclean
	$(PYTHON) setup.py sdist $(COMPILE)

releasetest: unittest
	desktop-file-validate $(RESOURCES_DIR)/$(PROJECT).desktop
	make -C $(PO_DIR) validate

# Internationalization Support

messages: $(MESSAGESPOT)
	make -C $(PO_DIR)

$(RESOURCES_DIR)/ui/%.ui.h: $(UIFILES)
	intltool-extract --quiet --type=gettext/glade $(subst .ui.h,.ui,$@)

$(MESSAGESPOT): $(TRANSLATABLE_SOURCE) $(UIFILES_H) $(BINFILE)
	xgettext -k_:1 -kN_:1 -kN_:1,2 -o $(MESSAGESPOT) $(TRANSLATABLE_SOURCE) $(UIFILES_H) $(BINFILE)

# This only works in a Git working commit, and assumes that the local Git
# HEAD has already been pushed to the main repository. It's mainly useful
# for the maintainer to quickly generate a commit link that can be
# posted online in bug trackers and mailing lists.
headlink:
	@echo http://git.liberalia.net/git/commit/`git show-ref HEAD | head -c8`

install: messages
	$(PYTHON) setup.py install --root=$(DESTDIR) $(COMPILE)

clean:
	@rm -rf MANIFEST build/ .coverage htmlcov/ 	\
	  src/$(PKGNAME).egg-info/ .profile locale/ 	\
	  $(PO_DIR)/$(PROJECT).pot
	@find . -name '*.py[oc]' -exec rm {} \;
	@find . -name '*.ui.h' -exec rm {} \;
	@find . -name '*~' -exec rm {} \;
	$(PYTHON) setup.py clean

distclean: clean
	rm -rf dist

# Check for common & easily catchable Python mistakes.
# Ignore the exit code in pyflakes, so 
# that pep8 is always run when "make lint"
pyflakes:
	-@PYFLAKES=`which pyflakes 2>/dev/null`;	\
	[ -f $$PYFLAKES ] && $$PYFLAKES src/$(PKGNAME)

# Check for coding standard violations.
pep8:
	-@PEP8=`which pep8 2>/dev/null`;		\
	if [ -f $$PEP8 ]; then				\
	    find . -name '*.py' -print0 | xargs -0 	\
		$$PEP8 --ignore E221,E222 --repeat;	\
	    find . -name '*.py' -print0 | xargs -0 	\
		$$PEP8 --ignore E221,E222 --statistics;	\
	fi

# Build API documentation.
apidocs:
	pydoctor --add-package $(PROJECT) 		\
		 --make-html --html-output=doc/api 	\
		 --project-name=$(PROJECT)

edit-apidocs:
	pydoctor --add-package $(PROJECT) 		\
		 --make-html --html-output=doc/api 	\
		 --project-name=$(PROJECT)		\
		 --verbose-about=epydoc2stan2 		\
		 --verbose-about=epydoc2stan2 		\
		 --verbose-about=server 		\
		 --verbose-about=server --local-only 	\
		 --server --edit

# Check for coding standard violations & flakes.
lint: pyflakes pep8

.PHONY: all test unittest release releasetest install 	\
	manpage clean distclean messages help headlink 	\
	lint pyflakes pep8 
