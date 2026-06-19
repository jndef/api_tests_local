from config.stages import get_stage

STAGE = get_stage()
SERVICE_POSTS_URL = "/api/posts"
SERVICE_COMMENTS_URL = "/api/comments"

class Endpoints:
    like_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/like"
    unlike_post = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/like"
    get_post_likes  = lambda self, post_id: f"{STAGE}{SERVICE_POSTS_URL}/{post_id}/likes"
    like_comment = lambda self, comment_id: f"{STAGE}{SERVICE_COMMENTS_URL}/{comment_id}/like"
    unlike_comment = lambda self, comment_id: f"{STAGE}{SERVICE_COMMENTS_URL}/{comment_id}/like"
