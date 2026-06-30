import pytest
import random
from Src.endpoints.PostsEndpoints import PostsEndpoints
from Src.endpoints.CommentsEndpoints import CommentsEndpoints

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
def generate_a_payload(generate_random_id):
    fake = Faker()
    title = fake.word()
    body = fake.sentence()
    userId = generate_random_id
    data = {'title': title,'body': body, 'userId': userId}
    return data

@pytest.fixture
def create_post(posts_endpoints, generate_a_payload):
    posts_endpoints.create_a_post(generate_a_payload)
    return posts_endpoints.created_post_id

@pytest.fixture
def delete_post(posts_endpoints):
    post_id_to_delete = None

    def _register_deletion(post_id):
        nonlocal post_id_to_delete
        post_id_to_delete = post_id

    yield _register_deletion

    if post_id_to_delete:
        posts_endpoints.delete_post(post_id_to_delete)
