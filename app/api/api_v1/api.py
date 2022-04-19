from fastapi import APIRouter

from app.api.api_v1.endpoints import bodies

api_router = APIRouter()

api_router.include_router(bodies.router, prefix="/bodies", tags=["bodies"])
