from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class CriminalResponse(BaseModel):
    id: int
    name: str | None
    nickname: str
    reward: float
    last_coordinates: str | None
    last_location_note: str | None
    difficulty: int
    armed: bool
    has_crew: bool
    escape_master: bool

    model_config = ConfigDict(from_attributes=True)


class HuntLogCreate(BaseModel):
    criminal_id: int
    success: bool
    notes: str | None = None


class HuntLogUpdate(BaseModel):
    success: bool | None = None
    notes: str | None = None


class HuntLogResponse(BaseModel):
    id: int
    criminal_id: int
    success: bool
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)