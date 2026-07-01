from faker import Faker
from pytest_check import check

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
        .assert_returned_requested_key(generate_random_id, "id")
    )

def test_get_comments_to_the_post(comments_endpoints, generate_random_id):
    response = (
        comments_endpoints.get_comments_to_the_post(generate_random_id)
        .assert_status(200)
        .assert_schema("comments_schema.json")
        .assert_returned_requested_key(generate_random_id, "postId")
        .assert_sorted_by_id()
    )

def test_create_a_new_post(posts_endpoints, generate_a_post_payload, delete_post):
    response = (
        posts_endpoints.create_a_post(generate_a_post_payload)
        .assert_status(201)
        .assert_schema("posts_schema_one_post.json")
    )
    delete_post(response.json_data.get("id"))
    response.check_returned_requested_content(generate_a_post_payload, response.json_data, excluded_key=["id"])

def test_replace_a_post(posts_endpoints, create_post_and_get_its_id, generate_a_post_payload, delete_post):
# test api doesn't actually "saves" new posts, thus a hardcoded post_id = 1 is used.
    response = (
        posts_endpoints.put_a_post(post_id=1, payload=generate_a_post_payload)
        .assert_status(200)
        .assert_schema("posts_schema_one_post.json")
    )
    delete_post(create_post_and_get_its_id)
    response.check_returned_requested_content(generate_a_post_payload, response.json_data, excluded_key=["id"])
    # this is designed to fail
    assert response.json_data.get("id") == create_post_and_get_its_id


# def test_delete_post(delete_endpoints, get_endpoints, create_post):
#     delete_endpoints.delete_post(base_url, create_post)
#     # deleted resourced return {} with status 200
#     delete_endpoints.check_response_status_is_200()
#     get_endpoints.get_posts_by_id(base_url, create_post)
#     get_endpoints.check_json_length_is_zero()


