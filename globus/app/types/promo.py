from typing import Optional


class Promo:
    """
    {
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
    """
    def __init__(self, data_info: dict):
        self.data_info = data_info

        self.type_: int = data_info['type_']
        self.offer_text: Optional[str] = data_info['offer_text']
        self.deeplink: Optional[str] = data_info['deeplink']
        self.chips_text: Optional[str] = data_info['chips_text']
        self.badge_text: str = data_info['badge_text']
        self.badge_text_additional: str = data_info['badge_text_additional']
        self.price_comments: list[str] = data_info['price_comments']
        self.date_end: str = data_info['date_end']
        self.discount_percent: int = data_info['discount_percent']
