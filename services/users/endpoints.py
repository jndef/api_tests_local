from config.stages import get_stage

STAGE = get_stage()
SERVICE_USERS_URL = "/api/users"

class Endpoints:

    get_users = f"{STAGE}{SERVICE_USERS_URL}"
    get_suggestions = f"{STAGE}{SERVICE_USERS_URL}/suggestions"
    get_profile_by_username = lambda self, username: f"{STAGE}{SERVICE_USERS_URL}/{username}"
    update_me = f"{STAGE}{SERVICE_USERS_URL}/me"
    update_avatar = f"{STAGE}{SERVICE_USERS_URL}/me/avatar"
    delete_avatar = f"{STAGE}{SERVICE_USERS_URL}/me/avatar"
    get_user_posts = lambda self, username: f"{STAGE}{SERVICE_USERS_URL}/{username}/posts"
    get_user_followers = lambda self, username: f"{STAGE}{SERVICE_USERS_URL}/{username}/followers"
    get_user_following = lambda self, username: f"{STAGE}{SERVICE_USERS_URL}/{username}/following"

