""" Generate a webpage displaying the matched shots and constellations with jinja2. """
import json
import pathlib

import arrow
import jinja2
import pandas as pd
import typer


def main(
    constellations_path: pathlib.Path,
    templates_path: pathlib.Path,
    output_path: pathlib.Path,
):
    # Fetch the constellations data
    constellations = [
        parse_constellation(path)
        for path in constellations_path.iterdir()
        if is_valid_constellation(path)
    ]
    constellations = sorted(constellations, key=lambda x: x['average_distance'])

    # Generate the template
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_path)
    )
    template = env.get_template('template.html')
    html = template.render(constellations=constellations)

    # Save to file
    with open(output_path/'index.html', 'w+') as file:
        file.write(html)



def is_valid_constellation(path):
    return path.is_dir() and (path/'match.json').exists()


def parse_constellation(path):
    # I should have just put everything into a SQLite database in the first
    # place, tbh. This is a little bit messy...
    stars = pd.read_csv(path/'stars.csv')
    shots = pd.read_csv(path/'shots.csv')
    with open(path/'match.json', 'r') as file:
        match_meta = json.load(file)

    date = arrow.get(get_unique_field(shots['kickoff']))

    return {
        'name': get_unique_field(stars['name']),
        'abbreviation': path.name,
        'game_label': get_unique_field(shots['game_label']),
        'team': get_unique_field(shots['team']),
        'date': date.format('Do MMMM YYYY'),
        'average_distance': match_meta['distance']/len(stars),
    }


def get_unique_field(data):
    uniques = data.unique()
    if len(uniques) != 1:
        raise ValueError('More than one value found!')
    return uniques[0]


if __name__ == '__main__':
    typer.run(main)
