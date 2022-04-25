import pytest
import functools
from context import match_constellation, geometry

import numpy as np
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays


st_finite_floats = functools.partial(st.floats, allow_nan=False, allow_infinity=False)


# TODO: test that `find_best_transformation` can recover an exact set of transformations
# i.e. `apply_transformations` to an array, and check that `res['x']` is the same


@given(arrays(float, [2, 10], elements=st_finite_floats(min_value=-100, max_value=100)))
def test_identical_arrays_have_exact_match(coords):
    assert np.isclose(match_constellation.evaluate_match(coords, coords, 0, 0, 0, 0), 0)


@given(arrays(float, [2, 10], elements=st_finite_floats(min_value=-100, max_value=100)))
def test_nonidentical_arrays_have_positive_distance(coords):
    comparison_coords = geometry.apply(
        coords,
        geometry.translation(3.5, 2.5),
        geometry.rotation(np.pi*0.5)
    )
    assert match_constellation.evaluate_match(coords, comparison_coords, 0, 0, 0, 0) > 0
