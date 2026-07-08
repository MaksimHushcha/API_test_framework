from src.core.BaseEndpoint import BaseEndpoint

class PostsEndpoints(BaseEndpoint):
    path = "posts"

    def get_all_posts(self, **kwargs):
        return self.get(self.path, **kwargs)

    def get_posts_by_id(self, post_id, **kwargs):
        return self.get(f"{self.path}/{post_id}", **kwargs)

    def get_comments_by_post_id(self, post_id, **kwargs):
        return self.get(f"{self.path}/{post_id}/comments", **kwargs)

    def delete_post(self, post_id, **kwargs):
        return self.delete(self.path + f"/{post_id}", **kwargs)

    def create_a_post(self, payload, **kwargs):
        return self.post(self.path, json=payload, headers = {"Content-Type": "application/json; charset=UTF-8"}, **kwargs)

    def put_a_post(self, post_id, payload, **kwargs):
        return self.put(f"{self.path}/{post_id}", json=payload, **kwargs)

    def patch_a_post(self, post_id, payload, **kwargs):
        return self.patch(f"{self.path}/{post_id}", json=payload, **kwargs)
