from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.project import project_repo
from app.repositories.place import place_repo


class ProjectService:

    @staticmethod
    async def delete_project(db: AsyncSession, project_id: int):
        try:
            project = await project_repo.get(db, project_id)
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")

            places = await place_repo.get_by_project_id(db, project_id)
            if any(p.is_visited for p in places):
                raise HTTPException(
                    status_code=400,
                    detail="Cannot delete project: it contains visited places",
                )

            await project_repo.delete(db, project_id)
            await db.commit()
            return project
        except HTTPException:
            await db.rollback()
            raise
        except Exception as e:
            await db.rollback()
            raise HTTPException(
                status_code=500, detail=f"Internal Server Error: {str(e)}"
            )
