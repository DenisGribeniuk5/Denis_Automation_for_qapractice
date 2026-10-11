from playwright.sync_api import expect

from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    def __init__(self, page):
        super().__init__(page)
        self.username = page.locator("#userName")
        self.password = page.locator("#password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error = page.locator("#name")

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def expect_invalid_credentials(self):
        expect(self.error).to_have_text("Invalid username or password!")
