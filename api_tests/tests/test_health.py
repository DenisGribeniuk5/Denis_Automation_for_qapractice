import allure
import pytest


@allure.feature("Health")
@pytest.mark.smoke
def test_ping_returns_201(client):
    response = client.ping()
    assert response.status_code == 201
