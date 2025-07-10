import asyncio 
import aiosqlite

DB_NAME = 'user_data.csv'

async def async_fetch_users():
    async with aiosqlite.Connect(DB_NAME) as db :
        async with db.execute("SELECT * FROM users ") as cursor:
            rows = await cursor.fetchall()
            print("\n all users:")
            for row in rows :
                print(row)
async def aync_fetch_old_users():
    async with aiosqlite.connect(DB_NAME) as db :
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor :
            rows = await cursor.fetchall()
            print("\n users older than 40 :")
            for row in rows : 
                print(row)               
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
if __name__ == '__main__':
    asyncio.run(fetch_concurrently)
