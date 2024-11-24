from src.db import initialize_database
from src.state.state_graph import user_approval_graph
from src.utils.event_printer import run_sample_questions
from src.config.settings import load_config


if __name__ == "__main__":

    # Initialize database
    print("Initializing the banking database...")
    initialize_database()

    # Load configuration
    user_id = "1"  # Example user ID for testing
    config = load_config(user_id=user_id)

    # Sample user queries
    user_questions = [
        # Discovering Accounts and Balances
        "Hi there, what accounts do I have with your system?",
        "Please send $50 to user id 2",
        "Could you list all the accounts associated with me, along with their balances after the transaction?",
        # Tracking Payments and Alerts
        "What recurring payments are currently active for me?",
        "I noticed there are some alerts on my account. Can you check if they're resolved?",
        "Please resolve all active alerts on my account.",
        "Have the alerts on my account been resolved?",
        # Managing Loans
        "Can you fetch all the loan details and tell me their current status?",
        "Are there any pending loan applications under my name?",
        "What options do I have if I want to apply for a new loan?",
        # Understanding Policies and Fees
        "What is the minimum credit score required to be eligible for a loan?",
        "Is there a fee for closing a checking account?",
        "How much liability will I have for unauthorized transactions if I report them within 2 business days?",
        # Exploring System Features
        "Can you give me all the accounts associated with user id 2?",
        # Web Retrieval
        "What are the current interest rates for savings accounts offered by major banks?",
    ]

    # Process sample questions
    print("\nStarting Banking Intelligence Agent...")
    run_sample_questions(user_approval_graph, config, user_questions)
