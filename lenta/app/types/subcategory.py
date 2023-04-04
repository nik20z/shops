from typing import Union

from lenta.app.types import Image


class Subcategory:

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
        self.category__id: int
        self.category__code: str
        self.code: str = data_info['code']
        self.name_: str = data_info['name']
        self.show_lentochka_banner: bool = data_info['showLentochkaBanner']
        self.sku_count: int = data_info['skuCount']
        self.sku_discount_count: int = data_info['skuDiscountCount']
        self.image: Image
        self.image_id: Union[int, None] = None
        self.url: str = data_info['url'].split('/')[-2]
