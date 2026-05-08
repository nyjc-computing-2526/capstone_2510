import os
import psycopg

URL = os.getenv("DB_URL")

def db_execute(query: str, params: list|None = None) -> tuple:
    """
    Run SQL queries on neon postgres.
    Can pass tuple/list of data items.

    Returns tuple (rows_modified, rows_returned).
    """
    with psycopg.connect(URL) as conn:
        with conn.cursor() as cursor:
            if params:
                cursor.execute(
                    query,
                    params
                )
            else:
                cursor.execute(query)
            
            try:
                fetched = cursor.fetchall()
            except psycopg.ProgrammingError:
                fetched = None # ie. No rows to fetch
            modified_n = cursor.rowcount
        conn.commit()
    
    return modified_n, fetched