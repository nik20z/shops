from typing import Optional


class Category:

    def __init__(self, data_info: dict, category_group_name: str):
        self.data_info = data_info

        self.category_group_name: str = category_group_name

        self.category__id: Optional[int] = None
        if 'payload_lvl_2' in data_info['link']:
            self.category__id: int = data_info['link']['payload_lvl_2']['category_id']

        self.name_: str = data_info['name']
        self.banner_image: str = data_info['banner_image'].replace('https://digitalone.globus.ru/files/cms/catalog_banners', '')

        self.deeplink = data_info['deeplink']
