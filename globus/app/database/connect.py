import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from misc.env import GlobusEnv


connection = psycopg2.connect(**GlobusEnv.DataBase)
connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
connection.set_client_encoding('UTF8')
cursor = connection.cursor()
