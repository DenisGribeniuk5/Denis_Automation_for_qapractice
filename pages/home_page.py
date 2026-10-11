"""
Home page: https://www.qapractice.com/

Locators use the accessible role and name, the way a user or a screen
reader finds the element. data-testid is used where the site provides one.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.set_locator(
            "heading",
            page.get_by_role(
                "heading", name="The Ultimate Automation Playground", exact=True
            ),
        )
        # These are <a> tags, but the site sets role="button" on them.
        # get_by_role follows the accessible role, so ask for a button.
        self.start_practicing = self.set_locator(
            "start_practicing",
            page.get_by_role("button", name="Start Practicing", exact=True),
        )
        self.browse_questions = self.set_locator(
            "browse_questions",
            page.get_by_role("button", name="Browse Interview Questions", exact=True),
        )

    def open_practice_sites_from_hero(self):
        """The big "Start Practicing" button, not the menu link."""
        from pages.practice_sites_page import PracticeSitesPage

        self.log.info("Click Start Practicing")
        self.click(self.start_practicing)
        return PracticeSitesPage(self.page)

    def open_interview_from_hero(self):
        from pages.interview_page import InterviewPage

        self.log.info("Click Browse Interview Questions")
        self.click(self.browse_questions)
        return InterviewPage(self.page)
