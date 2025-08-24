import aiosqlite
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routers import users, urls
from .db_requests import create_users_table, create_urls_table

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with aiosqlite.connect("mydb.sqlite") as db:
        await db.execute(create_urls_table)
        await db.execute(create_users_table)
        await db.commit()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(urls.router)
