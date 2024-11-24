import sqlite3
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables import RunnableConfig
from src.db.functions import get_db

db = get_db()


@tool
def create_transaction(config: RunnableConfig, to_user_id: int, amount: float, description: str = "") -> str:
    """
    Create a transaction from one user to another.

    Args:
        config (RunnableConfig): Configuration for the tool.
        to_user_id (int): The ID of the recipient user.
        amount (float): The transaction amount.
        description (str): A description for the transaction.

    Returns:
        str: A confirmation message indicating the transaction status.

    Raises:
        ValueError: If any account has insufficient funds or the user IDs are invalid.
    """
    configuration = config.get("configurable", {})
    user_id = configuration.get("user_id", None)
    if not user_id:
        raise ValueError("No user ID configured.")

    if amount <= 0:
        raise ValueError("Transaction amount must be greater than zero.")

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Fetch the sender's account
    cursor.execute(
        "SELECT account_id, account_balance FROM Accounts WHERE user_id = ? AND account_type = 'Checking' LIMIT 1",
        (user_id,),
    )
    from_account = cursor.fetchone()

    if not from_account:
        raise ValueError(f"User with ID {user_id} does not have a Checking account.")

    from_account_id, from_balance = from_account

    if from_balance < amount:
        raise ValueError("Insufficient funds in the sender's account.")

    # Fetch the recipient's account
    cursor.execute(
        "SELECT account_id FROM Accounts WHERE user_id = ? AND account_type = 'Checking' LIMIT 1",
        (to_user_id,),
    )
    to_account = cursor.fetchone()

    if not to_account:
        raise ValueError(f"User with ID {to_user_id} does not have a Checking account.")

    to_account_id = to_account[0]

    # Deduct the amount from the sender's account
    new_from_balance = from_balance - amount
    cursor.execute("UPDATE Accounts SET account_balance = ? WHERE account_id = ?", (new_from_balance, from_account_id))

    # Add the amount to the recipient's account
    cursor.execute("SELECT account_balance FROM Accounts WHERE account_id = ?", (to_account_id,))
    to_balance = cursor.fetchone()[0]
    new_to_balance = to_balance + amount
    cursor.execute("UPDATE Accounts SET account_balance = ? WHERE account_id = ?", (new_to_balance, to_account_id))

    # Record the transaction
    cursor.execute(
        """
        INSERT INTO Transactions (account_id, transaction_type, amount, description)
        VALUES (?, 'Debit', ?, ?)
        """,
        (from_account_id, amount, description or f"Transfer to user {to_user_id}"),
    )
    cursor.execute(
        """
        INSERT INTO Transactions (account_id, transaction_type, amount, description)
        VALUES (?, 'Credit', ?, ?)
        """,
        (to_account_id, amount, description or f"Transfer from user {user_id}"),
    )

    # Commit changes and close connection
    conn.commit()
    conn.close()

    return f"Transaction of {amount} from User {user_id} to User {to_user_id} completed successfully."
