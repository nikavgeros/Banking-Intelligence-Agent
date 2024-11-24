from .fraud_alerts import resolve_user_fraud_alert
from .transactions import create_transaction


sensitive_tools = [
    resolve_user_fraud_alert,
    create_transaction,
]
sensitive_tool_names = {t.name for t in sensitive_tools}
