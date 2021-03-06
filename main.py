from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from database.coredb import SessionLocal, database
from routes import routes

app = FastAPI(title="School")

app.include_router(routes)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.middleware("http")
async def middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
