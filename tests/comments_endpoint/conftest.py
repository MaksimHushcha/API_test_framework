import pytest
import random
from src.endpoints.CommentsEndpoints import CommentsEndpoints

from faker import Faker
fake = Faker()

@pytest.fixture()
def comments_endpoints():
    return CommentsEndpoints()

def pytest_generate_tests(metafunc):
    if "missing_key_comment_payload" in metafunc.fixturenames:
        scenarios = [
            lambda: {"name": fake.word(), "postId": random.randint(1, 100), "body": fake.sentence()},
            lambda: {"email": fake.email(), "userId": random.randint(1, 100),"body": fake.sentence()},
            lambda: {"name": fake.word(), "email": fake.email(), "body": fake.sentence()},
            lambda: {"name": fake.word(), "userId": random.randint(1, 100), "email": fake.email()}
        ]
        ids = ["missing_email", "missing_name", "missing_postId", "missing_body"]
        metafunc.parametrize("missing_key_comment_payload", scenarios, ids=ids)
    elif "one_key_comment_payload" in metafunc.fixturenames:
        scenarios = [
            lambda: {"name": fake.word()},
            lambda: {"email": fake.email()},
            lambda: {"body": fake.sentence()},
            lambda: {"userId": random.randint(1, 100)}
        ]
        ids = ["only_name_comment_key", "only_email_comment_key", "only_body_comment_key", "only_userID_comment_key"]
        metafunc.parametrize("one_key_comment_payload", scenarios, ids=ids)


@pytest.fixture()
def generate_a_comment_payload(generate_random_id):

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
def schedule_comment_deletion(request, comments_endpoints):
    def _register_deletion(post_id):
        request.addfinalizer(lambda: comments_endpoints.delete_comment(post_id))

    return _register_deletion