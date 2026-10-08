import allure
import pytest

from helper.builders import booking_payload
from helper.data import cases
from models.booking import Booking

DEFECT = pytest.mark.xfail(
    strict=True,
    reason="Known defect: the API stores invalid input and answers 200 instead of 400",
)


@pytest.fixture
def create(auth_client):
    """Creates bookings for the test and deletes every one afterwards."""
    created = []

    def _create(payload):
        response = auth_client.create_booking(payload)
        if response.ok:
            created.append(response.json()["bookingid"])
        return response

    yield _create
    for booking_id in created:
        auth_client.delete_booking(booking_id)


@allure.feature("Booking")
@allure.story("Validation")
@pytest.mark.parametrize("fields", cases("booking_edge_cases.json", "accepted"))
def test_valid_edge_case_is_saved_unchanged(client, create, fields):
    payload = booking_payload(**fields)

    response = create(payload)

    assert response.status_code == 200
    saved = client.get_booking(response.json()["bookingid"]).json()
    assert Booking.model_validate(saved) == Booking.model_validate(payload)


@allure.feature("Booking")
@allure.story("Validation")
def test_additional_needs_is_optional(client, create):
    payload = booking_payload()
    del payload["additionalneeds"]

    response = create(payload)

    assert response.status_code == 200
    assert "additionalneeds" not in client.get_booking(response.json()["bookingid"]).json()


@allure.feature("Booking")
@allure.story("Validation")
@pytest.mark.parametrize(
    "fields", cases("booking_edge_cases.json", "should_be_rejected", marks=DEFECT)
)
def test_invalid_booking_is_rejected(create, fields):
    response = create(booking_payload(**fields))

    assert response.status_code == 400


@allure.feature("Booking")
@allure.story("Validation")
@pytest.mark.xfail(strict=True, reason="Known defect: PATCH replaces the whole bookingdates object")
def test_patch_one_date_keeps_the_other(auth_client, booking):
    booking_id, payload = booking
    new_checkin = "2031-01-01"

    response = auth_client.partial_update_booking(
        booking_id, {"bookingdates": {"checkin": new_checkin}}
    )

    assert response.status_code == 200
    assert response.json()["bookingdates"] == {
        "checkin": new_checkin,
        "checkout": payload["bookingdates"]["checkout"],
    }
