from typing import Union


class Badge:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "text": 'value_',
            "backColor": 'back_color',
            "fontColor": 'font_color'
        }
        self.badge_id: Union[int, None] = None
        self.value_ = data_info['text']
        self.back_color = data_info['backColor']
        self.font_color = data_info['fontColor']
