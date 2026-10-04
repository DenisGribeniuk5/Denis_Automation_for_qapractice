"""
Step definitions for the feature files in features/.

Each sentence is defined once. pytest-bdd matches the feature text to these
functions. target_fixture="opened" is the page the later steps should use.
"""

import re

from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

from data.contact import CONTACT_MESSAGE
from data.interview import SEARCH_QUERY
from pages.about_page import AboutPage
from pages.base_page import BasePage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.interview_page import InterviewPage
from pages.practice_sites_page import PracticeSitesPage

# Data-driven steps take a page name from the Examples table in a feature file.
# These tables turn that name into the page class, or the menu click to use.
PAGES = {
    "Home": HomePage,
    "Practice Sites": PracticeSitesPage,
    "Interview Prep": InterviewPage,
    "About": AboutPage,
    "Contact": ContactPage,
}

MENU_LINKS = {
    "Practice Sites": BasePage.go_to_practice_sites,
    "Interview Prep": BasePage.go_to_interview,
    "About": BasePage.go_to_about,
    "Contact": BasePage.go_to_contact,
}

# The two big buttons on the home page, not the menu links.
HERO_BUTTONS = {
    "Start Practicing": HomePage.open_practice_sites_from_hero,
    "Browse Interview Questions": HomePage.open_interview_from_hero,
}


def quoted(value):
    """Drop the quote marks around a {string} value from a feature file.

    The sentence is written as the "Home" page. The parser keeps the marks,
    so the value arrives as '"Home"'.
    """
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


@given("the home page is open", target_fixture="opened")
def home_page_is_open(home):
    """The home fixture in the project conftest.py already opened the page."""
    return home


@given("the contact page is open", target_fixture="opened")
def contact_page_is_open(contact):
    return contact


@given("the interview page is open", target_fixture="opened")
def interview_page_is_open(interview):
    return interview


@given("the practice sites page is open", target_fixture="opened")
def practice_sites_page_is_open(practice_sites):
    return practice_sites


@given(parsers.parse("the {string} page is open"), target_fixture="opened")
def named_page_is_open(page, string):
    """Open any page by the name used in PAGES, for example "Contact"."""
    named_page = PAGES[quoted(string)](page)
    named_page.open()
    return named_page


@when("the user clicks Start Practicing", target_fixture="opened")
def click_start_practicing(opened):
    return opened.open_practice_sites_from_hero()


@when("the user opens Practice Sites from the menu", target_fixture="opened")
def open_practice_sites_from_menu(opened):
    return opened.go_to_practice_sites()


@when("the user opens Interview Prep from the menu", target_fixture="opened")
def open_interview_from_menu(opened):
    return opened.go_to_interview()


@when("the user opens About from the menu", target_fixture="opened")
def open_about_from_menu(opened):
    return opened.go_to_about()


@when("the user opens Contact from the menu", target_fixture="opened")
def open_contact_from_menu(opened):
    return opened.go_to_contact()


@when(parsers.parse("the user opens {string} from the menu"), target_fixture="opened")
def open_named_menu_link(opened, string):
    return MENU_LINKS[quoted(string)](opened)


@when(parsers.parse("the user clicks the hero button {string}"), target_fixture="opened")
def click_the_hero_button(opened, string):
    return HERO_BUTTONS[quoted(string)](opened)


@when(parsers.parse("the user opens the sandbox link to {string}"), target_fixture="opened")
def open_the_sandbox_link(opened, string):
    opened.open_sandbox(quoted(string))
    return opened


@when("the user clicks the logo", target_fixture="opened")
def click_the_logo(opened):
    return opened.go_home()


@when("the user searches the interview library", target_fixture="opened")
def search_the_interview_library(opened):
    opened.search(SEARCH_QUERY)
    return opened


@when("the user checks the JavaScript filter", target_fixture="opened")
def check_the_javascript_filter(opened):
    opened.check_javascript()
    return opened


@when(parsers.parse("the user searches the interview library for {string}"), target_fixture="opened")  # noqa: E501
def search_the_interview_library_for(opened, string):
    opened.search(quoted(string))
    return opened


@when(parsers.parse("the user ticks the topic filter {string}"), target_fixture="opened")
def tick_the_topic_filter(opened, string):
    opened.check_topic(quoted(string))
    return opened


@when("the user fills the contact form", target_fixture="opened")
def fill_the_contact_form(opened):
    opened.fill_message(**CONTACT_MESSAGE)
    return opened


# fmt: off
# One line, so the Cucumber extension can read the whole sentence.
@when(parsers.parse("the user fills the contact form with {name}, {email}, {topic} and {message}"), target_fixture="opened")  # noqa: E501
# fmt: on
def fill_the_contact_form_with(opened, name, email, topic, message):
    opened.fill_message(
        name=quoted(name),
        email=quoted(email),
        topic=quoted(topic),
        message=quoted(message),
    )
    return opened


@then("the main heading is visible")
def main_heading_is_visible(opened):
    expect(opened.heading).to_be_visible()


@then(parsers.parse("the page heading reads {string}"))
def page_heading_reads(opened, string):
    expect(opened.heading).to_have_text(quoted(string))


@then(parsers.parse("the address ends with {string}"))
def address_ends_with(opened, string):
    # Match the end of the URL only, so BASE_URL can change without editing features.
    path = quoted(string)
    expect(opened.page).to_have_url(re.compile(re.escape(path) + "$"))


@then(parsers.parse("the home page shows {string}"))
def home_page_shows(opened, string):
    # Same kind of locator as HomePage uses: the exact visible words.
    expect(opened.page.get_by_text(quoted(string), exact=True)).to_be_visible()


@then("Start Practicing is visible")
def start_practicing_is_visible(opened):
    expect(opened.start_practicing).to_be_visible()


@then("Browse Interview Questions is visible")
def browse_questions_is_visible(opened):
    expect(opened.browse_questions).to_be_visible()


@then("the Practice Sites heading is visible")
def practice_sites_heading_is_visible(opened):
    expect(opened.heading).to_be_visible()


@then("the Interview library heading is visible")
def interview_heading_is_visible(opened):
    expect(opened.heading).to_be_visible()


@then("the interview search box is visible")
def interview_search_box_is_visible(opened):
    expect(opened.search_box).to_be_visible()


@then("the About heading is visible")
def about_heading_is_visible(opened):
    expect(opened.heading).to_be_visible()


@then("the Contact heading is visible")
def contact_heading_is_visible(opened):
    expect(opened.heading).to_be_visible()


@then("every sandbox link is visible")
def every_sandbox_link_is_visible(opened):
    for link in opened.sandbox_links:
        expect(link).to_be_visible()


@then(parsers.parse("the sandbox link to {string} is visible"))
def sandbox_link_is_visible(opened, string):
    expect(opened.sandbox_link(quoted(string))).to_be_visible()


@then("the search box shows the typed query")
def search_box_shows_the_typed_query(opened):
    expect(opened.search_box).to_have_value(SEARCH_QUERY)


@then("the JavaScript checkbox is selected")
def javascript_checkbox_is_selected(opened):
    expect(opened.javascript_checkbox).to_be_checked()


@then("21 JavaScript questions are listed")
def javascript_question_count(opened):
    # The checkbox label on the site says "JavaScript (21)".
    expect(opened.result_count).to_have_text("21 questions")


@then("every visible question is about JavaScript")
def visible_questions_are_javascript(opened):
    cards = opened.question_cards
    expect(cards.first).to_be_visible()
    for index in range(cards.count()):
        expect(cards.nth(index)).to_contain_text("JavaScript")


@then(parsers.parse("the search box contains {string}"))
def search_box_contains(opened, string):
    expect(opened.search_box).to_have_value(quoted(string))


@then(parsers.parse("the topic filter {string} is selected"))
def topic_filter_is_selected(opened, string):
    expect(opened.topic_checkbox(quoted(string))).to_be_checked()


@then(parsers.parse("the result count reads {string}"))
def result_count_reads(opened, string):
    expect(opened.result_count).to_have_text(quoted(string))


@then(parsers.parse("every visible question mentions {string}"))
def visible_questions_mention(opened, string):
    cards = opened.question_cards
    expect(cards.first).to_be_visible()
    for index in range(cards.count()):
        expect(cards.nth(index)).to_contain_text(quoted(string))


@then("the contact form shows the typed message")
def contact_form_shows_the_typed_message(opened):
    expect(opened.name_input).to_have_value(CONTACT_MESSAGE["name"])
    expect(opened.email_input).to_have_value(CONTACT_MESSAGE["email"])
    expect(opened.topic_select).to_have_value(CONTACT_MESSAGE["topic"])
    expect(opened.message_input).to_have_value(CONTACT_MESSAGE["message"])


# fmt: off
# One line, so the Cucumber extension can read the whole sentence.
@then(parsers.parse("the contact form shows {name}, {email}, {topic} and {message}"))
# fmt: on
def contact_form_shows(opened, name, email, topic, message):
    expect(opened.name_input).to_have_value(quoted(name))
    expect(opened.email_input).to_have_value(quoted(email))
    expect(opened.topic_select).to_have_value(quoted(topic))
    expect(opened.message_input).to_have_value(quoted(message))


@then("the send button is visible")
def send_button_is_visible(opened):
    expect(opened.submit_button).to_be_visible()
