from typing import Union


class Image:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "thumbnail": 'thumbnail',
            "medium": 'medium',
            "fullSize": 'full_size',
            "mediumLossy": 'medium_lossy'
        }

        self.image_id: Union[int, None] = None
        self.thumbnail: str = data_info['thumbnail']
        self.medium: str = data_info['medium']
        self.full_size: str = data_info['fullSize']
        self.medium_lossy: str = data_info['mediumLossy']
