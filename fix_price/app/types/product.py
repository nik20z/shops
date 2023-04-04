from typing import Optional


class Product:

    def __init__(self, data_info: dict, subcategory_id: int, city_id: int):
        self.data_info = data_info

        try:

            self.product_id: int = data_info['id']
            self.subcategory_id: int = subcategory_id
            self.city_id: int = city_id

            self.title: str = data_info['title']
            self.is_fresh: bool = data_info['isFresh']
            self.is_new: bool = data_info['isNew']
            self.is_promo: bool = data_info['isPromo']
            self.adult: bool = data_info['adult']
            self.is_season: bool = data_info['isSeason']
            self.is_hit: bool = data_info['isHit']
            self.is_qr_mark: bool = data_info['isQRMark']
            self.forbidden: bool = data_info['forbidden']
            self.active: bool = data_info['active']
            self.unit = data_info['unit']

            self.image_title: Optional[str] = None
            self.image_src: Optional[str] = None

            if data_info['image'] is not None:
                self.image_title = data_info['image']['title']
                self.image_src = data_info['image']['src'].split('/')[-1]

            self.special_price: Optional[int] = None
            self.special_price_active_to: Optional[str] = None

            if data_info['specialPrice'] is not None:
                self.special_price = data_info['specialPrice']['price']
                self.special_price_active_to = data_info['specialPrice']['activeTo']

            self.price: float = data_info['price']
            self.min_price: float = data_info['minPrice']
            self.maxPrice: float = data_info['maxPrice']
            self.variant_count: int = data_info['variantCount']
            self.variant_id: int = data_info['variantId']
            self.url: str = data_info['url']
            self.in_stock: bool = data_info['inStock']
            self.variant_properties: bool = data_info['variantProperties']

        except:
            print(data_info)
            raise Exception
