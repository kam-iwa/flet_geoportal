from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter()

@router.get("/status")
async def get_status() -> JSONResponse:
    return JSONResponse(content = {"status": "OK"}, status_code=200)