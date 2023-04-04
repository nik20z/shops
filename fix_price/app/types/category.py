

class Category:
    """
    https://img.fix-price.com/static/categories/
    """
    def __init__(self, data_info: dict):
        self.data_info = data_info

        self.category__id: int = data_info['id']
        self.title: str = data_info['title']
        self.alias_: str = data_info['alias']
        self.src: str = data_info['src'].split('/')[-1]
        self.icon: str = data_info['icon'].split('/')[-1]
        self.catalog_image: str = data_info['catalogImage'].split('/')[-1]
        self.adult: bool = data_info['adult']
