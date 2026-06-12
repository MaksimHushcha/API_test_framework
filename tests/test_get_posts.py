import requests
import pytest_check as check

base_url = "https://jsonplaceholder.typicode.com/posts"

def test_get_posts():
    response = requests.get(base_url)
    assert response.status_code == 200, f"Expected 200, but got: {response.status_code}"

    json_data = response.json()

    assert isinstance(json_data, list), f"Response is not a list, but {type(json_data)}"
    assert len(json_data) > 0, "Json data is empty"

    first_post = json_data[0]
    assert isinstance(first_post, dict), f"Expected a dictionary, but got {type(first_post)} "

    for expected_id, item in enumerate(json_data, start=1):
        check.equal(item.get("id"), expected_id, f"Expected id {expected_id}")