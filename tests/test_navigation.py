"""
Menu checks. Every screen inherits the header from BasePage,
so these tests start on Home and walk through the shared menu.
"""

from playwright.sync_api import expect


def test_menu_opens_practice_sites(home):
    practice = home.go_to_practice_sites()
    expect(practice.heading).to_be_visible()


def test_menu_opens_interview_prep(home):
    interview = home.go_to_interview()
    expect(interview.heading).to_be_visible()
    expect(interview.search_box).to_be_visible()


def test_menu_opens_about(home):
    about = home.go_to_about()
    expect(about.heading).to_be_visible()


def test_menu_opens_contact(home):
    contact = home.go_to_contact()
    expect(contact.heading).to_be_visible()


def test_logo_returns_home(contact):
    home = contact.go_home()
    expect(home.heading).to_be_visible()
