from dotenv.variables import Literal
from faker import Faker

fake = Faker()


class Payloads:

    def create_comment(self, content: str=None) -> dict:
        payload = {}
        if content:
            return {
                "content": content,
            }
        return payload

    def update_comment(self, content: str=None) -> dict:
        payload = {}
        if content:
            return {
                "content": content,
            }
        return payload


    def create_reply(self, content: str=None) -> dict:
        payload = {}
        if content:
            return {
                "content": content,
            }
        return payload
