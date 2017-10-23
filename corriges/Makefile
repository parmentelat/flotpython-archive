# -*- coding: utf-8 -*-
TOOL = ../tools/corriges.py

w2 = w2s2_regexp.py w2s6_slicing.py w2s6_strings.py w2s7_comprehensions.py w2s7_for.py w2s7_if.py
w3 = w3s1_files.py w3s4_marine_dict.py w3s4_parse_graph.py w3s5_marine_set.py
w4 = w4s3_pgcd.py w4s6_fun_args.py
w5 = w5s2_functional.py w5s5_decode_zen.py w5s6_rpcproxy.py

# pour la semaine 5 on met
# dans le latex les deux fichiers (via $(TOOL))
# dans le text un seul fichier (via $(TOOL))
# plus le fichier shipdict.py tel quel
w5_latex = w5s6_rpcproxy.py shipdict.py 
w5_text = w5s6_rpcproxy.py
w5_code  = ../data/shipdict.py

w6_latex = w6s6_regexp.py
w6_text = w6s6_regexp.py
w6_code = ../exo-meteo/meteodata.py ../exo-diskusage/diskusage.py ../exo-crawler/webcrawler.py

WEEKS = 2 3 4 5

define find_source
$(wildcard ../modules/corrections/$(1) ../data/$(1))
endef

define week_latex_sources
$(foreach python,$(w$(1)_latex), $(call find_source,$(python)))
endef

define week_text_sources
$(foreach python,$(w$(1)_text), $(call find_source,$(python)))
endef

SOURCES = $(foreach week,$(WEEKS),$(call week_latex_sources,$(week)))

all: $(foreach week, $(WEEKS), corriges-w$(week).tex corriges-w$(week).txt) corriges.tex corriges.txt code

corriges.tex corriges.txt: $(SOURCES) $(TOOL)
	$(TOOL) --output corriges --title "MOOC Python;Tous les corrigés" --contents $(SOURCES)
corriges.pdf: corriges.tex
	pdflatex corriges.tex
superclean::
	rm -f corriges.*
pdf:: corriges.pdf


define week_values
w$(1)_text = $(or $(w$(1)_text),$(w$(1)))
w$(1)_latex = $(or $(w$(1)_latex),$(w$(1)))
endef

$(foreach week, $(WEEKS), $(eval $(call week_values,$(week))))

define code_target
corriges-w$(3)-$(2): $(1)
	egrep -v '@BEG|@END' $(1) > corriges-w$(3)-$(2)
	chmod +x corriges-w$(3)-$(2)

code:: corriges-w$(3)-$(2)

code-clean::
	rm -f corriges-w$(3)-$(2)
endef

superclean:: code-clean

define week_target
corriges-w$(1).tex: $(call week_latex_sources,$(1)) $(TOOL)
	$(TOOL) --latex --output corriges-w$(1) --title "MOOC Python;Corrigés de la semaine $(1)" $(call week_latex_sources,$(1))

corriges-w$(1).pdf: corriges-w$(1).tex
	pdflatex corriges-w$(1).tex

corriges-w$(1).txt: $(call week_text_sources,$(1)) $(TOOL)
	$(TOOL) -T -o corriges-w$(1) -t "Corrigés de la semaine $(1)" $(call week_text_sources,$(1))

superclean::
	rm -f corriges-w$(1).*

pdf:: corriges-w$(1).pdf

$(foreach code,$(w$(1)_code),$(eval $(call code_target,$(code),$(notdir $(code)),$(1))))
endef

$(foreach week, $(WEEKS), $(eval $(call week_target,$(week))))

.PHONY: all code clean superclean code-clean pdf

clean:
	rm -f *.{aux,log,tex,toc,py}

index:
	for tex in *.tex; do pdflatex $$tex; done

# convenience to generate a notebook fragment
# that can validate all known exos at once
validation:
	$(TOOL) -N -o ../modules/corrections/validation $(SOURCES)

