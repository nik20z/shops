import json
from requests import Response, Session
from typing import Optional, Union


from fix_price.app.config import HOST
from fix_price.app import parse
from fix_price.app.my_exceptions import *


def _get_url(api_version: str, api_method: str) -> str:
    """Собираем запрос к API"""
    return f"https://{HOST}/buyer/{api_version}/{api_method}"


def _response_decorator(func):
    def wrapper(*args, **kwargs) -> ResponseMethodApi:
        response_dict = func(*args, **kwargs)

        # Связь между названием функции API и функцией парсинга
        get_method_name_by_func_name = {
            'city': 'city',
            'store': 'store',
            'category': 'category',
            'subcategory': 'subcategory',
            'product': 'product'
        }
        method_name = get_method_name_by_func_name.get(func.__name__, '')
        return ResponseMethodApi(response_dict, method_name)

    return wrapper


class ResponseMethodApi(Response):

    def __init__(self, response_dict: dict, method_name: str,):
        super().__init__()
        self.data_parse = None

        self.response: Response = response_dict['response']
        self.response_json: dict = self.response.json()
        self.method_name: str = method_name

        match self.method_name:

            case 'city':
                self.data_parse = parse.methods.city(self.response_json)

            case 'store':
                self.data_parse = parse.methods.store(self.response_json)

            case 'category':
                self.data_parse = parse.methods.category(self.response_json)

            case 'subcategory':
                category_id = response_dict['category_id']
                self.data_parse = parse.methods.subcategory(self.response_json, category_id)

            case 'product':
                subcategory_id = response_dict['subcategory_id']
                city_id = response_dict['city_id']
                self.data_parse = parse.methods.product(self.response_json, subcategory_id, city_id)

    def get(self):
        """Метод для получения данных класса"""
        return self.data_parse


class FixPriceSession:

    def __init__(self, session: Session):
        self.session = session

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
                '''
                self.session.headers.update({
                    'x-city': '397',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Accept-Encoding': 'gzip'
                })
                '''
                headers = self.session.headers
                headers['Content-Type'] = 'application/json; charset=UTF-8'
                headers['Accept-Encoding'] = 'gzip'

                return self.session.post(url,
                                         data=self.data,
                                         params=self.params,
                                         headers=headers)

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

    def __init__(self, session: Session, favorite_city_id: Optional[int]):
        self.session = session
        self.favorite_city_id = favorite_city_id

        self.fix_price_session = FixPriceSession(session)

    @_response_decorator
    def city(self, sort: str = None, title_part: str = None):
        """Города"""
        params = {}
        if sort is not None:
            params['sort'] = sort

        if title_part is not None:
            params['titlePart'] = title_part

        response = self.fix_price_session.send('GET', 'v1', 'location/city', params=params)

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def store(self, city_id: int = None):
        """Магазины"""
        params = {}

        # Получить список магазинов в конкретном городе
        if city_id is not None:
            params['cityId'] = city_id

        response = self.fix_price_session.send('GET', 'v1', 'store', params=params)

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def category(self, city_id: int = None):
        """Список категорий"""
        params = {}

        # Получить список категорий в конкретном городе
        if city_id is not None:
            params['cityId'] = city_id

        response = self.fix_price_session.send('GET', 'v2', 'category', params=params)

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def subcategory(self, category_id: int):
        """Список подкатегорий"""
        response = self.fix_price_session.send('GET', 'v2', f"category/{category_id}")

        data_return = {
            'response': response,
            'category_id': category_id
        }
        return data_return

    @_response_decorator
    def product(self,
                category_id: int,
                subcategory_id: int,
                city_id: Optional[int] = None,
                sort: str = 'sold',
                page: int = 1,
                limit: int = 28):
        """Товар"""
        if city_id is None:
            city_id = self.favorite_city_id

        params = {
            "sort": sort,
            "page": page,
            "limit": limit,

        }

        data = {
            'category': [category_id],
            'filter': {}
        }

        response = self.fix_price_session.send('POST', 'v2', 'product/filter', params=params, data=data)

        data_return = {
            'response': response,
            'subcategory_id': subcategory_id,
            'city_id': city_id,
        }
        return data_return
