# -*- coding: utf-8 -*-

# all files in this repo are expected to be utf-8
# for transcoding, use e.g. 
#     recode ISO-8859-15..UTF-8 <filename>

all: 
.PHONY: all

WEEKS=$(wildcard W?) 

# for phony targets
force:

#
tags: force
	git ls-files | xargs etags
.PHONY: tags

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

.PHONY: norm normalize normalize-nb normalize-notebook normalize-quiz

#
CLEAN_FIND= -name '*~' -o -name '.\#*' -o -name '*pyc'

toclean: force
	find . $(CLEAN_FIND) -print0 | xargs -0 ls

clean:: force
	find . $(CLEAN_FIND) -name '*~' -o -name '.#*' -print0 | xargs -0 rm -f

#################### corriges
all: corriges
corriges:
	$(MAKE) -C corriges

corriges-pdf:
	$(MAKE) -C corriges pdf

corriges-clean:
	$(MAKE) -C corriges clean

.PHONY: corriges corriges-pdf corriges-clean 

########################################
# historical note
# students asked for an alternate format for notebooks
# (*) at the beginning we went for a PDF approach, generating
# markdown and then using gitprint
# this resulted in a lot of approximate - if at all correct - output
# (*) I then tried to use latex -> pdf, which is better now that
# we don't use rawnbconvert anymore; result was more reliable,
# but really not nice to look at - in other words
# it would require a lot of styling, I'm thinking
# a complete latex document class to have something decent
# (*) so finally I came to consider html output as the most
# reliable + pretty-to-look-at approach
#
# as of June 19 2015:
# * I remove all by-products from git (be it pdf, html or markdown)
# this was suboptimal as these files can be generated from the rest of the git contents
# * I remove the make recipes for producing pdf, either based on pdflatex or gitprint
# let's keep it simple (it's already a mess like this)

########################################

# list of notebooks
NOTEBOOKS = $(wildcard W*/W*S[0-9]*.ipynb)

# simple basename
define sbn
$(basename $(notdir $(1)))
endef

define markdown_location
markdown/$(call sbn,$(1)).md
endef

define html_location
html/$(call sbn,$(1)).html
endef

define ipynb_location
ipynb/$(call sbn,$(1)).ipynb
endef

MARKDOWNS = $(foreach notebook,$(NOTEBOOKS),$(call markdown_location,$(notebook)))
HTMLS	  = $(foreach notebook,$(NOTEBOOKS),$(call html_location,$(notebook)))
IPYNBS	  = $(foreach notebook,$(NOTEBOOKS),$(call ipynb_location,$(notebook)))

########## how to redo individual stuff
# apply this rule to all notebooks
define notebook_rule
$(call markdown_location,$(1)): $(1)
	ipython nbconvert --to markdown $(1) --stdout > $(call markdown_location,$(1))

$(call html_location,$(1)): $(1)
	ipython nbconvert --to html $(1) --stdout > $(call html_location,$(1))

$(call ipynb_location,$(1)): $(1)
	(mkdir -p ipynb; cd ipynb; ln -f -s ../$(1) $(notdir $(1)))

# redo all targets about one notebook
# e.g make -n W1-S2-C1-accents
$(call sbn,$(1)): $(call markdown_location,$(1)) $(call html_location,$(1))

.PHONY: $(call sbn,$(1))
endef

$(foreach notebook,$(NOTEBOOKS),$(eval $(call notebook_rule,$(notebook))))

#################### markdown
md markdown: $(MARKDOWNS)

md-clean markdown-clean:
	rm -f markdown/*.md

.PHONY: md markdown md-clean markdown-clean
all: md

#################### html
html: $(HTMLS)

html-clean:
	rm -f html/*.html

.PHONY: html html-clean
all: html

#################### ipynb
ipynb: force
	@mkdir -p ipynb; echo populating ipynb with notebooks from 'W*'
	@rsync -aL $(NOTEBOOKS) ipynb
	@mkdir -p ipynb/corrections; echo syncing modules/corrections onto ipynb/corrections
	@rsync -a $$(git ls-files modules/corrections) ipynb/corrections
	@mkdir -p ipynb/data; echo syncing data onto ipynb/data
	@rsync -a $$(git ls-files data) ipynb/data
	@mkdir -p ipynb/media; echo syncing media onto ipynb/media
	@rsync -a $$(git ls-files media) ipynb/media

ipynb-clean:
	rm -rf ipynb

.PHONY: ipynb ipynb-clean

####################
# xxx misses ipynb ?
out: html markdown ipynb
out-clean: html-clean markdown-clean ipynb-clean

.PHONY: out out-clean
############################## outputs : tars and export (rsync)
RSYNC_URL = tparment@srv-diana.inria.fr:/proj/planete/www/Thierry.Parmentelat/flotpython/
RSYNC	   = rsync -av --delete

TARS =

########## html
# tar
TARS += notebooks-html.tar
NOTEBOOKS-HTML = $(foreach notebook,$(NOTEBOOKS),$(call html_location,$(notebook)))
notebooks-html.tar: html
	tar -chf $@ html/custom.css $(NOTEBOOKS-HTML)

html-tar: notebooks-html.tar

# rsync
html-rsync:
	$(RSYNC) html/custom.css $(NOTEBOOKS-HTML) $(RSYNC_URL)/html/
rsync: html-rsync

.PHONY: html-tar html-rsync

########## markdown
# tar
TARS += notebooks-markdown.tar
NOTEBOOKS-MARKDOWN = $(foreach notebook,$(NOTEBOOKS),$(call markdown_location,$(notebook)))
notebooks-markdown.tar: markdown
	tar -chf $@ $(NOTEBOOKS-MARKDOWN)

markdown-tar: notebooks-markdown.tar

# rsync
markdown-rsync:
	$(RSYNC) $(NOTEBOOKS-MARKDOWN) $(RSYNC_URL)/markdown/

########## ipynb
# tar 
TARS += notebooks-ipynb.tar
NOTEBOOKS-IPYNB = $(foreach notebook,$(NOTEBOOKS),notebooks/$(call sbn,$(notebook)).ipynb)
notebooks-ipynb.tar: ipynb
	tar -chf $@ ipynb

ipynb-tar: notebooks-ipynb.tar

# rsync
ipynb-rsync:
	$(RSYNC) ipynb/ $(RSYNC_URL)/ipynb/
rsync: ipynb-rsync

.PHONY: ipynb-tar ipynb-rsync

########## corriges
# tar
TARS += corriges.tar
corriges.tar: force
	tar -cf $@ corriges/*.{pdf,txt,py}
corriges-tar: corriges.tar

# rsync
corriges-rsync:
	$(RSYNC) corriges/*.{pdf,txt,py} $(RSYNC_URL)/corriges/
rsync: corriges-rsync

.PHONY: corriges-tar corriges-rsync


##########
TGZS = $(subst .tar,.tgz,$(TARS))

%.tgz: %.tar
	gzip -c9 $*.tar > $@

all-tars.tar: $(TGZS)
	tar -cf $@ $(TGZS)

tars: $(TARS) $(TGZS) all-tars.tar

tars-clean:
	rm -f ipynb $(TARS) $(TGZS) all-tars.tar

.PHONY: tars tars-clean

# rsync the tars themselves
tars-rsync: $(TGZS)
	$(RSYNC) $(TGZS) $(RSYNC_URL)/tars/
rsync: tars-rsync

########## count stuff - essentially detect sequels in html/ or markdown/
########## that would need deletion after renamings or similar
GITCOUNT = xargs git ls-files | wc -l
COUNT    = wc -l

check: check-files check-w check-html check-markdown
# check-pdf-latex check-pdf-gitprint

check-files: force
	@echo NOTEBOOKS make variable has $(words $(NOTEBOOKS)) words

#check-nonw: force
#	@echo "allow for one more (W2/exo-sample.ipynb)"
#	ls W*/*nb | grep -v '/W' | $(GITCOUNT)

check-w: force
	ls W*/W*nb | $(GITCOUNT)

check-html: force
	ls html/W*.html | $(COUNT)

check-markdown: force
	ls markdown/W*.md | $(COUNT)

############################## textual index 
#
# rough index based on the *SUMMARY.txt
# I need to set LC_ALL otherwise grep misreads line with accents and gives truncated results
INDEX_POST= sed -e 's,\(\#\# Vid\),========== \1,'

index: force
	export LC_ALL=en_US.ISO8859-15;\
	for s in $(WEEKS); do echo ==================== $$s; \
	    ls $$s/*SUMMARY.txt | xargs egrep '(^C[0O]12AL.*txt|^NIVEAU|^\#\# Vid|^OK|^TODO|^ONGO|^NICE|^DROP)' | $(INDEX_POST) ; \
	    echo ""; \
	    echo ""; \
	    echo ""; \
	done > index.long
.PHONY: index

# all: index

#################### convenience, for debugging only
# make +foo : prints the value of $(foo)
# make ++foo : idem but verbose, i.e. foo=$(foo)
++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
