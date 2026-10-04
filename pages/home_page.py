"""
Home page: https://www.qapractice.com/

Locators use the visible text string, the same words a student sees on
the screen. Reach for data-testid when the site provides one.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.set_locator(
            "heading",
            page.get_by_text("The Ultimate Automation Playground", exact=True),
        )
        # Match the words on the link. The site also sets role="button",
        # but the visible text string is enough.
        self.start_practicing = self.set_locator(
            "start_practicing",
            page.get_by_text("Start Practicing", exact=True),
        )
        self.browse_questions = self.set_locator(
            "browse_questions",
            page.get_by_text("Browse Interview Questions", exact=True),
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
