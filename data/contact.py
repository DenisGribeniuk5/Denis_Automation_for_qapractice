"""
Text typed into the contact form.

The values come from helper.fake. This file only decides which values
the contact form needs, and keeps them in one dictionary for the test.
"""

from helper.fake import fake_choice, fake_email, fake_name, fake_sentence

# These strings match the <option> values on the contact page.
TOPICS = [
    "General question",
    "Report a bug on a practice page",
    "Suggest a topic or feature",
    "Content or copyright query",
    "Privacy request",
]

CONTACT_MESSAGE = {
    "name": fake_name(),
    "email": fake_email(),
    "message": f"Practice message. Do not send. {fake_sentence()}",
    "topic": fake_choice(TOPICS),
}
