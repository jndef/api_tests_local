import allure
import pytest

from config.base_test import BaseTest


@allure.epic("Users")
@allure.feature("Users")
@allure.parent_suite("Users")
class TestUsers(BaseTest):

    @allure.title("Get List users")
    @allure.tag("")
    @allure.title("Get List users with params: {queries}")
    @pytest.mark.parametrize("queries", [
        ({"search": "admin", "page": 1, "per_page": 10}),
        # ({"search": "eve", "page": 1, "per_page": 20}, 200, True),
        # ({}, 200, True)
    ])
    # @pytest.mark.parametrize("domain", open("domains.txt").readlines())
    # @pytest.mark.working
    @pytest.mark.smoke
    def test_get_users(self, queries):
        self.admin.users_api.get_list_users(params=queries)

    @allure.title("Get user suggestions")
    @allure.description("Return up to 5 active users that the current user does not follow yet.")
    def test_get_suggestions(self):
        self.admin.users_api.get_user_suggestions()
        self.user_eve.users_api.get_user_suggestions()



    @allure.title("Get user profile")
    @pytest.mark.parametrize("username", ["admin", "dave_quiet", "bob_photo"])
    @allure.description("Return user profile with provided username: {username}")
    def test_get_user_profile(self, username):
        user = self.admin.users_api.get_user_profile(username=username)
        assert user.username == username, f"AR: {user.username} != {username}"



    @allure.title("Update me")
    @pytest.mark.parametrize("display_name, bio, is_private, expected_success, status_code",[
                                 ("A", "some bio", True, True, 200),  # min boundary
                                 ("A" * 100, "some bio", False, True, 200),  # max boundary
                                 ("A" * 101, "some bio", True, False, 200),  # above max
                                 ("", "some bio", False, False, 422),  # below min
                                 ("Normal", "", True, True, 200),  # empty bio
                                 ("Normal", "", False, True, 200),  # empty bio + is_private coverage
                             ])
    @allure.description(f"Update user profile using provided data set")
    def test_update_profile(self, display_name, bio, is_private, expected_success, status_code):
        updated_profile = self.user_eve.users_api.update_profile(display_name=display_name, bio=bio,
                                                                 is_private=is_private,
                                                                 expected_success=expected_success,
                                                                 status_code=status_code)
        if expected_success:
            assert updated_profile.display_name == display_name, f"AR: {updated_profile.display_name} != {display_name}"
            assert updated_profile.bio == bio, f"AR: {updated_profile.bio} != {bio}"
            assert updated_profile.is_private == is_private, f"AR: {updated_profile.is_private} != {is_private}"



    @allure.title("Upload Avatar")
    @allure.description(f"Upload Avatar using local file")
    @pytest.mark.parametrize("file_name", [
        "image.png",
        # "image.jpg",
        # "image.webp",
    ])
    def test_upload_avatar(self, file_name):
        current_profile = self.user_eve.auth_api.get_me()
        current_avatar = current_profile.avatar_url
        updated_avatar_profile = self.user_eve.users_api.update_profile_avatar(file_name_with_ext=f"{file_name}")
        assert updated_avatar_profile.avatar_url != current_avatar
        updated_current_profile = self.user_eve.auth_api.get_me()
        updated_avatar = updated_current_profile.avatar_url
        assert current_avatar != updated_avatar



    @allure.title("Delete Avatar")
    @allure.description(f"Delete existed avatar")
    def test_delete_avatar(self):
        # Precondition - add avatar
        self.user_eve.users_api.update_profile_avatar(file_name_with_ext="image.png")

        current_profile = self.user_eve.auth_api.get_me()
        current_avatar = current_profile.avatar_url
        self.user_eve.users_api.delete_profile_avatar()
        updated_current_profile = self.user_eve.auth_api.get_me()
        updated_avatar = updated_current_profile.avatar_url
        assert current_avatar != updated_avatar



    @allure.title("Get user followers, user: {username}")
    @pytest.mark.parametrize("username, params, positive_case, status_code",[
            # fully valid request with minimum boundaries
            ("admin", {"page": 1, "per_page": 1}, True, 200),

            # valid maximum boundary for per_page
            ("bob_photo", {"page": 2, "per_page": 100}, True, 200),

            # invalid page below minimum
            ("admin", {"page": 0, "per_page": 10}, False, 422),

            # invalid per_page below minimum
            ("bob_photo", {"page": 1, "per_page": 0}, False, 422),

            # invalid per_page above maximum
            ("dave_quiet", {"page": 3, "per_page": 101}, False, 422),

            # non-existing username
            ("unknown_user", {"page": 1, "per_page": 10}, False, 404),

            # optional params omitted
            ("admin", {}, True, 200),
        ])
    @allure.description("Return followers of user")

    def test_get_user_followers(self, username, params, positive_case, status_code):
        self.admin.users_api.get_user_followers(username=username, params=params, expected_success=positive_case, status_code=status_code)



    @allure.title("Get user following, user: {username}")
    @pytest.mark.parametrize("username, params, positive_case, status_code",[
            # fully valid request with minimum boundaries
            ("admin", {"page": 1, "per_page": 1}, True, 200),

            # valid maximum boundary for per_page
            ("bob_photo", {"page": 2, "per_page": 100}, True, 200),

            # invalid page below minimum
            ("admin", {"page": 0, "per_page": 10}, False, 422),

            # invalid per_page below minimum
            ("bob_photo", {"page": 1, "per_page": 0}, False, 422),

            # invalid per_page above maximum
            ("dave_quiet", {"page": 3, "per_page": 101}, False, 422),

            # non-existing username
            ("unknown_user", {"page": 1, "per_page": 10}, False, 404),

            # optional params omitted
            ("admin", {}, True, 200),
        ])
    @allure.description("Return following list of the user")
    def test_get_user_followers(self, username, params, positive_case, status_code):
        self.admin.users_api.get_user_following(username=username, params=params, expected_success=positive_case,
                                                status_code=status_code)
