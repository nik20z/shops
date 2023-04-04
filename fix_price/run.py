import random
import time

from fix_price.app import FixPriceApp


fix_price_app = FixPriceApp(favorite_city_id=397)


'''
# КАТЕГОРИИ
r = fix_price_app.category()
Insert.category(r.get())

'''


'''
# ПОДКАТЕГОРИИ
category__id_list = Select.send_query("SELECT category__id FROM category_", to_list=True)

for category__id in category__id_list:
    print("category__id", category__id)
    r = fix_price_app.subcategory(category__id)
    Insert.subcategory(r.get())
    time.sleep(1)
'''

'''
# ВОЗВРАЩАЕТ НЕ ВСЕ ГОРОДА
r = fix_price_app.city()
Insert.city(r.get())
'''


'''
# МАГАЗИНЫ
r = fix_price_app.store()
print(r.response_json)
# Insert.store(r.get())
'''

'''
# Получить все товары по store_id, category__id, subcategory_id
r = fix_price_app.product(397, 2004, 2796)
print(r.response_json)
# Insert.product(r.get())
'''


subcategory_id_list = fix_price_app.Select.send_query("SELECT DISTINCT subcategory_id, title FROM subcategory;")

# Перебираем подкатегории товаров
for subcategory_id, title in subcategory_id_list:
    print(title, subcategory_id)

    cnt = 0
    count_products = 28
    page = 1

    while count_products >= 28:
        r = fix_price_app.product(subcategory_id, subcategory_id, page=page)
        fix_price_app.Insert.product_in_city(r.get())

        count_products = len(r.get())
        cnt += count_products
        page += 1

        time.sleep(random.randint(3, 7))

    print(f"Общее кол-во товаров: {cnt}")
    print()






'''
ПОКА НЕ ПОНЯТНО, КАК ПОЛУЧАТЬ ТОВАРЫ ИЗ КОНКРЕТНЫХ МАГАЗИНОВ
НЕ ПОНЯТНО, РАЗЛИЧАЮТСЯ ЛИ ЦЕНЫ
ПОЭТОМУ ДЕЛАЕМ РАЗДЕЛЕНИЕ НЕ ПО store_id, а по city_id
'''

