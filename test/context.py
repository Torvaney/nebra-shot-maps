import pathlib
import sys

# Add src directory to path for tests

src_path = pathlib.Path(__file__).absolute().parents[1]/'src'
sys.path.insert(0, str(src_path))

from python import (
    geometry
)
