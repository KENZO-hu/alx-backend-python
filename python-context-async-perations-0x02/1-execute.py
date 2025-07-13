import sqlite3

class ExecuteQuery:
    """
    A reusable class-based context manager for executing database queries.
    Manages both connection and query execution.
    """
    
    def __init__(self, db_name, query, params=None):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            db_name (str): Name of the database file
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the context manager.
        Opens connection, executes query, and returns results.
        
        Returns:
            list: Query results
        """
        # Open database connection
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
        # Execute the query with parameters
        self.cursor.execute(self.query, self.params)
        
        # Fetch all results
        self.results = self.cursor.fetchall()
        
        return self.results
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager.
        Closes cursor and connection, handles transactions.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        
        Returns:
            bool: False to propagate exceptions
        """
        if self.cursor:
            self.cursor.close()
        
        if self.connection:
            if exc_type is None:
                # No exception occurred, commit any pending transactions
                self.connection.commit()
            else:
                # Exception occurred, rollback any pending transactions
                self.connection.rollback()
            self.connection.close()
        
        # Return False to propagate any exceptions that occurred
        return False

# Usage example
if __name__ == "__main__":
    # Use the ExecuteQuery context manager to execute a parameterized query
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)
    
    with ExecuteQuery('users.db', query, param) as results:
        print("Users older than 25:")
        for row in results:
            print(row)
