from typing import Union
from requests import Response

from fix_price.app.types import *


def _parse_decorator(func):
    def wrapper(response: Union[Response, dict], *args, **kwargs):
        data_response = response
        if type(response) is Response:
            data_response = response.json()

        if data_response:
            return func(data_response, *args, **kwargs)
    return wrapper


@_parse_decorator
def city(data_response) -> list:
    """Город"""
    city_objects = [City(one_city) for one_city in data_response]
    return city_objects


@_parse_decorator
def store(data_response) -> list:
    """Магазин"""
    store_objects = [Store(one_store) for one_store in data_response]
    return store_objects


@_parse_decorator
def category(data_response) -> list:
    """Категории"""
    category_objects = [Category(one_category) for one_category in data_response]
    return category_objects


@_parse_decorator
def subcategory(data_response, category__id: int) -> list:
    """Подкатегории"""
    subcategory_objects = [Subcategory(one_subcategory, category__id) for one_subcategory in data_response['subcatalogs']]
    return subcategory_objects


@_parse_decorator
def product(data_response,
            subcategory_id: int,
            city_id: int) -> list:
    """Товар"""
    product_objects = [Product(one_product, subcategory_id, city_id) for one_product in data_response]
    return product_objects
