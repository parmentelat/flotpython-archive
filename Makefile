# -*- coding: utf-8 -*-

# all files in this repo are expected to be utf-8
# for transcoding, use e.g. 
#     recode ISO-8859-15..UTF-8 <filename>

RSYNC = rsync --exclude .du --exclude .DS_Store

all: 
.PHONY: all


# work on one week at a time with FOCUS=W2
FOCUS     = W?


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

# -type f : we need to skip symlinks
normalize-nb normalize-notebook: force
	find $(FOCUS) -name '*.ipynb' -type f | fgrep -v '/.ipynb_checkpoints/' | xargs $(NORM) $(NORM_OPTIONS)

normalize-quiz: force
	find $(FOCUS) -name '*.quiz' | xargs tools/quiznorm.py

all: norm

.PHONY: norm normalize normalize-nb normalize-notebook normalize-quiz

#
CLEAN_FIND= -name '*~' -o -name '.\#*' -o -name '*pyc'

junk-clean: force
	find . $(CLEAN_FIND) -name '*~' -o -name '.#*' -print0 | xargs -0 rm -f
CLEAN-TARGETS += junk-clean

#################### corriges
all: corriges
corriges:
	$(MAKE) -C corriges

corriges-pdf:
	$(MAKE) -C corriges pdf

corriges-clean:
	$(MAKE) -C corriges clean
CLEAN-TARGETS += corriges-clean

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
NOTEBOOKS = $(wildcard $(FOCUS)/W*S[0-9]*.ipynb)

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
# when converting to html and markdown, we want to have the cells executed
CONVERT = ipython nbconvert --ExecutePreprocessor.enabled=True --ExecutePreprocessor.allow_errors=True

# apply these rules to all notebooks
define notebook_rule
$(call markdown_location,$(1)): $(1)
	$(CONVERT) --to markdown $(1) --stdout > $(call markdown_location,$(1)) || rm $(call markdown_location,$(1))

$(call html_location,$(1)): $(1)
	$(CONVERT) --to html $(1) --stdout > $(call html_location,$(1)) || rm $(call html_location,$(1))

$(call ipynb_location,$(1)): $(1)
	(mkdir -p ipynb; cd ipynb; ln -f -s ../$(1) $(notdir $(1)))

# redo all targets about one notebook
# e.g make -n W1-S2-C1-accents
$(call sbn,$(1)): $(call markdown_location,$(1)) $(call html_location,$(1))

.PHONY: $(call sbn,$(1))
endef

$(foreach notebook,$(NOTEBOOKS),$(eval $(call notebook_rule,$(notebook))))

#################### markdown
markdown: $(MARKDOWNS)

markdown-clean:
	rm -f markdown/*.md
SUPERCLEAN-TARGETS += markdown-clean

.PHONY: markdown markdown-clean
all: markdown

#################### html
html: $(HTMLS) media
	$(RSYNC) -a media html/

html-clean:
	rm -f html/*.html
SUPERCLEAN-TARGETS += html-clean

.PHONY: html html-clean
all: html

#################### ipynb
ipynb: force
	@mkdir -p ipynb; echo populating ipynb with notebooks from 'W*'
	@$(RSYNC) -aL $(NOTEBOOKS) ipynb
	@mkdir -p ipynb/corrections; echo syncing modules/corrections onto ipynb/corrections
	@$(RSYNC) -a $$(git ls-files modules/corrections) ipynb/corrections
	@mkdir -p ipynb/data; echo syncing data onto ipynb/data
	@$(RSYNC) -a $$(git ls-files data) ipynb/data
	@mkdir -p ipynb/media; echo syncing media onto ipynb/media
	@$(RSYNC) -a $$(git ls-files media) ipynb/media

ipynb-clean:
	rm -rf ipynb/
CLEAN-TARGETS += ipynb-clean

.PHONY: ipynb ipynb-clean

####################
# xxx misses ipynb ?
out: html markdown ipynb
out-clean: html-clean markdown-clean ipynb-clean

.PHONY: out out-clean
############################## outputs : tars and export (rsync)
# Note on UTF-8 - need to instruct apache about our using utf-8
# tparment@srv-diana $ cat /proj/planete/www/Thierry.Parmentelat/flotpython/.htaccess
# AddDefaultCharset utf-8
RSYNC_URL = tparment@srv-diana.inria.fr:/proj/planete/www/Thierry.Parmentelat/flotpython/
RSYNC_DEL = $(RSYNC) -av --delete --delete-excluded

tars-dir:
	mkdir -p tars
.PHONY: tars-dir

TARS =

########## html
# tar
TAR-HTML = tars/notebooks-html.tar
TARS += $(TAR-HTML)
NOTEBOOKS-HTML = $(foreach notebook,$(NOTEBOOKS),$(call html_location,$(notebook)))
CONTENTS-HTML = html/custom.css $(NOTEBOOKS-HTML)
$(TAR-HTML): tars-dir html $(CONTENTS-HTML)
	tar -chf $@ $(CONTENTS-HTML)

html-tar: $(TAR-HTML)

# rsync
html-rsync:
	$(RSYNC_DEL) html/custom.css html/media $(NOTEBOOKS-HTML) $(RSYNC_URL)/html/
RSYNC-TARGETS += html-rsync

.PHONY: html-tar html-rsync

########## markdown
# tar
TAR-MARKDOWN = tars/notebooks-markdown.tar
TARS += $(TAR-MARKDOWN)
NOTEBOOKS-MARKDOWN = $(foreach notebook,$(NOTEBOOKS),$(call markdown_location,$(notebook)))
$(TAR-MARKDOWN): markdown tars-dir $(NOTEBOOKS-MARKDOWN)
	tar -chf $@ $(NOTEBOOKS-MARKDOWN)

markdown-tar: $(TAR-MARKDOWN)

# rsync
markdown-rsync:
	$(RSYNC_DEL) $(NOTEBOOKS-MARKDOWN) $(RSYNC_URL)/markdown/
RSYNC-TARGETS += markdown-rsync

########## ipynb
# tar 
TAR-IPYNB = tars/notebooks-ipynb.tar
TARS += $(TAR-IPYNB)
NOTEBOOKS-IPYNB = $(foreach notebook,$(NOTEBOOKS),$(call ipynb_location,$(notebook)))
$(TAR-IPYNB): ipynb tars-dir $(NOTEBOOKS-IPYNB)
	tar -chf $@  $(NOTEBOOKS-IPYNB) ipynb/corrections ipynb/data ipynb/media

ipynb-tar: $(TAR-IPYNB)

# rsync
ipynb-rsync:
	$(RSYNC_DEL) ipynb/ $(RSYNC_URL)/ipynb/
RSYNC-TARGETS += ipynb-rsync

.PHONY: ipynb-tar ipynb-rsync

########## corriges
# tar
TAR-CORRIGES = tars/corriges.tar
TARS += $(TAR-CORRIGES)
CORRIGES-CONTENTS = $(wildcard corriges/*.pdf) $(wildcard corriges/*.txt) $(wildcard corriges/*py)
$(TAR-CORRIGES): force tars-dir $(CORRIGES-CONTENTS)
	tar -cf $@ $(CORRIGES-CONTENTS)
corriges-tar: $(TAR-CORRIGES)

# rsync
corriges-rsync:
	$(RSYNC_DEL) corriges/*.{pdf,txt,py} $(RSYNC_URL)/corriges/
RSYNC-TARGETS += corriges-rsync

.PHONY: corriges-tar corriges-rsync


##########
TGZS = $(subst .tar,.tgz,$(TARS))

%.tgz: %.tar
	gzip -c9 $*.tar > $@

TAR-ALL = tars/all-tgzs.tar
$(TAR-ALL): $(TGZS) tars-dir
	tar -cf $@ $(TGZS)

tars: $(TARS) $(TGZS) $(TAR-ALL)

tars-clean:
	rm -rf tars/
CLEAN-TARGETS += tars-clean

.PHONY: tars tars-clean

# rsync the tars themselves
tars-rsync: $(TGZS)
	$(RSYNC_DEL) $(TGZS) $(RSYNC_URL)/tars/
RSYNC-TARGETS += tars-rsync

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
	for s in $(FOCUS); do echo ==================== $$s; \
	    ls $$s/*SUMMARY.txt | xargs egrep '(^C[0O]12AL.*txt|^NIVEAU|^\#\# Vid|^OK|^TODO|^ONGO|^NICE|^DROP)' | $(INDEX_POST) ; \
	    echo ""; \
	    echo ""; \
	    echo ""; \
	done > index.long
.PHONY: index

# all: index

############################## standalone
standalone: ipynb
	mkdir -p standalone
	rsync -av W?/*.mov standalone/
	rsync -av W?/*.quiz standalone/
	rsync -av ipynb/ standalone/

standalone-clean:
	rm -rf standalone/
CLEAN-TARGETS += standalone-clean

.PHONY: standalone standalone-clean

############################## 
clean: $(CLEAN-TARGETS)
# html and markdown are so slow to rebuild..
superclean: $(CLEAN-TARGETS) $(SUPERCLEAN-TARGETS)

rsync: $(RSYNC-TARGETS)

.PHONY: clean superclean rsync
#################### convenience, for debugging only
# make +foo : prints the value of $(foo)
# make ++foo : idem but verbose, i.e. foo=$(foo)
++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
