all:
	ships.py json/*

REF-FILES =  ALL_SHIPS.kml.ref	ALL_SHIPS.txt.ref

ref-tar:
	tar cf ../data/ships-ref.tar $(REF-FILES)

ref-zip:
	zip ../data/ships-ref.zip $(REF-FILES)

ref: ref-tar ref-zip
.PHONY: ref-tar ref-zip

json-tar:
	tar cf ../data/ships-json.tar json/

json-tgz:
	tar czf ../data/ships-json.tgz json/

json-zip:
	zip ../data/ships-json.zip json/*

json: json-tar json-tgz json-zip
.PHONY: json-tar json-tgz json-zip
