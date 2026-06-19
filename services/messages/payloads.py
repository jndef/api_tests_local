from dotenv.variables import Literal
from faker import Faker

from utils.data_helper import DataHelper

fake = Faker()


class Payloads:

    def create_conversation(self, participant_ids: list[str], name: str=None) -> dict:
        if name is None:
            name = "Test-"+DataHelper().generate_text(15)
        return {
            "participant_ids": participant_ids,
            "is_group": False,
            "name": name,
        }

    def create_message(self, content: str, image_url:str=None) -> dict:
        return {
            "content": content,
            "image_url": image_url
        }
