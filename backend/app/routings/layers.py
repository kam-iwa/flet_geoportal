from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import JSONResponse

from services.layers import LayerService
from services.system import get_token
from database import get_db


router = APIRouter()

@router.get("/layers")
async def get_layers(
        db = Depends(get_db)
    ) -> JSONResponse:
    try:
        layers = await LayerService().get_layers(db)
        return JSONResponse(content = {"data": layers}, status_code=400)
        
    except Exception as e:
        return JSONResponse(content = {"status": f"{e.args}"}, status_code=400)
    
#TODO
@router.get("/layers/<layer_name>")
async def get_layer() -> JSONResponse:
    return None
        
@router.post("/layers")
async def new_layer(
    file: UploadFile,
    layer_name: str,
    db = Depends(get_db),
    token: dict = Depends(get_token)
) -> JSONResponse:
    output = await LayerService().add_layer(db, token, file, layer_name)
    return JSONResponse(content = output[0], status_code=output[1])

#TODO
@router.delete("/layers/<layer_name>")
async def delete_layer() -> JSONResponse:
    return None