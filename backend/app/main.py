from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/status")
async def get_status() -> JSONResponse:
    return JSONResponse(content = {"status": "OK"}, status_code=200)