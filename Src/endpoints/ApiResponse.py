import json
from typing import Any
from pathlib import Path
from jsonschema import validate, ValidationError

class ApiResponse:
    def __init__(self, response):
        self.raw_response = response
        self.status_code = response.status_code
        self.json_data: dict[str, Any] | list[Any] | None = None
        try:
            self.json_data = response.json()
        except ValueError:
            self.json_data = None

    def assert_status(self, expected_code):
        assert self.status_code == int(expected_code), \
            f" Expected status {expected_code}.but got {self.status_code}. Response body: {self.raw_response.text}"
        return self

    def assert_schema(self, expected_schema):
        if self.json_data is None:
            raise AssertionError("Response returned empty data")
        base_path = Path(__file__).resolve().parents[2]
        schema_path = base_path / "Test_data" / "Schemas" / expected_schema
        try:
            with open(schema_path, "r") as schema_file:
                loaded_schema = json.load(schema_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Schema not found at {schema_path}")
        except json.JSONDecodeError:
            raise ValueError(f"The schema file at {schema_path} is not valid JSON.")
        try:
            validate(instance=self.json_data, schema=loaded_schema)
        except ValidationError as err:
            raise AssertionError(
                f"JSON data does not match the expected schema '{expected_schema}'. Error: {err.message}")
        return self

    # def check_that_elements_are_ordered_by_id(self):
    #     for expected_id, item in enumerate(self.json_data, start=1):
    #         check.equal(item.get("id"), expected_id, f"Expected id {expected_id}, but got {item.get('id')}")
    #
    # def check_that_returned_single_post(self):
    #     assert len(self.json_data) == 1, f"Expected a single element, but got {len(self.json_data)}"
    #
    # def check_post_id_equal_requested_post(self):
    #     check.equal(self.requested_post_id, self.returned_post_id ,
    #                 f"Expected postId to be {self.requested_post_id,}, but got {self.returned_post_id}")
    #
    # def check_userid_exists_in_response(self):
    #     check.is_not_none(self.returned_userId,
    #                       f"Expected userId to be in the response, but got value: {self.returned_userId}")
    #
    #
    # def check_title_exists_in_response(self):
    #     check.is_not_none(self.returned_title,
    #                       f"Expected userId to be in the response, but got value: {self.returned_title}")
    #
    #
    # def check_body_exists_in_response(self):
    #     check.is_not_none(self.returned_body,
    #                       f"Expected userId to be in the response, but got value: {self.returned_body}")
    #
    # def verify_comment_data(self):
    #     for item in self.json_data:
    #         check.equal(item.get("postId"), self.requested_post_id, f"Expected postId to match the requested post, but got value: {item.get('postId')}")
    #         check.is_not_none(item.get("id"), "Expected id to not be null")
    #         check.is_not_none(item.get("email"), "Expected email to not be null")
    #         check.is_not_none(item.get("body"), "Expected body to not be null")