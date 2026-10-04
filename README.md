# Denis_Automation_for_qapractice

Class project: UI tests for [QA Practice](https://www.qapractice.com/) with **Python**, **pytest**, **Playwright**, **Allure**, and **uv**.

The framework follows the Page Object Model and stays small on purpose (KISS). Locators live in `pages/`. Input values live in `data/`. Tests live in `tests/` and only call page methods.

Run every command in this folder, the one that contains this README. If the terminal prompt says `QA Practice`, move in first:

```bash
cd Denis_Automation_for_qapractice
```

## Layout

```
config.py            # site address, used by every page
conftest.py          # opens a page object for each test, then builds the Allure report
pages/               # one class per screen
  base_page.py       # header menu, shared by every page
  home_page.py
  practice_sites_page.py
  interview_page.py
  about_page.py
  contact_page.py
data/                # values the tests type in (not locators)
  contact.py         # contact form message, built with helper.fake
  interview.py       # search text
helper/              # shared tools
  fake.py            # fake_name(), fake_email(), fake_sentence(), fake_choice()
  users.py           # get_user("valid") reads one username / password pair from .env
.env                 # practice accounts, not committed
logs/                # tests.log from the last run, not committed
tests/               # one behaviour per test
pytest.ini           # pytest options, including the log file and its level
pyproject.toml       # dependencies for uv
```

## Setup

```bash
uv sync
uv run playwright install chromium
```

`uv sync` creates `.venv` and installs the Python packages from `pyproject.toml` (pytest, Playwright, Faker, python-dotenv, Allure's pytest plugin). The second command downloads the Chromium browser Playwright drives.

Install the Allure command-line tool once, separate from Python: [Allure install](https://allurereport.org/docs/install/). Without it, pytest still runs, but it cannot write `reports/index.html`.

## Run

```bash
uv run pytest
```

Watch the browser:

```bash
uv run pytest --headed
```

Slow the actions down (the number is milliseconds):

```bash
uv run pytest tests/test_interview.py --headed --slowmo 500
```

Run one file:

```bash
uv run pytest tests/test_home.py
```

## Allure report

`uv run pytest` saves the report as one HTML file: `reports/index.html`. Open that file:

```bash
open reports/index.html
```

A failed test includes a screenshot in the report.

Do not run `allure generate -o allure-report` and do not open `allure-report/index.html`. That page loads its data from extra files. A browser opened from disk blocks those requests and shows **500 Failed to fetch**.

## Logs

Every run writes `logs/tests.log`. The next run replaces it.

The default level is **INFO**. It records each test's start and result, every page opened, and every click:

```
2026-10-04 18:28:37 INFO  [test_start_practicing_opens_the_sandbox_list[chromium]] tests: START tests/test_home.py::test_start_practicing_opens_the_sandbox_list[chromium]
2026-10-04 18:28:37 INFO  [test_start_practicing_opens_the_sandbox_list[chromium]] HomePage: Open https://www.qapractice.com/
2026-10-04 18:28:40 INFO  [test_start_practicing_opens_the_sandbox_list[chromium]] HomePage: Click Start Practicing
2026-10-04 18:28:40 INFO  [test_start_practicing_opens_the_sandbox_list[chromium]] tests: PASSED tests/test_home.py::test_start_practicing_opens_the_sandbox_list[chromium] (call)
```

The name in `[...]` is the running test, so you can search the log for one test's lines:

```bash
grep test_start_practicing logs/tests.log
```

**DEBUG** also records the values typed into forms:

```bash
uv run pytest --log-file-level=DEBUG
```

To log from a page object, use `self.log`. `BasePage` names it after the class:

```python
self.log.info("Click Submit")             # a step: always in the log
self.log.debug("Email: %r", email)        # a detail: only with DEBUG
```

## Accounts

`.env` stores each practice account as one pair, `username / password`:

```
VALID=user@premiumbank.com / Bank@123
INVALID=wrong@example.com / nope
```

In a test:

```python
from helper.users import get_user

username, password = get_user("valid")
```

The valid pair is the demo login published on the [login practice page](https://www.qapractice.com/practice-login-form). Do not put a real personal password in `.env`.

## Add a test

1. If the screen is new, add `pages/your_page.py` and inherit `BasePage`. Set `PATH` and the locators in `__init__`.
2. Add a fixture in `conftest.py` only if several tests open that page directly.
3. Add `tests/test_your_page.py`. Ask for the fixture by name and assert with `expect(...)`.
4. If the test types text, put that text in `data/` and import it. Use `helper/fake.py` when the text should be made up. Do not paste the same string in the test and in the assertion.

Prefer `get_by_role` or `get_by_test_id`. The practice site puts `id` and `data-testid` on interactive elements so selectors stay stable.
