from datetime import date, timedelta

import allure
import pytest

from models.booking import BookingId


@allure.feature("Booking")
@allure.story("Search")
def test_list_returns_booking_ids(client):
    response = client.get_booking_ids()

    assert response.status_code == 200
    ids = [BookingId.model_validate(item) for item in response.json()]
    assert ids


@allure.feature("Booking")
@allure.story("Search")
@pytest.mark.parametrize("field", ["firstname", "lastname"])
def test_filter_by_name_finds_booking(client, booking, field):
    booking_id, payload = booking

    response = client.get_booking_ids(**{field: payload[field]})

    assert response.status_code == 200
    assert {"bookingid": booking_id} in response.json()


@allure.feature("Booking")
@allure.story("Search")
def test_filter_with_unknown_name_returns_empty_list(client):
    response = client.get_booking_ids(firstname="NoSuchGuestXyz123")

    assert response.status_code == 200
    assert response.json() == []


def _shift(iso_date: str, days: int) -> str:
    return (date.fromisoformat(iso_date) + timedelta(days=days)).isoformat()


@allure.feature("Booking")
@allure.story("Search")
@pytest.mark.parametrize(
    "field, days, found",
    [
        ("checkin", -1, True),
        ("checkin", 1, False),
        ("checkout", 1, True),
        ("checkout", -1, False),
    ],
    ids=["checkin before", "checkin after", "checkout after", "checkout before"],
)
def test_filter_by_date(client, booking, field, days, found):
    booking_id, payload = booking
    filter_date = _shift(payload["bookingdates"][field], days)

    response = client.get_booking_ids(firstname=payload["firstname"], **{field: filter_date})

    assert response.status_code == 200
    assert ({"bookingid": booking_id} in response.json()) is found


@allure.feature("Booking")
@allure.story("Search")
@pytest.mark.xfail(
    strict=True, reason="Known defect: checkin filter skips bookings that start on that date"
)
def test_checkin_filter_includes_same_day(client, booking):
    booking_id, payload = booking

    response = client.get_booking_ids(
        firstname=payload["firstname"], checkin=payload["bookingdates"]["checkin"]
    )

    assert {"bookingid": booking_id} in response.json()
