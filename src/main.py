from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import event_request, event_task, staff_request, financial_request

app = FastAPI()

# Configure CORS
origins = [
    "*",  # Allow all origins for simplicity; adjust as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_request.router)
app.include_router(event_task.router)
app.include_router(staff_request.router)
app.include_router(financial_request.router)


@app.get("/")
async def root():
    return {"message": "Welcome to SEP Business !"}

@app.get("/health")
async def health():
    return {"status": "ok"}
