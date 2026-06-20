from faker import Faker

fake = Faker()

base_url = "https://jsonplaceholder.typicode.com/posts"

def test_get_posts(get_endpoints):
    get_endpoints.get_all_posts(base_url)
    get_endpoints.check_response_status_is_200()
    get_endpoints.check_data_is_a_list()
    get_endpoints.check_json_length_is_not_zero()
    get_endpoints.check_first_element_is_dictionary()
    get_endpoints.check_that_elements_are_ordered_by_id()

def test_get_post_by_id(get_endpoints, generate_random_id):
    random_post_id = generate_random_id

    get_endpoints.get_posts_by_id(base_url, random_post_id)
    get_endpoints.check_response_status_is_200()
    get_endpoints.check_that_returned_single_post()
    get_endpoints.check_post_id_equal_requested_post()
    get_endpoints.check_userid_exists_in_response()
    get_endpoints.check_title_exists_in_response()
    get_endpoints.check_body_exists_in_response()

def test_get_comments_to_the_post(get_endpoints, generate_random_id):
    random_post_id = generate_random_id

    get_endpoints.get_comments_to_the_post(base_url, random_post_id)
    get_endpoints.check_response_status_is_200()
    get_endpoints.check_json_length_is_not_zero()
    get_endpoints.verify_comment_data()

def test_create_a_post(post_endpoints, generate_random_id, delete_post):
    title = fake.word()
    body = fake.sentence()
    userId = generate_random_id
    data = {'title': title,'body': body, 'userId': userId}

    post_endpoints.create_a_post(base_url, data)
    post_endpoints.check_response_status_is_201()
    post_endpoints.check_json_length_is_not_zero()
    post_endpoints.check_returned_userid_is_created_userid()
    post_endpoints.check_returned_title_is_created_title()
    post_endpoints.check_returned_body_is_created_body()
    delete_post(base_url, post_endpoints.created_post_id)

def test_delete_post(delete_endpoints, get_endpoints, create_post):
    delete_endpoints.delete_post(base_url, create_post)
    # deleted resourced return {} with status 200
    delete_endpoints.check_response_status_is_200()
    get_endpoints.get_posts_by_id(base_url, create_post)
    get_endpoints.check_json_length_is_zero()


