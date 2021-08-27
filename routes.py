from fastapi import APIRouter
from controllers import access_controller, user_controler, curse_controler

routes = APIRouter()

routes.include_router(access_controller.routes)
routes.include_router(user_controler.routes)
routes.include_router(curse_controler.routes)
