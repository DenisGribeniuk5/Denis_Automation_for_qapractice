"""Interview library: search box, and the JavaScript technology checkbox."""

from playwright.sync_api import expect

from data.interview import SEARCH_QUERY


def test_search_box_keeps_the_query(interview):
    interview.search(SEARCH_QUERY)
    expect(interview.search_box).to_have_value(SEARCH_QUERY)


def test_javascript_checkbox_filters_questions(interview):
    # The checkbox label on the site says "JavaScript (21)".
    interview.check_javascript()

    expect(interview.javascript_checkbox).to_be_checked()
    expect(interview.result_count).to_have_text("21 questions")

    # Every card still on the page should be a JavaScript question.
    cards = interview.question_cards
    expect(cards.first).to_be_visible()
    for index in range(cards.count()):
        expect(cards.nth(index)).to_contain_text("JavaScript")
