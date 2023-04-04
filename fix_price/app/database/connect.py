import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from misc.env import FixPriceEnv


connection = psycopg2.connect(**FixPriceEnv.DataBase)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
connection.set_client_encoding('UTF8')
cursor = connection.cursor()
