import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password123")
TIMEOUT = 15
# Slowest acceptable answer for a single call, in seconds.
RESPONSE_TIME_LIMIT = float(os.getenv("RESPONSE_TIME_LIMIT", "3"))

# Book Store API, documented at https://demoqa.com/swagger/
DEMOQA_URL = os.getenv("DEMOQA_URL", "https://demoqa.com")
