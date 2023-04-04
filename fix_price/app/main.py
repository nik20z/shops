import requests
from typing import Optional

from fix_price.app import database
from fix_price.app.api import MethodsApi
from fix_price.app.config import HEADERS
from fix_price.app.database import utils, Insert, Select


class FixPriceApp(MethodsApi):

    def __init__(self, favorite_city_id: Optional[int] = None):
        database.utils.create_table()

        self.utils = database.utils
        self.Insert = database.Insert
        self.Select = database.Select

        self.session = requests.Session()
        self.session.headers.update(HEADERS)

        self.favorite_city_id = favorite_city_id

        MethodsApi.__init__(self, self.session, favorite_city_id)
