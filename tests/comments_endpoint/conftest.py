import pytest
import random
from Src.endpoints.CommentsEndpoints import CommentsEndpoints
import requests

from faker import Faker


@pytest.fixture()
def comments_endpoints():
    return CommentsEndpoints()

@pytest.fixture()
def generate_a_comment_payload(generate_random_id):

    fake = Faker()
    return {
        'name': fake.word(),
        'email': fake.email(),
        'body': fake.sentence(),
        'postId': generate_random_id,
        }

@pytest.fixture
def create_and_teardown_the_comment(comments_endpoints, generate_a_comment_payload, request):
    response = comments_endpoints.create_a_comment(generate_a_comment_payload)
    created_comment_id = response.json_data.get('id')

    request.addfinalizer(lambda: comments_endpoints.delete_comment(created_comment_id))
    # we return post id
    return created_comment_id

@pytest.fixture
def create_a_comment(comments_endpoints, generate_a_comment_payload, request,):
    response = comments_endpoints.create_a_comment(generate_a_comment_payload)
    created_post_id = response.json_data.get('id')
    return created_post_id


@pytest.fixture
def get_comment(comments_endpoints):

    def _get_comment(comment_id):
        return comments_endpoints.get_comments_by_id(comment_id)
    return _get_comment

@pytest.fixture
def delete_comment(request, comments_endpoints):
    def _register_deletion(post_id):
        request.addfinalizer(lambda: comments_endpoints.delete_comment(post_id))

    return _register_deletion