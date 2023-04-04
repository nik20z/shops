from typing import Optional
import requests

from globus.app import database
from globus.app.api import MethodsApi
from globus.app.config import HEADERS


class GlobusApp(MethodsApi):

    def __init__(self, favorite_store_id: Optional[int] = None):
        database.utils.create_table()

        self.utils = database.utils
        self.Insert = database.Insert
        self.Select = database.Select

        self.favorite_store_id = favorite_store_id

        self.session = requests.Session()
        self.session.headers.update(HEADERS)

        MethodsApi.__init__(self, self.session, favorite_store_id)
