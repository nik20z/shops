import requests
from typing import Optional

from lenta.app import database
from lenta.app.config import HEADERS
from lenta.app.api import MethodsApi
from lenta.app.functions import GetValueByIdFromTable


class LentaApp(MethodsApi):

    def __init__(self,
                 phone_number: Optional[str] = None,
                 email_address: Optional[str] = None,
                 refresh_token: Optional[str] = None,
                 access_token: Optional[str] = None,
                 update_in_db: bool = False):
        """
        Будет несколько типов аутентификации:

        1. user_id (номер телефона в числовом представлении)
            Если пользователя нет в БД, то через специальный метод производится авторизация:
                отправка запроса на сервер,
                получение кода SMS (придумать, как можно автоматизировать или просить ввести в консоль).

        2. email_address - если человек есть в БД
            Если в БД есть ТОЛЬКО access_token, то выводим предупреждение и либо бот работает,
                либо сразу уходит в ошибку
            Если есть refresh_token, то бот его чекает и при необходимости получает новые access_token и refresh_token

        !!!Следующие методы БЕЗ ДОБАВЛЕНИЯ В БД!!!

        3. access_token - работа до тех пор, пока бот не уйдёт в эксепшен

        4. refresh_token - если есть access_token, то пока работаем с ним, а потом при необходимости обновляем

        """
        database.utils.create_table()

        self.utils = database.utils
        self.Insert = database.Insert
        self.Select = database.Select

        self.phone_number = phone_number
        self.email_address = email_address
        self.refresh_token = refresh_token
        self.access_token = access_token

        self.headers = HEADERS
        # self.headers['Authorization'] = f"Bearer {self.access_token}"

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        data_tables_dict = GetValueByIdFromTable()
        data_tables_dict.convert_table_to_dict('brand')
        data_tables_dict.convert_table_to_dict('sub_title')
        data_tables_dict.convert_table_to_dict('product_promo_type')
        data_tables_dict.convert_table_to_dict('stock_type')
        data_tables_dict.convert_table_to_dict('badge')

        MethodsApi.__init__(self,
                            self.session,
                            self.phone_number,
                            self.refresh_token,
                            self.access_token,
                            data_tables_dict=data_tables_dict)
