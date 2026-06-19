from dotenv.variables import Literal
from faker import Faker

fake = Faker()


class Payloads:

    def like_post(self, reaction: str=None) -> dict:
        payload = {}
        if reaction:
            return {
                "reaction": reaction,
            }
        return payload

    def like_comment(self, reaction: str=None) -> dict:
        payload = {}
        if reaction:
            return {
                "reaction": reaction,
            }
        return payload
