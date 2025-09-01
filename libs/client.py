import os
from typing import List

import logfire
import requests


class Client:
    def __init__(self):
        self.base_url = os.getenv("MT5_CLIENT_BASE_URL")
        self.auth_token = os.getenv("MT5_CLIENT_AUTH_TOKEN")

    def close_multiple_positions(self, logins: List[int]):
        try:
            response = requests.post(
                url=f"{self.base_url}/api/close_multiple_account_positions",
                json={"logins": logins},
                headers={"x-token": self.auth_token},
            )
            response.raise_for_status()

            data = response.json()

            return data.get("success", False)

        except requests.RequestException as e:
            logfire.error(f"Request failed: {e}")
            return False

    def get_user_by_logins(self, logins: List[int]):
        try:
            response = requests.get(
                url=f"{self.base_url}/api/users_by_logins",
                json={"logins": logins},
                headers={"x-token": self.auth_token},
            )
            response.raise_for_status()

            data = response.json()
            if not data.get("success", False):
                return None

            user_data = data.get("users", [])
            return user_data

        except requests.RequestException as e:
            logfire.error(f"Request failed: {e}")
            return None
