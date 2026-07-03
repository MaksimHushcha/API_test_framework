import pytest
import random
from Src.endpoints.PostsEndpoints import PostsEndpoints
from Src.endpoints.CommentsEndpoints import CommentsEndpoints
import requests

from faker import Faker


@pytest.fixture()
def posts_endpoints():
    return PostsEndpoints()

@pytest.fixture()
def comments_endpoints():
    return CommentsEndpoints()

@pytest.fixture()
def generate_random_id():
    return random.randint(1, 100)

@pytest.fixture()
def generate_a_post_payload(generate_random_id):

    fake = Faker()
    return {
        'title': fake.word(),
        'body': fake.sentence(),
        'userId': generate_random_id,
        }

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
def create_and_teardown_the_post(posts_endpoints, generate_a_post_payload, request):
    response = posts_endpoints.create_a_post(generate_a_post_payload)
    created_post_id = response.json_data.get('id')

    request.addfinalizer(lambda: posts_endpoints.delete_post(created_post_id))
    # we return post id
    return created_post_id

@pytest.fixture
def create_a_post(posts_endpoints, generate_a_post_payload, request,):
    response = posts_endpoints.create_a_post(generate_a_post_payload)
    created_post_id = response.json_data.get('id')
    return created_post_id

@pytest.fixture
def get_post(posts_endpoints):

    def _get_post(post_id):
        return posts_endpoints.get_posts_by_id(post_id)
    return _get_post

@pytest.fixture
def get_comment(comments_endpoints):

    def _get_comment(comment_id):
        return comments_endpoints.get_comments_by_id(comment_id)
    return _get_comment

@pytest.fixture
def delete_post(request, posts_endpoints):

    def _register_deletion(post_id):
        request.addfinalizer(lambda: posts_endpoints.delete_post(post_id))

    return _register_deletion

@pytest.fixture
def delete_comment(request, comments_endpoints):
    def _register_deletion(post_id):
        request.addfinalizer(lambda: comments_endpoints.delete_comment(post_id))

    return _register_deletion