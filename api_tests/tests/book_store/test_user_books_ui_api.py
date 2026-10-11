import logging

import allure
import pytest

from models.book_store import BookList, User
from pages.book_page import BookPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage

log = logging.getLogger(__name__)


@allure.feature("Book Store")
@allure.story("API and UI")
@pytest.mark.smoke
def test_books_added_in_ui_and_removed_through_api(page, api_user):
    """API creates the user, the UI adds 3 books, the API removes 1, and the UI shows the other 2.
    Then the API deletes the books and the user, and the UI login rejects that user."""
    client, user_id, username, password = api_user
    books = BookList.model_validate(client.get_books().json()).books[:3]

    with allure.step("Log in through the UI"):
        log.info("Log in through the UI as %s", username)
        LoginPage(page).open().login(username, password)
        profile = ProfilePage(page)
        profile.expect_user(username)
        # Each login replaces the user's token, so the API must use the one the browser got.
        client.authorize(profile.token())

    with allure.step("Add 3 books through the UI"):
        for book in books:
            log.info("Add %s (%s) through the UI", book.title, book.isbn)
            message = BookPage(page, book.isbn).open().add_to_collection()
            assert message == "Book added to your collection."

    with allure.step("API shows the 3 books"):
        log.info("Check the API lists the 3 books")
        saved = User.model_validate(client.get_user(user_id).json())
        assert [b.isbn for b in saved.books] == [b.isbn for b in books]

    with allure.step("Delete the first book through the API"):
        log.info("Delete %s through the API", books[0].isbn)
        response = client.delete_book(user_id, books[0].isbn)
        assert response.status_code == 204, response.text

    with allure.step("UI shows the other 2 books"):
        log.info("Check the UI lists the other 2 books")
        ProfilePage(page).open().expect_books([b.title for b in books[1:]])

    with allure.step("Delete all books and the user through the API"):
        log.info("Delete all books and the user through the API")
        assert client.delete_all_books(user_id).status_code == 204
        assert client.delete_user(user_id).status_code == 204

    with allure.step("UI login rejects the deleted user"):
        log.info("Check the UI rejects login for the deleted user")
        page.context.clear_cookies()
        login = LoginPage(page).open()
        login.login(username, password)
        login.expect_invalid_credentials()
