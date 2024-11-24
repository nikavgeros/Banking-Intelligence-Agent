import os
from dotenv import load_dotenv
import uuid


def load_env() -> dict:
    """Load environment variables from a .env file."""
    load_dotenv()

    # Access environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY")
    tavily_api_key = os.getenv("TAVILY_API_KEY")

    if not openai_api_key or not tavily_api_key:
        raise ValueError("Missing required environment variables. Please check your .env file.")

    return {"openai_api_key": openai_api_key, "tavily_api_key": tavily_api_key}


def load_config(user_id: str) -> dict:

    # Update with the backup file so we can restart from the original place in each section
    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            # The user_id is used in our banking tools to
            # fetch the user's flight information
            "user_id": user_id,
            # Checkpoints are accessed by thread_id
            "thread_id": thread_id,
        }
    }

    return config
