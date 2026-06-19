from config.stages import get_stage

STAGE = get_stage()
SERVICE_POSTS_URL = "/api/posts"

class Endpoints:
    get_list_posts = f"{STAGE}{SERVICE_POSTS_URL}"
    create_post = f"{STAGE}{SERVICE_POSTS_URL}"
    get_feed = f"{STAGE}{SERVICE_POSTS_URL}/feed"
    get_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}"
    update_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}"
    delete_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}"
    repost_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/repost"
    pin_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/pin"
    unpin_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/pin"
