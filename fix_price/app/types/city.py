
class City:

    def __init__(self, data_info: dict):
        self.data_info = data_info

        self.city_id: int = data_info['id']
        self.name_: str = data_info['name']
        self.title: str = data_info['title']
        self.region_title: str = data_info['regionTitle']
        self.longitude: float = data_info['longitude']
        self.latitude: float = data_info['latitude']
        self.kladr = data_info['kladr']
        self.fiasid: str = data_info['fiasid']
        self.fias: str = data_info['fias']
        self.prefix: str = data_info['prefix']
