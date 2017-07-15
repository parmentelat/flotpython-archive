# -*- coding: utf-8 -*-

# all files in this repo are expected to be utf-8
# for transcoding, use e.g. 
#     recode ISO-8859-15..UTF-8 <filename>

RSYNC = rsync --exclude .du --exclude .DS_Store
RSYNC_DEL = $(RSYNC) -av --delete --delete-excluded

all: 
.PHONY: all

TOPLEVEL=$(shell pwd)

# work on one week at a time with FOCUS=w2
FOCUS     = w?
NOTEBOOKS = $(shell git ls-files $(FOCUS) | grep '\.ipynb$$')
NOTEBASES = $(subst .ipynb,,$(NOTEBOOKS))

# for phony targets
force:

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
export PYTHONPATH=$(CURDIR)/modules

CONVERT = jupyter nbconvert --ExecutePreprocessor.enabled=True --ExecutePreprocessor.allow_errors=True

# apply these rules to all notebooks
define notebook_rule
$(call markdown_location,$(1)): $(1)
	$(CONVERT) --to markdown $(1) --stdout > $(call markdown_location,$(1)) || rm $(call markdown_location,$(1))

$(call html_location,$(1)): $(1)
	$(CONVERT) --to html $(1) --stdout > $(call html_location,$(1)) || rm $(call html_location,$(1))

# not used; the ipynb target uses rsync to fill in ipynb/
#$(call ipynb_location,$(1)): $(1)
#	(mkdir -p ipynb; cd ipynb; ln -f -s ../$(1) $(notdir $(1)))

# redo all targets about one notebook
# e.g make -n w1-s2-c1-accents
$(call sbn,$(1)): $(call markdown_location,$(1)) $(call html_location,$(1))

.PHONY: $(call sbn,$(1))
endef

$(foreach notebook,$(NOTEBOOKS),$(eval $(call notebook_rule,$(notebook))))

#################### markdown
markdown: $(MARKDOWNS) media
	$(RSYNC) -a media markdown/

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
	@mkdir -p ipynb; echo populating ipynb with notebooks from 'w*'
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
out: html markdown ipynb
out-clean: html-clean markdown-clean ipynb-clean

.PHONY: out out-clean

############################## outputs : tars and zips
# Note on infrastructure - Oct 2015
# because now we produce html and markdown with the code cells evaluated
# we need to run this part of the make process on a dedicated box
# this is jupyter.pl.sophia.inria.fr that runs an up-to-date deployment
# of a dual-kernel jupyter
# so the html and markdown targets, and thus tars and zips
# need to be run on that box; so we now have these 2 targets
# retrieve and publish
# that go fetch the stuff on jupyter, and then
# push the same stuff on srv-diana (a.k.a. http://planete.inria.fr)
###
# Note on UTF-8 - need to instruct apache about our using utf-8
# tparment@srv-diana $ cat /proj/planete/www/Thierry.Parmentelat/flotpython/.htaccess
# AddDefaultCharset utf-8
###
RETRIEVE_ID  = thierry@jupyter.pl.sophia.inria.fr
RETRIEVE_URL = $(RETRIEVE_ID):flotpython/
PUBLISH_URL  = tparment@srv-diana.inria.fr:/proj/planete/www/Thierry.Parmentelat/flotpython/

bundles-dir:
	mkdir -p bundles
bundles-clean:
	rm -rf bundles/
CLEAN-TARGETS += bundles-clean 

.PHONY: bundles-dir bundles-clean

### all this stuff is expected to run on jupyter.pl.sophia.inria.fr

# how to redo file bundles/<bundle-name>.tar (and .zip)
# bundle_target(bundle-name, contents, deps)
# and to define shorthand phony target <phony>-tar in the mix
# bundle_phony(phony,bundle_name)
TARS =
ZIPS =

# e.g. bundle_target(notebooks-html,$(BUNDLE-HTML), html $(BUNDLE-HTML))
# -> redo bundles/notebooks-html.tar
# using files $(BUNDLE-HTML)
# with deps 'html and $(BUNDLE-HTML)'
# and of course same for zip
define bundle_target
bundles/$(1).tgz: bundles-dir $(3)
ifneq "" "$(2)"
	tar -czf bundles/$(1).tgz $(2)
endif
bundles/$(1).zip: bundles-dir $(3)
ifneq "" "$(2)"
	zip -r bundles/$(1) $(2)
endif
endef

# e.g. bundle_target(notebooks-html,html)
# defines various shortcuts like 'html-tar' 
# + this will be done when doing make tars
define bundle_shortcut
TARS += bundles/$(1).tgz
ZIPS += bundles/$(1).zip
$(2)-tar: bundles/$(1).tgz
$(2)-zip: bundles/$(1).zip
$(2)-bundles: $(2)-tar $(2)-zip
.PHONY: $(2)-bundles $(2)-tar $(2)-html
endef

# do all 7 weeks in one pass
# e.g. bundle_all_weeks(html-focus,html-weeks)
define bundle_all_weeks
$(2)-tars:
	for focus in $(FOCUS); do $(MAKE) $(1)-tar FOCUS=$$$$focus; done
TARS += $(2)-tars
$(2)-zips:
	for focus in $(FOCUS); do $(MAKE) $(1)-zip FOCUS=$$$$focus; done
ZIPS += $(2)-zips
$(2): $(2)-tars $(2)-zips
.PHONY: $(2)-tars $(2)-zips $(2)
endef

########## html
NOTEBOOKS-HTML = $(foreach notebook,$(NOTEBOOKS),$(call html_location,$(notebook)))
BUNDLE-HTML = html/custom.css html/media $(NOTEBOOKS-HTML)

$(eval $(call bundle_target,notebooks-html,$(BUNDLE-HTML),html $(BUNDLE-HTML)))
$(eval $(call bundle_shortcut,notebooks-html,html))

# this only makes sense in a context where FOCUS is defined to one week
$(eval $(call bundle_target,$(FOCUS)-notebooks-html,$(BUNDLE-HTML),html $(BUNDLE-HTML)))
ifneq "$(FOCUS)" "w?"
$(eval $(call bundle_shortcut,$(FOCUS)-notebooks-html,html-focus))
endif

$(eval $(call bundle_all_weeks,html-focus,html-weeks))

########## markdown
NOTEBOOKS-MARKDOWN = $(foreach notebook,$(NOTEBOOKS),$(call markdown_location,$(notebook)))
BUNDLE-MARKDOWN = markdown/media $(NOTEBOOKS-MARKDOWN)

$(eval $(call bundle_target,notebooks-markdown,$(BUNDLE-MARKDOWN),markdown $(BUNDLE-MARKDOWN)))
$(eval $(call bundle_shortcut,notebooks-markdown,markdown))

# this only makes sense in a context where FOCUS is defined to one week
$(eval $(call bundle_target,$(FOCUS)-notebooks-markdown,$(BUNDLE-MARKDOWN),markdown $(BUNDLE-MARKDOWN)))
ifneq "$(FOCUS)" "w?"
$(eval $(call bundle_shortcut,$(FOCUS)-notebooks-markdown,markdown-focus))
endif

$(eval $(call bundle_all_weeks,markdown-focus,markdown-weeks))

########################################
# these 2 (notebooks in ipynb format, and corriges) in principle could be run locally
# but the rule of thumb would be to do it on jupyter as well
# this way everything can be harvested using make retrieve
# plus, chances are the working space is cleaner on jupyter

########## ipynb
# there's no target ipynb/corrections and similar
# so these must go in the contents, but not in deps
NOTEBOOKS-IPYNB = $(foreach notebook,$(NOTEBOOKS),$(call ipynb_location,$(notebook)))
BUNDLE-IPYNB = $(NOTEBOOKS-IPYNB) ipynb/corrections ipynb/data ipynb/media 

$(eval $(call bundle_target,notebooks-ipynb,$(BUNDLE-IPYNB),ipynb $(NOTEBOOKS-IPYNB)))
$(eval $(call bundle_shortcut,notebooks-ipynb,ipynb))

########## corriges
BUNDLE-CORRIGES-FOCUS = $(wildcard corriges/corriges-$(FOCUS)*.txt corriges/corriges-$(FOCUS)*.pdf corriges/corriges-$(FOCUS)*.py)
BUNDLE-CORRIGES = $(wildcard corriges/*.pdf) $(wildcard corriges/*.txt) $(wildcard corriges/*py)

$(eval $(call bundle_target,corriges,$(BUNDLE-CORRIGES),corriges-pdf))
$(eval $(call bundle_shortcut,corriges,corriges))

$(eval $(call bundle_target,$(FOCUS)-corriges,$(BUNDLE-CORRIGES-FOCUS),corriges-pdf))
ifneq "$(FOCUS)" "w?"
$(eval $(call bundle_shortcut,$(FOCUS)-corriges,corriges-focus))
endif
$(eval $(call bundle_all_weeks,corriges-focus,corriges-weeks))

##########
tars: $(TARS)
zips: $(ZIPS)
bundles: $(TARS) $(ZIPS)
.PHONY: tars zips bundles

######################################## back on a local box
remote:
	ssh $(RETRIEVE_ID) 'cd flotpython; git reset --hard HEAD; git pull; make clean superclean; make bundles'

retrieve:
	mkdir -p bundles
	$(RSYNC_DEL) $(RETRIEVE_URL)/bundles/ ./bundles/

publish:
	$(RSYNC_DEL) ./bundles/ $(PUBLISH_URL)/bundles/

full-monty: remote retrieve publish

.PHONY: full-monty remote retrieve publish
############################## standalone
# this must be run lcoally, as the videos are not in git
# it just wraps videos and notebooks in a single directory
standalone: ipynb
	mkdir -p standalone
	rsync -av w?/*.mov standalone/
	rsync -av w?/*.quiz standalone/
	rsync -av ipynb/ standalone/

standalone-clean:
	rm -rf standalone/
CLEAN-TARGETS += standalone-clean

.PHONY: standalone standalone-clean

############################## 
clean: $(CLEAN-TARGETS)
# html and markdown are so slow to rebuild..
superclean: $(CLEAN-TARGETS) $(SUPERCLEAN-TARGETS)

.PHONY: clean superclean 
############################################################
# various development targets
############################################################

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

#
tags: force
	git ls-files | xargs etags
.PHONY: tags

# run nbnorm on all notebooks
norm normalize: normalize-notebook normalize-quiz

# add the --sign option only on Thierry's macos to reduce noise-only changes
NORM = tools/nbnorm.py
NORM_OPTIONS = --author "Thierry Parmentelat" --author "Arnaud Legout" --version 3.0 --logo-path media/inria-25-alpha.png --kernel 3

# -type f : we need to skip symlinks
normalize-nb normalize-notebook: force
	find $(FOCUS) -name '*.ipynb' -type f | sort | fgrep -v '/.ipynb_checkpoints/' | xargs $(NORM) $(NORM_OPTIONS)

normalize-quiz: force
	find $(FOCUS) -name '*.quiz' | sort | xargs tools/quiznorm.py

#all: norm

.PHONY: norm normalize normalize-nb normalize-notebook normalize-quiz

#
CLEAN_FIND= -name '*~' -o -name '.\#*' -o -name '*pyc'

junk-clean: force
	find . $(CLEAN_FIND) -name '*~' -o -name '.#*' -print0 | xargs -0 rm -f
CLEAN-TARGETS += junk-clean

#################### convenience, for debugging only
# make +foo : prints the value of $(foo)
# make ++foo : idem but verbose, i.e. foo=$(foo)
++%: varname=$(subst +,,$@)
++%:
	@echo "$(varname)=$($(varname))"
+%: varname=$(subst +,,$@)
+%:
	@echo "$($(varname))"
