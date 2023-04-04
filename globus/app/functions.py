import random
import time
from psycopg2.errors import ForeignKeyViolation

from globus.app import parse
from globus.app.database import Insert, Select
from globus.app.main import GlobusApp


def parse_all_subcategory_and_products(
        globus_app: GlobusApp,
        per_page: int = 100,
        time_sleep_start: int = 5,
        time_sleep_stop: int = 10):
    """ПАРСИМ ВСЕ КАТЕГОРИИ И ТОВАРЫ"""
    r = globus_app.category()
    # Массив всех subcategory_id
    subcategory_id_list = Select.send_query("SELECT subcategory_id FROM subcategory;", to_list=True)

    # Перебираем категории товаров
    for category__obj in r.get():
        print(f"Категория {category__obj.name_}")
        category__id = category__obj.category__id
        r = globus_app.products_by_subcategory(category__id)

        product_item_list = r.response_json['data']['products']['items']

        # Перебираем товары в этой категории
        for product_item in product_item_list:
            subcategory_id = product_item['main_category_id']

            # Если подкатегория уже есть в БД, то continue
            if subcategory_id not in subcategory_id_list:
                print('subcategory_id', subcategory_id)

                page = 1  # Текущая страница
                total_page = 1  # Всего страниц

                while page <= total_page:
                    # Делаем запросы до тех пор, пока не переберутся все страницы page
                    response_product = globus_app.products_by_subcategory(subcategory_id, page=page, per_page=per_page)

                    pagination = response_product.response_json['data']['products']['pagination']

                    # total = pagination['total']
                    total_page = pagination['total_page']
                    '''
                    Необходимо оптимальным способом высчитывать количество страниц в следующем запросе
                    Например, если товаров 207, то первый запрос обработает 100, а второй должен взять 107
                    При этом, алгоритм должен работать с любыми per_page: {1, 8, 13, 20, 50, 97, 100}

                    '''

                    if page == 1:
                        subcategory_objects = parse.methods.subcategory(response_product.response_json)
                        Insert.subcategory(subcategory_objects)
                        subcategory_id_list.append(subcategory_id)

                    try:
                        Insert.product(response_product.get())
                    except ForeignKeyViolation:
                        ...

                    page += 1

                    time.sleep(random.randint(time_sleep_start, time_sleep_stop))
