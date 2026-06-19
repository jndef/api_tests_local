import os

import requests
from dotenv import load_dotenv

from auth.credentials import Credentials
from services.auth.api import AuthAPI

load_dotenv()
credentials = Credentials()


class  TokenProvider:
    _token_cache = {}  # кэш на уровне класса, не инстанса


    def get_token_for_role(self, role:str):
        if role in self._token_cache:
            return self._token_cache[role]

        auth = AuthAPI()
        creds = credentials.get_user(role)
        response = requests.post(
            url=auth.endpoints.login_account,
            headers={"Content-Type": "application/json"},
            json=auth.payloads.login_account(creds.email, creds.password)
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            self._token_cache[role] = token
            return token
        else:
            raise Exception(f"BE returns {response.status_code} code while auth test preparation. Info:\n{response.request.method}. {response.request.url}\nRequest body:{response.request.body if response.request.method == "POST" else None}\nResponse text: {response.text}")
