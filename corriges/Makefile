# -*- coding: utf-8 -*-
TOOL = ../tools/corriges.py

all: everything

exomap:
	../tools/exomap.sh

nbmap:
	(cd ..; git ls-files w?/w?-s?-[cx]*nb) > nbmap

.FORCE:

n2 = regexp_pythonid regexp_agenda regexp_phone regexp_url \
     exo_label exo_inconnue exo_laccess exo_divisible exo_wc exo_morceaux \
	 exo_liste_p exo_carre
n3 = exo_comptage exo_surgery  exo_graph_dict exo_marine_dict \
     exo_read_set exo_marine_set cls_fifo
n4 = exo_dispatch exo_libelle exo_pgcd exo_taxes exo_distance exo_numbers
n5 = exo_multi_tri exo_multi_tri_reverse \
     exo_doubler_premier exo_doubler_premier_kwds \
     exo_compare_all exo_compare_args \
     exo_aplatir exo_alternat exo_intersect \
     exo_produit_scalaire exo_decode_zen
# w6 n'a que l'exercice shipdict; faire 'make code' pour produire le corrigé
n7 = exo_stairs

# dans w6-s2 et w6-s4 resp.
others = exo_rpcproxy shipdict

define pys
$(foreach name, $(1), $(name).py)
endef

w2 = $(call pys, $(n2))
w3 = $(call pys, $(n3))
w4 = $(call pys, $(n4))
w5 = $(call pys, $(n5))
w6_code  = ../data/shipdict.py
w7 = $(call pys, $(n7))

WEEKS = 2 3 4 5 7

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

everything: $(foreach week, $(WEEKS), corriges-w$(week).tex corriges-w$(week).txt) corriges.tex corriges.txt code

corriges.tex corriges.txt: $(SOURCES) $(TOOL) exomap
	$(TOOL) --output corriges --title "MOOC Python;Tous les corrigés" --contents $(SOURCES)
corriges.pdf: corriges.tex
	pdflatex corriges.tex
superclean::
	rm -f corriges.* exomap nbmap
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
corriges-w$(1).tex: $(call week_latex_sources,$(1)) $(TOOL) exomap
	$(TOOL) --latex --output corriges-w$(1) --title "MOOC Python;Corrigés de la semaine $(1)" $(call week_latex_sources,$(1))

corriges-w$(1).pdf: corriges-w$(1).tex
	pdflatex corriges-w$(1).tex

corriges-w$(1).txt: $(call week_text_sources,$(1)) $(TOOL) exomap
	$(TOOL) -T -o corriges-w$(1) -t "Corrigés de la semaine $(1)" $(call week_text_sources,$(1))

superclean::
	rm -f corriges-w$(1).*

pdf:: corriges-w$(1).pdf

$(foreach code,$(w$(1)_code),$(eval $(call code_target,$(code),$(notdir $(code)),$(1))))
endef

$(foreach week, $(WEEKS), $(eval $(call week_target,$(week))))

.PHONY: all code clean superclean code-clean pdf

clean:
	rm -f *.{aux,log,tex,toc,py,out} exomap nbmap

index:
	for tex in *.tex; do pdflatex $$tex; done

# convenience to generate a notebook fragment
# that can validate all known exos at once
validation:
	$(TOOL) -N -o ../modules/corrections/validation $(SOURCES)
