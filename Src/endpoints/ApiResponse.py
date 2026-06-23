class ApiResponse:
    def __init__(self, response):
        self.raw_response = response
        self.status_code = response.status_code

        try:
            self.json_data = response.json()
        except ValueError:
            self.json_data = None

    def assert_status(self, expected_code):
        assert self.status_code == expected_code, \
            f" Expected status {expected_code}.but got {self.status_code}. Response: {self.raw_response}"
        return self