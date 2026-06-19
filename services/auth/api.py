import requests

from services.auth.endpoints import Endpoints
from services.auth.models.model_login import LoginResponse
from services.auth.models.model_me import GetMe
from utils.helper import Helper
from services.auth.payloads import Payloads
from config.headers import Headers


class AuthAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def login(self, email: str, password: str, status_code: int = 200, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.login_account,
            json=self.payloads.login_account(email, password),
            headers={"Content-Type": "application/json"}
        )
        return self.validate_response(response, LoginResponse, status_code=status_code, expected_success=expected_success)

    def refresh(self, refresh_token: str, status_code: int = 200, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.refresh,
            json=self.payloads.refresh(refresh_token),
            headers={"Content-Type": "application/json"}
        )
        return self.validate_response(response, LoginResponse, status_code=status_code, expected_success=expected_success)

    def logout(self, token, refresh_token: str, status_code: int = 204, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.logout,
            json=self.payloads.logout(refresh_token),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {token}"}
        )
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)


    def get_me(self, status_code: int = 200, expected_success: bool = True) -> GetMe:
        response = requests.get(
            url=self.endpoints.get_me,
            headers=self.headers.basic
        )
        return self.validate_response(response, GetMe, status_code, expected_success)
