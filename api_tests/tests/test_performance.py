import allure
import pytest

from config import RESPONSE_TIME_LIMIT
from helper.builders import booking_payload


@allure.feature("Performance")
@pytest.mark.parametrize(
    "call",
    [
        lambda c, i: c.ping(),
        lambda c, i: c.get_booking(i),
        lambda c, i: c.get_booking_ids(firstname="Jim"),
        lambda c, i: c.partial_update_booking(i, {"additionalneeds": "Dinner"}),
    ],
    ids=["ping", "get booking", "search", "patch"],
)
def test_response_time_is_within_limit(auth_client, booking, call):
    booking_id, _ = booking

    response = call(auth_client, booking_id)

    assert response.ok
    assert response.elapsed.total_seconds() < RESPONSE_TIME_LIMIT


@allure.feature("Performance")
def test_create_response_time_is_within_limit(auth_client):
    response = auth_client.create_booking(booking_payload())

    assert response.status_code == 200
    assert response.elapsed.total_seconds() < RESPONSE_TIME_LIMIT
    auth_client.delete_booking(response.json()["bookingid"])
