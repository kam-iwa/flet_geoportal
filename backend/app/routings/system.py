import os

from fastapi import APIRouter, Depends
from sqlalchemy import text
from starlette.responses import JSONResponse

from database import get_db
from models.system import UserLogin
from services.system import UserService, get_token

router = APIRouter()

@router.get("/status")
async def get_status(db = Depends(get_db)) -> JSONResponse:
    try:
        await db.execute(text("SELECT 1;"))
        return JSONResponse(content = {"status": "OK"}, status_code=200)
    except Exception as e:
        return JSONResponse(content = {"status": f"{e.args}"}, status_code=400)
    
@router.post("/login")
async def login(
        request: UserLogin,
        db = Depends(get_db)
) -> JSONResponse:
    user = await UserService().authenticate(db, request.login, request.password)
    
    if user is None:
        return JSONResponse(content = {"error": "Invalid login or password"}, status_code = 401)
    
    token = await UserService().create_token(
        data={"id": str(user["id"]), "name": user["name"]} 
    )

    return JSONResponse(content = {"token": token}, status_code = 200)

@router.post("/check_token")
async def check_token(token: dict = Depends(get_token)) -> JSONResponse:
    
    if token is None:
        return JSONResponse(content = {"status": "Invalid token"}, status_code = 401)
    
    return JSONResponse(content = {"status": "OK"}, status_code = 200)