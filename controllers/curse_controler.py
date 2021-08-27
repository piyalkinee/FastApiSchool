from fastapi import APIRouter

routes = APIRouter(prefix="/curses", tags=["Curses"])


@routes.get("/getOne")
async def cursesGetOne():
    return {"curses"}


@routes.post("/create")
async def cursesCreate():
    return {"curses"}


@routes.put("/update")
async def cursesUpdate():
    return {"curses"}


@routes.delete("/delete")
async def cursesDelete():
    return {"curses"}
