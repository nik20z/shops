from globus.app.database.connect import cursor
from functions import fetchall_to_list


def send_query(query_text: str, to_list: bool = False) -> list:
    """Произвольный запрос"""
    cursor.execute(query_text)
    result = cursor.fetchall()
    if to_list:
        return fetchall_to_list(result)
    return result


