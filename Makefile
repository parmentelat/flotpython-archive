# -*- coding: utf-8 -*-

# all files in this repo are expected to be utf-8
# for transcoding, use e.g. 
#     recode ISO-8859-15..UTF-8 <filename>

all: 

WEEKS=$(wildcard W?) 

# for phony targets
force:

#
# rough index based on the *SUMMARY.txt
# I need to set LC_ALL otherwise grep misreads line with accents and gives truncated results
INDEX_POST= sed -e 's,\(\#\# Vid\),========== \1,'

index: force
	export LC_ALL=en_US.ISO8859-15;\
	for s in $(WEEKS); do echo ==================== $$s; \
	    ls $$s/C012AL*SUMMARY.txt | xargs egrep '(^C[0O]12AL.*txt|^NIVEAU|^\#\# Vid|^OK|^TODO|^ONGO|^NICE|^DROP)' | $(INDEX_POST) ; \
	    echo ""; \
	    echo ""; \
	    echo ""; \
	done > index.long

all: index

#
# builds a html index of the ipynb files expected to be reachable on connect.inria.fr
# pthierry is built-in 
connect: connect.html

connect.html: force
	tools/nbindex.py

all: connect

#
tags: force
	git ls-files | xargs etags

# run nbnorm on all notebooks
norm normalize: normalize-notebook normalize-quiz

# add the --sign option only on Thierry's macos to reduce noise-only changes
NORM = tools/nbnorm.py
#UNAME := $(shell uname)
#ifeq ($(UNAME),Darwin)
#NORM_OPTIONS = --sign
#endif

normalize-nb normalize-notebook: force
	find W[0-9]* -name '*.ipynb' | fgrep -v '/.ipynb_checkpoints/' | xargs $(NORM) $(NORM_OPTIONS)

normalize-quiz: force
	find W[0-9]* -name '*.quiz' | xargs tools/quiznorm.py

all: norm

#
CLEAN_FIND= -name '*~' -o -name '.\#*' -o -name '*pyc'

toclean: force
	find . $(CLEAN_FIND) -print0 | xargs -0 ls

clean:: force
	find . $(CLEAN_FIND) -name '*~' -o -name '.#*' -print0 | xargs -0 rm -f

#################### corriges
all: corr
corr corriges:
	$(MAKE) -C corriges

######################################## the markdowns and PDFs
# list of notebooks
NOTEBOOKS = $(wildcard W*/S[0-9]*.ipynb)

BRANCH=master
GITPRINT_URL_ROOT = https://gitprint.com/parmentelat/flotpython/blob/$(BRANCH)/

define week
$(subst /,,$(dir $(1)))
endef
define mybasename
$(basename $(notdir $(1)))
endef

define markdown_location
markdown/$(1)-$(2).md
endef
define mymarkdown
$(call markdown_location,$(call week,$(1)),$(call mybasename,$(1)))
endef

define gitprint_location
pdf-gitprint/$(1)-$(2).pdf
endef
define mygitprint
$(call gitprint_location,$(call week,$(1)),$(call mybasename,$(1)))
endef
define gitprint_url
$(GITPRINT_URL_ROOT)/markdown/$(1)-$(2).md?download
endef
define my_url
$(call gitprint_url,$(call week,$(1)),$(call mybasename,$(1)))
endef

define pdflatex_location
pdf-latex/$(1)-$(2).pdf
endef
define mypdflatex
$(call pdflatex_location,$(call week,$(1)),$(call mybasename,$(1)))
endef

MARKDOWNS = $(foreach notebook,$(NOTEBOOKS),$(call mymarkdown,$(notebook)))
GITPRINTS = $(foreach notebook,$(NOTEBOOKS),$(call mygitprint,$(notebook)))
PDFLATEXS = $(foreach notebook,$(NOTEBOOKS),$(call mypdflatex,$(notebook)))

# apply this rule to all notebooks
define notebook_rule
$(call mymarkdown,$(1)): $(1)
	ipython nbconvert --to markdown $(1) --stdout > $(call mymarkdown,$(1))

$(call mygitprint,$(1)): $(call mymarkdown,$(1))
	curl -o $(call mygitprint,$(1)) $(call my_url,$(1))

$(call mypdflatex,$(1)): $(1)
	(cd pdf-latex; ipython nbconvert --to latex --post pdf ../$(1); \
	mv $(call mybasename,$(1)).tex $(subst .pdf,.tex,../$(call mypdflatex,$(1))); \
	mv $(call mybasename,$(1)).pdf ../$(call mypdflatex,$(1)))
endef

$(foreach notebook,$(NOTEBOOKS),$(eval $(call notebook_rule,$(notebook))))

all: md
md markdown: $(MARKDOWNS)

# these need to be done AFTER the markdown have been pushed up to github 
gitprint: $(GITPRINTS)

# the cool thing with this process is we do not need to commit to github first
pdflatex: $(PDFLATEXS)

# not sure this really is helpful but well
pdf: pdflatex gitprint

.PHONY: all md markdown gitprint corr corriges pdflatex pdf
