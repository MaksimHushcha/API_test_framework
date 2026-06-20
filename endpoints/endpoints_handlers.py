class Endpoint:
    status_code = None
    json_data = None

    def check_response_status_is_200(self):
        assert self.status_code == 200, f"Expected 200, but got: {self.status_code}"

    def check_json_length_is_zero(self):
        assert len(self.json_data) == 0, "Json data is not empty"