import os
from fastapi import Request
from fastapi.responses import JSONResponse

API_KEY = os.getenv("API_KEY")

async def api_key_middleware(request: Request, call_next):
    expected_key = API_KEY
    received_key = request.headers.get("x-api-key")

    if not expected_key or received_key != expected_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "Unauthorized"},
        )

    return await call_next(request)