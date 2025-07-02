import aiosqlite
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from . import get_longUrl, get_hash, add_url


app = FastAPI()

class AddUrlRequest(BaseModel):
    longUrl: str

@app.get("/show")
async def redirect_to_long(shortUrl):
    longUrl = await get_longUrl(shortUrl)
    print(f"url получена: {longUrl}")
    return RedirectResponse(url=longUrl, status_code=302)

@app.post("/add")
async def read_post(request: AddUrlRequest):
    longUrl = request.longUrl
    shortUrl = get_hash(longUrl)
    while True:
        try:
            await add_url(longUrl, shortUrl)
            break
        except ValueError:
            shortUrl = get_hash(shortUrl)
    return {"url": f"/show?shortUrl={shortUrl}"}

@app.on_event("startup")
async def startup():
    async with aiosqlite.connect("mydb.sqlite") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS urls (
        longUrl TEXT,
        shortUrl TEXT
        )
        """)
        await db.commit()
    print("бд инициализирована")
