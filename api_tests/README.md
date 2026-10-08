# Restful Booker API tests

API test framework for [Restful Booker](https://restful-booker.herokuapp.com/apidoc/), built with **Python**, **pytest**, **requests**, **pydantic**, and **Allure**.

53 tests cover the health check, token auth, the full booking CRUD flow, an end-to-end booking lifecycle, name and date filters, XML responses, response times, edge-case input, and negative cases (missing or invalid token, unknown id, missing required fields).

Eight of them are marked `xfail(strict=True)`: each one documents a defect found in the API. If the API is fixed, the test starts passing and strict mode fails the run, so the marker gets removed.

### Book Store API

`tests/book_store/` covers the [demoqa Book Store API](https://demoqa.com/swagger/) with one end-to-end test. A new user logs in with a bearer token, adds one book, checks it is in the collection, deletes all books, deletes the account, and checks that the user can no longer be found or log in. A `finally` block removes the user if any step fails.

`test_user_books_ui_api.py` mixes API and UI with Playwright. The API creates the user, the UI logs in and adds 3 books, the API deletes 1, and the UI profile shows the other 2. The API then deletes the books and the user, and the UI login rejects that user. Every UI login gives the user a new token, so the API client takes the token from the browser's cookie. Ads and trackers are blocked so pages load faster.

## Stack

| Concern | Tool |
| --- | --- |
| HTTP | `requests` with one shared `Session` per client |
| Tests | `pytest`, with `parametrize` for data-driven cases, run in parallel by `pytest-xdist` |
| UI | Playwright via `pytest-playwright`, with page objects in `pages/` |
| Response contracts | `pydantic` models with `extra="forbid"`, so a new or renamed field fails the test |
| Test data | Faker builders that return a valid booking, with any field overridable, and a JSON file of edge cases |
| Reporting | Allure. Each request and response is attached, and the run writes `reports/index.html` |
| Code style | `ruff` lint and format, checked in CI |
| Dependencies | `uv`, with a locked `uv.lock` |

## Design

- **API client layer.** `BaseClient` sends every request through one method that logs it and attaches it to Allure. `BookingClient` has one method per endpoint, so tests never build URLs.
- **Fixtures own setup and cleanup.** `booking` creates a fresh booking for the test and deletes it afterwards, so tests don't depend on each other or on shared data. The auth token is fetched once per session.
- **Contracts, not just status codes.** Responses are validated against pydantic models, and saved data is compared field by field with what was sent.
- **Retries only where they are safe.** The API runs on Heroku, which sometimes drops a connection or answers 503 while waking up. GET requests are retried with backoff. POST is not, because repeating it could create a second booking.
- **Parallel-safe.** Every test creates its own booking and searches by its own random name, so tests can run on four workers without seeing each other's data.
- **Known API quirks are documented in the tests.** Bad credentials return 200, delete returns 201, and a missing required field returns 500 instead of 400. Each assertion has a comment, so a change in behaviour is visible.

## Defects found

| Defect | Test |
| --- | --- |
| Negative, fractional, and text prices are accepted (text is stored as `null`, fractions are truncated) | `test_invalid_booking_is_rejected` |
| Checkout before checkin is accepted | `test_invalid_booking_is_rejected` |
| An invalid date is stored as `0NaN-aN-aN` | `test_invalid_booking_is_rejected` |
| Empty first and last names are accepted | `test_invalid_booking_is_rejected` |
| PATCH with one date wipes the other date | `test_patch_one_date_keeps_the_other` |
| The `checkin` filter leaves out bookings that start on that exact date | `test_checkin_filter_includes_same_day` |
| A missing required field returns 500, not 400 | `test_create_without_required_field_fails` |
| Changing an unknown booking returns 405, not 404 | `test_change_unknown_booking_returns_405` |
| XML responses are labelled `text/html` | `test_get_booking_as_xml` |
| Book Store: creating a user returns `userID`, but the spec says `userId` | `CreatedUser` model |
| Book Store: getting a deleted user returns 401, not 404 | `test_user_adds_book_then_clears_collection_and_is_deleted` |

## Layout

```
api/
  base_client.py     session, logging, Allure attachments
  booking_client.py  one method per endpoint
  book_store_client.py  demoqa Account and BookStore endpoints
models/              pydantic response models, one file per API
pages/               Playwright page objects for the demoqa Book Store UI
helper/builders.py   Faker booking payloads
helper/data.py       loads data/*.json cases as pytest params
data/                edge-case bookings, valid and invalid
tests/               test_*.py grouped by feature
conftest.py          client, token, and booking fixtures
config.py            BASE_URL, credentials, and response-time limit from .env
```

## Run

The project lives in `api_tests/`, separate from the UI framework at the repo root, and has its own dependencies.

```bash
cd api_tests
uv sync
uv run playwright install chromium
cp .env.example .env
uv run pytest
```

GitHub Actions (`.github/workflows/api-tests.yml`) runs the suite on every push that changes `api_tests/`, every such pull request, and daily at 06:00 UTC.

Useful variations:

```bash
uv run pytest -m smoke                  # smoke checks only
uv run pytest -k negative               # one group
uv run pytest -n 0                      # no parallel workers, easier to debug
uv run pytest tests/book_store --headed -n 0 --slowmo 500   # watch the UI test
uv run ruff check . && uv run ruff format .
uv run pytest --log-file-level=DEBUG    # also log request and response bodies
```

## Allure report

`uv run pytest` saves one HTML file: `reports/index.html`. Open that file:

```bash
open reports/index.html
```

The DemoQA Book Store test is in that report with the other API tests. Each call is a step, and the request and response are attached. Install the [Allure command](https://allurereport.org/docs/install/) once. Without it, pytest still runs and leaves the raw files in `allure-results/`.

Do not open `allure-report/index.html`. That page loads extra files, and a browser opened from disk blocks them and shows **500 Failed to fetch**.
