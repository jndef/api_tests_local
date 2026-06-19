import requests

from config.headers import Headers
from services.bookmarks.endpoints import Endpoints
from services.bookmarks.models.model_bookmark_list import ResponseBookmarksModel
from services.bookmarks.params import GetBookmarksParams
from services.bookmarks.payloads import Payloads
from utils.helper import Helper


class BookmarksAPI(Helper):
    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    def get_bookmarks(self, params: dict, status_code: int = 200, expected_success: bool = True):
        response = requests.get(
            url=self.endpoints.get_bookmarks_list,
            headers=self.headers.basic,
            params=GetBookmarksParams(**(params or {})).to_dict()
        )
        return self.validate_response(response, ResponseBookmarksModel, status_code=status_code,
                                      expected_success=expected_success)

    def bookmark_post(self, post_id: str, status_code: int = 201, expected_success: bool = True):
        response = requests.post(
            url=self.endpoints.bookmark_post(post_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)

    def remove_bookmark(self, post_id: str, status_code: int = 204, expected_success: bool = True):
        response = requests.delete(
            url=self.endpoints.unbookmark_post(post_id),
            headers=self.headers.basic,
        )
        return self.validate_response(response, None, status_code=status_code, expected_success=expected_success)
