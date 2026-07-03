from Src.endpoints.BaseEndpoint import BaseEndpoint

class CommentsEndpoints(BaseEndpoint):
    path = "comments"

    def get_all_comments(self, **kwargs):
        return self.get(self.path, **kwargs)

    def get_comments_by_id(self, comment_id, **kwargs):
        return self.get(f"{self.path}/{comment_id}", **kwargs)

    def delete_comment(self, comment_id, **kwargs):
        return self.delete(self.path + f"/{comment_id}", **kwargs)

    def create_a_comment(self, payload, **kwargs):
        return self.post(self.path, json=payload, headers = {"Content-Type": "application/json; charset=UTF-8"}, **kwargs)

    def put_a_comment(self, comment_id, payload, **kwargs):
        return self.put(f"{self.path}/{comment_id}", json=payload, **kwargs)

    def patch_a_comment(self, comment_id, payload, **kwargs):
        return self.patch(f"{self.path}/{comment_id}", json=payload, **kwargs)