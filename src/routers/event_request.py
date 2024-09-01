from typing import Annotated

from fastapi import APIRouter, Depends

from src.persistence.data_manager import dataManager
from src.models.requests import EventRequest
from src.utils.auth import auth_customer_service, auth_customer_manager


router = APIRouter()

# Configure CORS
origins = [
    "*",  # Allow all origins for simplicity; adjust as needed
]

router.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Starting HTTP RESTful API Server ...")


@router.get("/hello_well")
async def hello_well():
    return {"message": "Hello, Well!"}


@router.post("/event_requests/")
async def new_event_request(
    newRequest: EventRequest,
    # authorized: Annotated[bool, Depends(auth_customer_service)],
):
    dataManager.add_event_request(newRequest)
    return {"record_number": newRequest.record_number}


@router.get("/event_requests/")
async def get_event_requests(
    authorized: Annotated[bool, Depends(auth_customer_manager)]
):
    return {"event_requests": dataManager.get_event_requests()}


@router.get("/event_requests/{record_number}")
async def get_event_request(
    record_number: str, authorized: Annotated[bool, Depends(auth_customer_manager)]
):
    return {"event_request": dataManager.get_event_request(record_number)}


@router.delete("/event_requests/{record_number}")
async def discard_event_request(
    record_number: str, authorized: Annotated[bool, Depends(auth_customer_manager)]
):
    dataManager.delete_event_request(record_number)
    return {"discard": "ok"}
