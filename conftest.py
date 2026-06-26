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
    return CommentsEndpoints

@pytest.fixture()
def generate_random_id():
    return random.randint(1, 100)

@pytest.fixture
def create_post(post_endpoints, generate_random_id):
    fake = Faker()
    title = fake.word()
    body = fake.sentence()
    userId = generate_random_id
    data = {'title': title,'body': body, 'userId': userId}
    post_endpoints.create_a_post(data)
    return post_endpoints.created_post_id

@pytest.fixture
def delete_post(delete_endpoints):

    def _delete_post(url, post_id):
        delete_endpoints.delete_post(url, post_id)
    yield _delete_post
