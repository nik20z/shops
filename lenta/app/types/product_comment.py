

class ProductComment:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "id": 'id_',
            "userName": 'user_name',
            "text": 'text_',
            "rating": 'rating',
            "createdDate": 'created_date',
            "upvote": 'upvote',
            "downvote": 'downvote',
            "ratedByUser": 'rated_by_user',
            "parentId": 'parent_id',
            "replies": 'replies',
        }

        self.product_id: int

        self.id_: int = data_info['id']
        self.user_name: str = data_info['userName']
        self.text_: str = data_info['text']
        self.rating: int = data_info['rating']
        self.created_date: str = data_info['createdDate']
        self.upvote: int = data_info['upvote']
        self.downvote: int = data_info['downvote']
        self.rated_by_user: int = data_info['ratedByUser']
        self.parent_id: int = data_info['parentId']
        self.replies: list = data_info['replies']
