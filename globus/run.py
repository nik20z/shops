import random
import time

from globus.app import GlobusApp


globus_app = GlobusApp(favorite_store_id=5005)


'''
Список функций:
1. Спарсить все категории и товары - ТОЛЬКО для того, чтобы наполнить базу
2. Парсинг определённых категорий и товаров
'''


'''
# Актуализировать данные о конкретном товаре
r = globus_app.product('000000000000432483_ST')
print(r.response_json)
globus_app.Insert.product_in_store(r.get())
'''


'''
# ПЕРЕБИРАЕМ ВСЕ ИМЕЮЩИЕСЯ В БД КАТЕГОРИИ И ПАРСИМ ТОВАРЫ

subcategory_id_list = globus_app.Select.send_query("SELECT subcategory_id FROM subcategory;", to_list=True)

per_page = 200
cnt = 79
len_cnt = len(subcategory_id_list)

for subcategory_id in subcategory_id_list[79:]:
    print(f"{cnt}/{len_cnt}) subcategory_id - {subcategory_id}")
    page = 1  # Текущая страница
    total_page = 1  # Всего страниц

    while page <= total_page:
        # Делаем запросы до тех пор, пока не переберутся все страницы page
        response_product = globus_app.products_by_subcategory(subcategory_id, page=page, per_page=per_page)

        pagination = response_product.response_json['data']['products']['pagination']

        total = pagination['total']
        total_page = pagination['total_page']
        print(f"{total} - {page}/{total_page} ({len(response_product.get())})")

        globus_app.Insert.product_in_store(response_product.get())

        page += 1

        time.sleep(random.randint(2, 5))  # random.randint(2, 5)

    cnt += 1
'''
