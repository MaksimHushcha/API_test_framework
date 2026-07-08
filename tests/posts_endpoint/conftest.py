import pytest
import random
from Src.endpoints.PostsEndpoints import PostsEndpoints
from Src.endpoints.CommentsEndpoints import CommentsEndpoints
import requests

from faker import Faker
fake = Faker()

def pytest_generate_tests(metafunc):
    if "missing_key_payload" in metafunc.fixturenames:
        scenarios = [
            lambda: {"body": fake.sentence(), "userId": random.randint(1, 100)},
            lambda: {"title": fake.word(), "userId": random.randint(1, 100)},
            lambda: {"title": fake.word(), "body": fake.sentence()}
        ]
        ids = ["missing_title", "missing_body", "missing_userId"]

        metafunc.parametrize("missing_key_payload", scenarios, ids=ids)

    elif "one_key_payload" in metafunc.fixturenames:
        scenarios = [
            lambda: {"body": fake.sentence()},
            lambda: {"userId": random.randint(1, 100)},
            lambda: {"title": fake.word()}
        ]
        ids = ["body_only_payload", "userId_only_payload", "title_only_payload"]

        metafunc.parametrize("one_key_payload", scenarios, ids=ids)

@pytest.fixture()
def posts_endpoints():
    return PostsEndpoints()

@pytest.fixture()
def generate_a_post_payload(generate_random_id):

    return {
        'title': fake.word(),
        'body': fake.sentence(),
        'userId': generate_random_id,
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
def schedule_post_deletion(request, posts_endpoints):

    def _register_deletion(post_id):
        request.addfinalizer(lambda: posts_endpoints.delete_post(post_id))

    return _register_deletion