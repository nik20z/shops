from lenta.app.types import Image


class PromoCode:

    def __init__(self, data_info: dict):
        self.data = data_info
        self.replace_keys = {
            "contentGuid": 'content_guid',
            "webUrl": 'web_url'
        }

        self.content_guid: str = data_info['contentGuid']
        self.web_url: str = data_info['webUrl']

        # data - promo
        self.image_logo_mobile: Image
        self.image_background: Image
        self.open_url_via_browser: bool = True
        self.main_image: Image
        self.discount_value = None
        self.url_button: str = 'https://plus.yandex.ru/gift?promoName=lenta100'
        self.promo_code: str = '7RML6TTZS9'
        self.club: str = 'None'
        self.display_type: str = 'promoCode'
        self.id_: str = '2701935'
        self.title: str = 'ПЛЮС МУЛЬТИ 60 дней'
        self.subtitle: str = 'Получите 100 баллов Ленты с Яндекс Плюсом'
        self.rules_full: str = 'Срок Акции: с 16.01.2023 г. по 31.03.2023 г. Правила: <a href="https://yandex.ru/legal/plus_lenta100">yandex.ru/legal/plus_lenta100</a>. Активируйте на сайте <a href="https://plus.yandex.ru/gift">plus.yandex.ru/gift</a> до 28.03.2023г. Условия подписки Плюс Мульти: <a href="https://yandex.ru/legal/yandex_plus_conditions/">ya.cc/plus_conditions</a>. 60 дней Плюс Мульти бесплатно, далее автопродление - 299 руб./мес. Только для пользователей, не имеющих активной подписки Яндекс Плюс (или иную, ее включающую). Требуется указание данных банковской карты. 1 участник может активировать промокод только 1 раз.',
        self.validity_start_date: str = '2023-01-16 00:00:00'
        self.validity_end_date: str = '2023-03-27 23:59:00'
        self.offer_type: str = 'promoCode'
