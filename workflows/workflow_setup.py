# workflows/workflow_setup.py
from typing import Any, Literal
from langchain_core.messages import ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda, RunnableWithFallbacks
from workflows.state_management import State
from tools.db_tools import (
    list_tables_tool,
    get_schema_tool,
    db_query_tool,
    first_tool_call,
    model_check_query,
    query_gen_node,
)


def handle_tool_error(state: State) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> RunnableWithFallbacks[Any, dict]:
    """
    Create a ToolNode with a fallback to handle errors and surface them to the agent.
    """
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def should_continue(state: State) -> Literal[END, "correct_query", "query_gen"]:
    messages = state["messages"]
    last_message = messages[-1]
    if getattr(last_message, "tool_calls", None):
        return END
    if last_message.content.startswith("Error:"):
        return "query_gen"
    else:
        return "correct_query"


def setup_workflow():
    workflow = StateGraph(State)

    # Workflow nodes
    workflow.add_node("first_tool_call", first_tool_call)
    workflow.add_node(
        "list_tables_tool", create_tool_node_with_fallback([list_tables_tool])
    )

    model_get_schema = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(
        [get_schema_tool]
    )
    workflow.add_node(
        "model_get_schema",
        lambda state: {"messages": [model_get_schema.invoke(state["messages"])]},
    )
    workflow.add_node(
        "get_schema_tool", create_tool_node_with_fallback([get_schema_tool])
    )
    workflow.add_node("query_gen", query_gen_node)
    workflow.add_node("correct_query", model_check_query)
    workflow.add_node("execute_query", create_tool_node_with_fallback([db_query_tool]))

    # Define workflow edges
    workflow.add_edge(START, "first_tool_call")
    workflow.add_edge("first_tool_call", "list_tables_tool")
    workflow.add_edge("list_tables_tool", "model_get_schema")
    workflow.add_edge("model_get_schema", "get_schema_tool")
    workflow.add_edge("get_schema_tool", "query_gen")
    workflow.add_conditional_edges("query_gen", should_continue)
    workflow.add_edge("correct_query", "execute_query")
    workflow.add_edge("execute_query", "query_gen")

    return workflow.compile()
