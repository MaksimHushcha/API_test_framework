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
        .assert_returned_requested_content(generate_random_id, "id")
    )

def test_get_comments_to_the_post(comments_endpoints, generate_random_id):
    (
        comments_endpoints.get_comments_to_the_post(generate_random_id)
        .assert_status(200)
        .assert_schema("comments_schema.json")
        .assert_returned_requested_content(generate_random_id, "postId")
        .assert_sorted_by_id()
    )

def test_create_a_new_post(posts_endpoints, generate_a_payload, delete_post):
    response = (
        posts_endpoints.create_a_post(generate_a_payload)
        .assert_status(201)
        .assert_schema("posts_schema_one_post.json")
    )
    delete_post(response.json_data.get("id"))
    
    with check:
        assert response.json_data.get("userId") == generate_a_payload.get("userId"), \
            f"Invalid post id returned: Expected {generate_a_payload.get('userId')}, but got {response.json_data.get('userId')}"
        assert response.json_data.get("title") == generate_a_payload.get("title"), \
            f"Invalid post title returned: Expected {generate_a_payload.get('title')}, but got {response.json_data.get('title')}"
        assert response.json_data.get("body") == generate_a_payload.get("body"), \
          f"Invalid post title returned: Expected {generate_a_payload.get('body')}, but got {response.json_data.get('body')}"




# def test_delete_post(delete_endpoints, get_endpoints, create_post):
#     delete_endpoints.delete_post(base_url, create_post)
#     # deleted resourced return {} with status 200
#     delete_endpoints.check_response_status_is_200()
#     get_endpoints.get_posts_by_id(base_url, create_post)
#     get_endpoints.check_json_length_is_zero()


