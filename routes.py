from fastapi import APIRouter
from modules.access import access_controller
from modules.user import user_controler
from modules.course import course_controler

routes = APIRouter()

routes.include_router(access_controller.routes)
routes.include_router(user_controler.routes)
routes.include_router(course_controler.routes)
