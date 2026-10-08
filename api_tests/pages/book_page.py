from playwright.sync_api import expect

from pages.base_page import BasePage


class BookPage(BasePage):
    """One book's details, opened from the store at /books?search=<isbn>."""

    def __init__(self, page, isbn: str):
        super().__init__(page)
        self.path = f"/books?search={isbn}"
        self.isbn = page.get_by_text(isbn, exact=True)
        self.add_button = page.get_by_role("button", name="Add To Your Collection")

    def add_to_collection(self):
        """Clicks Add and accepts the alert the site shows. Returns the alert text."""
        expect(self.isbn).to_be_visible()
        with self.page.expect_event("dialog") as dialog_info:
            self.add_button.click()
        dialog = dialog_info.value
        message = dialog.message
        dialog.accept()
        return message
