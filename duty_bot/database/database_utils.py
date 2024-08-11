import psycopg2
import logging
import os
import time
from psycopg2 import OperationalError, Error


def create_connection(retries=5, delay=2):
    """Create a database connection to the PostgreSQL database with retry."""

    connection = None
    for attempt in range(retries):
        try:
            logging.info("Trying connect to PostgreSQL DB...")
            connection = psycopg2.connect(
                user=os.getenv('POSTGRESQL_USER'),
                password=os.getenv('POSTGRESQL_PASSWORD'),
                host=os.getenv('POSTGRESQL_HOST'),
                port=os.getenv('POSTGRESQL_PORT'),
                database=os.getenv('POSTGRESQL_DB_NAME')
            )
            logging.info("Connection to PostgreSQL DB successful")
            return connection
        except OperationalError as e:
            logging.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:  # Don't delay after the last attempt
                time.sleep(delay)
    logging.error("All connection attempts failed.")
    return connection


def execute_query(query, executemany, params=None, fetch=True):
    """Execute a query and return the results if fetch is True."""

    connection = create_connection()
    result = None
    if connection:
        cursor = connection.cursor()
        try:
            if executemany is False:
                cursor.execute(query, params)
                result = True
                if fetch:
                    result = cursor.fetchall()
                    logging.debug(f"Query result is {result}")
            else:
                cursor.executemany(query, params)
                result = True
            connection.commit()
            cursor.close()
        except Error as e:
            logging.info(f"The error '{e}' occurred")
            connection.rollback()
        finally:
            connection.close()
            logging.info("Connection closed")
    return result


def execute_write_query(query, params=None, executemany=False):
    """Execute a write (INSERT, UPDATE, DELETE) query."""

    return execute_query(query, executemany, params, fetch=False)


def execute_read_query(query, params=None, executemany=False):
    """Execute a read (SELECT) query and return the results."""

    return execute_query(query,executemany, params, fetch=True)
