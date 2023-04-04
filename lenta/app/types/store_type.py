

class StoreType:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "type": 'type_',
            "name": 'name_',
            "icon": 'icon',
            "color": 'color',
            "filterTitle": 'filter_title'
        }
        self.store_type_id: int
        self.type_: str = data_info['type']
        self.name_: str = data_info['name']
        self.icon: str = data_info['icon']
        self.color: str = data_info['color']
        self.filter_title: str = data_info['filterTitle']
