import allure
import pytest

from config.base_test import BaseTest


@allure.epic("Comments Service")
@allure.feature("Comments")
@allure.parent_suite("Tests Comments service API")
@allure.title("Tests Comments service API")
class TestComments(BaseTest):

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list")
    @pytest.mark.parametrize("test_data", [
        pytest.param(
            {"user": "user_eve", "params": {"sort_by": "created_at", "sort_order": "asc", "page": 1, "per_page": 1}},
            id="Valid minimal boundaries with created_at asc sorting"),
        pytest.param({"user": "moderator",
                      "params": {"sort_by": "likes_count", "sort_order": "desc", "page": 2, "per_page": 100}},
                     id="Valid max per_page boundary with likes_count desc sorting"),
        pytest.param({"user": "admin", "params": {"sort_by": "created_at"}},
                     id="Valid request with only sort by"),
        pytest.param({"user": "user_eve", "params": {}},
                     id="Valid request with omitted optional params"),
    ])
    def test_get_comments_list(self, get_post_only, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = get_post_only(test_data["user"])
        user.comments_api.get_list_comments(post_id=prepared_post_id, params=test_data["params"])

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect - invalid payload")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"params": {"sort_by": "invalid_sort", "sort_order": "asc", "page": 1, "per_page": 10},
                      "expected_success": False, "status_code": 422},
                     id="Invalid sort_by enum"),
        pytest.param({"params": {"sort_by": "created_at", "sort_order": "invalid_order", "page": 1, "per_page": 10},
                      "expected_success": False, "status_code": 422},
                     id="Invalid sort_order enum"),
        pytest.param({"params": {"page": 0, "per_page": 10}, "expected_success": False, "status_code": 422},
                     id="Invalid page below minimum boundary"),
        pytest.param({"params": {"page": 1, "per_page": 0}, "expected_success": False, "status_code": 422},
                     id="Invalid per_page below minimum boundary"),
        pytest.param({"params": {"page": 3, "per_page": 101}, "expected_success": False, "status_code": 422},
                     id="Invalid per_page above maximum boundary"),
    ])
    def test_get_comments_list_invalid_payload(self, test_data):
        user = self.get_actor("user_eve")
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.get_list_comments(post_id=prepared_post_id,
                                            params=test_data["params"],
                                            status_code=test_data["status_code"],
                                            expected_success=test_data["expected_success"])

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect - not existed post id")
    def test_get_comments_list_incorrect_not_existed(self, get_incorrect_post):
        user = self.get_actor("user_eve")
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.get_list_comments(post_id=prepared_post_id,
                                            status_code=404,
                                            expected_success=False)

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect - Invalid uuid")
    def test_get_comments_list_incorrect_invalid_uuid(self):
        user = self.get_actor("user_bob")
        prepared_post_id = self.data_helper.get_invalid_uuid()
        user.comments_api.get_list_comments(post_id=prepared_post_id,
                                            status_code=422,
                                            expected_success=False)

    @allure.suite("Get comments list")
    @allure.story("User can read existed comments to post")
    @allure.description("Get posts list, incorrect - Removed post")
    def test_get_comments_list_incorrect_removed_post(self, get_removed_post):
        user = self.get_actor("user_eve")
        prepared_post_id = get_removed_post
        user.comments_api.get_list_comments(post_id=prepared_post_id,
                                            status_code=404,
                                            expected_success=False)

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "payload": {"content": "A"}},
                     id="Valid minimal content boundary"),
        pytest.param({"user": "admin", "payload": {"content": "A" * 1000}},
                     id="Valid maximum content boundary"),
    ])
    def test_create_comment(self, get_post_only, test_data, comment_cleaner):
        user = self.get_actor(test_data["user"])
        prepared_post_id = get_post_only(test_data["user"])
        prepared_comment_body = test_data["payload"]["content"]
        comment = user.comments_api.create_comment(post_id=prepared_post_id, payload=test_data["payload"])
        comment_cleaner(comment.id, test_data["user"])  # регистрируем на удаление
        assert comment.content == prepared_comment_body, f"Created comment doesn't contain expected content.\nER: {prepared_comment_body}\nAR: {comment.content}"

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post, incorrect - invalid payload")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"payload": {"content": ""}, "expected_success": False, "status_code": 422},
                     id="Invalid content below minimum boundary"),
        pytest.param({"payload": {"content": "A" * 1001}, "expected_success": False,
                      "status_code": 422},
                     id="Invalid content above maximum boundary"),
        pytest.param({"payload": {}, "expected_success": False, "status_code": 422},
                     id="Missing required content field"),
    ])
    def test_create_comment_incorrect_invalid_payload(self, get_post_only, test_data):
        user = self.get_actor("user_eve")
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.create_comment(post_id=prepared_post_id,
                                         payload=test_data["payload"],
                                         status_code=test_data["status_code"],
                                         expected_success=test_data["expected_success"])

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post, incorrect - not existed post")
    def test_create_comment_incorrect_not_existed_post(self):
        user = self.get_actor("user_bob")
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.create_comment(post_id=prepared_post_id,
                                         payload={"content": "Valid comment"},
                                         status_code=404,
                                         expected_success=False)

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post, incorrect - Removed post")
    def test_create_comment_incorrect_removed_post(self, get_removed_post):
        user = self.get_actor("user_eve")
        prepared_post_id = get_removed_post("user_eve")
        user.comments_api.create_comment(post_id=prepared_post_id,
                                         payload=self.data_helper.get_random_comment_payload(),
                                         status_code=404,
                                         expected_success=False)

    @allure.suite("Create new comment")
    @allure.story("User can create new comment to the post")
    @allure.description("Create comment to post, incorrect - invalid post uuid")
    def test_create_comment_incorrect_invalid_uuid(self, get_incorrect_post):
        user = self.get_actor("user_eve")
        prepared_post_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.create_comment(post_id=prepared_post_id,
                                         payload={"content": "Valid comment"},
                                         status_code=422,
                                         expected_success=False)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment - success")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "user_eve", "payload": {"content": "A"}},
                     id="Valid minimal content boundary"),
        pytest.param({"user": "admin", "payload": {"content": "A" * 1000}},
                     id="Valid maximum content boundary"),
    ])
    def test_update_comment(self, get_comment_before, comment_cleaner, test_data):
        user = self.get_actor(test_data["user"])
        prepared_comment_id = get_comment_before(test_data["user"])
        prepared_comment_body = test_data["payload"]["content"]
        comment = user.comments_api.update_comment(comment_id=prepared_comment_id, payload=test_data["payload"])
        comment_cleaner(test_data["user"], comment.id)
        assert comment.content == prepared_comment_body, f"Updated comment doesn't contain expected content.\nER: {prepared_comment_body}\nAR: {comment.content}"

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment, incorrect - negative payload")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"payload": {"content": ""}, "expected_success": False, "status_code": 422},
                     id="Invalid content below minimum boundary"),
        pytest.param({"payload": {"content": "A" * 1001}, "expected_success": False,
                      "status_code": 422},
                     id="Invalid content above maximum boundary"),
        pytest.param({"payload": {}, "expected_success": False, "status_code": 422},
                     id="Missing required content field"),
    ])
    def test_update_comment_incorrect_invalid_payload(self, test_data):
        user = self.get_actor("user_eve")
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.update_comment(comment_id=prepared_comment_id,
                                         payload=test_data["payload"],
                                         status_code=test_data["status_code"],
                                         expected_success=test_data["expected_success"])

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment, incorrect - Invalid comment id format")
    def test_update_comment_incorrect_invalid_post_uuid(self):
        user = self.get_actor("user_eve")
        prepared_comment_id = self.data_helper.get_invalid_uuid()
        user.comments_api.update_comment(comment_id=prepared_comment_id,
                                         payload={"content": "Valid comment"},
                                         status_code=422,
                                         expected_success=False)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment, incorrect - Comment is deleted")
    def test_update_comment_incorrect_removed(self, create_comment_and_remove_before):
        user = self.get_actor("user_bob")
        prepared_comment_id = create_comment_and_remove_before("user_bob")
        user.comments_api.update_comment(comment_id=prepared_comment_id,
                                         payload={"content": "Valid comment"},
                                         status_code=404,
                                         expected_success=False)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment, incorrect - Comment has created by another user")
    def test_update_comment_incorrect_created_by_another(self, get_comment_before):
        user = self.get_actor("user_eve")
        prepared_comment_id = get_comment_before("user_bob")
        user.comments_api.update_comment(comment_id=prepared_comment_id,
                                         payload=self.data_helper.get_random_comment_payload(),
                                         status_code=False,
                                         expected_success=403)

    @allure.suite("Update existed comment")
    @allure.story("User can update existed comment")
    @allure.description("User can update existed comment, incorrect - invalid comment uuid")
    def test_update_comment_incorrect_invalid_uuid(self):
        user = self.get_actor("user_eve")
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.update_comment(comment_id=prepared_comment_id,
                                         payload={"content": "Valid comment"},
                                         status_code=404,
                                         expected_success=False)

    @allure.suite("Delete existed comment")
    @allure.story("User can remove existed comment")
    @allure.description("User can remove published comment - success")
    def test_remove_comment(self, create_comment_before):
        user = self.get_actor("user_eve")
        prepared_comment_id = create_comment_before("user_eve")
        user.comments_api.delete_comment(comment_id=prepared_comment_id)


    @allure.suite("Delete existed comment")
    @allure.story("User can remove existed comment")
    @allure.description("Attempt to remove the comment created by another user with higher role")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"user": "admin"},
                     id="Remove comment of another user as admin"),
        pytest.param({ "user": "moderator"},
                     id="Remove comment of another user as moderator"),
    ])
    def test_remove_comment_by_role(self, create_comment_before, test_data):
        prepared_comment_id = create_comment_before("user_eve")
        user = self.get_actor(test_data["user"])
        user.comments_api.delete_comment(comment_id=prepared_comment_id,
                                         expected_success=test_data["expected_success"],
                                         status_code=test_data["status_code"])


    @allure.suite("Delete existed comment")
    @allure.story("User can remove existed comment")
    @allure.description("As user try to remove the comment, created by another user")
    def test_remove_comment_by_role_incorrect(self, create_comment_before):
        prepared_comment_id = create_comment_before("user_eve")
        user = self.get_actor("user_bob")
        user.comments_api.delete_comment(comment_id=prepared_comment_id,
                                         expected_success=False,
                                         status_code=403)



    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list")
    @pytest.mark.parametrize("test_data", [

        pytest.param({"user": "user_eve", "params": {"page": 1, "per_page": 1}},
                     id="Valid minimal pagination boundaries"),

        pytest.param({"user": "moderator", "params": {"page": 2, "per_page": 100}},
                     id="Valid maximum per_page boundary"),

        pytest.param({"user": "admin", "params": {}},
                     id="Valid request with omitted optional params"),
    ])
    def test_get_replies(self, db_comment_with_replies, test_data):
        user = self.get_actor(test_data["user"])
        prepared_comment_id = db_comment_with_replies
        user.comments_api.get_list_replies(comment_id=prepared_comment_id, params=test_data["params"])


    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list, incorrect - invalid query param")
    @pytest.mark.parametrize("test_data", [
        pytest.param(
            {"params": {"page": 0, "per_page": 10}, "expected_success": False, "status_code": 422},
            id="Invalid page below minimum boundary"),
        pytest.param(
            {"params": {"page": 1, "per_page": 0}, "expected_success": False, "status_code": 422},
            id="Invalid per_page below minimum boundary"),
        pytest.param(
            {"params": {"page": 3, "per_page": 101}, "expected_success": False, "status_code": 422},
            id="Invalid per_page above maximum boundary"),
    ])
    def test_get_replies_incorrect_invalid_payload(self, test_data):
        user = self.get_actor("user_eve")
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.get_list_replies(comment_id=prepared_comment_id,
                                           params=test_data["params"],
                                           expected_success=test_data["expected_success"],
                                           status_code=test_data["status_code"])



    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list, incorrect - Invalid comment uuid")
    def test_get_replies_incorrect_invalid_uuid(self):
        user = self.get_actor("user_eve")
        prepared_comment_id = self.data_helper.get_invalid_uuid()
        user.comments_api.get_list_replies(comment_id=prepared_comment_id,
                                           expected_success=False,
                                           status_code=422)



    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list - Comment is deleted")
    def test_get_replies_removed_comment(self, create_comment_and_remove_before):
        user = self.get_actor("user_bob")
        prepared_comment_id = create_comment_and_remove_before("user_bob")
        user.comments_api.get_list_replies(comment_id=prepared_comment_id,
                                           expected_success=True,
                                           status_code=200)



    @allure.suite("Get replies list")
    @allure.story("User can read existed replies to comment")
    @allure.description("Get replies list, incorrect - Non-existing comment id")
    def test_get_replies_incorrect_not_existed(self):
        user = self.get_actor("user_eve")
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.get_list_replies(comment_id=prepared_comment_id,
                                           expected_success=False,
                                           status_code=404)



    @allure.suite("Create reply to comment")
    @allure.story("User can create a reply to existed comment")
    @allure.description("Create reply to comment")
    @pytest.mark.parametrize("test_data", [
        pytest.param({"payload": {"content": "A"}},
                     id="Valid minimal content boundary"),
        pytest.param({"payload": {"content": "A" * 1000}},
                     id="Valid maximum content boundary"),
    ])
    def test_create_reply(self, db_comment_with_replies, test_data, comment_cleaner):
        user = self.get_actor("user_eve")
        prepared_comment_id = db_comment_with_replies
        reply = user.comments_api.create_reply(comment_id=prepared_comment_id, payload=test_data["payload"])
        comment_cleaner(reply.id, "user_eve")
        assert reply.post_id != reply.parent_comment_id and prepared_comment_id == reply.parent_comment_id




    @allure.suite("Create reply to comment")
    @allure.story("User can create a reply to existed comment")
    @allure.description("Create reply to comment, incorrect - Comment is removed")
    def test_create_reply_incorrect_removed(self, create_comment_and_remove_before):
        user = self.get_actor("user_bob")
        prepared_comment_id = create_comment_and_remove_before("user_bob")
        user.comments_api.create_reply(comment_id=prepared_comment_id,
                                       payload={"content": "A"},
                                       expected_success=False,
                                       status_code=404)


    @allure.suite("Create reply to comment")
    @allure.story("User can create a reply to existed comment")
    @allure.description("Create reply to comment, incorrect - Comment does not exist")
    def test_create_reply_incorrect_not_existed(self):
        user = self.get_actor("user_bob")
        prepared_comment_id = self.data_helper.get_not_existed_uuid()
        user.comments_api.create_reply(comment_id=prepared_comment_id,
                                       payload={"content": "A"},
                                       expected_success=False,
                                       status_code=404)