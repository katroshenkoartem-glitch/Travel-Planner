from fastapi import FastAPI
from app.core.lifespan import lifespan

app = FastAPI(title="Travel Planner API", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "API is running"}
