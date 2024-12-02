import sqlite3
import textwrap
from contextlib import contextmanager


def get_inline_sql(sql: str) -> str:
    """Convert pretty SQL statement in docstring to something that looks good in console output or logs.

    - Cleanup PII if you are going to log all SQL queries 🤠
    """
    # Dedent first to normalize indentation
    sql = textwrap.dedent(sql)
    # Replace multiple whitespace characters with a single space
    sql = ' '.join(sql.split())
    # Remove starting and ending whitespace
    sql = sql.strip()
    return sql


# todo: thread safe implementation!
@contextmanager
def get_conn_cur(db_path: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        yield conn, cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()