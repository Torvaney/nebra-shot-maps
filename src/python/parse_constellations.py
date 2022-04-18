"""
Read constellations data (i.e. data/SnT_constellations.txt) and convert it
into a format we prefer.
"""
import csv
import math
import re
import sys

import typer


def main(snt: typer.FileText, names: typer.FileText):
    # load constellations data and names
    constellations = list(parse_snt(snt))
    name_lookup = parse_names(names)

    # Join constellations to names & add xy
    constellations_parsed = [
        wrangle_constellation(c, name_lookup) for c in constellations
    ]

    # write to stdout as csv
    fields = constellations_parsed[0].keys()
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for row in constellations_parsed:
        writer.writerow(row)


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


def wrangle_constellation(constellation, name_lookup):
    wrangled = constellation.copy()

    # Add full name of constellation
    wrangled['name'] = name_lookup[wrangled['constellation']]

    # Add "proper" x,y coordinates
    # NOTE: I don't think this actually works?
    ra_degrees = constellation['ra']*15
    xy = eqpole(
        long=ra_degrees,
        lat=constellation['dec']
    )
    wrangled['x'] = xy['x']
    wrangled['y'] = xy['y']

    return wrangled


def eqpole(long, lat, southpole=False):
    """
    Convert Right Ascension and declination to X,Y using an equal-area polar
    projection.

    Adapted from astrolibR package, available under GPL v2.
    """
    radeg = 180/math.pi

    if southpole:
        l1 = -long/radeg
        b1 = -lat/radeg
    else:
        l1 = long/radeg
        b1 = lat/radeg

    sq = max(2 * (1 - math.sin(b1)), 0)
    r = 18 * 3.53553391 * math.sqrt(sq)
    x = r*math.cos(l1)
    y = r*math.sin(l1)

    return {'x': x, 'y': y}


if __name__ == '__main__':
    typer.run(main)
