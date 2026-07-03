from faker import Faker
import pytest
import random
import json

fake = Faker()
def test_get_posts(posts_endpoints):
    (
    posts_endpoints.get_all_posts()
            .assert_status(200)
            .assert_schema("posts_schema_all.json")
            .assert_sorted_by_id()
    )

def test_get_post_by_id(posts_endpoints, generate_random_id):
    (
        posts_endpoints.get_posts_by_id(generate_random_id)
        .assert_status(200)
        .assert_schema("posts_schema_one_post.json")
        .assert_returned_key_value(expected_key="id", expected_value=generate_random_id)
    )

def test_get_comments_to_the_post(comments_endpoints, generate_random_id):
    (
        comments_endpoints.get_comments_to_the_post(generate_random_id)
        .assert_status(200)
        .assert_schema("comments_schema.json")
        .assert_returned_key_value(expected_key="postId", expected_value=generate_random_id)
        .assert_sorted_by_id()
    )

def test_create_a_new_post(posts_endpoints, generate_a_post_payload, delete_post, get_post):
    response = (
        posts_endpoints.create_a_post(generate_a_post_payload)
        .assert_status(201)
        .assert_schema("posts_schema_one_post.json")
    )
    delete_post(response.json_data.get("id"))
    response.check_returned_requested_content(response.json_data, generate_a_post_payload, excluded_key=["id"])

    actual_post_response = get_post(response.json_data.get("id"))

    # API actually doesn't create posts, so the test will always fail
    assert actual_post_response.json_data == response.json_data, \
        f"Expected to get a new post with requested content {response.json_data}, but got {actual_post_response.json_data}"


def test_replace_a_post(posts_endpoints, create_and_teardown_the_post, generate_a_post_payload, get_post):
    # we can swap userID while modifying the post
    response = (
        posts_endpoints.put_a_post(post_id=create_and_teardown_the_post, payload=generate_a_post_payload)
        .assert_status(200)
        .assert_schema("posts_schema_one_post.json")
    )
    response.check_returned_requested_content( response.json_data, generate_a_post_payload, excluded_key=["id"])

    # this is designed to fail
    modified_post_get_response = get_post(response.json_data.get("id"))

    assert modified_post_get_response.json_data == response.json_data, \
        f"Expected to get a new post with requested content {response.json_data}, but got {modified_post_get_response.json_data}"

@pytest.mark.parametrize("payload",
    [
        ({"title": "alice"}),
        ({"body": "bob"}),
        ({"userid": "123"}),
    ]
)
def test_patch_a_post(posts_endpoints, create_and_teardown_the_post, get_post, payload):
    response = (
        posts_endpoints.patch_a_post(post_id=create_and_teardown_the_post, payload=payload)
        .assert_status(200)
        .assert_schema("posts_schema_one_post_patch.json")
    )
    print(response.json_data)
    # assert response.json_data == payload, f"Expected to get a new post with requested content {payload}, but got {response.json_data}"

def test_delete_post(posts_endpoints, create_a_post, get_post):
    response = (
        posts_endpoints.delete_post(create_a_post)
        .assert_status(200)
    )
    assert response.json_data == {}
    assert get_post(create_a_post).json_data == {}



