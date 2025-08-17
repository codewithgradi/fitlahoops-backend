# middlewares.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

# --- DB Error Handling Middleware ---
async def db_exception_handler(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except OperationalError:
        return JSONResponse(
            status_code=500,
            content={"detail": "Database is unavailable. Please try again later."}
        )

def add_middlewares(app: FastAPI):
    origins = [
    "http://localhost:3000",  # your frontend URL
    "http://localhost",       # other allowed origins
    "https://yourdomain.com", # production domain
]

    # attach CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # restrict to your frontend in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # attach DB middleware
    app.middleware("http")(db_exception_handler)
