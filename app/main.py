from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.routers.project import router as project_router
from app.routers.place import project_places_router, places_router

app = FastAPI(title="Travel Planner API", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "API is running"}


app.include_router(project_router)
app.include_router(project_places_router)
app.include_router(places_router)
