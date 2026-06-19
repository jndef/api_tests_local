import requests

from config.headers import Headers
from services.likes.endpoints import Endpoints
from services.likes.models.model_comment_add_like import ResponseCommentReactionModel
from services.likes.models.model_post_add_like import ResponsePostReactionModel
from services.likes.models.model_post_likes_list import ResponsePostReactionsListModel
from services.likes.params import GetPostLikesParams
from services.likes.payloads import Payloads
from utils.helper import Helper
from utils.logger import logger


class LikesAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def like_post(self, post_id:str, payload: dict, status_code: int = 201, expected_success: bool = True):
        logger.info(f"Sending POST request to {self.endpoints.like_post(post_id)}")
        response = requests.post(
            url=self.endpoints.like_post(post_id),
            headers=self.headers.basic,
            json=self.payloads.like_post(**payload)
        )
        logger.debug(f"Received response: {response.json()}")
        return self.validate_response(response, ResponsePostReactionModel, status_code=status_code, expected_success=expected_success)



    def unlike_post(self, post_id:str, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.unlike_post(post_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)

    def get_post_likes(self, post_id:str, params: dict, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_post_likes(post_id),
            headers=self.headers.basic,
            params= GetPostLikesParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponsePostReactionsListModel, status_code=status_code, expected_success=expected_success)


    def like_comment(self, comment_id:str,  payload: dict,  status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.like_comment(comment_id),
            headers=self.headers.basic,
            json=self.payloads.like_comment(**payload)
        )
        return self.validate_response(response, ResponseCommentReactionModel, status_code=status_code, expected_success=expected_success)


    def unlike_comment(self, comment_id:str, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.unlike_comment(comment_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)
