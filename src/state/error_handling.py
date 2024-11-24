from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode


def handle_tool_error(state) -> dict:
    """
    Handles errors that occur during tool execution and formats error messages.

    Args:
        state (dict): The current state of the graph.

    Returns:
        dict: A dictionary containing error messages to be displayed to the user.
    """
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\nPlease fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    """
    Creates a ToolNode with a fallback mechanism for error handling.

    Args:
        tools (list): A list of tools to be included in the node.

    Returns:
        dict: A ToolNode with a fallback handler for errors.
    """
    return ToolNode(tools).with_fallbacks([RunnableLambda(handle_tool_error)], exception_key="error")
