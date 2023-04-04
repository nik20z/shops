import json
from requests import Response, Session
import time
from typing import Union, Optional

from lenta.app import parse
from lenta.app.config import HOST
from lenta.app.functions import GetValueByIdFromTable
from lenta.app.my_exceptions import ResponseErrorCode


def _get_url(api_version: str, api_method: str) -> str:
    """Собираем запрос к API"""
    return f"https://{HOST}/api/{api_version}/{api_method}"


def _response_decorator(func):
    def wrapper(*args, **kwargs) -> ResponseMethodApi:
        response_dict = func(*args, **kwargs)

        '''data_ = {}
        data_tables_dict = {}

        if 'data_' in response_dict:
            data_ = response_dict['data_']

        if 'data_tables_dict' in response_dict:
            data_tables_dict = response_dict['data_tables_dict']'''

        # Связь между названием функции API и функцией парсинга
        get_method_name_by_func_name = {
            'stories': 'story',
            'store_types': 'store_type',
            'store': 'store',
            'catalog': 'catalog',
            'product': 'product',
            'product_list': 'product_list',
            'product_comments': 'product_comments'
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

        if 'data_tables_dict' in response_dict:

            self.data_tables_dict = response_dict['data_tables_dict']

            if self.data_tables_dict is None and \
                    self.method_name in ('product', 'product_in_store', 'product_list',):
                self.data_tables_dict = GetValueByIdFromTable()
                self.data_tables_dict.convert_table_to_dict('brand')
                self.data_tables_dict.convert_table_to_dict('sub_title')
                self.data_tables_dict.convert_table_to_dict('product_promo_type')
                self.data_tables_dict.convert_table_to_dict('stock_type')
                self.data_tables_dict.convert_table_to_dict('badge')

        match self.method_name:
            case 'story':
                self.data_parse = parse.methods.story(self.response_json)

            case 'store_type':
                self.data_parse = parse.methods.store_type(self.response_json)

            case 'store':
                self.data_parse = parse.methods.store(self.response_json)

            case 'catalog':
                self.data_parse = parse.methods.catalog(self.response_json)

            case 'product' | 'product_in_store':
                store_id = response_dict['store_id']
                self.data_parse = parse.methods.product(self.response_json, store_id,
                                                        data_tables_dict=self.data_tables_dict)

            case 'product_list':
                store_id = response_dict['store_id']
                self.data_parse = parse.methods.product(self.response_json, store_id, product_info_type='product_data',
                                                        data_tables_dict=self.data_tables_dict)

    def get(self):
        """Метод для получения данных класса"""
        return self.data_parse


class LentaSession:

    def __init__(self,
                 session: Session,
                 number_phone: Optional[Union[str, int]],
                 refresh_token: Optional[Union[str, int]],
                 access_token: Optional[Union[str, int]]):
        self.session = session

        self.number_phone = number_phone
        self.refresh_token = refresh_token
        self.access_token = access_token

        self.params = {}
        self.data = {}

    def _request(self, method: str, url: str) -> Optional[Response]:
        """Отправка запроса"""
        if type(self.data) is dict:
            self.data = json.dumps(self.data)

        match method.lower():

            case 'get':
                return self.session.get(url, params=self.params)

            case 'post':
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
        response_json = response.json()

        if response.status_code != 200:

            '''
            {'message': 'Запрашиваемый ресурс требует авторизации.', 'errorCode': 'Unauthorized'}
            {'error': 'unsupported_grant_type'}
            {'message': 'Извините, на сайте ведутся технические работы. Попробуйте повторить операцию позднее.', 'errorCode': 'InternalServerError'}
            '''

            if 'errorCode' in response_json \
               and response_json['errorCode'] == 'Unauthorized' \
               and self.refresh_token is not None:

                self.signin()
                return self._request(method, url)

            raise ResponseErrorCode(response)

        return response

    def auth(self):
        """Авторизация по SMS"""
        '''
        Отправка запроса на отправку кода по SMS
        '''
        data = {
            "phoneNumber": self.number_phone
        }

        response = self.send('POST', 'v1', 'registration/requestUserStatus', data=data)
        print(response.json())
        # {'status': 'ActiveNewLoyalty', 'info': 'Новая программа лояльности активна', 'flashingCallAvailable': True, 'userType': 'NplUser'}

        # Авторизация
        ksid = ''
        vn = '4.32.0.49'

        verify_code = 123456

        data = {
            "username": self.number_phone,
            "grant_type": 'SMS',
            "verify_code": verify_code
        }

        self.send('POST', 'v1', f"signin?q=2&ksid={ksid}&vn={vn}", data=data)

    def signin(self):
        """Получения Bearer токена (access_token)"""
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token
        }
        # self.session.headers.update({'Content-Type': 'application/x-www-form-urlencoder'})

        response = self.send('POST', 'v1', 'signin?q=0', data=data)
        response_json = response.json()

        # Заносим данные в конфиг-файл
        self.access_token = response_json['access_token']
        self.refresh_token = response_json['refresh_token']

        print(self.refresh_token)
        print(self.access_token)

        '''self.session.headers.update(
            {'Authorization': f"Bearer {self.access_token}",
             'Content-Type': 'application/json; charset=UTF-8'}
        )'''
        time.sleep(1)

        data_dict = {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token
        }
        return data_dict


class MethodsApi:

    def __init__(self,
                 session: Session,
                 number_phone: Optional[Union[str, int]],
                 refresh_token: Optional[Union[str, int]],
                 access_token: Optional[Union[str, int]],
                 data_tables_dict: Optional[GetValueByIdFromTable] = None):
        self.session = session
        self.lenta_session = LentaSession(session,
                                          number_phone,
                                          refresh_token,
                                          access_token)

        self.data_tables_dict = data_tables_dict
        if data_tables_dict is None:
            self.data_tables_dict = GetValueByIdFromTable()

    @_response_decorator
    def labels_sku(self):
        """ПОДРОБНАЯ ИНФА О ВСЕХ ПОЛЯХ"""
        response = self.lenta_session.send('GET', 'v1', 'labels/sku')
        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def stories(self, store_id: str):
        """Истории из приложения"""
        params = {
            "storeId": store_id
        }
        response = self.lenta_session.send('GET', 'v1', 'stories', params=params)
        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def store_types(self):
        """Типы магазинов"""
        response = self.lenta_session.send('GET', 'v1', 'stores/types')
        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def store(self, store_id: str = None):
        """Перечень всех магазинов Лента
        api_version: v1 - больше информации, v2 - меньше информации
        """
        if store_id is None:
            response = self.lenta_session.send('GET', 'v1', 'stores')
        else:
            response = self.lenta_session.send('GET', 'v1', f"stores/{store_id}")

        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def catalog(self, store_id: str):
        """Список категорий и подкатегорий товаров
        api_version: v1, v2
        """
        response = self.lenta_session.send('GET', 'v2', f"stores/{store_id}/catalog")
        data_return = {
            'response': response
        }
        return data_return

    @_response_decorator
    def product(self,
                store_id: str,
                node_code: str,
                limit: int = 24,
                offset: int = 0,
                only_discounts: bool = False,
                sorting: str = "ByPopularity",  # ByCardPriceAsc
                min_price: int = 0,
                max_price: Optional[int] = None,
                filters: Optional[list] = None):
        """Показать все товары по node_code (catalog_group, category, subcategory)"""
        if filters is None:
            filters = []

        data = {
            "limit": limit,
            "offset": offset,
            "onlyDiscounts": only_discounts,
            "sorting": sorting,
            "nodeCode": node_code,
            'minPrice': min_price,
            'maxPrice': max_price,
            "filters": filters
        }

        if max_price is None:
            del data['maxPrice']

        response = self.lenta_session.send('POST', 'v1', f"stores/{store_id}/skus", data=data)
        data_return = {
            'response': response,
            'data_tables_dict': self.data_tables_dict,
            'store_id': store_id
        }
        return data_return

    @_response_decorator
    def product_list(self, store_id: str,  product_id_list: Optional[list[int]] = None):
        """Получить информацию о товарах по их product_id"""
        if product_id_list is not None:
            data = {
                "skuCodes": product_id_list
            }
            response = self.lenta_session.send('POST', 'v1', f"stores/{store_id}/skuslist", data=data)
            data_return = {
                'response': response,
                'data_tables_dict': self.data_tables_dict,
                'store_id': store_id
            }
            return data_return

    @_response_decorator
    def product_comment(self,
                        sku_id: int,
                        count: int = 10,
                        offset: int = 0):
        """Комментарии к товару"""
        params = {
            "count": count,
            "offset": offset
        }
        response = self.lenta_session.send('GET', 'v1', f"comments/{sku_id}", params=params)
        data_return = {
            'response': response
        }
        return data_return

    # МЕТОДЫ, ТРЕБУЮЩИЕ АВТОРИЗАЦИИ

    def my_lenta(self):
        """Информация об аккаунте"""
        response = self.lenta_session.send('GET', 'v1', 'mylenta')
        data_return = {
            'response': response
        }
        return data_return

    def store_all_info(self, store_id: str):
        """Вся информация о конкретном магазине (Главная страница)
        api_version: v1, v2, v3, v4
        carousels - какие-то акционные товары

        список акций под основной каруселью:
            festivalPromotions - один тип (цвет)
            catalogCrazyList - другой тип (цвет)

        categories - все основные категории
        ...
        brands - список брендов (собственные марки на главной странице)
        """
        response = self.lenta_session.send('GET', 'v4', f"stores/{store_id}/home")
        data_return = {
            'response': response
        }
        return data_return

    def mobile_promo(self,
                     store_id: str,
                     promo_type: str = "weekly",
                     hide_alcohol: bool = False,
                     limit: int = 10,
                     offset: int = 0):
        """
        Получить информацию о промо-акциях
        promo_type: weekly, crazy, instore, festival
        """
        params = {
            "type": promo_type,
            "hideAlcohol": hide_alcohol,
            "limit": limit,
            "offset": offset
        }

        # data =
        # ?hideAlcohol={hide_alcohol}&limit={limit}&offset={offset}&type={promo_type}
        response = self.lenta_session.send('GET', 'v1', f"stores/{store_id}/mobilepromo", params=params)
        data_return = {
            'response': response
        }
        return data_return

    def me_all_coupons(self, store_id: str):
        """Доступные купоны для данного магазина"""
        response = self.lenta_session.send('GET', 'v1', f"me/allcoupons?storeId={store_id}")
        data_return = {
            'response': response
        }
        return data_return

    def sync(self, store_id: str):
        """Избранное
        skus - список избранных товаров
        promotions - карусель с промо-акциями (только те, что активированы)
        """
        response = self.lenta_session.send('GET', 'v1', f"cart/sync?storeId={store_id}")
        data_return = {
            'response': response
        }
        return data_return
