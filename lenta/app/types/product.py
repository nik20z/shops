from typing import Optional

from lenta.app.types import Image
from lenta.app.functions import GetValueByIdFromTable


def _get_offer_description(n) -> Optional[int]:
    """Получить корректное значение размера скидки"""
    try:
        return -1 * int(n)
    except ValueError:
        ...


'''
# badges example
[{
    'text': 'Диплом качества',
    'backColor': '#89CA15',
    'fontColor': '#FFFFFF'
}]

[{
    'text': 'Только в Ленте',
    'backColor': '#FFDD00',
    'fontColor': '#444444'
}, {
    'text': 'Новинка',
    'backColor': '#079CEF',
    'fontColor': '#FFFFFF'
}]


# Цена с учётом фишек
'stampsPrice': [{
            'stampsCount': 0,
            'price': {
                'value': 4749.0,
                'integerPart': '4\xa0749',
                'fractionPart': '00'
            },
            'discount': 0,
            'isActive': False
        }, {
            'stampsCount': 5,
            'price': {
                'value': 2299.0,
                'integerPart': '2\xa0299',
                'fractionPart': '00'
            },
            'discount': 0,
            'isActive': False
        }],
'''


class Product:

    def __init__(self,
                 data_info: dict,
                 product_info_type: str,
                 store_id: str,
                 data_tables_dict: Optional[GetValueByIdFromTable] = None):
        self.data_info = data_info

        self.data_tables_dict = data_tables_dict

        if data_tables_dict is None:
            self.data_tables_dict = GetValueByIdFromTable()
            self.data_tables_dict.convert_table_to_dict('brand')
            self.data_tables_dict.convert_table_to_dict('sub_title')
            self.data_tables_dict.convert_table_to_dict('product_promo_type')
            self.data_tables_dict.convert_table_to_dict('stock_type')
            self.data_tables_dict.convert_table_to_dict('badge')

        self.store_id: str = store_id

        if product_info_type == 'from_catalog':
            self.average_rating: float = data_info['averageRating']
            self.comments_count: int = data_info['commentsCount']
            self.promo_percent: int = data_info['promoPercent']
            self.promo_id: int = data_info['promoId']
            self.place_output: str = data_info['placeOutput']
            self.price_by_promocode: float = data_info['priceByPromocode']

        elif product_info_type == 'product_data':
            self.specification: dict = data_info['specification']
            self.producer_info: dict = data_info['producerInfo']
            self.important_limitations: dict = data_info['importantLimitations']
            self.stamps_promotion: int = data_info['stampsPromotion']
            self.related_skus: list = data_info['relatedSkus']
            self.similar_skus: list = data_info['similarSkus']
            self.lentochka_promotion: bool = data_info['lentochkaPromotion']
            self.rates_total_count: int = data_info['rates']['totalCount']
            self.rate1: int = data_info['rates']['scores']['rate1']
            self.rate2: int = data_info['rates']['scores']['rate2']
            self.rate3: int = data_info['rates']['scores']['rate3']
            self.rate4: int = data_info['rates']['scores']['rate4']
            self.rate5: int = data_info['rates']['scores']['rate5']

            self.brand_page_id: str = data_info['brandPageId']
            self.price_per_kg: float = data_info['pricePerKg']

            # Пересекается с другими запросами
            self.average_rating: float = data_info['rates']['averageRate']
            self.comments_count: int = sum([self.rate1, self.rate2, self.rate3, self.rate4, self.rate5])

        elif product_info_type == 'favorites':
            self.is_posted_from_cart_page = data_info['isPostedFromCartPage']

        # Основные характеристики
        self.product_id: int = int(data_info['code'])
        self.title: str = data_info['title']
        # self.brand: str = data_info['brand']
        self.brand_id: int = data_tables_dict.get_id('brand', data_info['brand'])
        # self.sub_title: str = data_info['subTitle']
        self.sub_title_id: int = data_tables_dict.get_id('sub_title', data_info['subTitle'])
        self.description: str = data_info['description']
        self.regular_price: float = data_info['regularPrice']
        self.discount_price: float = data_info['discountPrice']
        self.is_show_one_price: bool = data_info['isShowOnePrice']
        self.offer_description: int = _get_offer_description(data_info['offerDescription'].replace('%', ''))
        self.promo_type_id: int = data_tables_dict.get_id('product_promo_type', data_info['promoType'])
        self.validity_start_date: str = data_info['validityStartDate']
        self.validity_end_date: str = data_info['validityEndDate']

        self.image: Optional[Image] = None  # = Image(data_info)
        self.image_id: Optional[int] = None
        self.images: list[Image] = []  # = [Image(data_info), Image(data_info)]
        self.images_ids: list[int] = []

        self.stamps_price: list = data_info['stampsPrice']
        self.web_url: str = data_info['webUrl'].split('/')[-2]
        self.order_limit: float = data_info['orderLimit']
        self.order_steps: list[float] = data_info['orderSteps']
        self.sku_weight: float = data_info['skuWeight']
        self.sku_dry_weight: float = data_info['skuDryWeight']
        self.is_available_for_order: bool = data_info['isAvailableForOrder']
        self.is_available_for_delivery: bool = data_info['isAvailableForDelivery']
        self.is_available_for_delivery_for_pro: bool = data_info['isAvailableForDeliveryForPro']
        self.is_weight_product: bool = data_info['isWeightProduct']
        self.stock_type_id: int = data_tables_dict.get_id('stock_type', data_info['stock'])

        self.subcategory_id: int
        self.subcategory_code: str = data_info['categories']['subcategory']['code']

        # self.badges: list = data_info['badges']
        self.badges_ids: list[int] = self.get_badges_ids(data_info['badges'])

    def get_badges_ids(self, badges: list[dict]) -> list[int]:
        """Получить массив badges"""
        return [self.data_tables_dict.get_id('badge', one_badge['text']) for one_badge in badges]
