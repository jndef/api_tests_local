import requests

from config.headers import Headers
from services.messages.endpoints import Endpoints
from services.messages.models.model_conversation_create import ResponseCreateConversationModel
from services.messages.models.model_conversation_find_or_create import ResponseFindOrCreateConversationModel
from services.messages.models.model_conversation_get import ResponseGetConversationModel
from services.messages.models.model_conversation_list import ResponseConversationsListModel
from services.messages.models.model_conversation_message_create import ResponseCreateMessageModel
from services.messages.models.model_conversation_messages_list import ResponseGetMessagesListModel
from services.messages.params import GetConversationsListParams, GetConversationMessagesListParams
from services.messages.payloads import Payloads
from utils.helper import Helper


class MessagesAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_conversations_list(self, params: dict, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_conversations_list,
            headers=self.headers.basic,
            params=GetConversationsListParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponseConversationsListModel, status_code=status_code,
                                      expected_success=expected_success)

    def create_conversation(self, participant_ids: list[str], conversation_name:str=None, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.create_conversation,
            headers=self.headers.basic,
            json=self.payloads.create_conversation(participant_ids, name=conversation_name)
        )
        return self.validate_response(response, ResponseCreateConversationModel, status_code=status_code,
                                      expected_success=expected_success)

    def find_or_create_dm(self, username: str, status_code: int = 200, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.find_or_create_dm(username),
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseFindOrCreateConversationModel, status_code=status_code,
                                      expected_success=expected_success)

    def get_conversation(self, conversation_id: str, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_conversation(conversation_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseGetConversationModel, status_code=status_code,
                                      expected_success=expected_success)

    def get_conversation_messages(self, conversation_id: str, params: dict = None, status_code: int = 200,
                                  expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_conversation_messages(conversation_id),
            headers=self.headers.basic,
            params=GetConversationMessagesListParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponseGetMessagesListModel, status_code=status_code,
                                      expected_success=expected_success)

    def send_message(self, conversation_id: str, payload: dict, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.create_messages(conversation_id),
            headers=self.headers.basic,
            json=self.payloads.create_message(**payload)
        )
        return self.validate_response(response, ResponseCreateMessageModel, status_code=status_code,
                                      expected_success=expected_success)


    def remove_message(self, conversation_id: str,status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.remove_message(conversation_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code=status_code,
                                      expected_success=expected_success)

    def read_conversation(self, conversation_id: str, status_code: int = 204, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.mark_conversation_read(conversation_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code=status_code,
                                      expected_success=expected_success)