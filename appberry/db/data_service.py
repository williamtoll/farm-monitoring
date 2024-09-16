import os
import logging
import time

from appberry.db.db_connection import Database

from pathlib import Path
import psycopg2.extras


logFile = Path(os.getenv('GPT_FOLDER')+'/gpt2.log')

logging.basicConfig(filename=logFile,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger("data_service")
logger.setLevel(logging.DEBUG)

def pg_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"))
    return conn

def fetch_data(query):
    logger.info("fetching data ")
    start_time = time.time()
    try:
        with Database().connection as connection:
            logger.info("--- elapsed %s seconds ---" % (time.time() - start_time))
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
    except Exception as e:
        logger.error("pg connection error %s ", e)
        return None



