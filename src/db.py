import aiosqlite
import asyncio


async def get_longUrl(shortUrl):
	async with aiosqlite.connect("mydb.sqlite") as db:
		cursor = await db.execute("SELECT longUrl FROM urls WHERE shortUrl = ?", (shortUrl,))
		rows = await cursor.fetchall()
		await cursor.close()
		return rows[0][0]

async def add_url(longUrl, shortUrl):
	async with aiosqlite.connect("mydb.sqlite") as db:
		cursor = await db.execute(
			"SELECT longUrl FROM urls WHERE shortUrl = ? and longUrl != ?", (shortUrl, longUrl)
		)
		rows = await cursor.fetchall()
		if rows:
			raise ValueError("Колизия")
		await db.execute(
			"INSERT INTO urls (longUrl, shortUrl) VALUES (?, ?)", (longUrl, shortUrl)
		)
		await db.commit()
	print("запись в дб добавлена")

