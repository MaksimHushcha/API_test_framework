import requests
import pytest_check as check
from Src.endpoints.BaseEndpoint import BaseEndpoint

class PostEndpoints(BaseEndpoint):
    response = None
    created_post_id = None
    returned_userId = None
    created_user_id = None
    returned_title = None
    created_title = None
    returned_body = None
    created_body = None

    def create_a_post(self, url, data):
        response = requests.post(url,
                                 headers={'Content-Type': 'application/json; charset=utf-8'},
                                 json=data)
        self.json_data = response.json()
        self.status_code = response.status_code
        self.created_user_id = data["userId"]
        self.created_title = data["title"]
        self.created_body = data["body"]
        self.returned_userId = self.json_data["userId"]
        self.returned_title = self.json_data["title"]
        self.returned_body = self.json_data["body"]
        self.created_post_id = self.json_data["id"]
        return self.created_post_id

    def check_response_status_is_201(self):
        assert self.status_code == 201, f"Expected 201, but got: {self.status_code}"

    def check_json_length_is_not_zero(self):
        assert len(self.json_data) > 0, "Json data is empty"

    def check_returned_userid_is_created_userid(self):
        check.equal(self.returned_userId, self.created_user_id,
                    f"Expected post to be created with userID: {self.created_title}, but got {self.returned_title}")

    def check_returned_title_is_created_title(self):
        check.equal(self.returned_title, self.created_title,
                    f"Expected post to be created with title: {self.created_title}, but got {self.returned_title}")

    def check_returned_body_is_created_body(self):
        check.equal(self.returned_body, self.created_body,
                    f"Expected post to be created with title: {self.created_body}, but got {self.returned_body}")


