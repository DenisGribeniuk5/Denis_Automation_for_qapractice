import allure
import pytest

from config import ADMIN_PASSWORD, ADMIN_USERNAME
from models.booking import Token


@allure.feature("Auth")
@pytest.mark.smoke
def test_valid_credentials_return_token(client):
    response = client.create_token(ADMIN_USERNAME, ADMIN_PASSWORD)

    assert response.status_code == 200
    assert Token.model_validate(response.json()).token


@allure.feature("Auth")
@pytest.mark.parametrize(
    "username, password",
    [
        (ADMIN_USERNAME, "wrong-password"),
        ("unknown-user", ADMIN_PASSWORD),
        ("", ""),
    ],
    ids=["wrong password", "unknown user", "empty credentials"],
)
def test_bad_credentials_are_rejected(client, username, password):
    response = client.create_token(username, password)

    # The API answers 200 with a reason instead of 401.
    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}
