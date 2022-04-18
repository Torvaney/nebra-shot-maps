PYTHON_VENV ?= venv


# DATA

# Fetch from db
data/shots.csv:
	@echo "TODO"

data/constellations.csv: data/SnT_constellations.txt data/constellation_names.eng.fab src/python/parse_constellations.py
	$(PYTHON_VENV)/bin/python src/python/parse_constellations.py \
		data/SnT_constellations.txt \
		data/constellation_names.eng.fab > \
		$@

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
	rm data/*

.PHONY: env
env:
	python -m venv $(PYTHON_VENV)
	$(PYTHON_VENV)/bin/pip install --upgrade pip
	$(PYTHON_VENV)/bin/pip install -r requirements.txt
	@echo "renv"
