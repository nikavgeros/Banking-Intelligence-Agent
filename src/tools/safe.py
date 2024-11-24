from langchain_community.tools.tavily_search import TavilySearchResults
from .accounts import fetch_user_accounts
from .fraud_alerts import fetch_user_fraud_alerts
from .loans import fetch_user_loans
from .payments import fetch_user_recurring_payments
from .policy import lookup_policy
from .user_info import fetch_user_information


# Define the tools to be used
safe_tools = [
    TavilySearchResults(max_results=1),
    lookup_policy,
    fetch_user_information,
    fetch_user_accounts,
    fetch_user_loans,
    fetch_user_fraud_alerts,
    fetch_user_recurring_payments,
]
