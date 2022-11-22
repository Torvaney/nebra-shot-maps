# Nebra Shot Maps

Matching constellations to shot maps.

Run `make all` to run the matching algorithm for all constellations and view the results at `data/constellations/{constellation}/...`, after making sure you've satisfied the **requirements** (listed below).

Alternatively, you can download a sample of matched constellations and shot maps [from the releases](https://github.com/Torvaney/nebra-shot-maps/releases/tag/data).

## Results

![](README/example.png)

The full results are available [here](https://torvaney.github.io/projects/nebra/)


## Requirements

* A Python environment (assumed to be at `venv`, unless otherwise set with the `PYTHON_VENV` environment variable). Anything version 3.6+ should be fine. Required packages are in `requirements.txt`.
  - You can create a virtual environment at `venv` and install the requirements with `make venv`
* An R installation, with the [tidyverse](https://github.com/tidyverse/tidyverse) and [ggsoccer](https://github.com/Torvaney/ggsoccer) installed. I used v3.6.3 (I haven't tested v4, but I assume that's fine, too)
* `data/shots.csv`. I used a csv with the following columns, one row per shot (I think [fbref](https://fbref.com/en/) publishes this data now, so you should be able to get it from there). Fields that aren't used by the main algorithm are shown in square brackets. Skipping these columns won't matter, but will result in a warning message. (There is a make rule for `data/shots.csv` that you can replace should you want to.)
  - [`id`]
  - `game_id`
  - `team_id`
  - [`team`]
  - [`game_label`]
  - [`kickoff`]
  - `x`
  - `y`
  - [`event_type`]


## Nebra?

The name for this project comes from the [Nebra sky disc](https://en.wikipedia.org/wiki/Nebra_sky_disc).
