import requests
import pytest_check as check
from Src.endpoints.BaseEndpoint import BaseEndpoint


class PostsEndpoints(BaseEndpoint):
    path = "posts"

    def get_all_posts(self):
        return self.get(self.path)


    def get_posts_by_id(self, url, post_id):
        response = requests.get(url, params={'id': post_id})
        self.status_code = response.status_code
        self.json_data = response.json()
        self.requested_post_id = post_id
        if self.json_data:
            self.returned_post_id = self.json_data[0].get("id")
            self.returned_userId = self.json_data[0].get("userId")
            self.returned_title = self.json_data[0].get("title")
            self.returned_body = self.json_data[0].get("body")

    def get_comments_to_the_post(self, url, post_id):
        response = requests.get(url + f"/{post_id}/comments")
        self.status_code = response.status_code
        self.json_data = response.json()
        self.requested_post_id = post_id
        self.json_data = response.json()

    def check_response_status_is_404(self):
        assert self.status_code == 404, f"Expected 404, but got: {self.status_code}"

    def check_data_is_a_list(self):
        assert isinstance(self.json_data, list), f"Response is not a list, but {type(self.json_data)}"

    def check_json_length_is_not_zero(self):
        assert len(self.json_data) > 0, "Json data is empty"

    def check_first_element_is_dictionary(self):
        assert isinstance(self.first_post, dict), f"Expected a dictionary, but got {type(self.first_post)}"

    def check_that_elements_are_ordered_by_id(self):
        for expected_id, item in enumerate(self.json_data, start=1):
            check.equal(item.get("id"), expected_id, f"Expected id {expected_id}, but got {item.get('id')}")

    def check_that_returned_single_post(self):
        assert len(self.json_data) == 1, f"Expected a single element, but got {len(self.json_data)}"

    def check_post_id_equal_requested_post(self):
        check.equal(self.requested_post_id, self.returned_post_id ,
                    f"Expected postId to be {self.requested_post_id,}, but got {self.returned_post_id}")

    def check_userid_exists_in_response(self):
        check.is_not_none(self.returned_userId,
                          f"Expected userId to be in the response, but got value: {self.returned_userId}")


    def check_title_exists_in_response(self):
        check.is_not_none(self.returned_title,
                          f"Expected userId to be in the response, but got value: {self.returned_title}")


    def check_body_exists_in_response(self):
        check.is_not_none(self.returned_body,
                          f"Expected userId to be in the response, but got value: {self.returned_body}")

    def verify_comment_data(self):
        for item in self.json_data:
            check.equal(item.get("postId"), self.requested_post_id, f"Expected postId to match the requested post, but got value: {item.get('postId')}")
            check.is_not_none(item.get("id"), "Expected id to not be null")
            check.is_not_none(item.get("email"), "Expected email to not be null")
            check.is_not_none(item.get("body"), "Expected body to not be null")