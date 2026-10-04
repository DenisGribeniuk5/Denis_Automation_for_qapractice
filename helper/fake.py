"""
Faker lives here, not in the data files.

    from helper.fake import fake_name, fake_email, fake_sentence, fake_choice

One Faker object is created when this file is imported. Every caller shares it,
so a value you already asked for does not change on its own.
"""

from faker import Faker

fake = Faker()


def fake_name() -> str:
    """A full name, such as 'Jane Doe'."""
    return fake.name()


def fake_email() -> str:
    """An email address. It is not a real inbox."""
    return fake.email()


def fake_sentence() -> str:
    """One short sentence."""
    return fake.sentence()


def fake_choice(options: list[str]) -> str:
    """Pick one item from the list you pass in. Faker does not invent that list."""
    return fake.random_element(options)
