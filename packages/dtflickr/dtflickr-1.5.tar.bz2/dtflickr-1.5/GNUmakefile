# DT Flickr
#
# Douglas Thrift
#
# $Id: GNUmakefile 48 2010-05-05 05:50:30Z douglas $

ifeq ($(OS),Windows_NT)
setup := python setup.py
else
setup := $(CURDIR)/setup.py
endif

.PHONY: all binary build clean register source upload

all: build

binary:
ifneq ($(OS),Windows_NT)
	$(setup) bdist --formats egg upload -s
else
	$(setup) bdist_wininst -p win32 --user-access-control auto upload -s
	$(setup) bdist_wininst -p win-amd64 --user-access-control auto upload -s
endif

build:
	$(setup) build

clean:
	$(setup) clean

register:
	$(setup) register

ifneq ($(OS),Windows_NT)
source:
	$(setup) sdist --formats bztar,gztar,zip upload -s
endif
