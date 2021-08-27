from fastapi import FastAPI, Request
from routes import routes

app = FastAPI(title="School")
app.include_router(routes)

@app.middleware("http")
async def startup(request: Request, call_next):
    responce = await call_next(request)
    return responce
