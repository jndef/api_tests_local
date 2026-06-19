import allure
import pytest

from config.base_test import BaseTest


@allure.epic("Posts Service")
@allure.feature("Posts")
@allure.parent_suite("Tests Posts service API")
@allure.title("Tests Posts service API")
class TestPosts(BaseTest):



    @allure.suite("Get posts list")
    @allure.story("User can read existed posts at platform")
    @allure.description("Get posts list - valid payload")
    @pytest.mark.parametrize("query_request_conditions", [
        pytest.param(({"params": {"hashtag": "coding", "author_id": "00000000-0000-0000-0000-000000000003", "sort_by": "created_at",
          "sort_order": "asc", "page": 1, "per_page": 1 }, "expected_success": True, "status_code": 200}),
                     id="fully valid request with minimum boundaries"),
        pytest.param(({"params": {"hashtag": "devlife", "author_id": "00000000-0000-0000-0000-000000000002", "sort_by": "likes_count",
          "sort_order": "desc", "page": 2, "per_page": 100}, "expected_success": True, "status_code": 200}),
                     id="valid max boundary + different enum values"),
        pytest.param(({"params": {"hashtag": "unknown_tag", "page": 1, "per_page": 10}, "expected_success": True, "status_code": 200}),
                     id="non-existing hashtag"),
        pytest.param(({"params": {"author_id": "00000000-0000-0000-0000-999999999999", "page": 1, "per_page": 10}, "expected_success": True, "status_code": 200}),
                     id="non-existing author_id"),
        pytest.param(({"params": {}, "expected_success": True, "status_code": 200}),
                     id="all optional params omitted"),
    ])
    @pytest.mark.smoke
    def test_get_posts(self, query_request_conditions):
        self.user_eve.posts_api.get_list_posts(params=query_request_conditions["params"],
                                               status_code=query_request_conditions["status_code"],
                                               expected_success=query_request_conditions["expected_success"])



    @allure.suite("Get posts list")
    @allure.story("User can read existed posts at platform")
    @allure.description("Get posts list - depending on role {role}")
    @pytest.mark.parametrize("role_conditions", [
        pytest.param(({"role": "admin", "expected_success": True, "status_code": 200}),
                     id="Request posts list as admin"),
        pytest.param(({"role": "moderator", "expected_success": True, "status_code": 200}),
                     id="Request posts list as moderator"),
        pytest.param(({"role": "user_bob", "expected_success": True, "status_code": 200}),
                     id="Request posts list as user"),
    ])
    def test_get_posts_depends_on_role(self, role_conditions):
        user = self.get_actor(role_conditions["role"])
        user.posts_api.get_list_posts(status_code=role_conditions["status_code"],
                                      expected_success=role_conditions["expected_success"])



    @allure.suite("Get posts list")
    @allure.story("User can read existed posts at platform")
    @allure.description("Get posts list - invalid queries")
    @pytest.mark.parametrize("query_request_conditions", [
        pytest.param(({"params": {"sort_by": "comments_count", "sort_order": "asc", "page": 0, "per_page": 10}, "expected_success": False, "status_code": 422}),
                     id="invalid page below minimum"),
        pytest.param(({"params": {"hashtag": "coding", "page": 1, "per_page": 0, }, "expected_success": False, "status_code": 422}),
                     id="invalid per_page below minimum"),
        pytest.param(({"params": {"author_id": "00000000-0000-0000-0000-000000000003", "page": 3, "per_page": 101}, "expected_success": False, "status_code": 422}),
                     id="invalid per_page above maximum"),
        pytest.param(({"params": {"sort_by": "views_count", "sort_order": "asc", "page": 1, "per_page": 10}, "expected_success": False, "status_code": 422}),
                     id="invalid sort_by enum"),
        pytest.param(({"params": {"sort_by": "created_at", "sort_order": "up", "page": 1, "per_page": 10}, "expected_success": False, "status_code": 422}),
                     id="invalid sort_order enum"),
    ])
    def test_get_posts_invalid_queries(self, query_request_conditions):
        self.user_eve.posts_api.get_list_posts(params=query_request_conditions["params"],
                                               status_code=query_request_conditions["status_code"],
                                               expected_success=query_request_conditions["expected_success"])









    @allure.suite("Create post")
    @allure.story("User can create post at platform")
    @allure.description("Create post - valid payload")
    @pytest.mark.parametrize("post_body_data", [
        pytest.param(({"payload":{"content": "A", "visibility": "public", "image_url": None}, "expected_success":True, "status_code":201}), id="Valid minimal boundary + default visibility"),
        pytest.param(({"payload":{"content": "A" * 2000, "image_url": "temp_data/image.png", "visibility": "followers_only"}, "expected_success":True, "status_code":201}), id="valid max boundary + explicit followers_only + image"),
        pytest.param(({"payload": {"content": "Another valid post", "visibility": "followers_only", "image_url": None},
                       "expected_success": True, "status_code": 201}), id="valid followers_only without image"),
        pytest.param(({"payload": {"content": "Image post", "image_url": "temp_data/image.jpg", "visibility": "public"},
                       "expected_success": True, "status_code": 201}), id="valid public with image"),
        pytest.param(({"payload": {"content": "Default visibility post", "visibility": "public"},
                       "expected_success": True, "status_code": 201}), id="optional image_url omitted + default visibility"),
    ])
    def test_create_post(self, post_body_data, post_cleaner):

        new_post = self.user_eve.posts_api.create_post(payload=post_body_data["payload"], status_code=post_body_data["status_code"],
                                                       expected_success=post_body_data["expected_success"])
        post_cleaner(new_post.id, "user_eve")  # регистрируем на удаление
        assert new_post.content == post_body_data["payload"]["content"]
        assert new_post.visibility == post_body_data["payload"]["visibility"]
        if post_body_data["payload"].get("image_url"):
            assert new_post.image_url == post_body_data["payload"]["image_url"]



    @allure.suite("Create post")
    @allure.story("User can create post at platform")
    @allure.description("Create post - depending on role {role}")
    @pytest.mark.parametrize("role_conditions", [
        pytest.param(({"role": "admin", "expected_success": True, "status_code": 201}),
                     id="Create post as admin"),
        pytest.param(({"role": "moderator", "expected_success": True, "status_code": 201}),
                     id="Create post as moderator"),
        pytest.param(({"role": "user_bob", "expected_success": True, "status_code": 201}),
                     id="Create post as user"),
    ])
    def test_get_posts_depends_on_role(self, role_conditions, post_cleaner):
        user = self.get_actor(role_conditions["role"])
        payload = {"content": "A", "visibility": "public", "image_url": None}

        new_post = user.posts_api.create_post(payload=payload,
                                              status_code=role_conditions["status_code"],
                                              expected_success=role_conditions["expected_success"])

        post_cleaner(new_post.id, role_conditions["role"])  # регистрируем на удаление
        assert new_post.content == payload["content"]
        assert new_post.visibility == payload["visibility"]



    @allure.suite("Create post")
    @allure.story("User can create post at platform")
    @allure.description("Get posts list - invalid payload")
    @pytest.mark.parametrize("post_body_data", [
        pytest.param(({"payload":{"content": "", "visibility": "public", "image_url": None}, "expected_success":False, "status_code":422}), id="invalid content below min boundary"),
        pytest.param(({"payload":{"content": "A" * 2001, "visibility": "public", "image_url": None}, "expected_success":False, "status_code":422}), id="invalid content above max boundary"),
        pytest.param(({"payload": {"content": "Valid post content", "visibility": "private"},
                       "expected_success": False, "status_code": 422}), id="invalid visibility enum")
    ])
    def test_create_post_invalid_payload(self, post_body_data):
        self.user_eve.posts_api.create_post(payload=post_body_data["payload"],
                                            status_code=post_body_data["status_code"],
                                            expected_success=post_body_data["expected_success"])









    @allure.suite("Tests get posts feed")
    @allure.story("User can read existed posts feed at platform")
    @allure.description("Get posts feed")
    @pytest.mark.parametrize("query_request_conditions", [
        pytest.param(({"params": {"page": 1, "per_page": 1}, "expected_success": True, "status_code": 200}),
                     id="valid minimum boundaries"),
        pytest.param(({"params": {"page": 2, "per_page": 100}, "expected_success": True, "status_code": 200}),
                     id="valid maximum boundary"),
        pytest.param(({"params": {}, "expected_success": True, "status_code": 200}),
                     id="empty query param"),
    ])
    def test_get_posts_feed(self, query_request_conditions):
        self.user_eve.posts_api.get_posts_feed(params=query_request_conditions["params"],
                                               status_code=query_request_conditions["status_code"],
                                               expected_success=query_request_conditions["expected_success"])



    @allure.suite("Tests get posts feed")
    @allure.story("User can read existed posts feed at platform")
    @allure.description("Get posts feed depending on user role -  {role}")
    @pytest.mark.parametrize("role_conditions", [
        pytest.param(({"role": "admin", "expected_success": True, "status_code": 200}),
                     id="Create post as admin"),
        pytest.param(({"role": "moderator", "expected_success": True, "status_code": 200}),
                     id="Create post as moderator"),
        pytest.param(({"role": "user_bob", "expected_success": True, "status_code": 200}),
                     id="Create post as user"),
    ])
    def test_get_posts_feed_depends_on_role(self, role_conditions):
        user = self.get_actor(role_conditions["role"])
        user.posts_api.get_posts_feed(status_code=role_conditions["status_code"],
                                      expected_success=role_conditions["expected_success"])



    @allure.suite("Tests get posts feed")
    @allure.story("User can read existed posts feed at platform")
    @allure.description("Get posts feed - invalid query params")
    @pytest.mark.parametrize("query_request_conditions", [
        pytest.param(({"params": {"page": 0, "per_page": 10}, "expected_success": False, "status_code": 422}),
                     id=" invalid page below minimum"),
        pytest.param(({"params": {"page": 1, "per_page": 0}, "expected_success": False, "status_code": 422}),
                     id="invalid per_page below minimum"),
        pytest.param(({"params": {"page": 3, "per_page": 101}, "expected_success": False, "status_code": 422}),
                     id="invalid per_page above maximum"),
    ])
    def test_get_posts_feed_invalid_payload(self, query_request_conditions):
        self.user_eve.posts_api.get_posts_feed(params=query_request_conditions["params"],
                                               status_code=query_request_conditions["status_code"],
                                               expected_success=query_request_conditions["expected_success"])









    @allure.suite("Tests get certain post")
    @allure.story("User can read existed post at platform")
    @allure.description("Get certain post - valid post depending on role - {role}")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"post_case":"public",  "create_by": "admin"}, {"user":"user_bob", "expected_success": True, "status_code": 200,}, id="As user get public post created by admin"),
        pytest.param({"post_case":"followers", "create_by": "user_eve"}, {"user":"moderator", "expected_success": True, "status_code": 200}, id="As moderator get the post (followers only) created by user"),
        pytest.param({"post_case":"public", "create_by": "moderator"}, {"user":"admin", "expected_success": True, "status_code": 200}, id="As admin get public post created by moderator"),
        ], indirect=["create_post_remove"])
    def test_get_post_depends_on_role(self, create_post_remove, test_data):
        prepared_post_id = create_post_remove
        user = self.get_actor(test_data["user"])
        user.posts_api.get_post(post_id=prepared_post_id,
                                         expected_success=test_data["expected_success"],
                                         status_code=test_data["status_code"])



    @allure.suite("Tests get certain post")
    @allure.story("User can read existed post at platform")
    @allure.description("Get certain post - invalid post_id")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"post_case":"removed",  "create_by": "admin"}, {"user":"user_bob", "expected_success": False, "status_code": 404,}, id="Try to get removed post"),
        pytest.param({"post_case": "not_existed"}, {"user": "user_bob", "expected_success": False, "status_code": 404 }, id="Try to get not existed post"),
    ], indirect=["get_incorrect_post"])
    def test_get_post_invalid_post(self, get_incorrect_post, test_data):
        prepared_post_id = get_incorrect_post
        user = self.get_actor(test_data["user"])
        user.posts_api.get_post(post_id=prepared_post_id,
                                expected_success=test_data["expected_success"],
                                status_code=test_data["status_code"])









    @allure.suite("Update post")
    @allure.feature("User can update created post")
    @allure.story("As a post creator i can update it after publishing")
    @allure.description("Update post as author")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_eve"}, {"user":"user_eve", "payload": {"content": "A"}, "expected_success": True, "status_code": 200},
            id="Update post created by author - Valid minimal boundary"),
        pytest.param({"create_by": "user_eve"}, {"user":"user_eve", "payload": {"content": "A" * 2000}, "expected_success": True, "status_code": 200},
            id="Update post created by author - Valid maximal boundary"),
        # pytest.param({"create_by": "user_eve"},{"user": "user_eve", "payload": {"content": "Valid post content", "visibility": "followers_only"},
        #               "expected_success": True, "status_code": 200},
        #     id="Update visibility parameter"),
        # pytest.param({"create_by": "user_eve"}, {"user": "user_eve", "payload": {"content": "Valid post content","image_url": "temp_data/image.jpg"},
        #                                          "expected_success": True, "status_code": 200},
        #     id="Update image parameter"),
    ], indirect=["create_post_remove"])
    def test_update_post(self, create_post_remove, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = create_post_remove
        prepared_post = user.posts_api.get_post(post_id=prepared_post_id)
        if test_data["payload"] is None:
            new_post_body  = {"content": "Updated content123"}
        else:
            new_post_body = test_data["payload"]

        updated_post = user.posts_api.update_post(post_id=prepared_post_id,
                                                                  payload=new_post_body,
                                                                  expected_success=test_data["expected_success"],
                                                                  status_code=test_data["status_code"])
        update_time_before = prepared_post.updated_at
        assert updated_post.updated_at > update_time_before, (updated_post.updated_at, update_time_before)
        assert prepared_post.content != updated_post.content, "Content does not updated after PATCH"
        if "image_url" in new_post_body.keys():
            assert prepared_post.image_url != updated_post.image_url, f"Image url does not updated after PATCH - {updated_post.image_url}"
        if "visibility" in new_post_body.keys():
            assert prepared_post.visibility != updated_post.visibility, f"Visibility does not updated after PATCH - {updated_post.visibility}"



    @allure.suite("Update post")
    @allure.feature("User can update created post")
    @allure.story("As a user i can update only own post in valid time range")
    @allure.description("Test attempt to update the post if post id is incorrect or user has no rules to do it")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"post_case": "late", "create_by": "user_eve"}, {"user": "user_eve", "expected_success": False, "status_code": 400},
                     id="As author update the post, that older than 15 minutes"),
        pytest.param({"post_case": "not_own", "create_by": "user_eve"},
                     {"user": "user_eve", "expected_success": False, "status_code": 403},
                     id="Update post created by another user"),
        pytest.param({"post_case": "not_existed"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Try to update post, that doesn't exist"),
        pytest.param({"post_case": "removed", "create_by": "user_eve"},
                     {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Try to update post, that was removed"),
    ], indirect=["get_incorrect_post"])
    def test_update_post_invalid_post_ownership(self, get_incorrect_post, test_data):
        prepared_post_id = get_incorrect_post
        post_body = {"content": "Updated content 321"}
        self.user_eve.posts_api.update_post(post_id=prepared_post_id,
                                                              payload=post_body,
                                                              expected_success=test_data["expected_success"],
                                                              status_code=test_data["status_code"])



    @allure.suite("Update post")
    @allure.story("User can update created post")
    @allure.description("Precondition: post created before test and will be removed after by fixture")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_eve"},{"user": "user_eve", "payload": {"content": ""}, "expected_success": False, "status_code": 422},
                     id="invalid content below min boundary"),
        pytest.param({"create_by": "user_eve"},{"user": "user_eve", "payload": {"content": "A" * 2001}, "expected_success": False, "status_code": 422},
                     id="invalid content above max boundary"),
        pytest.param({"create_by": "user_eve"},{"user": "user_eve", "payload": {"content": 2001}, "expected_success": False, "status_code": 422},
                     id="invalid content - integer"),
    ], indirect=["create_post_remove"])
    def test_update_post_invalid_payload(self, create_post_remove, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = create_post_remove
        user.posts_api.update_post(post_id=prepared_post_id,
                                   payload=test_data["payload"],
                                   expected_success=test_data["expected_success"],
                                   status_code=test_data["status_code"])









    @allure.suite("Remove post")
    @allure.story("User can remove created post")
    @allure.description("Precondition: post created before test")
    @pytest.mark.parametrize("create_post_only, test_data", [
        pytest.param({"create_by": "user_eve"},{"user": "user_eve", "params": None},
                     id="Remove post by its author"),
        pytest.param({"create_by": "user_eve"}, {"user": "user_eve", "params": {"reason": "Delete it immediately"}},
                     id="Remove post by its author with provided 'reason'"),
    ], indirect=["create_post_only"])
    def test_delete_post(self, create_post_only, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = create_post_only
        if test_data["params"] is not None:
            user.posts_api.delete_post(post_id=prepared_post_id, params=test_data["params"])
        else:
            user.posts_api.delete_post(post_id=prepared_post_id)
        user.posts_api.get_post(post_id=prepared_post_id, status_code=404, expected_success=False)



    @allure.suite("Remove post")
    @allure.story("User can remove created post")
    @allure.description("Attempt to remove the post depends on {user}")
    @pytest.mark.parametrize("create_post_only, test_data", [
        pytest.param({"create_by": "user_eve"}, {"user": "admin", "params": None},
                     id="Remove post of another user as admin"),
        pytest.param({"create_by": "user_eve"}, {"user": "moderator", "params": None},
                     id="Remove post of another user as moderator"),
    ], indirect=["create_post_only"])
    def test_delete_post_by_role(self, create_post_only, test_data):
        user = self.get_actor(test_data["user"])
        prepared_post_id = create_post_only
        if test_data["params"] is not None:
            user.posts_api.delete_post(post_id=prepared_post_id, params=test_data["params"])
        else:
            user.posts_api.delete_post(post_id=prepared_post_id)
        user.posts_api.get_post(post_id=prepared_post_id, status_code=404, expected_success=False)



    @allure.suite("Remove post")
    @allure.story("User can remove created post")
    @allure.description("Attempt to remove the post - invalid post id")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"create_by": "user_eve", "post_case":"not_own"}, {"user": "user_eve", "expected_success": False, "status_code": 403},
                     id="Remove post of another user"),
        pytest.param({"post_case": "not_existed"}, {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Post doesn't exist"),
        # pytest.param({"create_by": "user_eve", "post_case": "removed"},{"user": "user_eve", "expected_success": False, "status_code": 404},
        #              id="Post id existed, but post deleted"),
    ], indirect=["get_incorrect_post"])
    def test_delete_post_invalid(self, get_incorrect_post, test_data):
        prepared_post_id = get_incorrect_post
        user = self._service_by_role(test_data["user"])
        user.posts_api.delete_post(post_id=prepared_post_id,
                                   expected_success=test_data["expected_success"],
                                   status_code=test_data["status_code"])









    @allure.suite("Repost post")
    @allure.story("User can repost existed post")
    @allure.description("Precondition: post created before test, create repost to it and remove after")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_bob"},{"user": "user_eve", "payload": {"repost_type": "repost", "content": ""}},
                     id="Valid repost with empty optional content"),
        pytest.param({"create_by": "user_bob"},{"user": "user_eve", "payload": {"repost_type": "quote", "content": "A" * 2000}},
                     id="Valid quote repost with max content boundary"),
        pytest.param({"create_by": "user_eve"},{"user": "user_bob", "payload": {"content": "Content only"}},
                     id="Missing required repost type")
    ], indirect=["create_post_remove"])
    def test_repost_post(self, test_data, create_post_remove):
        prepared_post_id = create_post_remove
        case_payload = test_data["payload"]
        user = self._service_by_role(test_data["user"])
        reposted_post_before = user.posts_api.get_post(post_id=prepared_post_id)
        reposted_post_after = user.posts_api.repost_post(payload=case_payload,
                                         post_id=prepared_post_id)
        assert reposted_post_before.repost_type != reposted_post_after.repost_type, f"Repost_type isn't changed after repost. AR: {reposted_post_after.repost_type}"
        assert reposted_post_after.repost_type == case_payload["repost_type"], f"Repost_type isn't matched expected one. AR: {reposted_post_after.repost_type}"
        # assert reposted_post_before.reposts_count != reposted_post_after.reposts_count, f"Repost count isn't changed after repost. ER/AR: {reposted_post_before.reposts_count}/{reposted_post_after.reposts_count}"



    @allure.suite("Repost post")
    @allure.story("User can repost existed post")
    @allure.description("Attempt to create repost with invalid date at request payload")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_eve"},{"user": "user_bob", "payload": {"repost_type": "quote", "content": "A" * 2001}, "expected_success": False, "status_code": 422},
                     id="Invalid content above max boundary"),
        pytest.param({"create_by": "user_eve"}, {"user": "user_bob", "payload": {"repost_type": "invalid_type", "content": "Invalid repost type enum"}, "expected_success": False, "status_code": 422},
                     id="Invalid repost type enum")
                             ])
    def test_repost_post_invalid_payload(self, test_data, create_post_remove):
        prepared_post_id = create_post_remove
        user = self._service_by_role(test_data["user"])
        user.posts_api.repost_post( payload=test_data["payload"],
                                    post_id=prepared_post_id,
                                    expected_success=test_data["expected_success"],
                                    status_code=test_data["status_code"])



    @allure.suite("Repost post")
    @allure.story("User can repost existed post")
    @allure.description("Attempt to create repost, when post id is incorrect")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"create_by": "user_eve", "post_case": "not_existed"},{"user": "user_bob", "payload":  {"repost_type": "repost", "content": "Non-existing post id"}, "expected_success": False, "status_code": 404},
                     id="Non-existing post id"),
        pytest.param({"create_by": "user_eve", "post_case": "removed"}, {"user": "user_bob", "payload": {"repost_type": "repost", "content": "Attempt to repost removed post"}, "expected_success": False, "status_code": 404},
                     id="Attempt to repost removed post")
        ], indirect=["get_incorrect_post"])
    def test_repost_post_invalid_post(self, test_data, get_incorrect_post):
        prepared_post_id = get_incorrect_post
        user = self._service_by_role(test_data["user"])
        user.posts_api.repost_post(payload=test_data["payload"],
                                   post_id=prepared_post_id,
                                   expected_success=test_data["expected_success"],
                                   status_code=test_data["status_code"])









    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Precondition: post created before test and remove after")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_eve", "post_case":"pinned"},{"user": "user_eve"},
                     id="Pin the post as author"),
        pytest.param({"create_by": "user_eve"},{"user": "user_eve"},
                     id="Post already pinned"),
    ], indirect=["create_post_remove"])
    def test_pin_post(self, create_post_remove, test_data):
        prepared_post_id = create_post_remove
        user = self._service_by_role(test_data["user"])
        post_before = user.posts_api.get_post(post_id=prepared_post_id)
        user.posts_api.pin_post(post_id=prepared_post_id)

        pin_post_after = user.posts_api.get_post(post_id=prepared_post_id)
        assert post_before.is_pinned == pin_post_after.is_pinned if post_before.is_pinned is True else  post_before.is_pinned != pin_post_after.is_pinned



    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Attempt to pin post of another user by user with different roles: {test_data['user]}")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_eve"}, {"user": "admin", "expected_success": False, "status_code": 403},
                     id="Pin the post of another user as admin"),
        pytest.param({"create_by": "user_eve"}, {"user": "moderator", "expected_success": False, "status_code": 403},
                     id="Pin the post of another user as moderator"),
        pytest.param({"create_by": "user_eve"}, {"user": "user_bob", "expected_success": False, "status_code": 403},
                     id="Pin the post of another user as user")
    ], indirect=["create_post_remove"])
    def test_pin_post_by_another_user(self, create_post_remove, test_data):
        prepared_post_id = create_post_remove
        user = self._service_by_role(test_data["user"])
        user.posts_api.pin_post(post_id=prepared_post_id,
                                expected_success=test_data["expected_success"],
                                status_code=test_data["status_code"])



    @allure.suite("Pin/unpin post")
    @allure.story("User can pin existed post")
    @allure.description("Attempt to pin the post, when post id is invalid")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"post_case":"not_existed"}, {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Pin the post that doesn't exist"),
        pytest.param({"post_case":"removed", "create_by": "user_eve"}, {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Post id existed, but post is deleted"),
    ],indirect=["get_incorrect_post"])
    def test_pin_post_invalid_post(self, get_incorrect_post, test_data):
        prepared_post_id = get_incorrect_post
        user = self._service_by_role(test_data["user"])
        user.posts_api.pin_post(post_id=prepared_post_id,
                                expected_success=test_data["expected_success"],
                                status_code=test_data["status_code"])




    @allure.suite("Pin/unpin post")
    @allure.story("User can UNpin own post already pinned")
    @allure.description("Precondition: create and pin the post. Post condition: prepared post will be removed")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_eve", "post_case":"pinned"},{"user": "user_eve"},
                     id="UnPin the post as author"),
        pytest.param({"create_by": "user_bob"},{"user": "user_bob"},
                     id="UnPin the post as author, post isn't pinned"),
    ], indirect=["create_post_remove"])
    def test_unpin_post(self, create_post_remove, test_data):
        prepared_post_id = create_post_remove
        user = self._service_by_role(test_data["user"])

        post_before = user.posts_api.get_post(post_id=prepared_post_id)
        user.posts_api.unpin_post(post_id=prepared_post_id)
        post_after = user.posts_api.get_post(post_id=prepared_post_id)

        if post_before.is_pinned:
            assert post_before.is_pinned != post_after.is_pinned, f"Failed check is_pinned status.\nER/AR {post_before.is_pinned}/{post_after.is_pinned}"
        else:
            assert post_before.is_pinned == post_after.is_pinned, f"Failed check is_pinned status.\nER/AR {post_before.is_pinned}/{post_after.is_pinned}"



    @allure.suite("Pin/unpin post")
    @allure.story("User can UNpin own post already pinned")
    @allure.description("Attempt to pin post of another user by user with different roles: {test_data['user]}")
    @pytest.mark.parametrize("create_post_remove, test_data", [
        pytest.param({"create_by": "user_eve", "post_case": "pinned"}, {"user": "admin", "expected_success": False, "status_code": 403},
                     id="UnPin the post of another user as admin"),
        pytest.param({"create_by": "user_eve", "post_case": "pinned"}, {"user": "moderator", "expected_success": False, "status_code": 403},
                     id="UnPin the post of another user as moderator"),
        pytest.param({"create_by": "user_eve", "post_case": "pinned"}, {"user": "user_bob", "expected_success": False, "status_code": 403},
                     id="UnPin the post of another user as user")
    ], indirect=["create_post_remove"])
    def test_unpin_post_by_another_user(self, create_post_remove, test_data):
        prepared_post_id = create_post_remove
        user = self._service_by_role(test_data["user"])
        user.posts_api.unpin_post(post_id=prepared_post_id,
                                  expected_success=test_data["expected_success"],
                                  status_code=test_data["status_code"])



    @allure.suite("Pin/unpin post")
    @allure.story("User can UNpin own post already pinned")
    @allure.description("Attempt to pin the post, when post id is invalid")
    @pytest.mark.parametrize("get_incorrect_post, test_data", [
        pytest.param({"post_case":"not_existed"}, {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Pin the post that doesn't exist"),
        pytest.param({"post_case":"removed", "create_by": "user_eve"}, {"user": "user_eve", "expected_success": False, "status_code": 404},
                     id="Post id existed, but post is deleted"),
    ],indirect=["get_incorrect_post"])
    def test_unpin_post_invalid_post(self, get_incorrect_post, test_data):
        prepared_post_id = get_incorrect_post
        user = self._service_by_role(test_data["user"])
        user.posts_api.unpin_post(post_id=prepared_post_id,
                                  expected_success=test_data["expected_success"],
                                  status_code=test_data["status_code"])

