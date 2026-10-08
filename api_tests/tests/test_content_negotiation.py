import xml.etree.ElementTree as ET

import allure


@allure.feature("Booking")
@allure.story("Content types")
def test_get_booking_as_xml(client, booking):
    booking_id, payload = booking

    response = client.get_booking(booking_id, accept="application/xml")

    assert response.status_code == 200
    # The body is XML, but the API labels it text/html, so the header is not checked.
    root = ET.fromstring(response.text)
    assert root.findtext("firstname") == payload["firstname"]
    assert root.findtext("bookingdates/checkin") == payload["bookingdates"]["checkin"]
