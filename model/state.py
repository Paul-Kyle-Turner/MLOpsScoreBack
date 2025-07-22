from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field


def str_uuid() -> str:
    return str(uuid.uuid4())


class StateBase(BaseModel):
    """Base state model with common fields."""
    state: str = Field(
        max_length=512,
        description="State data as string",
        default_factory=str_uuid
    )


class State(StateBase):
    """Complete state model including database fields."""
    id: Optional[int] = Field(
        description="Unique identifier for the state entry"
    )
    created_at: datetime = Field(
        description="Timestamp when the state was created"
    )

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
