import requests
from Src.endpoints.BaseEndpoint import BaseEndpoint

class DeleteEndpoints(BaseEndpoint):
    response = None

    def delete_post(self, url, post_id):
        response = requests.delete(url + f"/{post_id}")
        self.status_code = response.status_code
        self.json_data = response.json()

    def check_response_status_is_204(self):
        assert self.status_code == 204, f"Expected 204, but got: {self.status_code}"