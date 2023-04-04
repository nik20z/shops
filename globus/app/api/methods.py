import json
from requests import Session
from typing import Union

from globus.app import parse
from globus.app.config import HOST
from globus.app.my_exceptions import *


def _get_url(api_version: str, api_method: str) -> str:
    """Собираем запрос к API"""
    return f"https://{HOST}/d1-mobile-bff/api/{api_version}/{api_method}"


def _response_decorator(func):
    def wrapper(*args, **kwargs) -> ResponseMethodApi:
        response_dict = func(*args, **kwargs)

        # Связь между названием функции API и функцией парсинга
        get_method_name_by_func_name = {
            'store': 'store',
            'pvz': 'pvz',
            'category': 'category',
            'products_by_subcategory': 'products_by_subcategory',
            'product': 'product'
        }
        method_name = get_method_name_by_func_name.get(func.__name__, '')
        return ResponseMethodApi(response_dict, method_name)

    return wrapper


class ResponseMethodApi(Response):

    def __init__(self, response_dict: dict, method_name: str):
        super().__init__()
        self.data_parse: list = []

        self.response: Response = response_dict['response']
        self.response_json: dict = self.response.json()
        self.method_name: str = method_name

        match self.method_name:

            case 'store':
                self.data_parse = parse.methods.store(self.response_json)

            case 'pvz':
                self.data_parse = parse.methods.pvz(self.response_json)

            case 'category':
                self.data_parse = parse.methods.category(self.response_json)

            case 'products_by_subcategory':
                store_id = response_dict['store_id']
                check_subcategory_id = response_dict['check_subcategory_id']
                self.data_parse = parse.methods.products_by_subcategory(self.response_json,
                                                                        store_id=store_id,
                                                                        check_subcategory_id=check_subcategory_id)

            case 'product':
                store_id = response_dict['store_id']
                self.data_parse = parse.methods.product(self.response_json, store_id=store_id)

    def get(self):
        """Метод для получения данных класса"""
        return self.data_parse


class GlobusSession:

    def __init__(self, session: Session, favorite_store_id: int):
        self.session: Session = session
        self.favorite_store_id: int = favorite_store_id

        self.params: dict = {}
        self.data: dict = {}

    def _request(self, method: str, url: str) -> Optional[Response]:
        """Отправка запроса"""
        if type(self.data) is dict:
            self.data = json.dumps(self.data)

        match method.lower():

            case 'get':
                return self.session.get(url, params=self.params)

            case 'post':
                if self.favorite_store_id is None:
                    raise FavoriteStoreIsNone()

                return self.session.post(url, data=self.data)

            case 'patch':
                return self.session.patch(url, data=self.data)

            case 'send':
                # return self.session.send()
                ...

    def send(self,
             method: str,
             api_version: str,
             api_method: str,
             params: Optional[dict] = None,
             data: Optional[Union[dict, str]] = None) -> Optional[Response]:
        """Формирование запроса"""
        self.params = params
        self.data = data

        url = _get_url(api_version, api_method)

        response = self._request(method, url)

        if response.status_code != 200:
            raise ResponseErrorCode(response)

        return response


class MethodsApi:

    def __init__(self, session: Session, favorite_store_id: Optional[int]):
        self.session = session
        self.favorite_store_id = favorite_store_id
        self.context_hash: str = ""
        self.globus_session: GlobusSession = GlobusSession(session, favorite_store_id)

    @_response_decorator
    def store(self):
        """Магазины"""
        response = self.globus_session.send('GET', 'v1', 'directories/stores')

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def pvz(self):
        """ПВЗ"""
        response = self.globus_session.send('GET', 'v1', 'directories/pvz')

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def select_store(self, store_id: int):
        """Выбор магазина"""
        data = {
            "context": {
                "purchase_method": 1,
                "store_id": store_id
            }
        }
        response = self.globus_session.send('PATCH', 'v1', 'context', data=data)

        # Если запрос "прошёл", то меняет favorite_store_id
        if response.status_code == 200 and response.json()['data']['result']:
            self.favorite_store_id = store_id
            self.context_hash = response.json()['data']['context_hash']

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def category(self):
        """Категории"""
        response = self.globus_session.send('POST', 'v1', 'catalog/lvl-1')

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def products_by_subcategory(self,
                                subcategory_id: int,
                                store_id: Optional[int] = None,
                                sort: str = 'default',
                                page: int = 1,
                                per_page: int = 20,
                                filter_: Optional[list] = None,
                                range_: Optional[list] = None,
                                is_favorite: bool = False):
        """Товары по subcategory_id"""
        if filter_ is None:
            filter_ = []

        if range_ is None:
            range_ = []

        # Если указан другой store_id, то меняем его
        if store_id is not None and store_id != self.favorite_store_id:
            self.select_store(store_id)

        data = {
            "category_id": subcategory_id,
            "sort": sort,
            "pagination": {
                'page': page,
                'per_page': per_page
            },
            "filter": {
                'filter': filter_,
                'range': range_,
                'is_favorite': is_favorite
            },
            "include": ['tags', 'category', 'products']
        }
        response = self.globus_session.send('POST', 'v1', 'catalog/lvl-2', data=data)

        data_return = {
            'response': response,
            'store_id': self.favorite_store_id,
            'check_subcategory_id': subcategory_id
        }
        return data_return

    @_response_decorator
    def product(self, product_id: str, store_id: Optional[int] = None):
        """Товар по product_id"""

        # Если указан другой store_id, то меняем его
        if store_id is not None and store_id != self.favorite_store_id:
            self.select_store(store_id)

        data = {
            "id": product_id
        }
        response = self.globus_session.send('POST', 'v1', 'catalog/pdp', data=data)

        data_return = {
            'response': response,
            'store_id': self.favorite_store_id
        }
        return data_return
