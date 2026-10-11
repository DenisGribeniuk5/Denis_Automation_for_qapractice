"""
Login sandbox: https://www.qapractice.com/practice-login-form

The form fields expose data-testid. The site documents those as the
locators to prefer, so this page uses them.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/practice-login-form"

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = self.set_locator(
            "heading",
            page.get_by_role(
                "heading", name="Login to Your Practice Account", exact=True
            ),
        )
        self.email_input = self.set_locator(
            "email_input", page.get_by_test_id("login-email")
        )
        self.password_input = self.set_locator(
            "password_input", page.get_by_test_id("login-password")
        )
        self.submit_button = self.set_locator(
            "submit_button", page.get_by_test_id("login-submit")
        )
        self.success_message = self.set_locator(
            "success_message", page.get_by_test_id("login-success")
        )
        self.error_message = self.set_locator(
            "error_message", page.get_by_test_id("login-error")
        )

    def sign_in(self, email: str, password: str):
        """Fill the form and click Sign in. The banner appears after the click."""
        self.log.info("Sign in")
        self.fill(self.email_input, email)
        self.fill(self.password_input, password)
        self.click(self.submit_button)
