from fastapi import APIRouter
from app.core.config import APP_VERSION

router = APIRouter()

@router.get("/version")
def version():
    return {"version": APP_VERSION}

