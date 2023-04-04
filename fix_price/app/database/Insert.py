from psycopg2.errors import ForeignKeyViolation


from fix_price.app.database.connect import cursor
from fix_price.app.database.connect import connection


def send_query(query: str, data: tuple = None) -> None:
    """Произвольный запрос"""
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    connection.commit()


def get_one_line(type_: str, x) -> tuple:
    """Получить одну строку записи в БД"""
    one_line = tuple()

    match type_:
        case 'city':
            one_line = (x.city_id, x.name_, x.title, x.region_title, x.longitude, x.latitude,
                        x.kladr, x.fiasid, x.fias, x.prefix, )

        case 'store':
            one_line = (x.store_id, x.pfm, x.address, x.longitude, x.latitude, x.is_active, x.city_id,
                        x.can_pay_card, x.can_pickup, x.temporarily_closed, )

        case 'category':
            one_line = (x.category__id, x.title, x.alias_, x.src, x.icon, x.catalog_image, x.adult, )

        case 'subcategory':
            one_line = (x.subcategory_id, x.category__id, x.title, x.adult, )

        case 'product':
            one_line = (x.product_id, x.subcategory_id, x.title, x.image_title, x.image_src, )

        case 'product_in_city':
            one_line = (x.product_id, x.city_id, x.is_fresh, x.is_new, x.is_promo, x.adult, x.is_season,
                        x.is_hit, x.is_qr_mark, x.forbidden, x.active, x.special_price,
                        x.special_price_active_to, x.price, x.min_price, x.maxPrice, x.variant_count,
                        x.variant_id, x.url, x.in_stock, x.variant_properties, )

    return one_line


def get_data_array(type_: str,
                   data: list,
                   check_unique: bool = False) -> tuple:
    """Получить массив данных по определённому классу/сущности для записи в БД"""
    data_for_insert = [get_one_line(type_, x) for x in data]
    if check_unique:
        return tuple(set(data_for_insert))
    return tuple(data_for_insert)


def city(data: list) -> None:
    """Город"""
    query = """INSERT INTO city (city_id, name_, title, region_title, longitude, 
                                 latitude, kladr, fiasid, fias, prefix) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    cursor.executemany(query, get_data_array('city', data))
    connection.commit()


def store(data: list) -> None:
    """Магазин"""
    query = """INSERT INTO store (store_id, pfm, address, longitude, latitude, is_active, city_id, 
                                  can_pay_card, can_pickup, temporarily_closed) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    store_objects = get_data_array('store', data)
    for one_store in store_objects:
        try:
            cursor.execute(query, one_store)
            connection.commit()
        except ForeignKeyViolation:
            print(f"Отсутствует город с city_id = {one_store[6]}")


def category(data: list):
    """Категория"""
    query = """INSERT INTO category_ (category__id, title, alias_, src, icon, catalog_image, adult) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    cursor.executemany(query, get_data_array('category', data))
    connection.commit()


def subcategory(data: list):
    """Подкатегории"""
    query = """INSERT INTO subcategory (subcategory_id, category__id, title, adult) 
                   VALUES (%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    cursor.executemany(query, get_data_array('subcategory', data))
    connection.commit()


def product(data: list):
    """Товар"""
    query = """INSERT INTO product (product_id, subcategory_id, title, image_title, image_src) 
                   VALUES (%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    cursor.executemany(query, get_data_array('product', data))
    connection.commit()


def product_in_city(data: list):
    """Товар с учётом города"""
    query = """INSERT INTO product_in_city (product_id, city_id, is_fresh, is_new, is_promo, adult, is_season,
                                            is_hit, is_qr_mark, forbidden, active, special_price, 
                                            special_price_active_to, price, min_price, maxPrice, variant_count,
                                            variant_id, url, in_stock, variant_properties) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    product_lines = get_data_array('product_in_city', data)

    try:
        cursor.executemany(query, product_lines)
    except ForeignKeyViolation:
        # Если какой-то из товаров отсутствует в основной таблице product
        product(data)
        cursor.executemany(query, product_lines)

    connection.commit()
