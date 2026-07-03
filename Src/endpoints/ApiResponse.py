import json
from typing import Any
from pathlib import Path
from jsonschema import validate, ValidationError
from pytest_check import check
import re

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

    def assert_sorted_by_id(self):
        first_object_id = 0
        assert isinstance(self.json_data, (list, dict)), f"Expected list or dict, got {type(self.json_data)}"
        for item in self.json_data:
            second_object_id = item.get("id")
            assert second_object_id > first_object_id,\
                f"Expected items to be sorted by id, but {second_object_id} is not higher than {first_object_id}"
            first_object_id = second_object_id
        return self

    def assert_returned_key_value(self, expected_key, expected_value = None, expected_regex = None):
        if (expected_value is not None) == (expected_regex is not None):
             raise AssertionError("You must provide exactly one validation method: either expected_value OR expected_regex.")
        assert isinstance(self.json_data, (list, dict)), f"Expected list or dict, got {type(self.json_data)}"

        items = self.json_data if isinstance(self.json_data, list) else [self.json_data]
        regex = re.compile(expected_regex) if expected_regex is not None else None

        for item in items:
            actual_value = item.get(expected_key)
            with check:
                if expected_value is not None:
                    assert actual_value == expected_value, \
                        f"Expected '{expected_value}' in '{expected_key}', but got '{actual_value}' instead."

                if regex is not None:
                    is_match = actual_value is not None and regex.match(str(actual_value))
                    assert is_match, \
                        f"Expected value in '{expected_key}' to match regex '{expected_regex}', but got '{actual_value}' instead."
        return self

    def check_returned_requested_content(self, received_key_value_dict, expected_key_value_dict, excluded_key=None):
        try:
            with check:
                for key in received_key_value_dict:
                    if key in excluded_key:
                        continue
                    with check:
                        assert received_key_value_dict.get(key) == expected_key_value_dict.get(key), \
                        f"Expected key: {key} to have value {expected_key_value_dict.get(key)}, but got {received_key_value_dict.get(key)}"
        except AssertionError:
            raise f"Response didn't return an iterable object {received_key_value_dict}"
        return self

