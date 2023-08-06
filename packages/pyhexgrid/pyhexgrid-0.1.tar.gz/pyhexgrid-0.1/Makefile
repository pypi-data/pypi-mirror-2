# Makefile for python module.

SETUP = python setup.py

SRC_FORMATS = gztar,zip
BIN_FORMATS = wininst

EPYDOC = epydoc -v --no-private

.DEFAULT:;	@ $(SETUP) $@
.PHONY:		build dist

all:		build
dist:		sdist
tags:;		find . -name '*.py' | xargs etags

build:;		@ $(SETUP) $@
sdist:;		@ $(SETUP) $@ -f --formats=$(SRC_FORMATS)
bdist:;		@ $(SETUP) $@ --formats=$(BIN_FORMATS)
help:;		@ $(SETUP) --help
commands:;	@ $(SETUP) --help-commands
upload:;	@ $(SETUP) sdist upload

doc:;		$(EPYDOC) -o docs hexgrid

clean:;		rm -rf MANIFEST PKG-INFO build dist
