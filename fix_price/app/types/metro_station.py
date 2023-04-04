
'''
[{
    'id': 95532,
    'name': 'Верхние Котлы',
    'lineColor': 'CC4C6E',
    'latitude': 55.69,
    'longitude': 37.618889
}]
'''

class MetroStation:

    def __init__(self, data_info: dict):
        self.data_info = data_info

        self.id_: int = data_info['id']
        self.name_: str = data_info['name']
        # Цвет в формате HEX
        # self.line_color: str = data_info['lineColor']
        self.latitude: str = data_info['latitude']
        self.longitude: str = data_info['longitude']