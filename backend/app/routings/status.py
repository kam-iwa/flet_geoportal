from fastapi import APIRouter, Depends
from sqlalchemy import text
from starlette.responses import JSONResponse

from database import get_db

router = APIRouter()

@router.get("/status")
async def get_status(db = Depends(get_db)) -> JSONResponse:
    try:
        await db.execute(text("SELECT 1;"))
        return JSONResponse(content = {"status": "OK"}, status_code=200)
    except Exception as e:
        return JSONResponse(content = {"status": f"{e.args}"}, status_code=400)