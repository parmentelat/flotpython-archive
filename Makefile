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

clean: force
	find . $(CLEAN_FIND) -name '*~' -o -name '.#*' -print0 | xargs -0 rm -f


# xxx we need to have the quiz files encoded in UTF-8 right at the beginning
# I don't maintain all.quiz anymore
#all: quiz
quiz: 
	cat */*.quiz > 00-all.quiz
	recode ISO-8859-15..UTF-8 00-all.quiz
