import sqlite3
import functools
import json
import datetime

#### decorator to log SQL queries

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from the function arguments
        # Assuming the query is passed as a keyword argument or first positional argument
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            # Look for query in positional arguments
            for arg in args:
                if isinstance(arg, str) and ('SELECT' in arg.upper() or 'INSERT' in arg.upper() or 'UPDATE' in arg.upper() or 'DELETE' in arg.upper()):
                    query = arg
                    break
        
        if query:
            # Log to console
            print(f"Executing SQL Query: {query}")
            
            # Log to text file
            with open('query_log.txt', 'a', encoding='utf-8') as txt_file:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                txt_file.write(f"[{timestamp}] Function: {func.__name__} | Query: {query}\n")
            
            # Log to JSON file
            log_entry = {
                'timestamp': datetime.datetime.now().isoformat(),
                'function': func.__name__,
                'query': query
            }
            
            try:
                # Try to read existing JSON data
                try:
                    with open('query_log.json', 'r', encoding='utf-8') as json_file:
                        logs = json.load(json_file)
                except (FileNotFoundError, json.JSONDecodeError):
                    logs = []
                
                # Append new log entry
                logs.append(log_entry)
                
                # Write back to JSON file
                with open('query_log.json', 'w', encoding='utf-8') as json_file:
                    json.dump(logs, json_file, indent=2, ensure_ascii=False)
                    
            except Exception as e:
                print(f"Error logging to JSON: {e}")
        
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

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
