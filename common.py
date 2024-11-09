import os
import sqlite3


def init_db():
    # File path
    user_profile = os.environ["USERPROFILE"]
    documents_dir = os.path.join(user_profile, "Documents")
    db_path = os.path.join(documents_dir, "QuickTextInput.db")

    # Connect to database
    conn = sqlite3.connect(db_path, autocommit=True)
    conn.execute("PRAGMA foreign_keys=ON")

    # Initialize tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    if len(tables) == 0:
        cursor.execute(
            """
        CREATE TABLE words (
            word TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        ) STRICT;
        """
        )

    return conn
