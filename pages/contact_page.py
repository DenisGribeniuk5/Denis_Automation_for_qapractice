"""
Contact page: https://www.qapractice.com/contact

The form fields expose data-testid. The site documents that as the
locator to prefer. We use it here.

The label "for" attributes do not match the input ids, so get_by_label()
is a poor fit on this form. data-testid does not have that problem.

Do not click "Open email draft" in a test. That button opens the
mail app on the machine running the test. Fill the fields and assert
the values instead.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class ContactPage(BasePage):
    PATH = "/contact"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.set_locator(
            "heading", page.get_by_text("Contact QA Practice", exact=True)
        )
        self.name_input = self.set_locator(
            "name_input", page.get_by_test_id("contact-name")
        )
        self.email_input = self.set_locator(
            "email_input", page.get_by_test_id("contact-email")
        )
        self.topic_select = self.set_locator(
            "topic_select", page.get_by_test_id("contact-topic")
        )
        self.message_input = self.set_locator(
            "message_input", page.get_by_test_id("contact-message")
        )
        self.submit_button = self.set_locator(
            "submit_button", page.get_by_test_id("contact-submit")
        )

    def fill_message(
        self, name: str, email: str, message: str, topic: str | None = None
    ):
        """Type a message. Leaves the topic on its default unless one is passed."""
        self.log.info("Fill contact form")
        self.fill(self.name_input, name)
        self.fill(self.email_input, email)
        if topic:
            self.select(self.topic_select, topic)
        self.fill(self.message_input, message)
