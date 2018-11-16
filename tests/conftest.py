"""Tests main conftest file."""
import sys
import warnings

if not sys.version_info >= (3, 5):
    warnings.simplefilter("error", category=DeprecationWarning)
