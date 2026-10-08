import json
import logging

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import BASE_URL, TIMEOUT

log = logging.getLogger(__name__)

# The API is hosted on Heroku, which sometimes drops a connection or answers 503 while waking up.
# Only GET is retried: repeating a POST could create a second booking.
RETRY = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[502, 503, 504],
    allowed_methods=["GET"],
)


class BaseClient:
    """Sends every request through one place so each call is logged and attached to Allure."""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=RETRY))
        self.session.headers.update(
            {"Accept": "application/json", "Content-Type": "application/json"}
        )

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{path}"
        kwargs.setdefault("timeout", TIMEOUT)
        with allure.step(f"{method} {path}"):
            response = self.session.request(method, url, **kwargs)
            log.info(
                "%s %s -> %s in %.2fs",
                method,
                url,
                response.status_code,
                response.elapsed.total_seconds(),
            )
            log.debug("request body: %s", kwargs.get("json"))
            log.debug("response body: %s", response.text)
            self._attach(method, url, kwargs.get("json"), response)
        return response

    @staticmethod
    def _attach(method, url, body, response):
        request_text = f"{method} {url}"
        if body is not None:
            request_text += "\n\n" + json.dumps(body, indent=2, ensure_ascii=False)
        allure.attach(request_text, "request", allure.attachment_type.TEXT)
        allure.attach(
            f"{response.status_code}\n\n{response.text}", "response", allure.attachment_type.TEXT
        )
