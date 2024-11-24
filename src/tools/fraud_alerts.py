import sqlite3
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables import RunnableConfig
from src.db.functions import get_db


db = get_db()


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