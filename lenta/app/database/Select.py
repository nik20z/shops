from lenta.app.database.connect import cursor

from functions import fetchall_to_list, fetchall_to_list_decorator


def send_query(query: str, to_list: bool = False) -> list:
    """Произвольный запрос"""
    cursor.execute(query)
    result = cursor.fetchall()
    if to_list:
        return fetchall_to_list(result)
    return result


def query_info_by_column_name(select_col: str, check_col: str, table_name: str) -> str:
    """Получить данные из конкретной таблицы по конкретному условию"""
    return "(SELECT {2}.{0} FROM {2} WHERE {2}.{1} = %s)".format(select_col, check_col, table_name)


def store_type_id(type_: str) -> list:
    """Получить store_type_id"""
    query = "SELECT store_type_id FROM store_type WHERE type_ = %s;"
    cursor.execute(query, (type_,))
    return cursor.fetchone()


@fetchall_to_list_decorator
def catalog_code(table_name: str) -> list:
    """Получить массив из code для Группы, Категории или Подкатегории"""
    query = "SELECT code FROM {0};".format(table_name)
    cursor.execute(query)
    return cursor.fetchall()


def catalog_group(order_by: str = 'group__id', limit: int = None):
    """Получить список всех Групп товаров"""
    query = "SELECT group__id, code, name_, url FROM catalog_group ORDER BY {0}".format(order_by)

    if limit is not None:
        query += f"LIMIT {limit}"

    cursor.execute(query)
    return cursor.fetchall()
