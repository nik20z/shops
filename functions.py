

def fetchall_to_list(fetchall_data: list) -> list:
    """Преобразовать fetchall (list[tuple]) с одной колонкой в читаемый массив"""
    data_list = []
    for x in fetchall_data:
        try:
            data_list.append(x[0])
        except IndexError:
            ...
    return data_list


def fetchall_to_list_decorator(func):
    """Декоратор из функции fetchall_to_list"""
    def wrapper(cursor_fetchall) -> list:
        return fetchall_to_list(func(cursor_fetchall))
    return wrapper
