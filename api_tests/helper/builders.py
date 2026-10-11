from datetime import timedelta

from faker import Faker

fake = Faker()


def booking_payload(**overrides) -> dict:
    """A valid booking with random values. Pass keyword arguments to pin any field."""
    checkin = fake.date_between(start_date="+1d", end_date="+60d")
    payload = {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(50, 2000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": checkin.isoformat(),
            "checkout": (checkin + timedelta(days=fake.random_int(1, 14))).isoformat(),
        },
        "additionalneeds": fake.random_element(["Breakfast", "Lunch", "Late checkout", "Parking"]),
    }
    payload.update(overrides)
    return payload


# DemoQA accepts only these symbols. Faker also emits ( ) _ +, which the API rejects.
_PASSWORD_SYMBOLS = "!@#$%^&*"
_PASSWORD_POOL = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" + _PASSWORD_SYMBOLS
)


def user_credentials() -> tuple[str, str]:
    """A unique user name and a password that meets the Book Store rules.

    At least 8 characters, with one upper case letter, one lower case letter,
    one digit, and one symbol from !@#$%^&*.
    """
    username = f"qa_{fake.user_name()}_{fake.random_int(1000, 9999)}"
    chars = [
        fake.random_element(_PASSWORD_SYMBOLS),
        fake.random_element("0123456789"),
        fake.random_element("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        fake.random_element("abcdefghijklmnopqrstuvwxyz"),
        *(fake.random_element(_PASSWORD_POOL) for _ in range(8)),
    ]
    fake.random.shuffle(chars)
    return username, "".join(chars)
