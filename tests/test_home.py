"""
Home page checks.

Rule of thumb: one behaviour per test, and a name that says what you expect.
The assertion stays in the test. The page object only knows how to find things.
"""

from playwright.sync_api import expect


def test_home_shows_main_heading(home):
    expect(home.heading).to_be_visible()


def test_home_offers_practice_and_interview(home):
    expect(home.start_practicing).to_be_visible()
    expect(home.browse_questions).to_be_visible()


def test_start_practicing_opens_the_sandbox_list(home):
    practice = home.open_practice_sites_from_hero()
    expect(practice.heading).to_be_visible()
