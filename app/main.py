import uvicorn
from fastapi import FastAPI
from app.api.api import api_router
from app.db.db import engine
from app.models import customers


app = FastAPI(title="Zenskar", description="Two-Way Integrations")


def create_tables():
    print("Creating tables")
    customers.Base.metadata.create_all(bind=engine)


app.include_router(api_router)


@app.on_event("startup")
async def startup_event():
    create_tables()


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     """
#     A middleware that handles the lifespan events.
#     This approach aligns with the latest FastAPI practices as suggested in the documentation.
#     """
#     response = await call_next(request)
#     return response


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
