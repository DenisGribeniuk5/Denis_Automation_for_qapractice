"""
Interview question library: https://www.qapractice.com/interview

The search field is a searchbox in the accessibility tree, so get_by_role
finds it by the label a screen reader would announce.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class InterviewPage(BasePage):
    PATH = "/interview"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.set_locator(
            "heading",
            page.get_by_role("heading", name="Interview Question Library"),
        )
        self.search_box = self.set_locator(
            "search_box",
            page.get_by_role("searchbox", name="Search interview questions"),
        )
        # data-testid is on the checkbox. The visible word "JavaScript"
        # is on the label. This is the JavaScript topic, not the
        # separate "JavaScript Coding" checkbox.
        self.javascript_checkbox = self.set_locator(
            "javascript_checkbox", page.get_by_test_id("filter-tech-javascript")
        )
        self.javascript_label = self.set_locator(
            "javascript_label", page.locator("label[for='tech-javascript']")
        )
        self.result_count = self.set_locator(
            "result_count", page.get_by_test_id("result-count")
        )
        self.question_cards = self.set_locator(
            "question_cards", page.locator("[data-testid^='question-card-']")
        )

    def search(self, text: str):
        """Type into the library search. Playwright clears the box first with fill()."""
        self.log.info("Search interview questions")
        self.fill(self.search_box, text)

    def check_javascript(self):
        """Tick JavaScript by clicking its label.

        A click on the input itself does not change this checkbox.
        The label next to it does, which is also what a user clicks.
        """
        self.log.info("Tick JavaScript filter")
        self.click(self.javascript_label)
