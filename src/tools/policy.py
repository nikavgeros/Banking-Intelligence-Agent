import openai
from langchain_core.tools import tool
from src.utils.policy import fetch_policy_text_from_file, split_policies_into_chunks
from src.retrievers import VectorStoreRetriever
from src.config.settings import load_env

# Load environment variables from a .env file
env_vars = load_env()

# Read banking policies
policy_text = fetch_policy_text_from_file(file_path="banking-policies.md")

# Split policies into chunks for retrieval
docs = split_policies_into_chunks(policy_text)

# Initialize the VectorStoreRetriever using documents and an OpenAI client to generate embeddings
retriever = VectorStoreRetriever.from_docs(docs, openai.Client())


# Assistant Tools
@tool
def lookup_policy(query: str) -> str:
    """Consult the banking policies or terms and conditions to check regulations, eligibility, or account features.
    Use this for questions related to banking services or fees."""
    docs = retriever.query(query, k=2)
    return "\n\n".join([doc["page_content"] for doc in docs])
