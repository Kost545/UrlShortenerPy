from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from aiosqlite import connect
from ..logics import get_short_url
from ..db_requests import *

router = APIRouter(prefix="/{user_name}", tags=["urls"])

@router.get("/")
async def get_urls_for_user(user_name: str):
    try:
        async with connect("mydb.sqlite") as db:
            async with db.execute(get_urls_by_user_name, (user_name,)) as cursor:
                urls = await cursor.fetchall()
        return {"user_name": user_name, "urls": urls}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{short_url}")
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
    
@router.post("/")
async def create_url_for_user(user_name: str, original_url: str, custom_url: str | None = None):
    try:
        async with connect("mydb.sqlite") as db:
            async with db.execute(get_user_id_by_username, (user_name,)) as cursor:
                row = await cursor.fetchone()
                if row is None:
                    return {"status": "error", "message": "User not found"}
                user_id = row[0]

            short_url = get_short_url(original_url)
            if custom_url is not None:
                async with db.execute(get_urls_by_user_name_and_short_urls, (user_name, custom_url)) as cursor:
                        row = await cursor.fetchone()
                        if row is not None:
                            return {"status": "error", "message": "Custom URL already exists"}
                short_url = custom_url

            await db.execute(add_url, (user_id, original_url, short_url))
            await db.commit()
        return {"status": "url created", "short_url": short_url}
    except Exception as e:
        return {"status": "error", "message": str(e)}   

@router.delete("/{short_url}")
async def delete_url_for_user(user_name: str, short_url: str):
    try:
        async with connect("mydb.sqlite") as db:
            await db.execute(delete_url_by_short_url, (short_url, user_name))
            await db.commit()
        return {"status": "url deleted"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
