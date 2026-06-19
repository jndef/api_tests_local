import requests

from config.headers import Headers
from services.follows.endpoints import Endpoints
from services.follows.models.model_follow_requests import ResponseFollowersListModel
from services.follows.models.model_follow_user import ResponseFollowRequestModel
from services.follows.models.model_follow_request_accept import ResponseFollowRequestModel
from services.follows.params import GetUserFollowsParams
from services.follows.payloads import Payloads
from utils.helper import Helper


class FollowsAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()



    def follow_user(self, username, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.follow_user(username),
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseFollowRequestModel, status_code, expected_success)



    def unfollow_user(self, username, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.unfollow_user(username),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code, expected_success)



    def get_follow_requests(self, params:dict=None, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_follow_req,
            headers=self.headers.basic,
            params=GetUserFollowsParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponseFollowersListModel, status_code, expected_success)



    def accept_follow_request(self,follow_id:str, status_code: int = 200, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.accept_follow_req(follow_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, ResponseFollowRequestModel, status_code, expected_success)



    def reject_follow_request(self,follow_id:str, status_code: int = 204, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.reject_follow_req(follow_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code, expected_success)