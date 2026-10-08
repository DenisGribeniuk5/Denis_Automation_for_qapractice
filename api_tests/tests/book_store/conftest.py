import re

import allure
import pytest

from api.book_store_client import BookStoreClient
from helper.builders import user_credentials

# demoqa loads many ads and trackers. Blocking them makes pages load faster and more reliably.
AD_HOSTS = re.compile(
    r"googlesyndication|doubleclick|googletagmanager|google-analytics|adservice|"
    r"amazon-adsystem|criteo|openx|rtbhouse|id5-sync|crwdcntrl|pubmatic|adnxs"
)


@pytest.fixture
def page(page, request, pytestconfig):
    page.route(AD_HOSTS, lambda route: route.abort())
    yield page
    _attach_video(page, request.node, pytestconfig.getoption("video"))


def _attach_video(page, item, mode):
    """Attaches the recording to Allure when --video is on, or failed with retain-on-failure."""
    if page.video is None:
        return
    failed = getattr(item, "rep_call", None) is not None and item.rep_call.failed
    if mode == "on" or (mode == "retain-on-failure" and failed):
        # The video file is complete only after its browser context closes.
        page.context.close()
        allure.attach.file(page.video.path(), "video", allure.attachment_type.WEBM)


@pytest.fixture
def api_user():
    """Creates a user through the API and logs it in. Deletes it afterwards if the test didn't."""
    client = BookStoreClient()
    username, password = user_credentials()
    response = client.create_user(username, password)
    assert response.status_code == 201, response.text
    user_id = response.json()["userID"]
    client.authorize(client.generate_token(username, password).json()["token"])

    yield client, user_id, username, password

    # A UI login replaces the token, so log in again before cleaning up.
    token = client.generate_token(username, password).json()["token"]
    if token:
        client.authorize(token)
        client.delete_user(user_id)
