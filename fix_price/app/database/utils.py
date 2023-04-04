from typing import Union
from typing import KeysView

from fix_price.app.database.connect import cursor
from fix_price.app.database.connect import connection


extensions_create_names = ()


table_create_queries = {
    "region": """
        CREATE TABLE IF NOT EXISTS city (
            region_id integer,
            title text,
            PRIMARY KEY (region_id));""",

    "city": """
        CREATE TABLE IF NOT EXISTS city (
            city_id integer,
            name_ text,
            title text,
            region_id smallint,
            longitude numeric(9, 6),
            latitude numeric(9, 6),
            kladr text,
            fiasid text,
            fias text,
            prefix varchar(7),
            PRIMARY KEY (city_id),
            FOREIGN KEY (region_id) REFERENCES region (region_id));""",

    "store": """
        CREATE TABLE IF NOT EXISTS store (
            store_id integer,
            pfm varchar(5),
            address text,
            longitude numeric(9, 6),
            latitude numeric(9, 6),
            is_active bool,
            city_id integer,
            can_pay_card bool,
            can_pickup bool,
            schedule_weekdays interval[2],
            schedule_saturday interval[2],
            schedule_sunday interval[2],
            temporarily_closed bool,
            metro_stations_id integer[] ,
            PRIMARY KEY (store_id),
            FOREIGN KEY (city_id) REFERENCES city (city_id));""",

    "category_": """
        CREATE TABLE IF NOT EXISTS category_ (
            category__id integer,
            title text NOT NULL,
            alias_ text,
            src text,
            icon text,
            catalog_image text,
            adult bool,
            PRIMARY KEY (category__id));""",

    "subcategory": """
        CREATE TABLE IF NOT EXISTS subcategory (
            subcategory_id integer,
            category__id integer,
            title text NOT NULL,
            adult bool,
            PRIMARY KEY (subcategory_id),
            FOREIGN KEY (category__id) REFERENCES category_ (category__id));""",

    "product": """
        CREATE TABLE IF NOT EXISTS product (
            product_id integer,
            subcategory_id integer,
            title text,
            image_title text,
            image_src text,
            PRIMARY KEY (product_id),
            FOREIGN KEY (subcategory_id) REFERENCES subcategory (subcategory_id));""",

    "product_in_city": """
        CREATE TABLE IF NOT EXISTS product_in_city (
            product_id integer,
            city_id integer,
            is_fresh bool,
            is_new bool,
            is_promo bool,
            adult bool,
            is_season bool,
            is_hit bool,
            is_qr_mark bool,
            forbidden bool,
            active bool,
            special_price real,
            special_price_active_to timestamp,
            price real,
            min_price real,
            maxPrice real,
            variant_count smallint,
            variant_id integer,
            url text,
            in_stock integer,
            variant_properties bool,
            PRIMARY KEY (product_id, city_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id),
            FOREIGN KEY (city_id) REFERENCES city (city_id));""",
}

view_create_queries = {

}

function_create_queries = {

}


def create_extension(extension_name: Union[str, list, tuple] = None) -> None:
    """Добавляем расширения"""
    if extension_name is None:
        create_extension(extension_name=extensions_create_names)
    else:
        if type(extension_name) is str:
            extension_name = [extension_name]

        for x in extension_name:
            cursor.execute(f"CREATE EXTENSION IF NOT EXISTS {x};")
            connection.commit()


def create_table(table_name: Union[str, list, tuple, KeysView] = None) -> None:
    """Создаём таблицу"""
    if table_name is None:
        create_table(table_name=table_create_queries.keys())
    else:
        if type(table_name) is str:
            table_name = [table_name]

        for x in table_name:
            cursor.execute(table_create_queries.get(x, None))
            connection.commit()


def create_view(view_name: Union[str, list, tuple, KeysView] = None) -> None:
    """Создаём представление"""
    if view_name is None:
        create_view(view_name=view_create_queries.keys())
    else:
        if type(view_name) is str:
            view_name = [view_name]

        for x in view_name:
            cursor.execute(view_create_queries.get(x, None))
            connection.commit()


def create_functions(function_name: Union[str, list, tuple, KeysView] = None) -> None:
    """Создаём функции"""
    if function_name is None:
        create_functions(function_name=function_create_queries.keys())
    else:
        if type(function_name) is str:
            function_name = [function_name]

        for x in function_name:
            cursor.execute(function_create_queries.get(x, None))
            connection.commit()


def delete_from_table(table_name: Union[str, list, tuple, KeysView] = None) -> None:
    """Удаляем все данные из таблицы"""
    if table_name is not None:
        if type(table_name) is str:
            table_name = [table_name]

        for x in table_name:
            cursor.execute(f"DELETE FROM {x};")
            connection.commit()


def drop_table(table_name: Union[str, list, tuple, KeysView] = None, cascade_state: bool = False) -> None:
    """Удаляем таблицу"""
    if table_name is not None:
        if type(table_name) is str:
            table_name = [table_name]

        for x in table_name:
            cascade = "CASCADE" if cascade_state else ""
            cursor.execute(f"DROP TABLE IF EXISTS {x} {cascade};")
            connection.commit()


def add_column(table_name: str,
               column_name: str,
               data_type: str,
               constraint: str = "") -> None:
    """Добавить новую колонку"""
    query = """ALTER TABLE {0} 
               ADD COLUMN IF NOT EXISTS {1} {2} {3};
               """.format(table_name, column_name, data_type, constraint)
    cursor.execute(query)
    connection.commit()
