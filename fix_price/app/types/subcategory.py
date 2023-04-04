

class Subcategory:

    def __init__(self, data_info: dict, category__id: int):
        self.data_info = data_info

        self.subcategory_id: int = data_info['id']
        self.category__id: int = category__id
        self.title: str = data_info['title']
        self.adult: bool = data_info['adult']
        self.product_count: int = data_info['productCount']
