from typing import Union


class Brand:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "brand": 'value_'
        }
        self.brand_id: Union[int, None] = None
        self.value_: str = data_info['brand']
