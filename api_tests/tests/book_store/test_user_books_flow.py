import allure
import pytest

from api.book_store_client import BookStoreClient
from helper.builders import user_credentials
from models.book_store import AddedBooks, ApiError, BookList, CreatedUser, Token, User


@allure.feature("Book Store")
@allure.story("End to end")
@pytest.mark.smoke
def test_user_adds_book_then_clears_collection_and_is_deleted():
    """A new user adds one book, removes all books, and deletes the account."""
    client = BookStoreClient()
    username, password = user_credentials()
    user_id = None

    try:
        with allure.step("Create user"):
            response = client.create_user(username, password)
            assert response.status_code == 201, response.text
            user = CreatedUser.model_validate(response.json())
            assert user.username == username
            assert user.books == []
            user_id = user.user_id

        with allure.step("Log in"):
            response = client.generate_token(username, password)
            assert response.status_code == 200, response.text
            token = Token.model_validate(response.json())
            assert token.status == "Success"
            client.authorize(token.token)

        with allure.step("Add one book"):
            book = BookList.model_validate(client.get_books().json()).books[0]
            response = client.add_books(user_id, [book.isbn])
            assert response.status_code == 201, response.text
            assert AddedBooks.model_validate(response.json()).books == [{"isbn": book.isbn}]

            saved = User.model_validate(client.get_user(user_id).json())
            assert saved.books == [book]

        with allure.step("Delete all books"):
            response = client.delete_all_books(user_id)
            assert response.status_code == 204, response.text
            assert User.model_validate(client.get_user(user_id).json()).books == []

        with allure.step("Delete user"):
            response = client.delete_user(user_id)
            assert response.status_code == 204, response.text
            user_id = None

        with allure.step("User is gone"):
            response = client.get_user(user.user_id)
            # The API answers 401 rather than 404 for a deleted user.
            assert response.status_code == 401
            assert ApiError.model_validate(response.json()).message == "User not found!"
            assert client.generate_token(username, password).json()["status"] == "Failed"
    finally:
        if user_id:
            client.delete_user(user_id)
