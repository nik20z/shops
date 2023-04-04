from typing import Optional


'''
promotion': {
    'type': 1,
    'offer_text': None,
    'deeplink': None,
    'chips_text': None,
    'badge_text': '-27%',
    'badge_text_additional': 'по карте',
    'price_comments': ['Акция до 11 апреля', 'Без карты 179,99 ₽'],
    'date_end': '2023-04-11T00:00:00.000000Z',
    'discount_percent': 27
}
'''


def _get_package_type_id(package_type: str) -> int:
    """Получить ID типа упаковки"""
    package_type_dict = {
        "piece": 1,  # Часть
        "weight-by-piece": 2,  # Поштучно
        "weight": 3  # На развес
    }
    return package_type_dict.get(package_type)


def _get_badges_id_list(badges: list[str]) -> list[int]:
    """Получить массив badges"""
    badges_id_dict = {
        'ecoproduct': 1,
        'vegetarian': 2,
        'gluten_free': 3,
        'frozen': 4
    }
    badges_id_list = []
    for x in badges:
        if x in badges_id_dict:
            badges_id_list.append(badges_id_dict[x])
    return badges_id_list


def _replace_on_none(text: str, s: str, old: str) -> Optional[str]:
    """Сделать replace или вернуть None при ошибке"""
    try:
        return text.replace(s, old)
    except AttributeError:
        ...


class Product:
    """
    Short-ссылка на изображение:
    https://image.globus.ru/mobile
    """

    def __init__(self,
                 data_info: dict,
                 store_id: Optional[int] = None,
                 data_type: str = 'from_catalog'):
        self.data_info = data_info

        self.store_id: int = store_id

        self.product_id: str = data_info['id']
        self.subcategory_id: int = data_info['main_category_id']

        self.active: bool = data_info['active']
        self.active_text: Optional[str] = data_info['active_text']
        self.package_type: str = data_info['package_type']
        self.package_type_id: int = _get_package_type_id(self.package_type)
        self.weight_text: Optional[str] = data_info['weight_text']
        self.price_per: str = data_info['price_per']
        self.order_price: int = data_info['order_price'] / 100
        self.condition_text: Optional[str] = data_info['condition_text']
        self.is_favorite: bool = data_info['is_favorite']
        self.is_own: bool = data_info['is_own']
        self.pickup_only: bool = data_info['pickup_only']
        self.badges: list[str] = data_info['badges']
        self.badges_id: list[int] = _get_badges_id_list(self.badges)
        self.is_adult: bool = data_info['is_adult']
        self.is_available_other_store = data_info['is_available_other_store']
        self.promotion: dict = data_info['promotion']
        self.unit_basket_text: str = data_info['unit_basket_text']
        self.unit_price_text: str = data_info['unit_price_text']
        self.basket_step: float = data_info['basket_step']
        self.basket_min_volume: float = data_info['basket_min_volume']
        self.price: float = data_info['price'] / 100
        self.cost = data_info['cost']
        self.quantity: float = data_info['quantity']
        self.quantity_max: float = data_info['quantity_max']

        if data_type == 'from_catalog':
            self.name_: str = data_info['name_optional']
            self.name_required: str = data_info['name_required']
            self.preview_image: Optional[str] = _replace_on_none(data_info['preview_image'],
                                                                 'https://image.globus.ru/mobile', '')

        elif data_type == 'product_page':
            self.name_: str = data_info['name']
            self.name_required: str = self.name_.split(',')[-1]

            self.preview_image: Optional[str] = _replace_on_none(data_info['images'][0],
                                                                 'https://image.globus.ru/mobile', '')
