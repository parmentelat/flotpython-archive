TOOL = ../tools/corriges.py

W2 = w2_slicing.py w2_if.py w2_for.py w2_strings.py
W3 = w3_marine_dict.py w3_marine_set.py w3_decode_zen.py w3_if.py
W4 = w4_files.py w4_pgcd.py w4_functional.py w4_comprehensions.py w4_fun_args.py 
W5 = w5_rpcproxy.py
W6 = w6_regexp.py

WEEKS=2 3 4 5 6

define week_sources
$(foreach python,$(W$(1)),../modules/corrections/$(python))
endef

SOURCES = $(foreach week,$(WEEKS),$(call week_sources,$(week)))

all: $(foreach week, $(WEEKS), corriges-w$(week).tex) corriges.tex

corriges.tex corriges.txt: $(SOURCES) $(TOOL)
	$(TOOL) -o corriges -t "Tous les corrigés" -c $(SOURCES)
corriges.pdf: corriges.tex
	pdflatex corriges.tex
clean::
	rm -f corriges.*
pdf: corriges.pdf

define week_target
corriges-w$(1).tex: $(call week_sources,$(1)) $(TOOL)
	$(TOOL) -o corriges-w$(1) -t "Corrigés de la semaine $(1)" $(call week_sources,$(1))

corriges-w$(1).pdf: corriges-w$(1).tex
	pdflatex corriges-w$(1).tex

clean::
	rm -f corriges-w$(1).*

pdf: corriges-w$(1).pdf
endef


$(foreach week, $(WEEKS), $(eval $(call week_target,$(week))))
