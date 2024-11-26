from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import tools_condition
from src.state.assistant import State, Assistant
from src.state.error_handling import create_tool_node_with_fallback
from src.tools import safe_tools, sensitive_tools, sensitive_tool_names
from src.tools.user_info import fetch_user_information
from src.utils.prompt_templates import get_primary_assistant_prompt


llm = ChatOpenAI(model="gpt-4o")
primary_assistant_prompt = get_primary_assistant_prompt()
assistant_runnable = primary_assistant_prompt | llm.bind_tools(safe_tools + sensitive_tools)

builder = StateGraph(State)


def user_info(state: State):
    return {"user_info": fetch_user_information.invoke({})}


# Define nodes: these do the work
builder.add_node("fetch_user_info", user_info)
builder.add_edge(START, "fetch_user_info")
builder.add_node("assistant", Assistant(assistant_runnable))
builder.add_node("safe_tools", create_tool_node_with_fallback(safe_tools))
builder.add_node("sensitive_tools", create_tool_node_with_fallback(sensitive_tools))

# Define edges: these determine how the control flow moves
builder.add_edge("fetch_user_info", "assistant")


def route_tools(state: State):
    next_node = tools_condition(state)
    # If no tools are invoked, return to the user
    if next_node == END:
        return END
    ai_message = state["messages"][-1]
    # This assumes single tool calls. To handle parallel tool calling, you'd want to
    # use an ANY condition
    first_tool_call = ai_message.tool_calls[0]
    if first_tool_call["name"] in sensitive_tool_names:
        return "sensitive_tools"
    return "safe_tools"


builder.add_conditional_edges("assistant", route_tools, ["safe_tools", "sensitive_tools", END])
builder.add_edge("safe_tools", "assistant")
builder.add_edge("sensitive_tools", "assistant")

# The checkpointer lets the graph persist its state
# this is a complete memory for the entire graph.
memory = MemorySaver()
user_approval_graph = builder.compile(
    checkpointer=memory,
    # NEW: The graph will always halt before executing the "tools" node.
    # The user can approve or reject (or even alter the request) before
    # the assistant continues
    interrupt_before=["sensitive_tools"],
)
