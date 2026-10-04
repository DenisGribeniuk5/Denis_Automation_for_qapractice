"""
Step definitions for the feature files in features/.

Each sentence is defined once. pytest-bdd matches the feature text to these
functions. target_fixture="opened" is the page the later steps should use.
"""

from playwright.sync_api import expect
from pytest_bdd import given, then, when

from data.contact import CONTACT_MESSAGE
from data.interview import SEARCH_QUERY


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


@when("the user fills the contact form", target_fixture="opened")
def fill_the_contact_form(opened):
    opened.fill_message(**CONTACT_MESSAGE)
    return opened


@then("the main heading is visible")
def main_heading_is_visible(opened):
    expect(opened.heading).to_be_visible()


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


@then("the contact form shows the typed message")
def contact_form_shows_the_typed_message(opened):
    expect(opened.name_input).to_have_value(CONTACT_MESSAGE["name"])
    expect(opened.email_input).to_have_value(CONTACT_MESSAGE["email"])
    expect(opened.topic_select).to_have_value(CONTACT_MESSAGE["topic"])
    expect(opened.message_input).to_have_value(CONTACT_MESSAGE["message"])


@then("the send button is visible")
def send_button_is_visible(opened):
    expect(opened.submit_button).to_be_visible()
