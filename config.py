"""
config.py — all environment-specific settings live here.

Edit the values below (or better, set them as environment variables)
to match your MySQL server before running the app.
"""
import os

DB_CONFIG = {
    "host": os.environ.get("HMS_DB_HOST", "localhost"),
    "port": int(os.environ.get("HMS_DB_PORT", 3306)),
    "user": os.environ.get("HMS_DB_USER", "root"),
    "password": os.environ.get("HMS_DB_PASSWORD", "rootpass"),
    "database": os.environ.get("HMS_DB_NAME", "hospital_db"),
}

SECRET_KEY = os.environ.get("HMS_SECRET_KEY", "dev-key-change-this-in-production")
