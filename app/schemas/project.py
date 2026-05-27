from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import date
from .place import PlaceCreate, PlaceResponse


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    places: Optional[List[PlaceCreate]] = Field(default=[], max_length=10)


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class ProjectResponse(ProjectBase):
    id: int
    is_completed: bool
    places: List[PlaceResponse] = []

    model_config = ConfigDict(from_attributes=True)
