from lenta.app.database.connect import cursor
from lenta.app.database.connect import connection


def user_info(key: str,
              value_,
              user_id: int = None,
              email_address: str = None):
    """Обновить информацию о пользователе"""
    query = ""

    cursor.execute(query)


def sku_in_store(data: list):
    """Актуализируем данные о товаре по store_id"""
    query = """UPDATE sku_in_store SET (regular_price, discount_price, offer_description, 
                                        promo_type_id, validity_start_date, validity_end_date, 
                                        stock_type_id, badges_ids, time_update) = 
                                        ()
                WHERE store_id = %s AND sku_id = %s;"""

    cursor.executemany(query, data)

