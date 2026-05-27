from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.place import PlaceCreate, PlaceUpdate, PlaceResponse
from app.repositories.place import place_repo
from app.services.place import PlaceService

project_places_router = APIRouter(
    prefix="/projects/{project_id}/places", tags=["Project Places"]
)


@project_places_router.post(
    "/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED
)
async def add_place_to_project(
    project_id: int, place_in: PlaceCreate, db: AsyncSession = Depends(get_db)
):
    return await PlaceService.create_place(db, project_id, place_in)


@project_places_router.get("/", response_model=List[PlaceResponse])
async def list_project_places(project_id: int, db: AsyncSession = Depends(get_db)):
    return await place_repo.get_by_project_id(db, project_id)


places_router = APIRouter(prefix="/places", tags=["Places"])


@places_router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(place_id: int, db: AsyncSession = Depends(get_db)):
    place = await place_repo.get(db, place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@places_router.patch("/{place_id}", response_model=PlaceResponse)
async def update_place(
    place_id: int, place_in: PlaceUpdate, db: AsyncSession = Depends(get_db)
):
    return await PlaceService.update_place(db, place_id, place_in)
