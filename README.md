# QA Practice UI tests

UI test framework for [qapractice.com](https://www.qapractice.com/), built with **Python**, **Playwright**, **pytest-bdd**, and **Allure**.

50 scenarios cover the home page, the site menu, the practice-sites index, the interview question library (search and topic filters), the contact form, and the login sandbox (the public demo account, and a password the site rejects).

## Stack

| Concern | Tool |
| --- | --- |
| Browser automation | Playwright (sync API) via `pytest-playwright` |
| Scenarios | Gherkin feature files run by `pytest-bdd` |
| Reporting | Allure, saved as one HTML file, with a screenshot on failure |
| Test data | Examples tables in the features, and Faker for generated input |
| Dependencies | `uv`, with a locked `uv.lock` |

## Design

- **Page Object Model.** Each screen is a class in `pages/` that holds its locators and actions. `BasePage` owns the header menu shared by every page, and routes clicks and typing through one place so each action is logged.
- **Locators by role, then test id.** Headings, links, and buttons are found by accessible role and name. Form fields and filters use the `data-testid` values the site provides. CSS by `href` is used only for the sandbox cards, which all share the same link text.
- **Behaviour in plain language.** `features/` describes what a user does and sees. Step definitions in `tests/conftest.py` are thin: they call page objects and assert with Playwright's auto-waiting `expect`.
- **Data-driven scenarios.** Each `*_ddt.feature` uses a `Scenario Outline` with an `Examples` table. One generic step covers every page, menu link, or topic, and lookup tables map the names in the table to page classes.
- **Traceable runs.** Every log line carries the running test's name, so `grep <test name> logs/tests.log` shows one scenario's steps. Failed tests attach a screenshot to the Allure report.
- **No side effects.** The contact scenarios fill and verify the form but never press "Open email draft", which would open the mail client on the machine running the suite.

## Layout

```
features/        Gherkin scenarios; *_ddt.feature are the data-driven versions
tests/
  conftest.py    step definitions
  test_*.py      load the feature files with scenarios()
pages/           page objects, one per screen, all inheriting BasePage
data/            input values for the plain scenarios
helper/
  fake.py        Faker wrappers
  users.py       reads username / password pairs from .env (for the login sandbox)
conftest.py      page fixtures, logging, failure screenshots, Allure report
config.py        BASE_URL
```

## Run

```bash
uv sync
uv run playwright install chromium
cp .env.example .env
uv run pytest
```

GitHub Actions runs the same command on every push and pull request.

Useful variations:

```bash
uv run pytest -m smoke                         # smoke-tagged scenarios only
uv run pytest tests/test_navigation_data_driven.py
uv run pytest --headed --slowmo 500            # watch the browser
uv run pytest --log-file-level=DEBUG           # also log locators and typed values
```

`.env.example` holds the public demo login from the site. The login scenarios read it through `get_user`.

## Report and logs

With the [Allure CLI](https://allurereport.org/docs/install/) installed, each run writes `reports/index.html`, a single file that opens straight from disk. Without it, the raw results stay in `allure-results/`.

Each run also replaces `logs/tests.log`:

```
2026-10-04 18:28:37 INFO  [test_start_practicing_opens_the_sandbox_list] HomePage: Open https://www.qapractice.com/
2026-10-04 18:28:40 INFO  [test_start_practicing_opens_the_sandbox_list] HomePage: Click Start Practicing
```

## Adding a scenario

1. New screen: add `pages/<name>_page.py` inheriting `BasePage`, with `PATH` and its locators.
2. Write the scenario in `features/<name>.feature`.
3. Add any new step sentences to `tests/conftest.py`.
4. Load the feature from `tests/test_<name>.py` with `scenarios(...)`.
