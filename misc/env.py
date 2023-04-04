from os import environ
from typing import Final


class FixPriceEnv:
    DataBase: Final = environ.get('DataBase',
                                  {
                                      'user': "postgres",
                                      'password': "",
                                      'host': "localhost",
                                      'port': 5432,
                                      'database': "fix_price"
                                  })


class GlobusEnv:
    DataBase: Final = environ.get('DataBase',
                                  {
                                      'user': "postgres",
                                      'password': "",
                                      'host': "localhost",
                                      'port': 5432,
                                      'database': "globus"
                                  })


class LentaEnv:
    DataBase: Final = environ.get('DataBase',
                                  {
                                      'user': "postgres",
                                      'password': "",
                                      'host': "localhost",
                                      'port': 5432,
                                      'database': "lenta"
                                  })
