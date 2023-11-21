import sqlite3
from typing import Union

from econ_types.trader import Trader


def create_trader(trader_instance, conn: sqlite3.Connection = None) -> None:
    user_id = trader_instance.user_id
    low_grade_balance = trader_instance.low_grade_balance
    medium_grade_balance = trader_instance.medium_grade_balance
    high_grade_balance = trader_instance.high_grade_balance

    conn = conn or sqlite3.connect("data/traders.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO traders (user_id, low_grade_balance, medium_grade_balance, high_grade_balance) VALUES (?, ?, ?, ?)",
        (user_id, low_grade_balance, medium_grade_balance, high_grade_balance),
    )

    conn.commit()
    cursor.close()
    


def get_trader(user_id, conn: sqlite3.Connection = None) -> Union[Trader, bool]:
    """Returns type Trader if successful, else it returns a bool False."""
    conn = conn or sqlite3.connect("data/traders.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM traders WHERE user_id=?", (user_id,))
    result = cursor.fetchone()

    cursor.close()
    

    if result:
        trader: Trader = Trader(
            user_id=user_id,
            bal_low_grade=result[2],
            bal_medium_grade=result[3],
            bal_high_grade=result[4],
        )

        return trader
    return False


def update_trader(user_id, conn: sqlite3.Connection = None, **kwargs) -> Union[bool, str]:
    """Returns bool True if successful, else it returns a string with the error."""
    try:
        conn = conn or sqlite3.connect("data/traders.db")
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info(traders)")
        field_names = [row[1] for row in cursor.fetchall()]

        if not set(kwargs.keys()).issubset(set(field_names)):
            return "Invalid field(s) provided."

        set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])

        values = tuple(kwargs.values()) + (user_id,)

        cursor.execute(f"UPDATE traders SET {set_clause} WHERE user_id=?", values)

        conn.commit()
        cursor.close()
        

        return True
    except Exception as e:
        print(e)
        return e


def delete_trader(user_id, conn: sqlite3.Connection = None) -> Union[bool, str]:
    """Returns bool True if successful, else it returns a string with the error."""
    try:
        conn = conn or sqlite3.connect("data/traders.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM traders WHERE user_id=?", (user_id,))

        conn.commit()
        cursor.close()
        

        return True
    except Exception as e:
        print(e)
        return e


def reset_trader_all_balances(
    user_id, conn: sqlite3.Connection = None
) -> Union[bool, str]:
    """Returns bool True if successful, else it returns a string with the error."""
    try:
        conn = conn or sqlite3.connect("data/traders.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE traders SET low_grade_balance = 0, medium_grade_balance = 0, high_grade_balance = 0 WHERE user_id=?",
            (user_id,),
        )

        conn.commit()
        cursor.close()
        

        return True
    except Exception as e:
        print(e)
        return e


def reset_trader_grade_balance(user_id, grade_type, conn: sqlite3.Connection = None) -> Union[bool, str]:
    """Returns bool True if successful, else it returns a string with the error."""
    try:
        conn = conn or sqlite3.connect("data/traders.db")
        cursor = conn.cursor()

        valid_grade_types = [
            "low_grade_balance",
            "medium_grade_balance",
            "high_grade_balance",
        ]
        if grade_type not in valid_grade_types:
            return "Invalid grade type provided."

        cursor.execute(
            f"UPDATE traders SET {grade_type} = 0 WHERE user_id=?", (user_id,)
        )

        conn.commit()
        cursor.close()
        

        return True
    except Exception as e:
        print(e)
        return e


def execute_raw_sql(sql_string: str, conn: sqlite3.Connection = None, fetch: bool = False) -> Union[bool, str, None]:
    """Returns bool True if successful, else it returns a string with the error. If fetch is True, returns the output."""
    try:
        conn = conn or sqlite3.connect("data/traders.db")
        cursor = conn.cursor()

        cursor.execute(sql_string)

        if fetch:
            result = cursor.fetchall()
            cursor.close()
            return result

        conn.commit()
        cursor.close()
        return True

    except Exception as e:
        return str(e)
