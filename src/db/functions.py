import os
import sqlite3


def get_db():
    return "bank.db"


def create_bank_database(db_name):
    """
    Create a SQLite database with tables for a bank system.

    Args:
        db_name (str): The name of the database file.
    """
    # Delete the database if it already exists
    if os.path.exists(db_name):
        os.remove(db_name)

    # Connect to the database (creates the file if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the Users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    # Create the Accounts table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Accounts (
            account_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            account_type TEXT NOT NULL,  -- e.g., Savings, Checking
            account_balance REAL NOT NULL,
            currency TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """
    )

    # Create the Transactions table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL,  -- e.g., Credit, Debit
            amount REAL NOT NULL,
            transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
        )
        """
    )

    # Create the Loans table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Loans (
            loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            loan_type TEXT NOT NULL,  -- e.g., Personal, Mortgage
            loan_amount REAL NOT NULL,
            loan_status TEXT NOT NULL DEFAULT 'Pending',  -- e.g., Pending, Approved, Rejected
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """
    )

    # Create the Fraud Alerts table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS FraudAlerts (
            alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            alert_description TEXT NOT NULL,
            alert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved INTEGER DEFAULT 0,  -- 0 for unresolved, 1 for resolved
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """
    )

    # Create the Recurring Payments table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS RecurringPayments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            due_date DATE NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
        )
        """
    )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print(f"Database '{db_name}' and tables created successfully.")


def insert_mock_data(db_name):
    """
    Insert mock data into the SQLite database tables.

    Args:
        db_name (str): The name of the database file.
    """
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Insert mock data into the Users table
    cursor.execute(
        """
        INSERT INTO Users (full_name, email, phone_number, hashed_password) 
        VALUES 
            ('John Doe', 'john.doe@example.com', '1234567890', 'hashed_password_123'),
            ('Jane Smith', 'jane.smith@example.com', '0987654321', 'hashed_password_456')
        """
    )

    # Insert mock data into the Accounts table
    cursor.execute(
        """
        INSERT INTO Accounts (user_id, account_type, account_balance, currency) 
        VALUES 
            (1, 'Checking', 1500.00, 'USD'),
            (1, 'Savings', 5000.00, 'USD'),
            (2, 'Checking', 250.00, 'EUR'),
            (2, 'Savings', 1200.00, 'EUR')
        """
    )

    # Insert mock data into the Transactions table
    cursor.execute(
        """
        INSERT INTO Transactions (account_id, transaction_type, amount, description) 
        VALUES 
            (1, 'Credit', 1000.00, 'Paycheck deposit'),
            (1, 'Debit', 200.00, 'Grocery shopping'),
            (1, 'Debit', 50.00, 'Coffee shop'),
            (2, 'Credit', 250.00, 'Birthday gift'),
            (3, 'Debit', 100.00, 'Online shopping'),
            (4, 'Credit', 500.00, 'Freelance work')
        """
    )

    # Insert mock data into the Loans table
    cursor.execute(
        """
        INSERT INTO Loans (user_id, loan_type, loan_amount, loan_status) 
        VALUES 
            (1, 'Personal', 10000.00, 'Approved'),
            (1, 'Mortgage', 250000.00, 'Pending'),
            (2, 'Car Loan', 15000.00, 'Rejected')
        """
    )

    # Insert mock data into the Fraud Alerts table
    cursor.execute(
        """
        INSERT INTO FraudAlerts (user_id, alert_description, resolved) 
        VALUES 
            (1, 'Suspicious login detected', 0),
            (2, 'Unusual transaction on Checking account', 1)
        """
    )

    # Insert mock data into the Recurring Payments table
    cursor.execute(
        """
        INSERT INTO RecurringPayments (user_id, amount, due_date, description) 
        VALUES 
            (1, 1200.00, '2024-12-01', 'Monthly rent'),
            (2, 50.00, '2024-12-05', 'Streaming service subscription')
        """
    )

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    print("Mock data inserted successfully.")


def initialize_database():
    """
    Sets up the database by creating the schema and inserting mock data.
    """
    db = get_db()
    create_bank_database(db_name=db)
    insert_mock_data(db_name=db)
