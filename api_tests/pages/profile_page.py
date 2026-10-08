from playwright.sync_api import expect

from pages.base_page import BasePage


class ProfilePage(BasePage):
    path = "/profile"

    def __init__(self, page):
        super().__init__(page)
        self.username = page.locator("#userName-value")
        # Each book row has a title link inside a span with id "see-book-<title>".
        self.book_titles = page.locator("span[id^='see-book-'] a")

    def token(self) -> str:
        """The token the site saved in a cookie after login."""
        cookies = self.page.context.cookies()
        return next(c["value"] for c in cookies if c["name"] == "token")

    def expect_user(self, username: str):
        expect(self.username).to_have_text(username)

    def expect_books(self, titles: list[str]):
        expect(self.book_titles).to_have_text(titles, ignore_case=False)
