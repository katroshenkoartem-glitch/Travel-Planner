from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.place import place_repo
from app.repositories.project import project_repo
from app.schemas.project import PlaceCreate
from app.schemas.place import PlaceUpdate
from app.services.chicago_api import ChicagoAPIClient


class PlaceService:

    @staticmethod
    async def create_place(db: AsyncSession, project_id: int, place_in: PlaceCreate):
        try:
            project = await project_repo.get(db, project_id)
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")

            current_places = await place_repo.get_by_project_id(db, project_id)
            if len(current_places) >= 10:
                raise HTTPException(
                    status_code=400, detail="Maximum 10 places per project allowed"
                )

            if any(p.external_id == place_in.external_id for p in current_places):
                raise HTTPException(
                    status_code=400, detail="Place already exists in this project"
                )

            is_valid = await ChicagoAPIClient.check_place_exists(place_in.external_id)
            if not is_valid:
                raise HTTPException(
                    status_code=400,
                    detail="Place not found in Chicago Art Institute API",
                )

            place_data = place_in.model_dump()
            place_data["project_id"] = project_id

            db_place = place_repo.model(**place_data)
            db.add(db_place)
            await db.flush()
            await db.refresh(db_place)

            await db.commit()
            return db_place
        except HTTPException:
            await db.rollback()
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Internal Server Error: {str(e)}"
            )

    @staticmethod
    async def update_place(db: AsyncSession, place_id: int, place_in: PlaceUpdate):
        try:
            place = await place_repo.get(db, place_id)
            if not place:
                raise HTTPException(status_code=404, detail="Place not found")

            updated_place = await place_repo.update(db, place, place_in)

            if place_in.is_visited:
                project_places = await place_repo.get_by_project_id(
                    db, updated_place.project_id
                )
                if all(p.is_visited for p in project_places):
                    project = await project_repo.get(db, updated_place.project_id)
                    project.is_completed = True
                    db.add(project)

            await db.commit()
            return updated_place
        except HTTPException:
            await db.rollback()
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Internal Server Error: {str(e)}"
            )
