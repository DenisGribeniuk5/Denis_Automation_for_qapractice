"""Data-driven home page scenarios. Sentences are defined in tests/conftest.py."""

from pathlib import Path

from pytest_bdd import scenarios

FEATURES = Path(__file__).resolve().parents[1] / "features"
scenarios(str(FEATURES / "home_ddt.feature"))
