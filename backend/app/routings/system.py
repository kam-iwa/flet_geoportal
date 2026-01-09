import os

from fastapi import APIRouter, Depends
from sqlalchemy import text
from starlette.responses import JSONResponse

from services.system import hash_password
from database import get_db

router = APIRouter()

@router.get("/status")
async def get_status(db = Depends(get_db)) -> JSONResponse:
    try:
        await db.execute(text("SELECT 1;"))
        return JSONResponse(content = {"status": "OK"}, status_code=200)
    except Exception as e:
        return JSONResponse(content = {"status": f"{e.args}"}, status_code=400)
    
@router.get("/login")
async def login(
        login: str,
        password: str,
        db = Depends(get_db)
) -> JSONResponse:
    password_hash = hash_password(password)
    user_query = await db.execute(text("""
                          SELECT u.id, u.name, u.password_hash 
                          FROM metadata.user as u
                          WHERE u.name = :login
                          """), {"login": login})
    user = user_query.fetchone()
    
    if user is None:
        return JSONResponse(content = {"error": "Invalid login or password"}, status_code = 200)
    
    if user[2] != password_hash:
        return JSONResponse(content = {"error": "Invalid login or password"}, status_code = 200)

    return JSONResponse(content = {"token": "###"}, status_code = 200)