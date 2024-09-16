import logging
import psycopg2
import os

logger = logging.getLogger("db_connection")
logger.setLevel(logging.DEBUG)

class Database():

   connection = None

   def __init__(self):
      if Database.connection is None:
         try:
            Database.connection = psycopg2.connect(
                  host=os.getenv("DB_HOST"),
                  database=os.getenv("DB_NAME"),
                  user=os.getenv("DB_USER"),
                  password=os.getenv("DB_PASS"))
         except Exception as error:
            logger.info("Error: Connection not established {}".format(error))
         else:
            logger.info("Connection established")

   def execute_query(self, sql):
      cursor = Database.connection.cursor()
      cursor.execute(sql)
      result = cursor.fetchall()
      return result