from typing import Union, Optional
from typing import KeysView

from lenta.app.database.connect import cursor
from lenta.app.database.connect import connection


extensions_create_names = ()


table_create_queries = {
    "user_info": """
        CREATE TABLE IF NOT EXISTS user_info (
            user_id bigint,
            access_token text,
            refresh_token text,
            email_address text UNIQUE,
            bonus_points numeric(8, 1),
            bonus_expiration_date date,
            bonus_points_to_expire numeric(8, 1),
            stamps_points smallint,
            stamps_daily_limit smallint,
            stamps_total_limit smallint,
            has_loyalty bool,
            is_loyalty_member bool,
            is_new_loyalty_member bool,
            loyalty_level smallint,
            is_user_pro bool,
            email_confirmed bool,
            is_bonus_game_choice bool,
            push_token_change_needed bool,
            data_update_time timestamptz,
            PRIMARY KEY (user_id));""",

    "social_network": """
        CREATE TABLE IF NOT EXISTS social_network (
            social_network_id smallserial,
            name_ text,
            icon_url text,
            web_url text UNIQUE,
            PRIMARY KEY (social_network_id));""",

    "store_type": """
        CREATE TABLE IF NOT EXISTS store_type (
            store_type_id smallserial,
            type_ text UNIQUE,
            name_ text,
            icon text,
            color varchar(7),
            filter_title text, 
            PRIMARY KEY (store_type_id));""",

    "city": """
        CREATE TABLE IF NOT EXISTS city (
            city_id smallserial,
            key_ text UNIQUE,
            name_ text,
            store_time_zone_offset time,
            PRIMARY KEY (city_id));""",

    "store": """
        CREATE TABLE IF NOT EXISTS store (
            store_id varchar(4),
            name_ text,
            address text,
            city_id smallint,
            store_type_id smallint,
            lat numeric(9, 6),
            long numeric(9, 6),
            opens_at smallint,
            closes_at smallint,
            is_default_store bool,
            is_ecom_available bool,
            is_pickup_available bool,
            is_delivery_available bool,
            is_lenta_scan_available bool,
            is_24h_store bool,
            has_pet_shop bool,
            division text,
            is_favorite bool,
            min_order_summ integer,
            max_order_summ integer,
            min_delivery_order_summ integer,
            max_delivery_order_summ integer,
            max_weight integer,
            max_delivery_weight integer,
            max_quantity_per_item integer,
            max_delivery_quantity_per_item integer,
            order_limit_overall integer,
            delivery_order_limit_overall integer,
            PRIMARY KEY (store_id),
            FOREIGN KEY (store_type_id) REFERENCES store_type (store_type_id),
            FOREIGN KEY (city_id) REFERENCES city (city_id));""",

    "image": """
        CREATE TABLE IF NOT EXISTS image (
            image_id serial,
            thumbnail text,
            medium text,
            full_size text,
            medium_lossy text,
            PRIMARY KEY (image_id));""",

    "catalog_group": """
        CREATE TABLE IF NOT EXISTS catalog_group (
            group__id smallserial,
            code text UNIQUE,
            name_ text,
            image_id integer,
            url text,
            PRIMARY KEY (group__id));""",

    "category_": """
        CREATE TABLE IF NOT EXISTS category_ (
            category__id smallserial,
            group__id smallint,
            code text UNIQUE,
            name_ text,
            image_id integer,
            url text,
            PRIMARY KEY (category__id),
            FOREIGN KEY (group__id) REFERENCES catalog_group (group__id),
            FOREIGN KEY (image_id) REFERENCES image (image_id));""",

    "subcategory": """
        CREATE TABLE IF NOT EXISTS subcategory (
            subcategory_id smallserial,
            category__id smallint,
            code text UNIQUE,
            name_ text,
            image_id integer,
            url text,
            PRIMARY KEY (subcategory_id),
            FOREIGN KEY (category__id) REFERENCES category_ (category__id),
            FOREIGN KEY (image_id) REFERENCES image (image_id));""",

    "brand": """
        CREATE TABLE IF NOT EXISTS brand (
            brand_id smallserial,
            value_ text UNIQUE NOT NULL,
            PRIMARY KEY (brand_id));""",

    "sub_title": """
        CREATE TABLE IF NOT EXISTS sub_title (
            sub_title_id smallserial,
            value_ text UNIQUE NOT NULL,
            PRIMARY KEY (sub_title_id));""",

    "product_promo_type": """
        CREATE TABLE IF NOT EXISTS product_promo_type (
            product_promo_type_id smallserial,
            value_ text UNIQUE NOT NULL,
            PRIMARY KEY (product_promo_type_id));""",

    "stock_type": """
        CREATE TABLE IF NOT EXISTS stock_type (
            stock_type_id smallserial,
            value_ text UNIQUE NOT NULL,
            PRIMARY KEY (stock_type_id));""",

    "badge": """
        CREATE TABLE IF NOT EXISTS badge (
            badge_id smallserial,
            value_ text UNIQUE NOT NULL,
            back_color varchar(7),
            font_color varchar(7),
            PRIMARY KEY (badge_id));""",

    "product": """
        CREATE TABLE IF NOT EXISTS product (
            product_id int,
            average_rating numeric(2, 1),
            comments_count smallint,
            title text,
            brand_id smallint,
            sub_title_id smallint,
            description text,
            image_id int,
            images_ids int[],
            web_url text,
            subcategory_id smallint,
            time_update timestamp,
            PRIMARY KEY (product_id),
            FOREIGN KEY (subcategory_id) REFERENCES subcategory (subcategory_id),
            FOREIGN KEY (brand_id) REFERENCES brand (brand_id),
            FOREIGN KEY (sub_title_id) REFERENCES sub_title (sub_title_id),
            FOREIGN KEY (image_id) REFERENCES image (image_id));""",

    "product_in_store": """
        CREATE TABLE IF NOT EXISTS product_in_store (
            store_id varchar(4),
            product_id int,
            regular_price numeric(9, 2),
            discount_price numeric(9, 2),
            offer_description smallint,
            promo_type_id smallint,
            validity_start_date timestamptz,
            validity_end_date timestamptz,
            stamps_price numeric(9, 2),
            order_limit numeric(9, 2),
            order_steps numeric(9, 2)[],
            sku_weight numeric(9, 2),
            sku_dry_weight numeric(9, 2),
            is_available_for_order bool,
            is_available_for_delivery bool,
            is_available_for_delivery_for_pro bool,
            is_weight_product bool,
            stock_type_id smallint,
            badges_ids smallint[],
            time_update timestamp,
            PRIMARY KEY (store_id, product_id),
            FOREIGN KEY (store_id) REFERENCES store (store_id),
            FOREIGN KEY (product_id) REFERENCES product (product_id),
            FOREIGN KEY (promo_type_id) REFERENCES product_promo_type (product_promo_type_id),
            FOREIGN KEY (stock_type_id) REFERENCES stock_type (stock_type_id));""",

    "story": """
        CREATE TABLE IF NOT EXISTS story (
            story_id integer,
            name_ text,
            link text,
            preview_image int,
            content_items_ids int[],
            open_url_via_browser bool,
            PRIMARY KEY (story_id));""",
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
