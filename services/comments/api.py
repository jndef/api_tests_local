import requests

from config.headers import Headers
from services.comments.endpoints import Endpoints
from services.comments.models.model_comment_create import ResponseCommentCreateModel
from services.comments.models.model_comment_update import ResponseCommentUpdateModel
from services.comments.models.model_comments_list import ResponseCommentsModel
from services.comments.models.model_reply_create import ResponseCreateReplyModel
from services.comments.params import GetCommentsParams, GetRepliesParams
from services.comments.payloads import Payloads
from utils.helper import Helper


class CommentsAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_list_comments(self, post_id:str, params: dict = None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_list_comments(post_id),
            headers=self.headers.basic,
            params= GetCommentsParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponseCommentsModel,status_code=status_code, expected_success=expected_success)

    def create_comment(self, post_id:str, payload: dict, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.create_comment(post_id),
            headers=self.headers.basic,
            json=self.payloads.create_comment(**payload)
        )
        return self.validate_response(response, ResponseCommentCreateModel, status_code=status_code, expected_success=expected_success)


    def update_comment(self, comment_id:str,  payload: dict, status_code: int = 200, expected_success: bool = True):
        response = requests.patch(
            url=self.endpoints.update_comment(comment_id),
            headers=self.headers.basic,
            json=self.payloads.update_comment(**payload)
        )
        return self.validate_response(response, ResponseCommentUpdateModel, status_code=status_code, expected_success=expected_success)

    def delete_comment(self, comment_id:str, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.delete_comment(comment_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)

    def get_list_replies(self, comment_id:str, params: dict = None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_list_replies(comment_id),
            headers=self.headers.basic,
            params= GetRepliesParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponseCommentsModel,status_code=status_code, expected_success=expected_success)

    def create_reply(self, comment_id:str, payload: dict, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.create_reply(comment_id),
            headers=self.headers.basic,
            json=self.payloads.create_reply(**payload) or {}
        )
        return self.validate_response(response, ResponseCreateReplyModel, status_code=status_code, expected_success=expected_success)
