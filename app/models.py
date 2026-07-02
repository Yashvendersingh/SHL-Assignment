"""Pydantic models for the SHL Assessment Recommendation Agent API."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Message(BaseModel):
    """A single message in the conversation history."""
    role: str = Field(..., pattern=r"^(user|assistant)$", description="Either 'user' or 'assistant'")
    content: str = Field(..., min_length=1, max_length=4000, description="Message text")


class ChatRequest(BaseModel):
    """Request body for POST /chat."""
    messages: list[Message] = Field(
        ...,
        min_length=1,
        max_length=16,  # 8 turns = 16 messages max
        description="Conversation history in chronological order",
    )


class Recommendation(BaseModel):
    """A single SHL assessment recommendation."""
    name: str = Field(..., description="Product name from the SHL catalog")
    url: str = Field(..., description="Product URL from the SHL catalog")
    test_type: str = Field(..., description="Assessment category (e.g. Ability & Aptitude)")


class ChatResponse(BaseModel):
    """Response body for POST /chat."""
    reply: str = Field(..., description="Agent reply text")
    recommendations: list[Recommendation] = Field(
        default_factory=list,
        max_length=10,
        description="0 items while clarifying, 1-10 when recommending",
    )
    end_of_conversation: bool = Field(
        default=False,
        description="True only when the agent considers the task complete",
    )


class HealthResponse(BaseModel):
    """Response body for GET /health."""
    status: str = "ok"
