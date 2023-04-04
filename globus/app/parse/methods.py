from typing import Optional, Union
from requests import Response

from globus.app.types import *


def _parse_decorator(func):
    def wrapper(response: Optional[Union[Response, dict]], *args, **kwargs) -> Optional[list]:
        data_response = response
        if type(response) is Response:
            data_response = response.json()

        if 'data' in data_response:
            data_response = data_response['data']

        if data_response:
            return func(data_response, *args, **kwargs)
    return wrapper


@_parse_decorator
def store(data_response: dict) -> list:
    """Магазины"""
    store_objects = [Store(one_store) for one_store in data_response['stores']]
    return store_objects


@_parse_decorator
def pvz(data_response: dict) -> list:
    """ПВЗ"""
    pvz_objects = [Pvz(one_pvz) for one_pvz in data_response['pvz']]
    return pvz_objects


@_parse_decorator
def category(data_response: dict) -> list:
    """Категории"""
    category_objects = []
    for one_category_group in data_response['blocks'][1]['payload_category_groups']['groups']:
        category_group_name = one_category_group['name']

        for item in one_category_group['items']:
            category_object = Category(item, category_group_name)

            if category_object.category__id is not None:
                category_objects.append(category_object)

    return category_objects


@_parse_decorator
def subcategory(data_response: dict) -> list:
    """Подкатегории"""
    subcategory_objects = [Subcategory(data_response['category'])]
    return subcategory_objects


@_parse_decorator
def products_by_subcategory(data_response: dict,
                            store_id: Optional[int] = None,
                            check_subcategory_id: Optional[int] = None) -> list:
    """Товары по subcategory_id"""
    product_objects = []

    if check_subcategory_id is None:
        """Если НЕ указан subcategory_id для проверки"""

        for one_product in data_response['products']['items']:
            product_objects.append(Product(one_product, store_id=store_id))

    else:
        for one_product in data_response['products']['items']:
            if one_product['main_category_id'] == check_subcategory_id:
                product_objects.append(Product(one_product, store_id=store_id))

    return product_objects


@_parse_decorator
def product(data_response: dict, store_id: Optional[int] = None) -> list:
    """Товар по product_id"""
    return [Product(data_response['product'], store_id=store_id, data_type='product_page')]
