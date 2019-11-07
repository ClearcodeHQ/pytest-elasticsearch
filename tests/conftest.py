"""Tests main conftest file."""
import warnings

from pytest_elasticsearch import factories

warnings.simplefilter("error", category=DeprecationWarning)
