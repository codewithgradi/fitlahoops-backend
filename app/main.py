from fastapi import FastAPI
from app.routes.admin import router
from app.middlewares.middleware import add_middlewares


app=FastAPI()
add_middlewares(app)
app.include_router(router)
