PYTHON_VENV ?= venv

CONSTELLATIONS = $(shell ls data/*/)


.PHONY: all
all: data
	$(MAKE) $(CONSTELLATIONS)

# MATCHING

# TODO: work out how to adequately model dependencies here
$(CONSTELLATIONS):
	$(PYTHON_VENV)/bin/python src/python/match_constellation.py \
		data/shots.csv \
		data/constellations/$@
	Rscript src/R/plot_constellation.R $@
	Rscript src/R/plot_shots.R $@
	if [ -f data/constellations/$@/stars.png ]; then \
		convert data/constellations/$@/stars.png -trim -fuzz 5% -transparent white data/constellations/$@/stars.png; \
		convert data/constellations/$@/shots.png -trim -fuzz 5% -transparent white data/constellations/$@/shots.png; \
	fi


# DATA

.PHONY: data
data: data/shots.csv constellations data/SnT_constellations.txt data/constellation_names.eng.fab

# Fetch from db
data/shots.csv:
	@echo "TODO"

# Creates links and stars for each constellation
.PHONY: constellations
constellations: data/SnT_constellations.txt data/constellation_names.eng.fab src/python/parse_constellations.py
	$(PYTHON_VENV)/bin/python src/python/parse_constellations.py \
		data/SnT_constellations.txt \
		data/constellation_names.eng.fab \
		data/constellations/

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
	rm -f data/shots.csv data/SnT_constellations.txt data/constellation_names.eng.fab
	rm -rf data/constellations/**/*.{csv,json,png}

.PHONY: env
env:
	python -m venv $(PYTHON_VENV)
	$(PYTHON_VENV)/bin/pip install --upgrade pip
	$(PYTHON_VENV)/bin/pip install -r requirements.txt
	@echo "renv"

.PHONY: test
test:
	$(PYTHON_VENV)/bin/pytest
