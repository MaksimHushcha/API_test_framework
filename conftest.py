import pytest
import random

@pytest.fixture()
def generate_random_id():
    return random.randint(1, 100)
