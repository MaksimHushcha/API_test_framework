from Src.endpoints.BaseEndpoint import BaseEndpoint

class CommentsEndpoints(BaseEndpoint):
    path = "comments"

    def get_comments_to_the_post(self, post_id, **kwargs):
        return self.get(self.path, params={"postId": post_id}, **kwargs)

