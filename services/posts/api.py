import requests

from config.headers import Headers
from services.posts.endpoints import Endpoints
from services.posts.models.model_post import ResponsePostModel
from services.posts.models.model_post_create import ResponseCreatePostModel
from services.posts.models.model_post_update import ResponsePostUpdateModel
from services.posts.models.model_posts_feed import ResponsePostsFeedModel
from services.posts.models.model_posts_list import ResponsePostsModel
from services.posts.params import GetPostsParams, GetFeedParams, DeletePostParams
from services.posts.payloads import Payloads
from utils.helper import Helper


class PostsAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_list_posts(self, params: dict = None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_list_posts,
            headers=self.headers.basic,
            params= GetPostsParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponsePostsModel,status_code=status_code, expected_success=expected_success)


    def create_post(self, payload: dict, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.create_post,
            headers=self.headers.basic,
            json=self.payloads.create_post(**payload)
        )
        return self.validate_response(response, ResponseCreatePostModel, status_code=status_code, expected_success=expected_success)

    def get_posts_feed(self, params: dict = None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_feed,
            headers=self.headers.basic,
            params= GetFeedParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponsePostsFeedModel, status_code=status_code, expected_success=expected_success)

    def get_post(self, post_id:str, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_post(post_id),
            headers=self.headers.basic
        )
        return self.validate_response(response, ResponsePostModel, status_code=status_code, expected_success=expected_success)

    def update_post(self, post_id:str,  payload: dict, status_code: int = 200, expected_success: bool = True):
        response = requests.patch(
            url=self.endpoints.update_post(post_id),
            headers=self.headers.basic,
            json=self.payloads.update_post(**payload)
        )
        return self.validate_response(response, ResponsePostUpdateModel, status_code=status_code, expected_success=expected_success)

    def delete_post(self, post_id:str, params: dict = None, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.delete_post(post_id),
            headers=self.headers.basic,
            params=DeletePostParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)


    def repost_post(self, post_id:str, payload: dict, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.repost_post(post_id),
            headers=self.headers.basic,
            json=self.payloads.create_repost(**payload) or {}
        )
        return self.validate_response(response, ResponsePostUpdateModel, status_code=status_code, expected_success=expected_success)

    def pin_post(self, post_id:str, status_code: int = 204, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.pin_post(post_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code, expected_success)

    def unpin_post(self, post_id:str, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.unpin_post(post_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code, expected_success)
