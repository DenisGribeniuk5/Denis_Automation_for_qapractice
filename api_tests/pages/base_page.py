from playwright.sync_api import Page

from config import DEMOQA_URL


class BasePage:
    path = "/"

    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto(f"{DEMOQA_URL}{self.path}", wait_until="domcontentloaded")
        return self
