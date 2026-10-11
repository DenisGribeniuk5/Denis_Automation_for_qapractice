import allure
import pytest

from helper.builders import booking_payload


@allure.feature("Booking")
@allure.story("Negative")
def test_get_unknown_booking_returns_404(client):
    response = client.get_booking(999_999_999)
    assert response.status_code == 404


@allure.feature("Booking")
@allure.story("Negative")
@pytest.mark.parametrize(
    "call",
    [
        lambda c, i: c.update_booking(i, booking_payload()),
        lambda c, i: c.partial_update_booking(i, {"firstname": "Hacker"}),
        lambda c, i: c.delete_booking(i),
    ],
    ids=["PUT", "PATCH", "DELETE"],
)
def test_changes_without_token_are_forbidden(client, booking, call):
    booking_id, payload = booking

    response = call(client, booking_id)

    assert response.status_code == 403
    assert client.get_booking(booking_id).json() == payload


@allure.feature("Booking")
@allure.story("Negative")
def test_invalid_token_is_forbidden(client, booking):
    booking_id, _ = booking
    client.authorize("not-a-real-token")

    response = client.delete_booking(booking_id)

    assert response.status_code == 403


@allure.feature("Booking")
@allure.story("Negative")
@pytest.mark.parametrize("missing", ["firstname", "lastname", "totalprice", "bookingdates"])
def test_create_without_required_field_fails(auth_client, missing):
    payload = booking_payload()
    del payload[missing]

    response = auth_client.create_booking(payload)

    # Known API defect: a missing required field gives 500 instead of 400.
    assert response.status_code == 500


@allure.feature("Booking")
@allure.story("Negative")
@pytest.mark.parametrize(
    "call",
    [
        lambda c: c.update_booking(999_999_999, booking_payload()),
        lambda c: c.partial_update_booking(999_999_999, {"firstname": "Ghost"}),
        lambda c: c.delete_booking(999_999_999),
    ],
    ids=["PUT", "PATCH", "DELETE"],
)
def test_change_unknown_booking_returns_405(auth_client, call):
    # The API answers 405 Method Not Allowed where 404 would be expected.
    assert call(auth_client).status_code == 405
