import time
import random

from lenta.app import LentaApp


REFRESH_TOKEN = ""
ACCESS_TOKEN = ""

t_start = time.time()

lenta_app = LentaApp()


r = lenta_app.product_list('0119', product_id_list=[676209])
lenta_app.Insert.product_in_store(r.get()['data'])


store_id = '0127'
group_list = lenta_app.Select.catalog_group()


for one_group in group_list:
    code = one_group[1]
    name_ = one_group[2]
    print(name_, code)

    cnt = 0
    offset = 0

    while True:

        r = lenta_app.product(store_id, code, offset=offset)
        lenta_app.Insert.product_in_store(r.get()['data'])

        offset += 24
        cnt += 1

        print(cnt, ')', r.response_json['total'], offset, round(offset / r.response_json['total'], 2) * 100, '%')

        if offset >= r.response_json['total']:
            break

        time.sleep(random.randint(3, 7))

    # break

print(f"{r.response_json['total']} товаров за {time.time() - t_start} с")


'''
def insert_data(self):
    """Добавить данные в БД"""
    match self.method_name:

        case 'story':
            Insert.story(self.data_for_insert['data'])

        case 'store_type':
            Insert.store_type(self.data_for_insert['data'])

        case 'store':
            Insert.city(self.data_for_insert['city'])
            Insert.store(self.data_for_insert['store'])

        case 'catalog':
            Insert.catalog_group(self.data_for_insert['catalog_group_objects'])
            Insert.category(self.data_for_insert['category__objects'])
            Insert.subcategory(self.data_for_insert['subcategory_objects'])

        case 'sku' | 'skus_list' | 'sku_in_store':
            Insert.sku_in_store(self.data_for_insert['data'])
'''
