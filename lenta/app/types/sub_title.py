from typing import Union


class SubTitle:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "subTitle": 'value_'
        }
        self.sub_title_id: Union[int, None] = None
        self.value_: str = data_info['subTitle']
