from typing import Optional


class Store:

    def __init__(self, data_info: dict):
        self.data_info = data_info

        self.store_id: int = data_info['id']
        self.name_: str = data_info['name']
        self.full_addr: str = data_info['full_addr']
        self.longitude: float = data_info['location']['longitude']
        self.latitude: float = data_info['location']['latitude']
        self.schedule: str = data_info['schedule']
        self.is_open: bool = data_info['is_open']
        self.applied: bool = data_info['applied']
        self.informer: Optional[str] = data_info['informer']
