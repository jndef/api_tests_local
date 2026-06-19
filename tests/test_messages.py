import allure
import pytest

from config.base_test import BaseTest


@allure.epic("Messages Service")
@allure.feature("Messages")
@allure.parent_suite("Tests Messages service API")
@allure.title("Tests Messages service API")
class TestMessages(BaseTest):

    @allure.suite("Get conversations list")
    @allure.story("User can see existed conversations")
    @allure.description("Get conversations list")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "params": {"page": 1, "per_page": 1}},
                     id="valid minimum boundaries"),
        pytest.param({"user": "moderator", "params": {"page": 2, "per_page": 100}},
                     id="valid maximum boundary"),
        pytest.param({"user": "admin", "params": {}},
                     id="empty query param"),
    ])
    def test_get_conversation_list(self, test_data):
        user = self.get_actor(test_data["user"])
        user.messages_api.get_conversations_list(params=test_data["params"])


    @allure.suite("Get conversations list")
    @allure.story("User can see existed conversations")
    @allure.description("Get conversations list - incorrect query params")
    @pytest.mark.parametrize("test_data", [
        pytest.param(
            {"user": "user_eve", "params": {"page": 0, "per_page": 10}, "expected_success": False, "status_code": 422},
            id="Invalid page below minimum boundary"),
        pytest.param(
            {"user": "user_eve", "params": {"page": 1, "per_page": 0}, "expected_success": False, "status_code": 422},
            id="Invalid per_page below minimum boundary"),
        pytest.param(
            {"user": "user_eve", "params": {"page": 3, "per_page": 101}, "expected_success": False, "status_code": 422},
            id="Invalid per_page above maximum boundary"),
    ])
    def test_get_conversation_list_incorrect_params(self, test_data):
        user = self.get_actor(test_data["user"])
        user.messages_api.get_conversations_list(params=test_data["params"],
                                                 expected_success=test_data["expected_success"],
                                                 status_code=test_data["status_code"])


    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "participant":"user_bob"},
                     id="Create conversation with valid user"),
        pytest.param({"user": "user_bob", "participant": "user_bob"},
                     id="Attempt to create conversation with yourself"),
    ])
    def test_create_conversation(self, test_data, db_cleanup_conversation):
        user = self.get_actor(test_data["user"])
        prepared_participant_id = self.get_user_info(test_data["participant"]).user_id

        conversation = user.messages_api.create_conversation(participant_ids=[f"{prepared_participant_id}"])
        assert conversation.participants[0].id == prepared_participant_id
        db_cleanup_conversation(conversation.id)


    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve",  "participant":"user_bob",  "name":"A"*100},
                     id="Max allowed conversation name"),
    ])
    def test_create_conversation_max_allowed_name(self, test_data, db_cleanup_conversation):
        user = self.get_actor(test_data["user"])
        prepared_participant_id = self.get_user_info(test_data["participant"]).user_id
        conversation = user.messages_api.create_conversation(participant_ids=[f"{prepared_participant_id}"],
                                                             conversation_name=test_data["name"])
        assert conversation.participants[0].id == prepared_participant_id
        assert conversation.name == test_data["name"]
        db_cleanup_conversation(conversation.id)



    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation - invalid participant id, not existed user")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_bob", "expected_success": False, "status_code": 404},
                     id="Attempt to create conversation with with not existed user"),
    ])
    def test_create_conversation_not_existed_user(self, test_data):
        user = self.get_actor(test_data["user"])
        prepared_participant_id = self.data_helper.random_uuid()
        user.messages_api.create_conversation(participant_ids=[f"{prepared_participant_id}"],
                                              expected_success=test_data["expected_success"],
                                              status_code=test_data["status_code"])


    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation - invalid participant id, invalid uuid")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_bob", "expected_success": False, "status_code": 422},
                     id="Attempt to create conversation using invalid uuid"),
    ])
    def test_create_conversation_incorrect_conversation(self, test_data):
        user = self.get_actor(test_data["user"])
        prepared_participant_id = self.data_helper.get_invalid_uuid()
        user.messages_api.create_conversation(participant_ids=[f"{prepared_participant_id}"],
                                              expected_success=test_data["expected_success"],
                                              status_code=test_data["status_code"])



    @allure.suite("Create conversation")
    @allure.story("User can create conversation")
    @allure.description("Create conversation - invalid participant id")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "name":"A"*101, "expected_success": False, "status_code": 422},
                     id="Too large conversation name"),
    ])
    def test_create_conversation_incorrect_conversation_name(self, test_data):
        user = self.get_actor(test_data["user"])
        prepared_participant_id = self.data_helper.random_uuid()
        user.messages_api.create_conversation(participant_ids=[f"{prepared_participant_id}"],
                                              conversation_name=test_data["name"],
                                              expected_success=test_data["expected_success"],
                                              status_code=test_data["status_code"])








    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "participant": "user_bob"},
                     id="Find or created new conversation"),
    ])
    def test_find_or_create_conversation(self, get_username, test_data, db_cleanup_conversation):
        user = self.get_actor(test_data["user"])
        participant_name = get_username(test_data["participant"])

        conversation = user.messages_api.find_or_create_dm(participant_name)
        assert conversation.participants[1].username == participant_name

        db_cleanup_conversation(conversation.id)