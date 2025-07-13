import asyncio
import aiosqlite

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        list: All users from the users table
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        return results

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.
    
    Returns:
        list: Users older than 40 from the users table
    """
    async with aiosqlite.connect('users.db') as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        return results

async def fetch_concurrently():
    """
    Execute both async_fetch_users and async_fetch_older_users concurrently
    using asyncio.gather().
    
    Returns:
        tuple: Results from both queries
    """
    # Use asyncio.gather to run both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    # Print results
    print("All users:")
    for user in all_users:
        print(user)
    
    print("\nUsers older than 40:")
    for user in older_users:
        print(user)
    
    return all_users, older_users

# Run the concurrent fetch
if __name__ == "__main__":
    # Use asyncio.run to execute the concurrent fetch
    asyncio.run(fetch_concurrently())
