from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from aiosqlite import connect
from ..logics import get_short_url
from ..db_requests import *

router = APIRouter(prefix="/users", tags=["users"])

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

@router.get("/{user_name}/urls/")
async def get_urls_for_user(user_name: str):
    try:
        async with connect("mydb.sqlite") as db:
            async with db.execute(get_urls_by_user_name, (user_name,)) as cursor:
                urls = await cursor.fetchall()
        return {"user_name": user_name, "urls": urls}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{user_name}/urls/{short_url}")
async def redirected_by_short_url(user_name: str, short_url: str):
    try:
        async with connect("mydb.sqlite") as db:
            async with db.execute(get_original_url_by_short_url, (short_url, user_name)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return {"status": "error", "message": "URL not found"}
                original_url = row[0]
        return RedirectResponse(url=original_url, status_code=302)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

@router.post("/{user_name}/urls/")
async def create_url_for_user(user_name: str, original_url: str):
    try:
        async with connect("mydb.sqlite") as db:
            async with db.execute(get_user_id_by_username, (user_name,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return {"status": "error", "message": "User not found"}
                user_id = row[0]
            short_url = get_short_url(original_url)
            await db.execute(add_url, (user_id, original_url, short_url))
            await db.commit()
        return {"status": "url created", "short_url": short_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}   

@router.delete("/{user_name}/urls/{short_url}")
async def delete_url_for_user(user_name: str, short_url: str):
    try:
        async with connect("mydb.sqlite") as db:
            await db.execute(delete_url_by_short_url, (short_url, user_name))
            await db.commit()
        return {"status": "url deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
