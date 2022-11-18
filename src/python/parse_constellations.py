"""
Read constellations data (i.e. data/SnT_constellations.txt) and convert it
into a format we prefer.
"""
import re
import sys
import pathlib

import typer
import numpy as np
import pandas as pd

import geometry


MIN_STARS = 5


def main(snt: typer.FileText, names: typer.FileText, output_dir: pathlib.Path):
    # load constellations data and names
    constellations = pd.DataFrame(parse_snt(snt))
    name_lookup = parse_names(names)

    # Join constellations to names & add xy
    for constellation_abbr, constellation_data in constellations.groupby('constellation'):
        if len(constellation_data) < MIN_STARS:
            typer.echo(f'{constellation_abbr} has fewer than {MIN_STARS} shots. Skipping.')
            continue

        full_name = name_lookup[constellation_abbr]

        # Add metadata, add coordinates, separate links and stars
        constellation_data['name'] = full_name
        links, stars = wrangle_constellation(constellation_data)

        # Save data
        constellation_dir = output_dir/constellation_abbr
        constellation_dir.mkdir(exist_ok=True)
        links.to_csv(constellation_dir/'links.csv', index=False)
        stars.to_csv(constellation_dir/'stars.csv', index=False)


def parse_snt(lines):
    """
    Reads data from the lines and returns a generator that
    returns a dict with each field parsed out.

    Adapted from https://github.com/Stellarium/stellarium/blob/master/skycultures/western_SnT/generate_constellationship.py
    """
    #                              mag           ra          npd             bayer              sup       weight    cons
    data_regex = re.compile(r'([0-9\. -]{5}) ([0-9\. ]{8}) ([0-9\. ]{8}) ([A-Za-z0-9 -]{3})([a-zA-Z0-9 ])([0-9])([a-zA-Z]{3})')
    for line in lines:
        line = line.rstrip('\n\r')
        m = re.match(data_regex, line)

        if m:
            # The S&T data has "Erj" as the continuation of Eridanus
            # after pi.  This is because the S&T data has a gap around
            # pi, since it lies slightly within Cetus.  S&T's own line
            # drawing software requires that one of the last four characters
            # change to signify a new line is to be started, rather than
            # continuing from the previous point.  So they had to create
            # a "fake" constellation to make their line drawing software
            # start a new line after pi.  Hence 'Erj'.
            constellation = m.group(7)
            if constellation == 'Erj':
                constellation = 'Eri'

            yield {
                "mag": float(m.group(1).strip()),
                "ra": round(float(m.group(2).strip()), 5),
                "npd": round(float(m.group(3).strip()), 4),
                "dec": round(90 - float(m.group(3).strip()), 4),
                "bayer": m.group(4).strip(),
                "superscript": None if m.group(5) == " " else m.group(5),
                "weight": int(m.group(6)),
                "constellation": constellation,
            }
        else:
            if not line.startswith('#'):
                print("WARNING: No match: {}".format(line), file=sys.stderr)


def parse_names(lines):
    name_lookup = {}
    for line in lines:
        abbr, name, _ = re.split(r'\t+', line)
        name = name.strip('"')

        name_lookup[abbr] = name
    return name_lookup


def wrangle_constellation(constellation_data):
    wrangled = constellation_data.copy()

    # Add raw x,y coordinates from orthographic projection, centered around
    # the constellation's center of "mass" (i.e. average position of constituent
    # stars)
    # NB: Right-ascension is stored in hours - to get degrees, we multiply by 15
    wrangled['ra_radians'] = degrees_to_radians(wrangled['ra']*15)
    wrangled['dec_radians'] = degrees_to_radians(wrangled['dec'])
    wrangled['raw_x'], wrangled['raw_y'] = orthographic_projection(
        lat=wrangled['dec_radians'],
        long=wrangled['ra_radians'],
        lat_origin=wrangled['dec_radians'].mean(),
        long_origin=wrangled['ra_radians'].mean(),
    )

    # Since we don't actually care about the absolute xy coordinates,
    # we recenter them to be roughly similar location and scale to shots.
    # This helps when finding the 'optimal' set of transformations to map a set
    # of shots to a set of stars
    coords = wrangled[['raw_x', 'raw_y']].values.transpose()

    # Data for recentering
    mid_x, mid_y = coords[0].mean(), coords[1].mean()
    # Per Opta coordinates, this will place the center of the constellation in
    # the middle of the attacking half
    target_x, target_y = 75, 50

    # Data for rescaling
    x_range = coords[0].max() - coords[0].min()
    y_range = coords[1].max() - coords[1].min()
    max_range = max(x_range, y_range)
    target_range = 20

    coords_recentered = geometry.apply_transformation(
        coords,
        angle=0,
        dx=target_x-mid_x,
        dy=target_y-mid_y,
        log_scale=np.log(target_range/max_range),
    )

    wrangled[['x', 'y']] = coords_recentered.transpose()

    # In the constellations data, each record refers to a link between two stars
    # (in the constellation visualisation). So, some stars are duplicated if they are
    # linked to multiple opther stars.
    # As a result, we separate and store the links and individual stars separately
    links = wrangled.copy()
    # Links are determined by their weight; all other columns are constant for each
    # star. Thus, each star can be identified by its coordinates, so simply taking the
    # distinct rows without the weight column returns the stars
    stars = wrangled.drop(['weight'], axis='columns').drop_duplicates()

    return links, stars


def degrees_to_radians(d):
    return d*np.pi/180


def orthographic_projection(long, lat, long_origin=0, lat_origin=0):
    """
    Project points onto cartesian plane using the orthographic projection,
    assuming a unit sphere (radius = 1).
    """
    x = np.cos(lat)*np.sin(long - long_origin)
    y = np.cos(lat_origin)*np.sin(lat) - np.sin(lat_origin)*np.cos(lat)*np.cos(long - long_origin)
    return x, y


if __name__ == '__main__':
    typer.run(main)
