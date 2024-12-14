# workflows/state_management.py
from typing import Annotated
from langgraph.graph.message import AnyMessage, add_messages
from typing_extensions import TypedDict
from pydantic import BaseModel, Field


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to the user based on the query results."""

    final_answer: str = Field(..., description="The final answer to the user")
