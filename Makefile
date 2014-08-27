tags: force
	git ls-files | xargs etags

# for phony targets
force:

# builds a html index of the ipynb files expected to be reachable on connect.inria.fr
# pthierry is built-in 
index: connect.html

connect.html: force
	tools/nbindex.py

# nbtool is more expected to be run on a need-by-need basis, but 

norm normalize normalize-notebooks: force
	find semaine[0-9]* -name '*.ipynb' | fgrep -v '/.ipynb_checkpoints/' | xargs tools/nbtool.py

CLEAN_FIND= -name '*~' -o -name '.\#*' -o -name '*pyc'

toclean: force
	find . $(CLEAN_FIND) -print0 | xargs -0 ls

clean: force
	find . $(CLEAN_FIND) -name '*~' -o -name '.#*' -print0 | xargs -0 rm -f

