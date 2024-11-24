import re
from typing import List, Dict


def fetch_policy_text_from_file(file_path: str) -> str:
    """
    Fetch the policy text from a local file.

    Args:
        file_path (str): Local path to the policy document.

    Returns:
        str: The content of the policy document.

    Raises:
        FileNotFoundError: If the local file is not found.
    """
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Local file not found: {file_path}") from e


def split_policies_into_chunks(policy_text: str) -> List[Dict[str, str]]:
    """
    Split the policy text into chunks for easier retrieval.

    Args:
        policy_text (str): The full text of the policy document.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing a chunk of the policy text.
                              Each dictionary has a single key "page_content" with the chunk as its value.
    """
    # Split the text into chunks using a regular expression to detect headings (e.g., starting with "##")
    return [{"page_content": txt.strip()} for txt in re.split(r"(?=\n##)", policy_text) if txt.strip()]
