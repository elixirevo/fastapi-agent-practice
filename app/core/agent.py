from typing import Annotated, TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.messages import SystemMessage
from app.core.tools import search_tavily, save_user_interest, get_user_interests


class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: str


def get_agent_executor():
    # Define tools
    tools = [search_tavily, save_user_interest, get_user_interests]
    tool_node = ToolNode(tools)

    # Initialize model and bind tools
    model = init_chat_model("gpt-4o-mini", model_provider="openai").bind_tools(tools)

    # Define node
    def call_model(state: State):
        messages = state["messages"]
        user_id = state.get("user_id", "anonymous")
        
        system_prompt = SystemMessage(content=(
            f"You are a helpful AI assistant. The current user's ID is '{user_id}'.\n"
            "Your main task is to deliver personalized latest updates based on the user's interests.\n"
            "When the user asks for updates, hobbies, or latest news, you MUST:\n"
            f"1. Use the `get_user_interests` tool to retrieve their interests for user_id='{user_id}'.\n"
            "2. If interests are found, use the `search_tavily` tool to search for the latest information/news related to those interests.\n"
            "3. Finally, summarize the search results and present them to the user in a friendly manner.\n\n"
            "If they mention new interests or changes to their interests, use the `save_user_interest` tool to save them."
        ))
        
        response = model.invoke([system_prompt] + messages)
        return {"messages": [response]}

    # Build graph
    workflow = StateGraph(State)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    return workflow.compile()
