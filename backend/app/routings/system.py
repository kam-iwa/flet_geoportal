import os

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
    
@router.get("/token")
async def get_token(
        admin_name: str,
        admin_password: str,
        db = Depends(get_db)
) -> JSONResponse:
    if admin_name != os.getenv("ADMIN_LOGIN"):
        return JSONResponse(content = {"error": "Invalid login or password"}, status_code=400)

    return JSONResponse(content = {"token": "###"}, status_code = 200)