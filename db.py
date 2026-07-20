"""
db.py — thin MySQL connection layer.

All Python code (routes, analytics) talks to MySQL through the two helpers
below: `query()` for SELECTs and `execute()` for INSERT/UPDATE/DELETE.
Keeping this in one place means the rest of the app never touches
mysql.connector directly.
"""
import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG

_pool = None


def get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="hospital_pool",
            pool_size=5,
            **DB_CONFIG,
        )
    return _pool


def get_connection():
    return get_pool().get_connection()


def query(sql, params=None, one=False):
    """Run a SELECT and return a list of dict rows (or a single dict if one=True)."""
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        cur.close()
        return (rows[0] if rows else None) if one else rows
    finally:
        conn.close()


def execute(sql, params=None):
    """Run an INSERT/UPDATE/DELETE. Returns the new row id (for INSERTs)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        new_id = cur.lastrowid
        cur.close()
        return new_id
    finally:
        conn.close()
