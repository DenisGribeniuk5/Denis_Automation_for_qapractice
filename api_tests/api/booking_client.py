from api.base_client import BaseClient


class BookingClient(BaseClient):
    """Endpoints of https://restful-booker.herokuapp.com/apidoc/"""

    def ping(self):
        return self.request("GET", "/ping")

    def create_token(self, username: str, password: str):
        return self.request("POST", "/auth", json={"username": username, "password": password})

    def authorize(self, token: str):
        self.session.cookies.set("token", token)

    def get_booking_ids(self, **filters):
        return self.request("GET", "/booking", params=filters)

    def get_booking(self, booking_id: int, accept: str = "application/json"):
        return self.request("GET", f"/booking/{booking_id}", headers={"Accept": accept})

    def create_booking(self, payload: dict):
        return self.request("POST", "/booking", json=payload)

    def update_booking(self, booking_id: int, payload: dict):
        return self.request("PUT", f"/booking/{booking_id}", json=payload)

    def partial_update_booking(self, booking_id: int, payload: dict):
        return self.request("PATCH", f"/booking/{booking_id}", json=payload)

    def delete_booking(self, booking_id: int):
        return self.request("DELETE", f"/booking/{booking_id}")
