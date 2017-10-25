# -*- coding: utf-8 -*-
TOOL = ../tools/corriges.py

n2 = regexp_pythonid regexp_agenda regexp_phone regexp_url \
     exo_libelle exo_carre exo_inconnue exo_divisible exo_morceaux exo_spam \
     exo_liste_p exo_multi_tri exo_multi_tri_reverse exo_produit_scalaire \
     exo_aplatir exo_alternat exo_intersect
# xxx this needs to be refreshed
n3 = exo_comptage exo_marine_dict exo_parse_graph exo_marine_set
n4 = exo_pgcd exo_distance exo_doubler_premier exo_doubler_premier_kwds exo_compare_args
n5 = exo_numbers exo_compare_all exo_decode_zen.py exo_rpcproxy.py

define pys
$(foreach name, $(1), $(name).py)
endef

w2 = $(call pys, $(n2))
w3 = $(call pys, $(n3))
w4 = $(call pys, $(n4))
w5 = $(call pys, $(n5))

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

