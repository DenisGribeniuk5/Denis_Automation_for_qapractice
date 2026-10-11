import allure
import pytest

from helper.builders import booking_payload


@allure.feature("Booking")
@allure.story("End to end")
@pytest.mark.smoke
def test_booking_lifecycle(client, auth_client):
    """A guest books, finds the booking, changes it, and cancels it."""
    payload = booking_payload()

    with allure.step("Create"):
        created = auth_client.create_booking(payload)
        assert created.status_code == 200
        booking_id = created.json()["bookingid"]

    try:
        with allure.step("Find by name"):
            found = client.get_booking_ids(
                firstname=payload["firstname"], lastname=payload["lastname"]
            )
            assert {"bookingid": booking_id} in found.json()

        with allure.step("Change the dates and add breakfast"):
            changed = {
                **payload,
                "bookingdates": {"checkin": "2031-06-01", "checkout": "2031-06-05"},
            }
            assert auth_client.update_booking(booking_id, changed).status_code == 200
            assert (
                auth_client.partial_update_booking(
                    booking_id, {"additionalneeds": "Breakfast"}
                ).status_code
                == 200
            )
            assert client.get_booking(booking_id).json() == {
                **changed,
                "additionalneeds": "Breakfast",
            }

        with allure.step("Cancel"):
            assert auth_client.delete_booking(booking_id).status_code == 201
            assert client.get_booking(booking_id).status_code == 404
    finally:
        auth_client.delete_booking(booking_id)
