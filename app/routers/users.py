from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from aiosqlite import connect
from ..db_requests import *

router = APIRouter(prefix="", tags=["users"])

@router.get("/")
async def get_user_names():
    try:
        async with connect("mydb.sqlite") as db:
            async with db.execute(get_users) as cursor:
                users = await cursor.fetchall()
        return {"users": [user[0] for user in users]}
    except Exception as e:
        return {"status": "error", "message": str(e)} 

@router.post("/")
async def create_user(user_name: str):
    try:
        async with connect("mydb.sqlite") as db:
            await db.execute(add_user, (user_name,))
            await db.commit()
        return {"status": "user created"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.delete("/{user_name}")
async def delete_user(user_name: str):
    try:
        async with connect("mydb.sqlite") as db:
            await db.execute(delete_user_by_username, (user_name,))
            await db.commit()
        return {"status": "user deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
