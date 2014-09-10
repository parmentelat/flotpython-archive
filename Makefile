all: index connect tags

# for phony targets
force:

#
# rough index based on the *SUM.txt
# I need to set LC_ALL otherwise grep misreads line with accents and gives truncated results
INDEX_POST= sed -e 's,\(\#\# Vid\),========== \1,'

index: force
	export LC_ALL=en_US.ISO8859-15;\
	for s in W?; do echo ==================== $$s; \
	    ls $$s/C[0O]12AL*SUM.txt | xargs egrep '(^C[0O]12AL.*txt|^\#\# Vid|^OK|^TODO|^ONGO)' | $(INDEX_POST) ; \
	    echo ""; \
	    echo ""; \
	    echo ""; \
	done > index.long

#
# builds a html index of the ipynb files expected to be reachable on connect.inria.fr
# pthierry is built-in 
connect: connect.html

connect.html: force
	tools/nbindex.py

#
tags: force
	git ls-files | xargs etags

# run nbtool on all notebooks
norm normalize normalize-notebooks: force
	find W[0-9]* -name '*.ipynb' | fgrep -v '/.ipynb_checkpoints/' | xargs tools/nbtool.py

#
CLEAN_FIND= -name '*~' -o -name '.\#*' -o -name '*pyc'

toclean: force
	find . $(CLEAN_FIND) -print0 | xargs -0 ls

clean: force
	find . $(CLEAN_FIND) -name '*~' -o -name '.#*' -print0 | xargs -0 rm -f

