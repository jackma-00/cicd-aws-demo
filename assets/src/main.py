from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from src.routers import event_request, event_task, staff_request, financial_request

app = FastAPI()


app.include_router(event_request.router)
app.include_router(event_task.router)
app.include_router(staff_request.router)
app.include_router(financial_request.router)


@app.get("/")
async def root():
    return {"message": "Spoon is the best Java code analyzer"}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/hello")
async def hello():
    # obtaib the environment variable SHA
    sha = os.getenv("SHA")

    return {"message": "Hello from commit " + sha}
