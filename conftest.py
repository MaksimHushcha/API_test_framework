import pytest
import random
from endpoints.get_json_placeholder_endpoints import GetEndpoints
from endpoints.delete_json_placeholder_endpoints import DeleteEndpoints
from endpoints.post_json_placeholder_endpoints import PostEndpoints

from faker import Faker


@pytest.fixture()
def get_endpoints():
    return GetEndpoints()

@pytest.fixture()
def post_endpoints():
    return PostEndpoints()

@pytest.fixture()
def delete_endpoints():
    return DeleteEndpoints()

@pytest.fixture()
def generate_random_id():
    return random.randint(1, 100)

@pytest.fixture
def create_post(post_endpoints, generate_random_id):
    base_url = "https://jsonplaceholder.typicode.com/posts"
    fake = Faker()
    title = fake.word()
    body = fake.sentence()
    userId = generate_random_id
    data = {'title': title,'body': body, 'userId': userId}
    post_endpoints.create_a_post(base_url, data)
    return post_endpoints.created_post_id

@pytest.fixture
def delete_post(delete_endpoints):

    def _delete_post(url, post_id):
        delete_endpoints.delete_post(url, post_id)
    yield _delete_post
