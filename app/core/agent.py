from typing import Annotated, TypedDict

from langchain.chat_models import init_chat_model
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from app.core.tools import search_tavily


class State(TypedDict):
    messages: Annotated[list, add_messages]


def get_agent_executor():
    # Define tools
    tools = [search_tavily]
    tool_node = ToolNode(tools)

    # Initialize model and bind tools
    model = init_chat_model("gpt-4o-mini", model_provider="openai").bind_tools(tools)

    # Define node
    def call_model(state: State):
        messages = state["messages"]
        response = model.invoke(messages)
        return {"messages": [response]}

    # Build graph
    workflow = StateGraph(State)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", tools_condition)
    workflow.add_edge("tools", "agent")

    return workflow.compile()
