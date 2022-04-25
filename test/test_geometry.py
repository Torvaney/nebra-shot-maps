import functools
from context import geometry

import numpy as np
from hypothesis import given, strategies as st
from hypothesis.extra.numpy import arrays


st_finite_floats = functools.partial(st.floats, allow_nan=False, allow_infinity=False)


def test_rotation_at_right_angles():
    coord = np.asarray([[1], [1]])

    assert np.allclose(geometry.apply(coord, geometry.rotation(0)), coord)
    assert np.allclose(geometry.apply(coord, geometry.rotation(np.pi*0.5)),
                       np.asarray([[-1], [1]]))
    assert np.allclose(geometry.apply(coord, geometry.rotation(np.pi)),
                       np.asarray([[-1], [-1]]))
    assert np.allclose(geometry.apply(coord, geometry.rotation(np.pi*1.5)),
                       np.asarray([[1], [-1]]))
    assert np.allclose(geometry.apply(coord, geometry.rotation(np.pi*2)), coord)


@given(st_finite_floats())
def test_unit_scaling(x):
    coord = np.asarray([[1], [1]])
    new_coord = geometry.apply(coord, geometry.scaling(x))
    assert np.allclose(new_coord, np.asarray([[x], [x]]))


def test_apply_transformation():
    coords = np.asarray([[2, 2, 1, 1],
                         [2, 1, 2, 1]])

    scaled = geometry.apply_transformation(coords, 0, 0, 0, np.log(3))
    scaled_target = np.asarray([[3, 3, 0, 0],
                                [3, 0, 3, 0]])
    assert np.allclose(scaled, scaled_target)

    scaled = geometry.apply_transformation(coords, 0, 1, 1, np.log(3))
    assert np.allclose(scaled, scaled_target+1)


# Each transformation should be reversible

def transformation_with_reverse(coord, transformation, *args, reverse=lambda x: -x):
    forward = transformation(*args)
    backward = transformation(*[reverse(x) for x in args])

    end_coord = geometry.apply(coord, forward, backward)
    return np.allclose(coord, end_coord)


@given(arrays(float, [2, 10], elements=st_finite_floats()),
       st_finite_floats(),
       st_finite_floats())
def test_translation_is_reversible(coord, dx, dy):
    assert transformation_with_reverse(coord, geometry.translation, dx, dy)


@given(arrays(float, [2, 10], elements=st_finite_floats(min_value=-1e+5, max_value=1e+5)),
       st_finite_floats(min_value=-8, max_value=8))
def test_rotation_is_reversible(coord, angle):
    # NOTE: Hypothesis uncovered that at *extremely* large coordinates or number of turns
    #       there are some small errors introduced by this rotation calculation
    assert transformation_with_reverse(coord, geometry.rotation, angle)


@given(arrays(float, [2, 10], elements=st_finite_floats()),
       st_finite_floats(min_value=0.000001, exclude_min=True))
def test_scaling_is_reversible(coord, by):
    assert transformation_with_reverse(coord, geometry.scaling, by, reverse=lambda x: 1/x)
