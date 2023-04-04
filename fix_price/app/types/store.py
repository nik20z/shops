from typing import Union


class Store:

    def __init__(self, data_info: dict):
        self.data_info = data_info

        self.store_id: int = data_info['id']
        self.pfm: str = data_info['pfm']
        self.address: str = data_info['address']
        self.longitude: float = data_info['longitude']
        self.latitude: float = data_info['latitude']
        self.is_active: bool = data_info['isActive']
        self.city_id: int = data_info['cityId']
        self.can_pay_card: bool = data_info['canPayCard']
        self.can_pickup: bool = data_info['canPickup']
        # self.schedule_weekdays: Union[list, None] = data_info['scheduleWeekdays'].split('-')
        # self.schedule_saturday: Union[list, None] = data_info['scheduleSaturday'].split('-')
        # self.schedule_sunday: Union[list, None] = data_info['scheduleSunday'].split('-')
        self.temporarily_closed: bool = data_info['temporarilyClosed']
        self.metro_stations: list[str] = data_info['metroStations']
