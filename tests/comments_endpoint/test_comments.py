from faker import Faker
import pytest
fake = Faker()
comments_schema_folder = "comments_schemas"

def test_get_all_comments(comments_endpoints):
    (
        comments_endpoints.get_all_comments()
        .assert_status(200)
        .assert_schema(folder=comments_schema_folder, expected_schema="comments_schema.json")
        .assert_sorted_by_id()
    )

def test_get_comments_by_id(comments_endpoints, generate_random_id):
        email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
        (
        comments_endpoints.get_comments_by_id(generate_random_id)
        .assert_status(200)
        .assert_schema(folder=comments_schema_folder, expected_schema="comment_schema_one_comment.json")
        .assert_returned_key_value(expected_key="id", expected_value=generate_random_id)
        .assert_returned_key_value(expected_key="email", expected_regex=email_regex)
    )

@pytest.mark.xfail(reason="Fake API, designed to fail")
def test_create_a_new_comment(comments_endpoints, generate_a_comment_payload, delete_comment, get_comment):
    response = (
        comments_endpoints.create_a_comment(generate_a_comment_payload)
        .assert_status(201)
        .assert_schema(folder=comments_schema_folder, expected_schema="comment_schema_one_comment.json")
    )
    delete_comment(response.json_data.get("id"))
    response.check_returned_requested_content(response.json_data, generate_a_comment_payload, excluded_key=["id"])

    actual_post_response = get_comment(response.json_data.get("id"))

    # API actually doesn't create comments, so the test will always fail
    assert actual_post_response.json_data == response.json_data, \
        f"Expected to get a new post with requested content {response.json_data}, but got {actual_post_response.json_data}"

@pytest.mark.xfail(reason="Fake API, designed to fail")
def test_put_edit_comment(comments_endpoints, create_and_teardown_the_comment, generate_a_comment_payload, get_comment):
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


@pytest.mark.parametrize("payload",
    [
        ({"email": f"{fake.email()}", "id": 5}),
        ({"body": f"{fake.sentence()}", "id": 5}),
        ({"name": f"{fake.word()}", "id": 5})
    ]
)
def test_patch_edit_comment(comments_endpoints, create_and_teardown_the_comment, payload, get_comment):
    # swapping comment_id to an existing id, because the API doesn't actually support create/delete content
    response = (
        comments_endpoints.put_a_comment(comment_id=5, payload=payload)
        .assert_status(200)
        .assert_schema(folder=comments_schema_folder, expected_schema="comment_schema_one_comment_patch.json")
    )
    assert payload == response.json_data


def test_delete_comment(comments_endpoints, create_a_comment, get_comment):
    response = (
        comments_endpoints.delete_comment(create_a_comment)
        .assert_status(200)
    )
    assert response.json_data == {}
    assert get_comment(create_a_comment).json_data == {}
#test


