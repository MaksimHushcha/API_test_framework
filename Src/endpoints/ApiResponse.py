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

    def assert_sorted_by_id(self):
        first_object_id = 0
        for item in self.json_data:
            second_object_id = item.get("id")
            assert second_object_id > first_object_id,\
                f"Expected items to be sorted by id, but {second_object_id} is not higher than {first_object_id}"
            first_object_id = second_object_id
        return self

    def assert_returned_requested_content(self, expected_id, expected_key):
        if type(self.json_data) == list:
            for item in self.json_data:
                assert item.get(expected_key) == expected_id, f"Expected {expected_key} to be returned by id, but got {expected_id} instead"
        if type(self.json_data) == dict:
            assert self.json_data.get(expected_key) == expected_id, f"Expected {expected_key} to be returned by id, but got {expected_id} instead"
        return self

