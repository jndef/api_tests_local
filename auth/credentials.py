import os
from dataclasses import dataclass

from collections import namedtuple

from dotenv import load_dotenv
load_dotenv()

@dataclass
class UserProfile:
    alias: str
    user_id: str
    email: str
    password: str

class Credentials:
    _roles = ["admin", "moderator", "user_bob", "user_eve", "user_alice", "user_banned"]

    def role_checker(self, update_role=None):
        role = os.getenv("role")
        if update_role is not None:
            role = update_role
        if not isinstance(role, str):
            raise Exception("Invalid role - not str")
        if role not in self._roles:
            raise BaseException(f"Invalid role: {role}. Not in allowed list")
        return role

    def _cred_name_combinator(self, update_role=None):
        role = self.role_checker(update_role)
        role = role.strip().upper()
        stage = os.getenv("STAGE").upper()
        LOGIN_PARAM_NAME = f"{stage}_{role}_LOGIN"
        PASSWORD_PARAM_NAME = f"{stage}_{role}_PASSWORD"
        return LOGIN_PARAM_NAME, PASSWORD_PARAM_NAME

    def get_credentials(self, update_role=None):
        CredDataCredData = namedtuple("_", ["email", "password"])

        cred_names = self._cred_name_combinator(update_role=update_role)
        print(cred_names)
        login, password = os.getenv(cred_names[0]), os.getenv(cred_names[1])
        if login is None or password is None:
            raise BaseException("No such credential name or password")
        return CredDataCredData(login, password)


    def get_user(self, alias: str) -> UserProfile:
        alias = self.role_checker(alias)
        stage = "LOCAL" if os.getenv("STAGE") == "local_docker" else os.getenv("STAGE").upper()
        role = alias.upper()
        return UserProfile(
            alias=alias,
            user_id=os.getenv(f"{stage}_{role}_ID"),
            email=os.getenv(f"{stage}_{role}_LOGIN"),
            password=os.getenv(f"{stage}_{role}_PASSWORD"),
        )


    # def get_user_id_by_elias(self, elias:str):
    #     elias = self.role_checker(update_role=elias)
    #     return self._roles_info[elias]