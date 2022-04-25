""" Match constellations to shot-maps. """
import itertools
import sys
import json
import pathlib

import pandas as pd
import scipy.optimize as op
import numpy as np
import tqdm
import typer

import geometry


def find_best_transformation(shots, stars):
    """
    Find the best set of transformations to match a set of stars
    with a set of shots.
    """
    result = op.minimize(
        lambda x: evaluate_match(shots, stars, *x),
        x0=[0, 0, 0, 0]
    )
    return result


def evaluate_match(coords1, coords2, angle, dx, dy, log_scale):
    coords2_transformed = geometry.apply_transformation(coords2, angle, dx, dy, log_scale)

    # Construct cost matrix for linear sum assignment
    n_coords = coords1.shape[1]
    cost_matrix = np.zeros([n_coords, n_coords])
    for i1, i2 in itertools.product(range(n_coords), repeat=2):
        cost_matrix[i1, i2] = geometry.euclidean_distance(coords1[:, i1], coords2_transformed[:, i2])**2

    # Perform linear sum assignment and get mean squared distance
    sol_rows, sol_cols = op.linear_sum_assignment(cost_matrix)
    mean_dist = cost_matrix[sol_rows, sol_cols].mean()

    return mean_dist


def apply_transformation_to_df(df, transformations, pivot=None, xcol='x', ycol='y'):
    df = df.copy()
    coords = df[[xcol, ycol]].values.transpose()
    coords_transformed = geometry.apply_transformation(coords, *transformations, pivot=pivot)
    df[['x', 'y']] = coords_transformed.transpose()
    return df


def main(shots: typer.FileText, constellation_path: pathlib.Path):
    constellation = constellation_path.name
    min_stars = 5

    # Load the shots and constellation data
    shots = pd.read_csv(shots)
    stars = pd.read_csv(constellation_path/'stars.csv')
    links = pd.read_csv(constellation_path/'links.csv')

    if len(stars) < min_stars:
        typer.echo(f'{constellation} has fewer than {min_stars} shots. Skipping.')
        sys.exit(0)

    typer.echo('Counting shots for each game...')
    shot_counts = shots[['game_id', 'team_id']].value_counts()
    valid_games = shot_counts.loc[lambda n: n == len(stars)]
    typer.echo(f'Found {len(valid_games)} possible matches (with {len(stars)} shots)...')

    # For each valid set of match shots, evaluate the best possible match
    typer.echo(f'Matching {constellation} to shot-map...')
    transformations = {}
    for game_id, team_id in tqdm.tqdm(valid_games.index):
        game_shots = shots.loc[lambda df: (df['game_id'] == game_id) & (df['team_id'] == team_id)]

        # Find the best matching score subject to rotation, translation (x and y), and scaling
        # and store the result
        res = find_best_transformation(
            game_shots[['x', 'y']].values.transpose(),
            stars[['x', 'y']].values.transpose(),
        )
        transformations[(game_id, team_id)] = res

    typer.echo('Done! Saving output...')

    # Extract the best match and store the result
    game_id, team_id = min(transformations, key=lambda x: transformations[x]['fun'])
    match_result = transformations[(game_id, team_id)]
    match_metadata = {
        'constellation': constellation,
        'game_id': game_id,
        'team_id': team_id,
        'squared_distance': match_result['fun'],
        'transformations': list(match_result['x'])
    }

    # Fetch matched shots
    shots_matched = shots.loc[lambda df: (df['game_id'] == game_id) & (df['team_id'] == team_id)]

    # Transform stars and links
    stars_transformed = apply_transformation_to_df(stars, match_result['x'])
    links_transformed = apply_transformation_to_df(
        links, match_result['x'],
        pivot=(stars['x'].mean(), stars['y'].mean())
    )

    # Save metadata, matched shots, transformed stars and links
    with open(constellation_path/'match.json', 'w+') as json_file:
        json.dump(match_metadata, json_file)

    shots_matched.to_csv(constellation_path/'shots.csv', index=False)
    stars_transformed.to_csv(constellation_path/'stars_transformed.csv', index=False)
    links_transformed.to_csv(constellation_path/'links_transformed.csv', index=False)


if __name__ == '__main__':
    typer.run(main)
