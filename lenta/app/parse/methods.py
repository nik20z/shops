from typing import Union, Optional
from requests.models import Response

from lenta.app.types import *
from lenta.app.database import Select
from lenta.app.functions import GetValueByIdFromTable


def _parse_decorator(func):
    def wrapper(response: Union[Response, dict], *args, **kwargs) -> Optional[list]:
        data_response = response
        if type(response) is Response:
            data_response = response.json()

        if data_response:
            return func(data_response, *args, **kwargs)

    return wrapper


@_parse_decorator
def store_type(data_response: dict) -> dict:
    """Типы магазинов"""
    store_type_objects = [StoreType(data_info) for data_info in data_response]
    data_return = {
        'data': store_type_objects
    }
    return data_return


@_parse_decorator
def store(data_response: dict) -> dict:
    """Магазины"""
    store_objects = [Store(data_info) for data_info in data_response]
    city_objects = [City(data_info) for data_info in data_response]
    data_return = {
        'store': store_objects,
        'city': city_objects
    }
    return data_return


@_parse_decorator
def catalog(data_response: dict) -> dict:
    """Группы товаров, категории и подкатегории"""
    catalog_groups_array = data_response['catalogGroups']
    catalog_group_objects = []
    category__objects = []
    subcategory_objects = []

    # CatalogGroup
    for catalog_group_data in catalog_groups_array:
        catalog_group_objects.append(CatalogGroup(catalog_group_data))

        # Category
        catalog__group_code = catalog_group_data['code']
        for category_data in catalog_group_data['categories']:
            category__obj = Category(category_data)
            category__obj.catalog_group_code = catalog__group_code
            category__objects.append(category__obj)

            # Subcategory
            category__code = category__obj.code
            for subcategory_data in category_data['subcategories']:
                subcategory_obj = Subcategory(subcategory_data)
                subcategory_obj.category__code = category__code
                subcategory_objects.append(subcategory_obj)

    data_return = {
        'catalog_group_objects': catalog_group_objects,
        'category__objects': category__objects,
        'subcategory_objects': subcategory_objects
    }
    return data_return


'''
@_parse_decorator
def brand(data_response: dict) -> list:
    """Бренд"""


@_parse_decorator
def product_promo_type(data_response: dict) -> list:
    """Тип скидки"""
    product_promo_type_objects = []
    product_promo_type_value_in_table = Select.send_query("SELECT value_ FROM product_promo_type;", to_list=True)

    for data_info in data_response:
        x = ProductPromoType(data_info)

        if x.value_ is not None and x.value_ not in product_promo_type_value_in_table:
            product_promo_type_value_in_table.append(x.value_)
            product_promo_type_objects.append(x)

    return product_promo_type_objects


@_parse_decorator
def stock(data_response: dict) -> list:
    """Свойство, характеризующее количество товаров в магазине"""
    stock_objects = []
    stock_value__in_table = Select.send_query("SELECT value_ FROM stock_type;", to_list=True)

    for data_info in data_response:
        x = StockType(data_info)

        if x.value_ is not None and x.value_ not in stock_value__in_table:
            stock_value__in_table.append(x.value_)
            stock_objects.append(x)

    return stock_objects


@_parse_decorator
def badge(data_response: dict) -> list:
    """Значок у товара"""
    badge_objects = []
    badge_value__in_table = Select.send_query("SELECT text_ FROM badge;", to_list=True)

    for data_info in data_response:
        x = Badge(data_info)

        if x.value_ not in badge_value__in_table:
            badge_value__in_table.append(x.value_)
            badge_objects.append(x)

    return badge_objects
'''


@_parse_decorator
def product(data_response: dict,
            store_id: str,
            product_info_type: str = 'from_catalog',
            data_tables_dict: Optional[GetValueByIdFromTable] = None) -> dict:
    """Товары"""

    if data_tables_dict is None:
        data_tables_dict = GetValueByIdFromTable()
        data_tables_dict.convert_table_to_dict('brand')
        data_tables_dict.convert_table_to_dict('sub_title')
        data_tables_dict.convert_table_to_dict('product_promo_type')
        data_tables_dict.convert_table_to_dict('stock_type')

    if 'skus' in data_response:
        data_response = data_response['skus']

    product_objects = []
    for data_info in data_response:
        try:
            product_objects.append(Product(data_info, product_info_type, store_id, data_tables_dict=data_tables_dict))
        except AttributeError:
            ...

    data_return = {
        'data': product_objects
    }
    return data_return


@_parse_decorator
def story(data_response: dict) -> dict:
    """История из приложения"""
    story_objects = [Story(data_info) for data_info in data_response]
    data_return = {
        'data': story_objects
    }
    return data_return


@_parse_decorator
def product_comment(data_response: dict) -> dict:
    """Отзывы о товаре"""
    product_comment_objects = [ProductComment(data_info) for data_info in data_response]
    data_return = {
        'data': product_comment_objects
    }
    return data_return
