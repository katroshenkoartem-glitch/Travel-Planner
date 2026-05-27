from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.repositories.project import project_repo
from app.services.project import ProjectService
from app.services.place import PlaceService
from app.models.project import Project

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project_in: ProjectCreate, db: AsyncSession = Depends(get_db)):
    try:
        project_data = project_in.model_dump(exclude={"places"})
        db_project = Project(**project_data)
        db.add(db_project)
        await db.flush()

        if project_in.places:
            for place_in in project_in.places:
                await PlaceService.create_place(db, db_project.id, place_in)

        await db.commit()
        await db.refresh(db_project)
        return db_project
    except HTTPException:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    return await project_repo.get_all(db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await project_repo.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int, project_in: ProjectUpdate, db: AsyncSession = Depends(get_db)
):
    project = await project_repo.get(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    updated_project = await project_repo.update(db, project, project_in)
    await db.commit()
    return updated_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    await ProjectService.delete_project(db, project_id)
