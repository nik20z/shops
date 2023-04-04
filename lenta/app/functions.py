from typing import Optional

from lenta.app.database import Insert
from lenta.app.database import Select


def check_str_none(s: str) -> Optional[str]:
    """Проверка строки на None"""
    if s.lower() not in ('none', 'null'):
        return s


def _convert_table_to_dict(table_name: str) -> dict:
    """Конвертировать таблицу вида table_name_id: value_"""
    query = "SELECT {0}_id, value_ FROM {0};".format(table_name)
    table_data = Select.send_query(query)

    return {id_: value_ for id_, value_ in table_data}


def _add_value_in_table(table_name: str, value_: str) -> None:
    """Заносим новое значение в таблицу"""
    query = f"INSERT INTO {table_name} (value_) VALUES (%s) ON CONFLICT DO NOTHING;"
    Insert.send_query(query, data=(str(value_), ))


class GetValueByIdFromTable:
    """
    Класс, содержащий в себе ключи - названия таблиц, а значения - словари вида {value_: id_}
    Класс нужен для того, чтобы один раз сделать запрос и получить статические данные из БД
    Например: stock_type, product_promo_type, badge
    """

    def __init__(self):
        self.table_dict = {}

    def convert_table_to_dict(self, table_name: str) -> dict:
        """Конвертировать таблицу вида table_name_id: value_"""
        query = "SELECT {0}_id, value_ FROM {0};".format(table_name)
        table_data = Select.send_query(query)

        self.table_dict[table_name] = {str(value_): int(id_) for id_, value_ in table_data}
        return self.table_dict[table_name]

    def get_id(self, table_name: str, check_value_: str) -> Optional[int]:
        """Вернуть id_ по названию таблицы и значению"""
        #  Если значения нет в словаре, то нужно занести новое значение в БД и обновить словарь
        if str(check_value_).lower() != 'none':

            # Если значения нет в таблице, то заносим его
            if str(check_value_) not in self.table_dict[table_name]:
                print("if str(check_value_) not in self.table_dict[table_name]", check_value_, table_name)
                _add_value_in_table(table_name, check_value_)
                self.convert_table_to_dict(table_name)

            return self.table_dict[table_name][str(check_value_)]

    def get_value(self, table_name: str, check_id_: int) -> Optional[str]:
        """Вернуть значение по названию таблицы и id_"""
        for value_, id_ in self.table_dict[table_name]:
            if id_ == check_id_:
                return value_
