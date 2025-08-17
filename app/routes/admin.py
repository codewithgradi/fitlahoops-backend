from fastapi import APIRouter
from app.routes import  authentication,events,gallery,volunteers

router = APIRouter()

router.include_router(authentication.router)
router.include_router(events.router)
router.include_router(gallery.router)
router.include_router(volunteers.router)












