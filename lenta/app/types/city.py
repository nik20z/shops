
class City:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "cityKey": 'key_',
            "cityName": 'name_',
            "storeTimeZoneOffset": 'store_time_zone_offset'
        }

        self.city_id: int
        self.key_: str = data_info['cityKey']
        self.name_: str = data_info['cityName']
        self.store_time_zone_offset: str = data_info['storeTimeZoneOffset'].lower().replace('gmt+', '')
