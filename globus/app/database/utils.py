from typing import KeysView, Optional, Union

from globus.app.database.connect import cursor, connection


extensions_create_names = ()


table_create_queries = {
    "store": """
        CREATE TABLE IF NOT EXISTS store (
            store_id integer,
            name_ text NOT NULL,
            full_addr text,
            longitude numeric(9, 6),
            latitude numeric(9, 6),
            schedule text,
            applied bool,
            PRIMARY KEY (store_id));""",

    "pvz": """
        CREATE TABLE IF NOT EXISTS pvz (
            pvz_id integer,
            name_ text NOT NULL,
            full_addr text,
            longitude numeric(9, 6),
            latitude numeric(9, 6),
            schedule text,
            applied bool,
            PRIMARY KEY (pvz_id));""",

    "category_": """
        CREATE TABLE IF NOT EXISTS category_ (
            category__id integer,
            name_ text NOT NULL,
            category_group_name text NOT NULL,
            banner_image text,
            deeplink text,
            PRIMARY KEY (category__id));""",

    "subcategory": """
        CREATE TABLE IF NOT EXISTS subcategory (
            subcategory_id integer,
            name_ text NOT NULL,
            PRIMARY KEY (subcategory_id));""",

    "product": """
        CREATE TABLE IF NOT EXISTS product (
            product_id text,
            subcategory_id int,
            name_ text,
            preview_image text,
            name_required text,
            package_type_id smallint,
            badges_id smallint[],
            time_update timestamp,
            PRIMARY KEY (product_id),
            FOREIGN KEY (subcategory_id) REFERENCES subcategory (subcategory_id));""",

    "product_in_store": """
        CREATE TABLE IF NOT EXISTS product_in_store (
            store_id integer,
            product_id text,
            active bool,
            order_price numeric(8, 2),
            is_own bool,
            pickup_only bool,
            is_adult bool,
            unit_basket_text text,
            unit_price_text text,
            basket_step real,
            basket_min_volume real,
            price numeric(8, 2),
            quantity real,
            quantity_max real,
            time_update timestamp,
            PRIMARY KEY (store_id, product_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id));""",

}

view_create_queries = {

}

function_create_queries = {

}


def create_extension(extension_name: Optional[Union[str, list, tuple]] = None) -> None:
    """Добавляем расширения"""
    if extension_name is None:
        create_extension(extension_name=extensions_create_names)
    else:
        if type(extension_name) is str:
            extension_name = [extension_name]

        for x in extension_name:
            cursor.execute(f"CREATE EXTENSION IF NOT EXISTS {x};")
            connection.commit()


def create_table(table_name: Optional[Union[str, list, tuple, KeysView]] = None) -> None:
    """Создаём таблицу"""
    if table_name is None:
        create_table(table_name=table_create_queries.keys())
    else:
        if type(table_name) is str:
            table_name = [table_name]

        for x in table_name:
            cursor.execute(table_create_queries.get(x, None))
            connection.commit()


def create_view(view_name: Optional[Union[str, list, tuple, KeysView]] = None) -> None:
    """Создаём представление"""
    if view_name is None:
        create_view(view_name=view_create_queries.keys())
    else:
        if type(view_name) is str:
            view_name = [view_name]

        for x in view_name:
            cursor.execute(view_create_queries.get(x, None))
            connection.commit()


def create_functions(function_name: Optional[Union[str, list, tuple, KeysView]] = None) -> None:
    """Создаём функции"""
    if function_name is None:
        create_functions(function_name=function_create_queries.keys())
    else:
        if type(function_name) is str:
            function_name = [function_name]

        for x in function_name:
            cursor.execute(function_create_queries.get(x, None))
            connection.commit()


def delete_from_table(table_name: Optional[Union[str, list, tuple, KeysView]] = None) -> None:
    """Удаляем все данные из таблицы"""
    if table_name is not None:
        if type(table_name) is str:
            table_name = [table_name]

        for x in table_name:
            cursor.execute(f"DELETE FROM {x};")
            connection.commit()


def drop_table(table_name: Optional[Union[str, list, tuple, KeysView]] = None, cascade_state: bool = False) -> None:
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
