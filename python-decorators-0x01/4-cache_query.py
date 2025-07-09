# 4-cache_query.py

import time
import sqlite3 
import functools

def with_db_connection(func):
    """Decorator that automatically handles database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the original function with connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Always close the connection
            conn.close()
    return wrapper

query_cache = {}

def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from arguments
        query = None
        if len(args) > 1:  # conn is first arg, query might be second
            query = args[1] if isinstance(args[1], str) else None
        if not query and 'query' in kwargs:
            query = kwargs['query']
        
        # If query is found and cached, return cached result
        if query and query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        
        # Execute the function and cache the result
        result = func(*args, **kwargs)
        
        if query:
            query_cache[query] = result
            print(f"Query result cached: {query}")
        
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example usage
if __name__ == "__main__":
    # First call will cache the result
    print("First call (will cache):")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users")
    
    print("\nSecond call (will use cache):")
    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users_again)} users")
