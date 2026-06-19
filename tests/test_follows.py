import allure
import pytest

from config.base_test import BaseTest


@allure.epic("Follows")
@allure.feature("Follows")
@allure.parent_suite("Follows")
class TestFollows(BaseTest):

    @allure.title("Get Follow requests")
    @allure.tag("")
    @allure.title("Get Follow requests")
    @pytest.mark.parametrize(
        "queries, expected_success, status_code",
        [
            # valid minimum boundaries
            ({"page": 1, "per_page": 1}, True, 200),
            # valid maximum boundary
            ({"page": 2, "per_page": 100}, True, 200),
            # invalid page below minimum
            ({"page": 0, "per_page": 10}, False, 422),
            # invalid per_page below minimum
            ({"page": 1, "per_page": 0}, False, 422),
            # invalid per_page above maximum
            ({"page": 3, "per_page": 101}, False, 422),
            # optional params omitted
            ({}, True, 200),
        ]
    )
    # @pytest.mark.parametrize("domain", open("domains.txt").readlines())
    def test_get_users(self, queries, expected_success, status_code):
        self.admin.users_api.get_list_users(params=queries, expected_success=expected_success, status_code=status_code)

    @allure.title("UnFollow user, username: {unfollow_username}")
    @allure.tag("")
    @allure.title("Unfollow user")
    @pytest.mark.parametrize("unfollow_username, expected_success,status_code",[
            # unfollow user, success
            ("alice_dev", True, 204),
            # unfollow user, who has not been followed
            ("dave_quiet", False, 404),
            # unfollow not existed user
            ("unknown_walker", False, 404),
            # invalid data - empty string
            ("", False, 404)
        ])
    @pytest.mark.parametrize("follow_unfollow", [["admin", "alice_dev", "follow"]], indirect=True)
    def test_unfollow_user(self, unfollow_username, expected_success, status_code, follow_unfollow):
        self.admin.follows_api.unfollow_user(unfollow_username, expected_success=expected_success,
                                             status_code=status_code)

        own_username = self.admin.auth_api.get_me().username
        followers_list = self.admin.users_api.get_user_following(own_username).items

        for follower in followers_list:
            assert unfollow_username != follower.username


    @allure.title("Follow user, username: {follow_username}")
    @allure.tag("")
    @allure.title("Unfollow user")
    @pytest.mark.parametrize("following_username, expected_success, status_code",[
            # follow user, success
            ("admin", True, 201),
            # follow user, who has already been followed
            ("alice_dev", False, 409),
            # unfollow not existed user
            ("unknown_walker", False, 404),
            # invalid data - empty string
            ("", False, 404),
        ])
    @pytest.mark.parametrize("follow_unfollow", [["user_eve", "admin", "unfollow"]], indirect=True)

    def test_follow_user(self, following_username, expected_success, status_code, follow_unfollow):
        self.user_eve.follows_api.follow_user(following_username, expected_success=expected_success, status_code=status_code)

        own_username = self.user_eve.auth_api.get_me().username
        following_list = self.user_eve.users_api.get_user_following(own_username).items
        if expected_success:
            assert any([following_username == following.username for following in following_list])

