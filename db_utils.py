import time
import sqlite3
from .consts import RETRY_COUNT, CONNECTION_TIMEOUT


def connect_to_db(db_path: str):
    """Connects to a SQLite database with a configured timeout."""
    try:
        return sqlite3.connect(db_path, timeout=CONNECTION_TIMEOUT)
    except sqlite3.Error as e:
        print(f"SQLite connection error: {e}")
        return None


def execute_with_retry(db_path: str, operation):
    """
    Executes a database operation with retry logic.
    `operation` is a callable that accepts a cursor and performs the DB work.
    """
    attempt = 0
    while attempt < RETRY_COUNT:
        connection = None
        try:
            connection = connect_to_db(db_path)
            if connection is None:
                raise ConnectionError(f"Unable to connect to database: {db_path}")
            cursor = connection.cursor()
            operation(cursor)
            connection.commit()
            return
        except sqlite3.OperationalError as e:
            print(f"Attempt {attempt + 1} failed due to database lock: {e}")
            attempt += 1
            time.sleep(attempt + 1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
        finally:
            if connection:
                connection.close()

    print(f"All {RETRY_COUNT} attempts failed.")
