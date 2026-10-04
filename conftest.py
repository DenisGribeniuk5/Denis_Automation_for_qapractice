"""
Fixtures: setup that pytest hands to a test.

pytest-playwright already provides `page` — a new browser tab per test,
closed when the test finishes. You do not write browser start/stop code.

A fixture named `home` opens the home page and returns the page object.
The test asks for it by name:

    def test_something(home):
        ...
"""

import logging
import shutil
import subprocess
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType

from pages.about_page import AboutPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.interview_page import InterviewPage
from pages.practice_sites_page import PracticeSitesPage

# Lines from this file show as "tests: ..." in logs/tests.log.
log = logging.getLogger("tests")

# Faker and asyncio write many DEBUG lines of their own. Keep only their warnings,
# so --log-file-level=DEBUG shows our steps and not library internals.
for library in ("faker", "asyncio"):
    logging.getLogger(library).setLevel(logging.WARNING)

# Name of the running test, shown as [test] on every log line (see pytest.ini).
# "-" means no test is running, for example while the report is built.
current_test = "-"
_make_record = logging.getLogRecordFactory()


def _record_with_test_name(*args, **kwargs):
    record = _make_record(*args, **kwargs)
    record.test = current_test
    return record


logging.setLogRecordFactory(_record_with_test_name)


@pytest.fixture
def home(page):
    home_page = HomePage(page)
    home_page.open()
    return home_page


@pytest.fixture
def practice_sites(page):
    practice_page = PracticeSitesPage(page)
    practice_page.open()
    return practice_page


@pytest.fixture
def interview(page):
    interview_page = InterviewPage(page)
    interview_page.open()
    return interview_page


@pytest.fixture
def about(page):
    about_page = AboutPage(page)
    about_page.open()
    return about_page


@pytest.fixture
def contact(page):
    contact_page = ContactPage(page)
    contact_page.open()
    return contact_page


def pytest_runtest_logstart(nodeid, location):
    """Write the test name before its page steps, so the log is easy to follow."""
    global current_test
    # "tests/test_home.py::test_home_shows_main_heading[chromium]" -> "test_home_shows_main_heading[chromium]"
    current_test = nodeid.split("::")[-1]
    log.info("START %s", nodeid)


def pytest_runtest_logfinish(nodeid, location):
    """Clear the test name, so lines written after the test do not carry it."""
    global current_test
    current_test = "-"


def pytest_runtest_logreport(report):
    """Write the result. Setup and teardown appear only when they do not pass."""
    if report.when == "call" or not report.passed:
        log.info("%s %s (%s)", report.outcome.upper(), report.nodeid, report.when)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """After a failed test, attach a screenshot to the Allure report.

    The browser tab is still open here. Pytest closes it afterwards.
    """
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None:
        return

    allure.attach(
        page.screenshot(),
        name="screenshot",
        attachment_type=AttachmentType.PNG,
    )


def pytest_sessionfinish(session, exitstatus):
    """Save one HTML report in reports/ after the run.

    Pytest first writes raw files to allure-results/. The Allure command
    turns those files into reports/index.html. Open that file in a browser.
    """
    results = Path("allure-results")
    if not any(results.glob("*-result.json")):
        return

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
