"""
Project-wide fixtures and hooks.

- One fixture per page that opens it and returns the page object.
- The running test's name on every log line.
- A screenshot attached to Allure when a test fails.
- A single-file Allure report in reports/ at the end of the run.
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
from pages.login_page import LoginPage
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


@pytest.fixture
def login(page):
    login_page = LoginPage(page)
    login_page.open()
    return login_page


def pytest_runtest_logstart(nodeid, location):
    """Write the test name before its page steps, so the log is easy to follow."""
    global current_test
    # nodeid looks like "tests/test_home.py::test_the_main_heading_is_visible".
    # Keep only the part after "::".
    current_test = nodeid.split("::")[-1]
    log.info("pytest_runtest_logstart: START %s", nodeid)


def pytest_runtest_logfinish(nodeid, location):
    """Clear the test name, so lines written after the test do not carry it."""
    global current_test
    log.info("pytest_runtest_logfinish: FINISH %s", nodeid)
    current_test = "-"


def pytest_runtest_logreport(report):
    """Write the result. Setup and teardown appear only when they do not pass."""
    if report.when == "call" or not report.passed:
        log.info(
            "pytest_runtest_logreport: %s %s (%s)",
            report.outcome.upper(),
            report.nodeid,
            report.when,
        )


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

    log.info("pytest_runtest_makereport: attach screenshot of the failed test")
    allure.attach(
        page.screenshot(),
        name="screenshot",
        attachment_type=AttachmentType.PNG,
    )


# pytest-bdd hooks. They run for every scenario in every feature file.
# Each log line starts with the hook name, so you can see which hook wrote it:
#   grep pytest_bdd_ logs/tests.log
# Order for one step: before_step -> before_step_call -> after_step (or step_error).


def pytest_bdd_apply_tag(tag, function):
    """Runs once per tag on each scenario while pytest collects the tests, for example @smoke.

    No test is running yet, so these lines show [-]. Returning None lets
    pytest-bdd turn the tag into a mark as usual.
    """
    log.info("pytest_bdd_apply_tag: @%s", tag)
    return None


def pytest_bdd_before_scenario(request, feature, scenario):
    log.info(
        "pytest_bdd_before_scenario: Feature: %s | Scenario: %s",
        feature.name,
        scenario.name,
    )


def pytest_bdd_after_scenario(request, feature, scenario):
    log.info("pytest_bdd_after_scenario: Scenario: %s", scenario.name)


def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    """Runs before pytest-bdd prepares the step's arguments."""
    log.info("pytest_bdd_before_step: %s %s", step.keyword, step.name)


def pytest_bdd_before_step_call(
    request, feature, scenario, step, step_func, step_func_args
):
    """Runs just before the Python function for the step is called."""
    log.info(
        "pytest_bdd_before_step_call: %s(%s)",
        step_func.__name__,
        ", ".join(step_func_args),
    )


def pytest_bdd_after_step(
    request, feature, scenario, step, step_func, step_func_args
):
    log.info("pytest_bdd_after_step: PASSED %s %s", step.keyword, step.name)


def pytest_bdd_step_error(
    request, feature, scenario, step, step_func, step_func_args, exception
):
    log.error(
        "pytest_bdd_step_error: FAILED %s %s -> %s: %s",
        step.keyword,
        step.name,
        type(exception).__name__,
        exception,
    )


def pytest_bdd_step_func_lookup_error(request, feature, scenario, step, exception):
    """Runs when no function in tests/conftest.py matches the step's sentence."""
    log.error(
        "pytest_bdd_step_func_lookup_error: no step definition for %s %s",
        step.keyword,
        step.name,
    )


def pytest_sessionfinish(session, exitstatus):
    """Save one HTML report in reports/ after the run.

    Pytest first writes raw files to allure-results/. The Allure command
    turns those files into reports/index.html. Open that file in a browser.
    """
    log.info("pytest_sessionfinish: run finished, exit status %s", exitstatus)
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
