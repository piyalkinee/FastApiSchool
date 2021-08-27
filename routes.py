from fastapi import APIRouter
from .controllers import user_controler, curse_controler

routes = APIRouter()

routes.include_router(user_controler.routes)
routes.include_router(curse_controler.routes)
