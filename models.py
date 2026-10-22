
import sqlite3
from pathlib import Path
from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

DATABASE = Path(__file__).resolve().parent / "dashboard.db"

VALID_ROLES = {"admin", "manager", "team_member"}


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK (role IN (
                        'admin', 'manager', 'team_member'
                    ))
            )
        """)

def initialize_delivery_records():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS delivery_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                route_id TEXT NOT NULL,
                zone TEXT NOT NULL,
                defect_count INTEGER NOT NULL
                    CHECK (defect_count >= 0),
                route_date TEXT NOT NULL,
                created_by INTEGER NOT NULL,
                FOREIGN KEY (created_by) REFERENCES users(id)
            )
        """)


def create_delivery_record(
    route_id, zone, defect_count, route_date, user_id
):
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO delivery_records
            (route_id, zone, defect_count, route_date, created_by)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                route_id,
                zone,
                defect_count,
                route_date,
                user_id,
            ),
        )


def get_delivery_records():
    with get_connection() as connection:
        records = connection.execute(
            """
            SELECT id, route_id, zone,
                   defect_count, route_date, created_by
            FROM delivery_records
            ORDER BY id DESC
            """
        ).fetchall()

    return [dict(record) for record in records]


def create_user(username, password, role):
    username = username.strip()

    if not 3 <= len(username) <= 50:
        raise ValueError("Invalid username length.")

    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters.")

    if role not in VALID_ROLES:
        raise ValueError("Invalid role.")

    password_hash = generate_password_hash(password)

    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, ?)
            """,
            (username, password_hash, role),
        )


def verify_user(username, password):
    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id, username, password_hash, role
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    if user and check_password_hash(
        user["password_hash"], password
    ):
        return {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"],
        }

    return None


def get_user_by_id(user_id):
    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id, username, role
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    return dict(user) if user else None