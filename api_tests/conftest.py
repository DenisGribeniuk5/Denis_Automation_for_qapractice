import shutil
import subprocess
from pathlib import Path

import pytest

from api.booking_client import BookingClient
from config import ADMIN_PASSWORD, ADMIN_USERNAME, BASE_URL, DEMOQA_URL
from helper.builders import booking_payload


@pytest.fixture
def client() -> BookingClient:
    """A client with no auth token."""
    return BookingClient()


@pytest.fixture(scope="session")
def token() -> str:
    response = BookingClient().create_token(ADMIN_USERNAME, ADMIN_PASSWORD)
    assert response.status_code == 200, response.text
    return response.json()["token"]


@pytest.fixture
def auth_client(token) -> BookingClient:
    """A client that sends the admin token, needed for PUT, PATCH, and DELETE."""
    client = BookingClient()
    client.authorize(token)
    return client


@pytest.fixture
def booking(auth_client):
    """Creates a booking for the test and deletes it afterwards."""
    payload = booking_payload()
    response = auth_client.create_booking(payload)
    assert response.status_code == 200, response.text
    booking_id = response.json()["bookingid"]
    yield booking_id, payload
    auth_client.delete_booking(booking_id)


def pytest_sessionfinish(session, exitstatus):
    """Save one HTML report in reports/ after the run.

    Pytest writes raw files to allure-results/. The Allure command turns
    those into reports/index.html, including the DemoQA Book Store calls.
    Open that file in a browser. A multi-file report opened from disk
    shows "500 Failed to fetch".
    """
    # xdist workers finish before the controller has every result file.
    if getattr(session.config, "workerinput", None) is not None:
        return

    results = Path("allure-results")
    if not any(results.glob("*-result.json")):
        return

    results.joinpath("environment.properties").write_text(
        f"Restful-Booker={BASE_URL}\nDemoQA={DEMOQA_URL}\n"
    )

    allure_command = shutil.which("allure")
    if allure_command is None:
        print("Allure command was not found. Raw results stay in allure-results/.")
        return

    completed = subprocess.run(
        [
            allure_command,
            "generate",
            str(results),
            "--clean",
            "--single-file",
            "-o",
            "reports",
        ],
        check=False,
    )
    if completed.returncode == 0:
        print("HTML report: reports/index.html")
        print("Open it with: open reports/index.html")
