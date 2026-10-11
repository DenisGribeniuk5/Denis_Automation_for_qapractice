"""Data-driven contact form scenarios. Sentences are defined in tests/conftest.py."""

from pathlib import Path

from pytest_bdd import scenarios

FEATURES = Path(__file__).resolve().parents[1] / "features"
scenarios(str(FEATURES / "contact_ddt.feature"))
