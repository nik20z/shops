from typing import Union

from lenta.app.functions import check_str_none


class StockType:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "stock": 'value_'
        }

        self.stock_type_id: Union[int, None] = None
        self.value_: str = check_str_none(data_info['stock'])
