from psycopg2.errors import ForeignKeyViolation
from typing import Union

from globus.app.database.connect import cursor, connection
from globus.app.types import *


def send_query(query: str, data: tuple = None) -> None:
    """Произвольный запрос"""
    if data is None:
        cursor.execute(query)
    else:
        cursor.execute(query, data)
    connection.commit()


def get_one_line(type_: str, x: Union[Store, Pvz, Category, Subcategory, Product]) -> tuple:
    """Получить одну строку записи в БД"""
    one_line = tuple()

    match type_:
        case 'store':
            one_line = (x.store_id, x.name_, x.full_addr, x.longitude, x.latitude, x.schedule, x.applied, )

        case 'pvz':
            one_line = (x.pvz_id, x.name_, x.full_addr, x.longitude, x.latitude, x.schedule, x.applied, )

        case 'category':
            one_line = (x.category__id, x.name_, x.category_group_name, x.banner_image, x.deeplink, )

        case 'subcategory':
            one_line = (x.subcategory_id, x.name_)

        case 'product':
            one_line = (x.product_id, x.subcategory_id, x.name_, x.preview_image,
                        x.name_required, x.package_type_id, x.badges_id, )

        case 'product_in_store':
            one_line = (x.store_id, x.product_id, x.active, x.order_price, x.is_own,
                        x.pickup_only, x.is_adult, x.unit_basket_text,
                        x.unit_price_text, x.basket_step, x.basket_min_volume,
                        x.price, x.quantity, x.quantity_max, )

    return one_line


def get_data_array(type_: str,
                   data: list,
                   check_unique: bool = False) -> tuple:
    """Получить массив данных по определённому классу/сущности для записи в БД"""
    data_for_insert = [get_one_line(type_, x) for x in data]
    if check_unique:
        return tuple(set(data_for_insert))
    return tuple(data_for_insert)


def store(data: list[Store]) -> None:
    """Магазин"""
    query = """INSERT INTO store (store_id, name_, full_addr, longitude, latitude, schedule, applied) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    store_lines = get_data_array('store', data)
    cursor.executemany(query, store_lines)
    connection.commit()


def pvz(data: list[Pvz]) -> None:
    """ПВЗ"""
    query = """INSERT INTO pvz (pvz_id, name_, full_addr, longitude, latitude, schedule, applied) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    pvz_lines = get_data_array('pvz', data)
    cursor.executemany(query, pvz_lines)
    connection.commit()


def category(data: list[Category]) -> None:
    """Категории"""
    query = """INSERT INTO category_ (category__id, name_, category_group_name, banner_image, deeplink) 
                   VALUES (%s,%s,%s,%s,%s) 
                   ON CONFLICT DO NOTHING;"""

    category_lines = get_data_array('category', data)
    cursor.executemany(query, category_lines)
    connection.commit()


def subcategory(data: list[Subcategory]) -> None:
    """Подкатегории"""
    query = """INSERT INTO subcategory (subcategory_id, name_) 
                       VALUES (%s,%s) 
                       ON CONFLICT DO NOTHING;"""

    subcategory_lines = get_data_array('subcategory', data)
    cursor.executemany(query, subcategory_lines)
    connection.commit()


def product(data: list[Product]) -> None:
    """Товар"""
    query = """INSERT INTO product (product_id, subcategory_id, name_, preview_image, 
                                    name_required, package_type_id, badges_id, time_update) 
                               VALUES (%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP) 
                               ON CONFLICT DO NOTHING;"""
    product_lines = get_data_array('product', data)
    cursor.executemany(query, product_lines)
    connection.commit()


def product_in_store(data: list[Product]) -> None:
    """Товар в конкретном магазине"""
    query = """INSERT INTO product_in_store (store_id, product_id, active, order_price, is_own, 
                                             pickup_only, is_adult, unit_basket_text, 
                                             unit_price_text, basket_step, basket_min_volume, 
                                             price, quantity, quantity_max, time_update) 
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP) 
                               ON CONFLICT (store_id, product_id) DO UPDATE
                               SET (active, order_price, is_own, 
                                    pickup_only, is_adult, unit_basket_text, 
                                    unit_price_text, basket_step, basket_min_volume, 
                                    price, quantity, quantity_max, time_update) 
                                 = (EXCLUDED.active, EXCLUDED.order_price, EXCLUDED.is_own, 
                                    EXCLUDED.pickup_only, EXCLUDED.is_adult, EXCLUDED.unit_basket_text, 
                                    EXCLUDED.unit_price_text, EXCLUDED.basket_step, EXCLUDED.basket_min_volume, 
                                    EXCLUDED.price, EXCLUDED.quantity, EXCLUDED.quantity_max, CURRENT_TIMESTAMP);"""
    product_lines = get_data_array('product_in_store', data)

    try:
        cursor.executemany(query, product_lines)
    except ForeignKeyViolation:
        # Если какой-то из товаров отсутствует в основной таблице product
        product(data)
        cursor.executemany(query, product_lines)

    connection.commit()
