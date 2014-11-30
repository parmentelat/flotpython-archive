all:
	merger.py json/*

REF-FILES =  ALL_SHIPS.kml.ref	ALL_SHIPS.txt.ref ALL_SHIPS-v.txt.ref


ref-tar:
	tar cf ../data/ships-ref.tar $(REF-FILES)

ref-tgz:
	tar czf ../data/ships-ref.tgz $(REF-FILES)

ref-zip:
	zip ../data/ships-ref.zip $(REF-FILES)

ref: ref-tar ref-tgz ref-zip
.PHONY: ref-tar ref-tgz ref-zip


json-tar:
	tar cf ../data/ships-json.tar json/

json-tgz:
	tar czf ../data/ships-json.tgz json/

json-zip:
	zip ../data/ships-json.zip json/*

json: json-tar json-tgz json-zip
.PHONY: json-tar json-tgz json-zip


merger-help help-merger:
	python -c "from merger import Merger; help(Merger)"
compare-help help-compare:
	python -c "from compare import Compare; help(Compare)"
kml-help help-kml:
	python -c "from kml import KML; help(KML)"
shipdict-help help-shipdict:
	python -c "from shipdict import ShipDict; help(ShipDict)" > shipdict.help
ship-help help-ship:
	python -c "from shipdict import Ship; help(Ship)" > ship.help
position-help help-position:
	python -c "from shipdict import Position; help(Position)" > position.help

CODE-FILES = ./compare.py ./kml.py ./merger.py ./shipdict.py
DATA-FILES = $(subst ./,../data/,$(CODE-FILES))

define code_target
../data/$(subst ./,,$(1)): $(1)
	rsync -av $(1) ../data/
endef

$(foreach code,$(CODE-FILES),$(eval $(call code_target,$(code))))

code: $(DATA-FILES)


foo:
	echo $(DATA-FILES)
