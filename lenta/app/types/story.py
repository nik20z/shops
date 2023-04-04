from typing import Union

from lenta.app.types import Image
from lenta.app.types import ContentItem


class Story:

    def __init__(self, data_info: dict):
        self.data_info = data_info
        self.data = data_info
        self.replace_keys = {
            "id": 'value_',
            "name": 'name_',
            "club": 'club',
            "link": 'link',
            "buttonColor": 'button_color',
            "buttonTitle": 'button_title',
            "openUrlViaBrowser": 'open_url_via_browser',
            "announcementFullScreen": 'announcement_full_screen',
            "isPinned": 'is_pinned'
        }

        self.story_id: int = data_info['id']
        self.name_: str = data_info['name']
        self.club = None  # data_info['club']
        self.link: str = data_info['link']
        self.preview_image: Union[Image, None] = None
        self.button_color: str = data_info['buttonColor']
        self.button_title: str = data_info['buttonTitle']
        self.content_items_ids: list[int] = []
        self.open_url_via_browser: bool = data_info['openUrlViaBrowser']
        self.announcement_full_screen: bool = data_info['announcementFullScreen']
        self.is_pinned: bool = data_info['isPinned']
