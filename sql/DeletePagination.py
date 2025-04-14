import psycopg 
import os 
import sys
from dotenv import load_dotenv
import datetime

def _drop_table_last_week(conn: psycopg.Connection, table_name: str):
    """
    Drop the contnets of the table from the previous week 
    """

    try:
        with conn.cursor() as cur:
            # Check if the table exists
            cur.execute(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table_name}');")
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Table '{table_name}' does not exist")
                return

            # Get the current date and time
            now = datetime.datetime.now()

            # Calculate the date one week ago
            one_week_ago = now - datetime.timedelta(weeks=1)
            # Delete records older than one week
            cur.execute(f"DELETE FROM {table_name} WHERE created_at < %s;", (one_week_ago,))
            conn.commit()
            print(f"Records older than one week in table '{table_name}' deleted successfully")
    except Exception as e:
        print(f"An error occurred while deleting records from table '{table_name}': {e}")


