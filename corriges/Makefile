# -*- coding: utf-8 -*-
TOOL = ../tools/corriges.py

W2 = w2_slicing.py w2_if.py w2_for.py w2_strings.py
W3 = w3_marine_dict.py w3_marine_set.py w3_decode_zen.py w3_if.py
W4 = w4_files.py w4_pgcd.py w4_functional.py w4_comprehensions.py w4_fun_args.py 

# pour la semaine 5 on met
# dans le latex les deux fichiers (via $(TOOL))
# dans le text un seul fichier (via $(TOOL))
# plus le fichier shipdict.py tel quel
W5_latex = w5_rpcproxy.py shipdict.py 
W5_text = w5_rpcproxy.py
W5_code  = ../data/shipdict.py

W6_latex = w6_regexp.py
W6_text = w6_regexp.py
W6_code = ../exo-meteo/meteodata.py ../exo-diskusage/diskusage.py ../exo-crawler/webcrawler.py

WEEKS=2 3 4 5 6

define find_source
$(wildcard ../modules/corrections/$(1) ../data/$(1))
endef

define week_latex_sources
$(foreach python,$(W$(1)_latex), $(call find_source,$(python)))
endef

define week_text_sources
$(foreach python,$(W$(1)_text), $(call find_source,$(python)))
endef

SOURCES = $(foreach week,$(WEEKS),$(call week_latex_sources,$(week)))

all: $(foreach week, $(WEEKS), corriges-w$(week).tex corriges-w$(week).txt) corriges.tex corriges.txt code

corriges.tex corriges.txt: $(SOURCES) $(TOOL)
	$(TOOL) -o corriges -t "Tous les corrigés" -c $(SOURCES)
corriges.pdf: corriges.tex
	pdflatex corriges.tex
superclean::
	rm -f corriges.*
pdf:: corriges.pdf


define week_values
W$(1)_text = $(or $(W$(1)_text),$(W$(1)))
W$(1)_latex = $(or $(W$(1)_latex),$(W$(1)))
endef

$(foreach week, $(WEEKS), $(eval $(call week_values,$(week))))

define code_target
corriges-w$(3)-$(2): $(1)
	egrep -v '@BEG|@END' $(1) > corriges-w$(3)-$(2)

code:: corriges-w$(3)-$(2)

code-clean::
	rm -f corriges-w$(3)-$(2)
endef

superclean:: code-clean

define week_target
corriges-w$(1).tex: $(call week_latex_sources,$(1)) $(TOOL)
	$(TOOL) -L -o corriges-w$(1) -t "Corrigés de la semaine $(1)" $(call week_latex_sources,$(1))

corriges-w$(1).pdf: corriges-w$(1).tex
	pdflatex corriges-w$(1).tex

corriges-w$(1).txt: $(call week_text_sources,$(1)) $(TOOL)
	$(TOOL) -T -o corriges-w$(1) -t "Corrigés de la semaine $(1)" $(call week_text_sources,$(1))

superclean::
	rm -f corriges-w$(1).*

pdf:: corriges-w$(1).pdf

$(foreach code,$(W$(1)_code),$(eval $(call code_target,$(code),$(notdir $(code)),$(1))))
endef

$(foreach week, $(WEEKS), $(eval $(call week_target,$(week))))

.PHONY: all code clean superclean code-clean pdf

clean:
	rm -f *.{aux,log,tex,toc}
