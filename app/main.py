import uvicorn
from fastapi import FastAPI

from app.api.api import api_router
from app.db.db import engine
from app.models import customers


app = FastAPI(title="Zenskar", description="Two-Way Integrations")


def create_tables():
    """
    This can futher moved to a new initialization file, if we have more tables to create
    """
    customers.Base.metadata.create_all(bind=engine)


app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    create_tables()


@app.get("/")
async def read_root():
    return {"Hello": "W0rld"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
