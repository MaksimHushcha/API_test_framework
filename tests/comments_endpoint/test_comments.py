import random
import allure
from faker import Faker
import pytest
fake = Faker()
comments_schema_folder = "comments_schemas"


@allure.epic("API Test Framework>")
@allure.feature("Comments Endpoint")
@allure.story("Get Comments")
@allure.severity(allure.severity_level.CRITICAL)
class TestGetMethodComments:
    @allure.tag("Positive")
    def test_get_all_comments(self, comments_endpoints):
        (
            comments_endpoints.get_all_comments()
            .assert_status(200)
            .assert_schema(folder=comments_schema_folder, expected_schema="comments_schema.json")
            .assert_sorted_by_id()
        )
    @allure.tag("Positive")
    def test_get_comments_by_id(self, comments_endpoints, generate_random_id):
            email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
            (
            comments_endpoints.get_comments_by_id(generate_random_id)
            .assert_status(200)
            .assert_schema(folder=comments_schema_folder, expected_schema="comment_schema_one_comment.json")
            .assert_returned_key_value(expected_key="id", expected_value=generate_random_id)
            .assert_returned_key_value(expected_key="email", expected_regex=email_regex)
        )

    @allure.tag("Negative")
    def test_get_comment_by_invalid_id(self, comments_endpoints):
            response = (
            comments_endpoints.get_comments_by_id(fake.word())
            .assert_status(404)
            )
            assert response.json_data == {}

@allure.epic("API Test Framework>")
@allure.feature("Comments Endpoint")
@allure.story("Post Comments")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.xfail(reason="Fake API, designed to fail if run 'normally'")
class TestPostMethodComments:
    @allure.tag("Positive")
    def test_create_a_new_comment(self, comments_endpoints, generate_a_comment_payload, schedule_comment_deletion, get_comment):
        response = (
            comments_endpoints.create_a_comment(generate_a_comment_payload)
            .assert_status(201)
            .assert_schema(folder=comments_schema_folder, expected_schema="comment_schema_one_comment.json")
        )
        schedule_comment_deletion(response.json_data.get("id"))
        response.check_returned_requested_content(response.json_data, generate_a_comment_payload, excluded_key=["id"])
        actual_post_response = get_comment(response.json_data.get("id"))
        assert actual_post_response.json_data == response.json_data, \
            f"Expected to get a new post with requested content {response.json_data}, but got {actual_post_response.json_data}"

    @allure.tag("Negative")
    def test_create_a_new_comment_with_missing_keys(self, comments_endpoints, schedule_comment_deletion, get_comment, missing_key_comment_payload):
        payload = missing_key_comment_payload()
        response = (
            comments_endpoints.create_a_comment(payload)
            .assert_status(201)
        )
        schedule_comment_deletion(response.json_data.get("id"))
        response.check_returned_requested_content(received_key_value_dict=response.json_data, expected_key_value_dict=payload, excluded_key=["id"])
        actual_comment_response = get_comment(response.json_data.get("id"))
        assert actual_comment_response.json_data == response.json_data, \
            f"Expected to get a new post with requested content {response.json_data}, but got {actual_comment_response.json_data}"

@allure.epic("API Test Framework>")
@allure.feature("Comments Endpoint")
@allure.story("Edit Comments")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.xfail(reason="Fake API, designed to fail")
class TestPutMethodComments:
    @allure.tag("Positive")
    def test_put_edit_comment(self, comments_endpoints, create_and_teardown_the_comment, generate_a_comment_payload, get_comment):
            # swapping comment_id to an existing id, because the API doesn't actually support create/delete content
            response = (
                comments_endpoints.put_a_comment(comment_id=5, payload=generate_a_comment_payload)
                .assert_status(200)
                .assert_schema(folder=comments_schema_folder, expected_schema="comment_schema_one_comment.json")
            )
            response.check_returned_requested_content(response.json_data, generate_a_comment_payload, excluded_key=["id"])
            # this is designed to fail
            modified_comment_response = get_comment(response.json_data.get("id"))

            assert modified_comment_response.json_data == response.json_data, \
                f"Expected to get a new comment with requested content {response.json_data}, but got {modified_comment_response.json_data}"

    @allure.tag("Negative")
    def test_put_edit_comment_with_an_invalid_id(self, comments_endpoints, create_and_teardown_the_comment, generate_a_comment_payload,
                              get_comment):
        response = (
            comments_endpoints.put_a_comment(comment_id=fake.word(), payload=generate_a_comment_payload)
            .assert_status(500)
        )
        assert response.json_data is None

@allure.epic("API Test Framework>")
@allure.feature("Comments Endpoint")
@allure.story("Edit Comments")
@allure.severity(allure.severity_level.NORMAL)
class TestPatchMethodComments:
    @pytest.mark.xfail(reason="Fake API, designed to fail")
    @allure.tag("Positive")
    def test_patch_edit_comment(self, comments_endpoints, create_and_teardown_the_comment, get_comment, missing_key_comment_payload):
        payload = missing_key_comment_payload()
        response = (
            comments_endpoints.put_a_comment(comment_id=create_and_teardown_the_comment, payload=payload)
            .assert_status(200)
            .assert_schema(folder=comments_schema_folder, expected_schema="comment_schema_one_comment_patch.json")
        )
        assert payload == response.json_data

    @allure.tag("Negative")
    def test_patch_edit_comment_by_invalid_id(self, comments_endpoints, generate_a_comment_payload):
        response = (
            comments_endpoints.put_a_comment(comment_id=fake.word(), payload=generate_a_comment_payload)
            .assert_status(500)
        )
        assert response.json_data is None

@allure.epic("API Test Framework>")
@allure.feature("Comments Endpoint")
@allure.story("Delete Comments")
@allure.severity(allure.severity_level.NORMAL)
class TestDeleteMethodComments:
    @allure.tag("Positive")
    def test_delete_comment(self, comments_endpoints, create_a_comment, get_comment):
        response = (
            comments_endpoints.delete_comment(create_a_comment)
            .assert_status(200)
        )
        assert response.json_data == {}
        assert get_comment(create_a_comment).json_data == {}

    @allure.tag("Negative")
    def test_delete_comment_invalid_id(self, comments_endpoints):
        response = (
            comments_endpoints.delete_comment(fake.word())
            .assert_status(200)
        )
        assert response.json_data == {}

    @allure.tag("Negative")
    def test_delete_post_with_non_existing_id(self, comments_endpoints):
        response = (
            comments_endpoints.delete_comment(random.randint(100000, 2147483647))
            .assert_status(200)
        )
        assert response.json_data == {}


