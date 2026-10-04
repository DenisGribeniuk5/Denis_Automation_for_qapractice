"""
Practice Sites index: https://www.qapractice.com/practice-page-selection

This page only lists the sandboxes. When you automate one sandbox
(login, store, flights), add a new file in pages/ for that screen.
Do not grow this class into every practice app.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class PracticeSitesPage(BasePage):
    PATH = "/practice-page-selection"

    def __init__(self, page: Page):
        super().__init__(page)
        # The menu also says "Practice Sites", so the heading is the h1 only.
        self.heading = self.set_locator(
            "heading",
            page.locator("h1").get_by_text("Practice Sites", exact=True),
        )

        # href is the stable locator. Card titles can be edited without
        # changing the address. The store URL really is spelled "ecommerece".
        self.login_link = self.set_locator(
            "login_link", page.locator('a[href="/practice-login-form"]')
        )
        self.web_form_link = self.set_locator(
            "web_form_link", page.locator('a[href="/practice-forms"]')
        )
        self.store_link = self.set_locator(
            "store_link", page.locator('a[href="/practice-ecommerece-website"]')
        )
        self.flight_link = self.set_locator(
            "flight_link", page.locator('a[href="/flight-booking-scenarios"]')
        )
        self.ui_elements_link = self.set_locator(
            "ui_elements_link",
            page.locator('a[href="/practice-different-ui-elements"]'),
        )
        self.xpath_link = self.set_locator(
            "xpath_link", page.locator('a[href="/SeleniumXPathGuide"]')
        )
        self.forgot_password_link = self.set_locator(
            "forgot_password_link", page.locator('a[href="/forget-password"]')
        )
        self.register_link = self.set_locator(
            "register_link", page.locator('a[href="/register"]')
        )
        self.api_link = self.set_locator(
            "api_link", page.locator('a[href="/api-playground"]')
        )

        self.sandbox_links = [
            self.login_link,
            self.web_form_link,
            self.store_link,
            self.flight_link,
            self.ui_elements_link,
            self.xpath_link,
            self.forgot_password_link,
            self.register_link,
            self.api_link,
        ]
