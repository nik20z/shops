from typing import Union

# from lenta.app.types import Image


class CatalogGroup:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "name": 'name_',
            "code": 'code',
            "showLentochkaBanner": 'show_lentochka_banner',
            "skuCount": 'sku_count',
            "skuDiscountCount": 'sku_discount_count',
            "image": 'image',
            "url": 'url'
        }
        self.group__id: int
        self.code: str = data_info['code']
        self.name_: str = data_info['name']
        self.show_lentochka_banner: str = data_info['showLentochkaBanner']
        self.sku_count: str = data_info['skuCount']
        self.sku_discount_count: str = data_info['skuDiscountCount']
        self.image = None  # Union[Image, None] = None  # Image(data_info['image'])
        self.image_id: Union[int, None] = None
        self.url: str = data_info['url'].split('/')[-2]
