from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.place import Place
from app.schemas.project import PlaceCreate
from app.schemas.place import PlaceUpdate


class PlaceRepository(BaseRepository[Place, PlaceCreate, PlaceUpdate]):

    async def get_by_project_id(self, db: AsyncSession, project_id: int) -> List[Place]:
        query = select(self.model).where(self.model.project_id == project_id)
        result = await db.execute(query)
        return list(result.scalars().all())


place_repo = PlaceRepository(Place)
