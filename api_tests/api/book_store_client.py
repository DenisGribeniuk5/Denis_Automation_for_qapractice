from api.base_client import BaseClient
from config import DEMOQA_URL


class BookStoreClient(BaseClient):
    """Account and BookStore endpoints of https://demoqa.com/swagger/"""

    def __init__(self, base_url: str = DEMOQA_URL):
        super().__init__(base_url)

    def create_user(self, username: str, password: str):
        return self.request(
            "POST", "/Account/v1/User", json={"userName": username, "password": password}
        )

    def generate_token(self, username: str, password: str):
        return self.request(
            "POST", "/Account/v1/GenerateToken", json={"userName": username, "password": password}
        )

    def authorize(self, token: str):
        self.session.headers["Authorization"] = f"Bearer {token}"

    def get_user(self, user_id: str):
        return self.request("GET", f"/Account/v1/User/{user_id}")

    def delete_user(self, user_id: str):
        return self.request("DELETE", f"/Account/v1/User/{user_id}")

    def get_books(self):
        return self.request("GET", "/BookStore/v1/Books")

    def add_books(self, user_id: str, isbns: list[str]):
        return self.request(
            "POST",
            "/BookStore/v1/Books",
            json={"userId": user_id, "collectionOfIsbns": [{"isbn": isbn} for isbn in isbns]},
        )

    def delete_book(self, user_id: str, isbn: str):
        return self.request("DELETE", "/BookStore/v1/Book", json={"userId": user_id, "isbn": isbn})

    def delete_all_books(self, user_id: str):
        return self.request("DELETE", "/BookStore/v1/Books", params={"UserId": user_id})
