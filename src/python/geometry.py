import numpy as np


def euclidean_distance(coord1, coord2):
    return np.linalg.norm(coord1 - coord2)


# Creating & transforming coords

def to_homogenous(coords):
    _, n = coords.shape
    coords_homogenous = np.ones((3, n))
    coords_homogenous[:2, :] = coords
    return coords_homogenous


def apply(coord, *transformations):
    if len(transformations) == 0:
        return coord

    applied = np.linalg.multi_dot(
        list(reversed(transformations)) + [to_homogenous(coord)]
    )
    return applied[:2, :]


def apply_transformation(coords, angle, dx, dy, log_scale):
    mid_x = coords[0].mean()
    mid_y = coords[1].mean()
    return apply(
        coords,
        translation(-mid_x, -mid_y),  # translate to origin for scaling and rotation
        rotation(angle),
        scaling(np.exp(log_scale)),
        translation(mid_x, mid_y),    # translate back (from origin)
        translation(dx, dy),          # translate to final position
    )


# Create transformation matrices for 2D coordinates in homogenous form

def translation(dx, dy):
    return np.asarray([
        [1, 0, dx],
        [0, 1, dy],
        [0, 0, 1],
    ])


def rotation(angle):
    return np.asarray([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1],
    ])


def scaling(a):
    return np.asarray([
        [a, 0, 0],
        [0, a, 0],
        [0, 0, 1],
    ])
