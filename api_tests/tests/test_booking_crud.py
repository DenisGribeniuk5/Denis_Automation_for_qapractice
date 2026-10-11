import allure
import pytest

from helper.builders import booking_payload
from models.booking import Booking, CreatedBooking


@allure.feature("Booking")
@allure.story("Create")
@pytest.mark.smoke
def test_create_booking_returns_id_and_echoes_payload(auth_client):
    payload = booking_payload()

    response = auth_client.create_booking(payload)

    assert response.status_code == 200
    created = CreatedBooking.model_validate(response.json())
    assert created.booking == Booking.model_validate(payload)
    auth_client.delete_booking(created.bookingid)


@allure.feature("Booking")
@allure.story("Read")
@pytest.mark.smoke
def test_get_booking_returns_saved_data(client, booking):
    booking_id, payload = booking

    response = client.get_booking(booking_id)

    assert response.status_code == 200
    assert Booking.model_validate(response.json()) == Booking.model_validate(payload)


@allure.feature("Booking")
@allure.story("Update")
def test_put_replaces_whole_booking(auth_client, booking):
    booking_id, _ = booking
    new_payload = booking_payload()

    response = auth_client.update_booking(booking_id, new_payload)

    assert response.status_code == 200
    assert Booking.model_validate(response.json()) == Booking.model_validate(new_payload)
    assert auth_client.get_booking(booking_id).json() == response.json()


@allure.feature("Booking")
@allure.story("Update")
def test_patch_changes_only_given_fields(auth_client, booking):
    booking_id, payload = booking
    changes = {"firstname": "Patched", "totalprice": 999}

    response = auth_client.partial_update_booking(booking_id, changes)

    assert response.status_code == 200
    assert response.json() == {**payload, **changes}


@allure.feature("Booking")
@allure.story("Delete")
def test_delete_removes_booking(auth_client, booking):
    booking_id, _ = booking

    response = auth_client.delete_booking(booking_id)

    # The API answers 201 Created for a successful delete.
    assert response.status_code == 201
    assert auth_client.get_booking(booking_id).status_code == 404
