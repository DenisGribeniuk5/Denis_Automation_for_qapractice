"""
Base page — shared behaviour for every screen.

Page Object Model (POM), in one sentence:
a page class holds the locators and the clicks; a test only calls those methods.

The header menu is the same on every page of qapractice.com, so it lives here.
Home, Contact, and the other pages inherit this class and add their own fields.
"""

import logging

from playwright.sync_api import Page

from config import BASE_URL


class BasePage:
    # Each child page replaces this with its own path, for example "/contact".
    PATH = "/"

    def __init__(self, page: Page):
        self.page = page
        # One logger per page class, so the log shows "HomePage: ...".
        # The level and the file are set in pytest.ini.
        self.log = logging.getLogger(type(self).__name__)

        # Scope menu locators to the header. The footer repeats some of the
        # same link names, and an unscoped locator would match both.
        self.header = self.set_locator("header", page.locator("nav.navbar"))
        self.logo = self.set_locator("logo", self.header.locator("a.navbar-brand"))
        self.practice_sites_link = self.set_locator(
            "practice_sites_link",
            self.header.get_by_role("link", name="Practice Sites", exact=True),
        )
        self.interview_link = self.set_locator(
            "interview_link",
            self.header.get_by_role("link", name="Interview Prep", exact=True),
        )
        self.about_link = self.set_locator(
            "about_link", self.header.get_by_role("link", name="About", exact=True)
        )
        self.contact_link = self.set_locator(
            "contact_link", self.header.get_by_role("link", name="Contact", exact=True)
        )

    def set_locator(self, name, locator):
        """Keep a locator, and write its selector at DEBUG.

        Turn these lines on with pytest --log-file-level=DEBUG.
        """
        self.log.debug("Locator %s = %s", name, self.selector(locator))
        return locator

    def click(self, locator):
        """Click, and write the selector at DEBUG."""
        self.log.debug("Click %s", self.selector(locator))
        locator.click()

    def fill(self, locator, value):
        """Type into a locator, and write the selector and the value at DEBUG."""
        self.log.debug("Fill %s value=%r", self.selector(locator), value)
        locator.fill(value)

    def select(self, locator, value):
        """Choose a dropdown option, and write the selector and value at DEBUG."""
        self.log.debug("Select %s value=%r", self.selector(locator), value)
        locator.select_option(value)

    @staticmethod
    def selector(locator):
        """The selector text inside Playwright's locator, without the frame wrapper."""
        text = str(locator)
        marker = "selector='"
        start = text.rfind(marker)
        if start == -1:
            return text
        start += len(marker)
        end = text.rfind("'")
        return text[start:end]

    def open(self):
        """Open this page. Playwright waits until the load event before returning."""
        url = f"{BASE_URL}{self.PATH}"
        self.log.info("Open %s", url)
        self.page.goto(url)

    def go_to_practice_sites(self):
        # Import inside the method so this file does not import every page at startup.
        from pages.practice_sites_page import PracticeSitesPage

        self.log.info("Click menu link: Practice Sites")
        self.click(self.practice_sites_link)
        return PracticeSitesPage(self.page)

    def go_to_interview(self):
        from pages.interview_page import InterviewPage

        self.log.info("Click menu link: Interview Prep")
        self.click(self.interview_link)
        return InterviewPage(self.page)

    def go_to_about(self):
        from pages.about_page import AboutPage

        self.log.info("Click menu link: About")
        self.click(self.about_link)
        return AboutPage(self.page)

    def go_to_contact(self):
        from pages.contact_page import ContactPage

        self.log.info("Click menu link: Contact")
        self.click(self.contact_link)
        return ContactPage(self.page)

    def go_home(self):
        from pages.home_page import HomePage

        self.log.info("Click logo")
        self.click(self.logo)
        return HomePage(self.page)
