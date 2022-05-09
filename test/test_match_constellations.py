import functools
from context import match_constellation, geometry

import numpy as np
from hypothesis import given, strategies as st, settings
from hypothesis.extra.numpy import arrays


st_finite_floats = functools.partial(st.floats, allow_nan=False, allow_infinity=False)


@given(
    arrays(float, [2, 10], elements=st_finite_floats(min_value=-100, max_value=100)),
    arrays(float, [4], elements=st_finite_floats(min_value=-10, max_value=10))
)
@settings(max_examples=10)
def test_best_transformation_can_be_recovered(coords, params):
    coords2 = geometry.apply_transformation(coords, *params)
    res = match_constellation.find_best_transformation(
        coords,
        coords2,
        similarity=match_constellation.euclidean_similarity
    )
    assert np.isclose(res['x'], params).all()


@given(arrays(float, [2, 10], elements=st_finite_floats(min_value=-100, max_value=100)))
def test_identical_arrays_have_exact_match(coords):
    dist = match_constellation.evaluate_match(
        coords, coords,
        0, 0, 0, 0,
        similarity=match_constellation.euclidean_similarity
    )
    assert np.isclose(dist, 0)


@given(arrays(float, [2, 10], elements=st_finite_floats(min_value=-100, max_value=100)))
def test_nonidentical_arrays_have_positive_distance(coords):
    comparison_coords = geometry.apply(
        coords,
        geometry.translation(3.5, 2.5),
        geometry.rotation(np.pi*0.5)
    )
    dist = match_constellation.evaluate_match(
        coords, comparison_coords,
        0, 0, 0, 0,
        similarity=match_constellation.euclidean_similarity
    )
    assert dist > 0
