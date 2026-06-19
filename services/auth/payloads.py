from faker import Faker

fake = Faker()


class Payloads:

    def login_account(self, email: str, password: str):
        return {
            "email": email,
            "password": password
        }

    def refresh(self, refresh_token: str):
        return {
            "refresh_token": f"{refresh_token}"
        }

    def logout(self, refresh_token: str):
        return {
            "refresh_token": f"{refresh_token}"
        }
