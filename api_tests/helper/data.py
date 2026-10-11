import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def cases(file_name: str, group: str, **marks) -> list:
    """Loads one group of a data file as pytest params, using each case's id as the test id."""
    rows = json.loads((DATA_DIR / file_name).read_text(encoding="utf-8"))[group]
    return [pytest.param(row["fields"], id=row["id"], **marks) for row in rows]
