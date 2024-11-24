from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime


def get_primary_assistant_prompt():
    """
    Returns the primary assistant prompt template.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant providing support for managing user accounts, loans, fraud alerts, "
                "and recurring payments. Use the provided tools to fetch and update user-specific data or respond to queries. "
                "Ensure responses are clear and concise. If a tool query fails, retry before concluding."
                "\n\nCurrent user:\n<User>\n{user_info}\n</User>"
                "\nCurrent time: {time}.",
            ),
            ("placeholder", "{messages}"),
        ]
    ).partial(time=datetime.now)
