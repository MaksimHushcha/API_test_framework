from faker import Faker
import pytest
import random

fake = Faker()
posts_schema_folder = "posts_schemas"

class TestGetMethodPostsTests:
    def test_get_posts(self, posts_endpoints):
        (
        posts_endpoints.get_all_posts()
                .assert_status(200)
                .assert_schema(folder=posts_schema_folder, expected_schema="posts_schema_all.json")
                .assert_sorted_by_id()
        )

    def test_get_post_by_id(self, posts_endpoints, generate_random_id):
        (
            posts_endpoints.get_posts_by_id(generate_random_id)
            .assert_status(200)
            .assert_schema(folder=posts_schema_folder, expected_schema="posts_schema_one_post.json")
            .assert_returned_key_value(expected_key="id", expected_value=generate_random_id)
        )

    def test_get_post_with_invalid_id(self, posts_endpoints):
        response = (
            posts_endpoints.get_posts_by_id(fake.word())
            .assert_status(404)
        )
        assert response.json_data == {}


    def test_get_post_with_non_existent_id(self, posts_endpoints):
        response = (
            posts_endpoints.get_posts_by_id(random.randint(100000, 2147483647))
            .assert_status(404)
        )
        assert response.json_data == {}

class TestGetCommentsToPostTests:
    comments_schemas = "comments_schemas"
    def test_get_comments_to_the_post(self, posts_endpoints, generate_random_id):
        (
            posts_endpoints.get_comments_by_post_id(generate_random_id)
            .assert_status(200)
            .assert_schema(folder=self.comments_schemas, expected_schema="comments_schema.json")
            .assert_returned_key_value(expected_key="postId", expected_value=generate_random_id)
            .assert_sorted_by_id()
        )

    def test_get_comments_to_the_post_with_invalid_id(self, posts_endpoints):
        response = (
            posts_endpoints.get_comments_by_post_id(fake.word())
            .assert_status(200)
        )
        assert response.json_data == []

    def test_get_comments_to_the_post_with_non_existing_id(self, posts_endpoints):
        response = (
            posts_endpoints.get_comments_by_post_id(random.randint(100000, 2147483647))
            .assert_status(200)
        )
        assert response.json_data == []

@pytest.mark.xfail(reason="Fake API, designed to fail")
class TestPostMethodPostsTests:

    def test_create_a_new_post(self, posts_endpoints, generate_a_post_payload, schedule_post_deletion, get_post):
        response = (
            posts_endpoints.create_a_post(generate_a_post_payload)
            .assert_status(201)
            .assert_schema(folder=posts_schema_folder, expected_schema="posts_schema_one_post.json")
        )
        schedule_post_deletion(response.json_data.get("id"))
        response.check_returned_requested_content(response.json_data, generate_a_post_payload, excluded_key=["id"])
        actual_post_response = get_post(response.json_data.get("id"))

        assert actual_post_response.json_data == response.json_data, \
            f"Expected to get a new post with requested content {response.json_data}, but got {actual_post_response.json_data}"

    def test_create_a_new_post_with_missing_keys(self, posts_endpoints, schedule_post_deletion, get_post, missing_key_payload):
        payload = missing_key_payload()
        response = (
            posts_endpoints.create_a_post(payload=payload)
            .assert_status(201)
        )
        schedule_post_deletion(response.json_data.get("id"))
        response.check_returned_requested_content(received_key_value_dict=response.json_data, expected_key_value_dict=payload, excluded_key=["id"])
        actual_post_response = get_post(response.json_data.get("id"))

        assert actual_post_response.json_data == response.json_data, \
            f"Expected to get a new post with requested content {response.json_data}, but got {actual_post_response.json_data}"

class TestPutMethodPost:
    @pytest.mark.xfail(reason="Fake API, designed to fail, we are modifying non-existing ID, endpoint returns 500")
    def test_replace_a_post(self, posts_endpoints, create_and_teardown_the_post, generate_a_post_payload, get_post):
        response = (
            posts_endpoints.put_a_post(post_id=create_and_teardown_the_post, payload=generate_a_post_payload)
            .assert_status(200)
            .assert_schema(folder=posts_schema_folder, expected_schema="posts_schema_one_post.json")
        )
        response.check_returned_requested_content( response.json_data, generate_a_post_payload, excluded_key=["id"])
        modified_post_get_response = get_post(response.json_data.get("id"))
        assert modified_post_get_response.json_data == response.json_data, \
            f"Expected to get a new post with requested content {response.json_data}, but got {modified_post_get_response.json_data}"

    def test_replace_a_post_by_invalid_id(self, posts_endpoints, generate_a_post_payload, get_post):
        response = (
            posts_endpoints.put_a_post(post_id=fake.word(), payload=generate_a_post_payload)
            .assert_status(500)
        )
        assert response.json_data is None

class TestPatchMethodPostTests:
    def test_patch_a_post(self, posts_endpoints, create_and_teardown_the_post, get_post, one_key_payload):
        payload = one_key_payload()
        response = (
            posts_endpoints.patch_a_post(post_id=create_and_teardown_the_post, payload=payload)
            .assert_status(200)
            .assert_schema(folder=posts_schema_folder, expected_schema="posts_schema_one_post_patch.json")
        )
        assert payload == response.json_data

    def test_patch_a_post_by_invalid_id(self, posts_endpoints, generate_a_post_payload, get_post):
        response = (
            posts_endpoints.patch_a_post(post_id=fake.word(), payload=generate_a_post_payload)
            .assert_status(200)
        )
        assert response.json_data == generate_a_post_payload

class TestDeleteMethodPostTests:
    def test_delete_post(self, posts_endpoints, create_a_post, get_post):
        response = (
            posts_endpoints.delete_post(create_a_post)
            .assert_status(200)
        )
        assert response.json_data == {}
        assert get_post(create_a_post).json_data == {}

    def test_delete_post_with_invalid_id(self, posts_endpoints):
        response = (
            posts_endpoints.delete_post(fake.word())
            .assert_status(200)
        )
        assert response.json_data == {}

    def test_delete_post_with_non_existing_id(self, posts_endpoints):
        response = (
            posts_endpoints.delete_post(random.randint(100000, 2147483647))
            .assert_status(200)
        )
        assert response.json_data == {}