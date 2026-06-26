import os
import requests
from dotenv import load_dotenv
from Src.endpoints.ApiResponse import ApiResponse

load_dotenv()

class BaseEndpoint:

    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('API_TOKEN')}"
        })

    def _request(self, method, endpoint, **kwargs):
        full_url = f"{self.base_url}{endpoint}"
        response = self.session.request(method, full_url, **kwargs)
        return ApiResponse(response)

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)
    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)
    def put(self, endpoint, **kwargs):
        return self._request("PUT", endpoint, **kwargs)
    def patch(self, endpoint, **kwargs):
        return self._request("PATCH", endpoint, **kwargs)
    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)
