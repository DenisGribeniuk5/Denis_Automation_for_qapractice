"""
Contact form. We fill the fields and stop.

We do not click "Open email draft". That button opens a mail app
and would surprise whoever runs the suite.
"""

from playwright.sync_api import expect

from data.contact import CONTACT_MESSAGE


def test_contact_form_accepts_a_message(contact):
    contact.fill_message(**CONTACT_MESSAGE)

    expect(contact.name_input).to_have_value(CONTACT_MESSAGE["name"])
    expect(contact.email_input).to_have_value(CONTACT_MESSAGE["email"])
    expect(contact.topic_select).to_have_value(CONTACT_MESSAGE["topic"])
    expect(contact.message_input).to_have_value(CONTACT_MESSAGE["message"])
    expect(contact.submit_button).to_be_visible()
