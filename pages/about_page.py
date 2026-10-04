"""
About page: https://www.qapractice.com/AboutPage

The path uses a capital A. Copy it exactly; web servers can treat
"/AboutPage" and "/aboutpage" as different addresses.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class AboutPage(BasePage):
    PATH = "/AboutPage"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.set_locator(
            "heading", page.get_by_role("heading", name="About QA Practice")
        )
