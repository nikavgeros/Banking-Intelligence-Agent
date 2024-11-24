import sqlite3
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables import RunnableConfig
from src.state.assistant import State
from src.db.functions import get_db

db = get_db()


@tool
def fetch_user_information(config: RunnableConfig) -> dict:
    """Fetch information about the currently signed-in user."""
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "SELECT * FROM Users WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    row = cursor.fetchone()
    column_names = [column[0] for column in cursor.description]
    result = dict(zip(column_names, row)) if row else {}

    cursor.close()
    conn.close()

    return result


@tool
def fetch_user_accounts(config: RunnableConfig) -> list[dict]:
    """Fetch all accounts for the currently signed-in user."""
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "SELECT * FROM Accounts WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def fetch_user_loans(config: RunnableConfig) -> list[dict]:
    """Fetch all loans for the currently signed-in user."""
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "SELECT * FROM Loans WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def fetch_user_fraud_alerts(config: RunnableConfig) -> list[dict]:
    """Fetch all fraud alerts for the currently signed-in user."""
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "SELECT * FROM FraudAlerts WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def fetch_user_recurring_payments(config: RunnableConfig) -> list[dict]:
    """Fetch all recurring payments for the currently signed-in user."""
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "SELECT * FROM RecurringPayments WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()
    column_names = [column[0] for column in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return results


@tool
def resolve_user_fraud_alert(alert_id: int, config: RunnableConfig) -> str:
    """Resolve a fraud alert for the currently signed-in user."""
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "UPDATE FraudAlerts SET resolved = 1 WHERE alert_id = ? AND user_id = ?"
    cursor.execute(query, (alert_id, user_id))
    conn.commit()

    cursor.close()
    conn.close()

    return "Fraud alert resolved successfully."
