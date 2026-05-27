from pydantic import BaseModel, ConfigDict
from typing import Optional


class PlaceBase(BaseModel):
    external_id: str


class PlaceCreate(PlaceBase):
    notes: Optional[str] = None


class PlaceUpdate(BaseModel):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None


class PlaceResponse(PlaceBase):
    id: int
    project_id: int
    notes: Optional[str] = None
    is_visited: bool

    model_config = ConfigDict(from_attributes=True)
