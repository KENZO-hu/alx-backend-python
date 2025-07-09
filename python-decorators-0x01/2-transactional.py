# 2-transactional.py

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

def transactional(func):
    """Decorator that manages database transactions"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Start transaction (autocommit is off by default)
            result = func(conn, *args, **kwargs)
            # If function completes successfully, commit
            conn.commit()
            return result
        except Exception as e:
            # If function raises an exception, rollback
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise  # Re-raise the exception
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

# Example usage
if __name__ == "__main__":
    # Update user's email with automatic transaction handling 
    try:
        update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
        print("User email updated successfully")
    except Exception as e:
        print(f"Failed to update user email: {e}")
