PYTHON_VENV ?= venv
SIMILARITY_FUNCTION ?= euclidean

CONSTELLATIONS = $(shell ls data/*/)


.PHONY: all
all: html



# HTML

.PHONY: html
html: matching
html: html/static/css/styles.css html/index.html
html:
	$(MAKE) $(patsubst %,html/static/img/%/shots.png,$(CONSTELLATIONS))
	$(MAKE) $(patsubst %,html/static/img/%/stars.png,$(CONSTELLATIONS))


html/static/img/%/shots.png: data/constellations/%/shots.png
	mkdir -p html/static/img/$*
	cp $< $@

html/static/img/%/stars.png: data/constellations/%/stars.png
	mkdir -p html/static/img/$*
	cp $< $@


html/static/css/styles.css:
	mkdir -p html/static/css
	cp src/css/styles.css html/static/css/styles.css


html/index.html: data html/static/css/styles.css $(patsubst %,data/constellations/%/match.json,$(CONSTELLATIONS))
	$(PYTHON_VENV)/bin/python src/python/generate_webpage.py \
		data/constellations \
		src/html \
		html



# MATCHING

.PHONY: matching
matching: data
	@$(MAKE) $(patsubst %,data/constellations/%/match.json,$(CONSTELLATIONS))


data/constellations/%/match.json: data/constellations/%/stars.csv
	@$(PYTHON_VENV)/bin/python src/python/match_constellation.py \
		data/shots.csv \
		data/constellations/$* \
		--similarity $(SIMILARITY_FUNCTION)
	@Rscript src/R/plot_constellation.R $*
	@Rscript src/R/plot_shots.R $*
	@if [ -f data/constellations/$*/stars.png ]; then \
		convert data/constellations/$*/stars.png -trim -fuzz 5% -transparent white data/constellations/$*/stars.png; \
		convert data/constellations/$*/shots.png -trim -fuzz 5% -transparent white data/constellations/$*/shots.png; \
	fi

# Stars rule performs the matching and generates images, too
data/constellations/%/stars.png: data/constellations/%/match.json

data/constellations/%/shots.png: data/constellations/%/match.json



# DATA

.PHONY: data
data: data/shots.csv data/SnT_constellations.txt data/constellation_names.eng.fab data/constellations

# Fetch from db
data/shots.csv:
	@if [ ! -f data/shots.csv ]; then \
		echo "You need to add a 'shots.csv' file to the 'data' folder!"; \
		exit 1; \
	fi


# Creates links and stars for each constellation (using the directory to inform
# make of how up-to-date they are)
data/constellations: data/SnT_constellations.txt data/constellation_names.eng.fab
	mkdir -p data/constellations/
	$(PYTHON_VENV)/bin/python src/python/parse_constellations.py \
		data/SnT_constellations.txt \
		data/constellation_names.eng.fab \
		data/constellations/
	touch data/constellations

data/constellations/%/stars.csv: data/constellations

data/constellations/%/links.csv: data/constellations


data/SnT_constellations.txt:
	wget \
		https://raw.githubusercontent.com/Stellarium/stellarium/43d4dba4c85d3264244faad27cf1f60ddf92083c/skycultures/western_SnT/SnT_constellations.txt \
		-O data/SnT_constellations.txt

data/constellation_names.eng.fab:
	wget \
		https://raw.githubusercontent.com/Stellarium/stellarium/43d4dba4c85d3264244faad27cf1f60ddf92083c/skycultures/western_SnT/constellation_names.eng.fab \
		-O data/constellation_names.eng.fab



# DEV

.PHONY: clean
clean:
	rm -f  data/SnT_constellations.txt data/constellation_names.eng.fab
	rm -rf data/constellations/*


.PHONY: env
env:
	python -m venv $(PYTHON_VENV)
	$(PYTHON_VENV)/bin/pip install --upgrade pip
	$(PYTHON_VENV)/bin/pip install -r requirements.txt
	@echo "TODO: renv"


.PHONY: test
test:
	$(PYTHON_VENV)/bin/pytest
