from psycopg2.errors import ForeignKeyViolation
from psycopg2.errors import UniqueViolation

from lenta.app.database.connect import cursor
from lenta.app.database.connect import connection
from lenta.app.database import Select
from lenta.app.types import *


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
        case 'store_type':
            one_line = (x.type_, x.name_, x.icon, x.color, x.filter_title, )

        case 'city':
            one_line = (x.key_, x.name_, x.store_time_zone_offset, )

        case 'store':
            one_line = (x.store_id, x.name_, x.address, x.city_key, x.type_, x.lat, x.long,
                        x.opens_at, x.closes_at, x.is_default_store, x.is_ecom_available,
                        x.is_pickup_available, x.is_delivery_available, x.is_lenta_scan_available,
                        x.is_24h_store, x.has_pet_shop, x.division, x.is_favorite, x.min_order_summ,
                        x.max_order_summ, x.min_delivery_order_summ, x.max_weight, x.max_delivery_weight,
                        x.max_quantity_per_item, x.max_delivery_quantity_per_item, x.order_limit_overall,
                        x.delivery_order_limit_overall, )

        case 'catalog_group':
            one_line = (x.code, x.name_, x.image_id, x.url, )

        case 'category':
            one_line = (x.catalog_group_code, x.code, x.name_, x.image_id, x.url, )

        case 'subcategory':
            one_line = (x.category__code, x.code, x.name_, x.image_id, x.url, )

        case 'brand' | 'product_promo_type' | 'stock_type':
            one_line = (x.value_, )

        case 'badge':
            one_line = (x.text_, x.back_color, x.font_color, )

        case 'product':
            one_line = (x.product_id, x.average_rating, x.comments_count, x.title,
                        x.brand_id, x.sub_title_id, x.description, x.image_id,
                        x.images_ids, x.web_url, x.subcategory_code, )

        case 'product_in_store':
            one_line = (x.store_id, x.product_id, x.regular_price, x.discount_price,
                        x.offer_description, x.promo_type_id, x.validity_start_date,
                        x.validity_end_date, x.order_limit, x.order_steps, x.sku_weight,
                        x.sku_dry_weight, x.is_available_for_order, x.is_available_for_delivery,
                        x.is_available_for_delivery_for_pro, x.is_weight_product,
                        x.stock_type_id, x.badges_ids, )

        case 'story':
            one_line = (x.story_id, x.name_, x.link, x.preview_image,
                        x.content_items_ids, x.open_url_via_browser, )

    return one_line


def get_data_array(type_: str,
                   data: list,
                   check_unique: bool = False) -> list:
    """Получить массив данных по определённому классу/сущности для записи в БД"""
    data_for_insert = [get_one_line(type_, x) for x in data]
    if check_unique:
        return list(set(data_for_insert))
    return data_for_insert


def store_type(data: list[StoreType]) -> None:
    """Занести данные о типах магазинов"""
    query = "INSERT INTO store_type (type_, name_, icon, color, filter_title) VALUES (%s,%s,%s,%s,%s);"

    cursor.executemany(query, get_data_array('store_type', data))
    connection.commit()


def city(data: list[City]) -> None:
    """Заносим данные о городах"""
    query = "INSERT INTO city (key_, name_, store_time_zone_offset) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;"

    cursor.executemany(query, get_data_array('city', data, check_unique=True))
    connection.commit()


def store(data: list[Store]) -> None:
    """Занести данные о магазинах"""
    query = """INSERT INTO store (store_id, name_, address, city_id, store_type_id, lat, long,
                          opens_at, closes_at, is_default_store, is_ecom_available, is_pickup_available,
                          is_delivery_available, is_lenta_scan_available, is_24h_store, has_pet_shop,
                          division, is_favorite, min_order_summ, max_order_summ, min_delivery_order_summ,
                          max_weight, max_delivery_weight, max_quantity_per_item, max_delivery_quantity_per_item,
                          order_limit_overall, delivery_order_limit_overall) 
                VALUES (%s,%s,%s,{0},{1},%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING;
            """.format(Select.query_info_by_column_name('city_id', 'key_', 'city'),
                       Select.query_info_by_column_name('store_type_id', 'type_', 'store_type'))

    cursor.executemany(query, get_data_array('store', data))
    connection.commit()


def image(data: list[Image]):
    """"""
    pass


def catalog_group(data: list[CatalogGroup]) -> None:
    """Группы товаров"""
    query = "INSERT INTO catalog_group (code, name_, image_id, url) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING;"

    data_set = set(data)
    group__code_in_table = Select.catalog_code('catalog_group')
    data_checked = [x for x in data_set if x.code not in group__code_in_table]

    cursor.executemany(query, get_data_array('catalog_group', data_checked))
    connection.commit()


def category(data: list[Category]) -> None:
    """Категории товаров"""
    query = """INSERT INTO category_ (group__id, code, name_, image_id, url) 
               VALUES ({0},%s,%s,%s,%s) 
               ON CONFLICT DO NOTHING;
               """.format(Select.query_info_by_column_name('group__id', 'code', 'catalog_group'))

    data_set = set(data)
    category__code_in_table = Select.catalog_code('category_')
    data_checked = [x for x in data_set if x.code not in category__code_in_table]

    cursor.executemany(query, get_data_array('category', data_checked))
    connection.commit()


def subcategory(data: list[Subcategory]) -> None:
    """Подкатегории товаров"""
    query = """INSERT INTO subcategory (category__id, code, name_, image_id, url) 
               VALUES ({0},%s,%s,%s,%s) 
               ON CONFLICT DO NOTHING;
               """.format(Select.query_info_by_column_name('category__id', 'code', 'category_'))

    data_set = set(data)
    subcategory_code_in_table = Select.catalog_code('subcategory')
    data_checked = [x for x in data_set if x.code not in subcategory_code_in_table]

    cursor.executemany(query, get_data_array('subcategory', data_checked))
    connection.commit()


def brand(data: list[Brand]) -> None:
    """Бренд"""
    query = "INSERT INTO brand (value_) VALUES (%s) ON CONFLICT DO NOTHING;"

    cursor.executemany(query, get_data_array('brand', data))
    connection.commit()


def product_promo_type(data: list[ProductPromoType]) -> None:
    """Тип скидки у Товара"""
    query = "INSERT INTO product_promo_type (value_) VALUES (%s) ON CONFLICT DO NOTHING;"

    cursor.executemany(query, get_data_array('product_promo_type', data))
    connection.commit()


def stock_type(data: list[StockType]) -> None:
    """Свойство, отображающее количество товаров"""
    query = "INSERT INTO stock_type (value_) VALUES (%s) ON CONFLICT DO NOTHING;"

    cursor.executemany(query, get_data_array('stock_type', data))
    connection.commit()


def badge(data: list[Badge]) -> None:
    """Значок у товара"""
    query = "INSERT INTO badge (text_, back_color, font_color) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING;"

    cursor.executemany(query, get_data_array('badge', data))
    connection.commit()


def product(data: list[Product]) -> None:
    """Товар"""
    query = """INSERT INTO product (product_id, average_rating, comments_count, title,
                                    brand_id, sub_title_id, description, image_id,
                                    images_ids, web_url, subcategory_id, time_update) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,{0}, CURRENT_TIMESTAMP)
                ON CONFLICT (product_id) DO UPDATE 
                SET (average_rating, comments_count, description, image_id, images_ids, time_update) = 
                    (EXCLUDED.average_rating, EXCLUDED.comments_count, EXCLUDED.description, 
                     EXCLUDED.image_id, EXCLUDED.images_ids, CURRENT_TIMESTAMP);
            """.format(Select.query_info_by_column_name('subcategory_id', 'code', 'subcategory'))

    cursor.executemany(query, get_data_array('product', data))
    connection.commit()


def product_in_store(data: list[Product]) -> None:
    """Товар"""
    query = """INSERT INTO product_in_store 
                    (store_id, product_id, regular_price, discount_price, offer_description, 
                     promo_type_id, validity_start_date, validity_end_date,
                     order_limit, order_steps, sku_weight, sku_dry_weight, is_available_for_order,
                     is_available_for_delivery, is_available_for_delivery_for_pro, is_weight_product,
                     stock_type_id, badges_ids, time_update) 
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, CURRENT_TIMESTAMP)
                ON CONFLICT (store_id, product_id) DO UPDATE
                SET (regular_price, discount_price, offer_description, 
                     promo_type_id, validity_start_date, validity_end_date,
                     order_limit, order_steps, sku_weight, sku_dry_weight, is_available_for_order,
                     is_available_for_delivery, is_available_for_delivery_for_pro, is_weight_product,
                     stock_type_id, badges_ids, time_update)
                = (EXCLUDED.regular_price, EXCLUDED.discount_price, EXCLUDED.offer_description, 
                   EXCLUDED.promo_type_id, EXCLUDED.validity_start_date, EXCLUDED.validity_end_date,
                   EXCLUDED.order_limit, EXCLUDED.order_steps, EXCLUDED.sku_weight, EXCLUDED.sku_dry_weight, 
                   EXCLUDED.is_available_for_order, EXCLUDED.is_available_for_delivery, 
                   EXCLUDED.is_available_for_delivery_for_pro, EXCLUDED.is_weight_product,
                   EXCLUDED.stock_type_id, EXCLUDED.badges_ids, CURRENT_TIMESTAMP);"""

    try:
        cursor.executemany(query, get_data_array('product_in_store', data))
        connection.commit()
    except ForeignKeyViolation:
        # Заносим товар в Главную таблицу product
        product(data)
        cursor.executemany(query, get_data_array('product_in_store', data))
        connection.commit()
    # except UniqueViolation:
        # Обновляем данные в таблице product_in_store
        # ...


def story(data: list[Story]) -> None:
    """История из приложения"""
    query = """INSERT INTO story (story_id, name_, link, preview_image, content_items_ids, open_url_via_browser) 
               VALUES (%s,%s,%s,%s,%s,%s) 
               ON CONFLICT DO NOTHING;"""

    cursor.executemany(query, get_data_array('story', data))
    connection.commit()
