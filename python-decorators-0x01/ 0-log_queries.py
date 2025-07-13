# 0-log_queries.py

import sqlite3
import functools

def log_queries(func):
    """Decorator to log SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract query from arguments
        query = None
        if args:
            query = args[0] if isinstance(args[0], str) else None
        if not query and 'query' in kwargs:
            query = kwargs['query']
        
        # Log the query
        if query:
            print(f"Executing query: {query}")
        
        # Execute the original function
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Example usage
if __name__ == "__main__":
    # This will log: "Executing query: SELECT * FROM users"
    users = fetch_all_users(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users")
