import sqlite3
from faker import Faker
fake = Faker()
import pytest

from auth.credentials import Credentials
from config.db_config import MyLocalDBConfig
from utils.db_helper import DataBaseHandler
creds = Credentials()

@pytest.fixture(name="db_connect", scope="session")
def connect_database():
    data_base = DataBaseHandler(MyLocalDBConfig)

    data_base.connect()

    # connection = sqlite3.connect("pytest_allure/test.db")
    print("БД подключена")
    yield data_base
    data_base.close_connection()
    print("БД отключена")

    # connection.close()



@pytest.fixture()
def db_cleanup_conversation(db_connect):

    def _cleanup(conversation_id):
        # conversation_id = db_connect.get_conversation_id_between_users(user_a,user_b)

        if conversation_id is not None:
            db_connect.delete_conversation(conversation_id)
            count = db_connect.check_conversation_by_id(conversation_id)
            assert count == 0
            print(f"cleanup_conversation: {conversation_id}")
    return _cleanup

@pytest.fixture()
def cleanup_conversation_by_id_after(request, db_connect):
    case_info = request.param
    yield
    conversation_id = db_connect.get_conversation_id_between_users(user_alias1=case_info["user1"], user_alias2=case_info["user2"])
    if conversation_id is not None:
        db_connect.delete_conversation(conversation_id)





@pytest.fixture()
def db_get_user_name_by_alias(request, db_connect):
    case_info = request.param
    username = db_connect.get_user_by_name(case_info["alias"])
    if username is not None:
        yield username

@pytest.fixture()
def get_username(db_connect):
    def _get(alias: str) -> str:
        return db_connect.get_user_by_name(alias)
    return _get


@pytest.fixture()
def get_conversation(request, db_connect):
    case_info = request.param
    conversation_id = db_connect.get_conversation_id_between_users(user_alias1=case_info["user1"], user_alias2=case_info["user2"])
    if conversation_id is not None:
        yield conversation_id

@pytest.fixture(name="reset_role_after")
def set_users_role_back(db_connect, request):
    yield
    change_role_data = request.param
    db_connect.set_role(table="users", user_name=change_role_data[0], role=change_role_data[1])

@pytest.fixture(name="mark_unread_all")
def mark_all_notifications_as_unred(db_connect, request):
    mark_unread = request.param
    db_connect.mark_all_notifications_unread(for_user=mark_unread)
    yield

@pytest.fixture(name="db_comment_with_replies")
def get_comment_with_replies(db_connect):
    comment_id = db_connect.get_comment_with_replies()
    yield comment_id["parent_comment_id"]
    # def _set_role_for_user(user_name, role_back:str="user"):
    #     db_connect.set_role(table="user", user_name=change_role_data[0], role=change_role_data[2])
    # return _set_role_for_user

@pytest.fixture()
def get_participant_id(request):

    case_info = request.param
    if case_info["case"] in ["valid", "yourself"]:
        user_id = creds.get_user(alias=case_info["participant"])
        yield user_id
    if case_info["case"]  == "invalid_uuid":
        yield "10AZ000-0Z0-0Z0-0Z0-00a00000003"
    elif case_info["case"] == "not_existed":
        participant = fake.uuid4()
        print(f"participant: {participant}")
        yield participant
        yield user_id
    if case_info["case"]  == "invalid_uuid":
        yield "10AZ000-0Z0-0Z0-0Z0-00a00000003"
    elif case_info["case"] == "not_existed":
        participant = fake.uuid4()
        print(f"participant: {participant}")
        yield participant

#
# case_info = request.param
# if case_info["case"] in ["valid", "yourself"]:
#     user_id = creds.get_user_id_by_elias(case_info["participant"])
#     yield user_id
# if case_info["case"]  == "invalid_uuid":
#     yield "10AZ000-0Z0-0Z0-0Z0-ZZa00000003"
# elif case_info["case"] == "not_existed":
#     participant = fake.uuid4()
#     print(f"participant: {participant}")
#     yield participant
