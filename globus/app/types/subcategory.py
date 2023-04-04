

class Subcategory:

    def __init__(self, data_info: dict, category__id: int = None):
        self.data_info = data_info

        # self.category__id: int = category__id
        self.subcategory_id: int = data_info['id']
        self.name_ = data_info['name']
        self.banner_image: bool = data_info['banner_image']
        self.description: bool = data_info['description']
        self.is_adult: bool = data_info['is_adult']
        self.disclaimer: bool = data_info['disclaimer']
