import sqlite3


def setup(db_path: str = "db/traders.db", print_info: bool = True, dont_close_conn: bool = False):
    if print_info: print("[setup_db] Setting up the database...")
    conn = sqlite3.connect(db_path)

    conn.execute(
        """
    CREATE TABLE IF NOT EXISTS traders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        low_grade_balance INTEGER NOT NULL DEFAULT 0,
        medium_grade_balance INTEGER NOT NULL DEFAULT 0,
        high_grade_balance INTEGER NOT NULL DEFAULT 0
    )
    """
    )

    if print_info: print("[setup_db] Table 'traders' created successfully.")
    if not dont_close_conn: conn.close()
