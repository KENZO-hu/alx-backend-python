import sqlite3

class DatabaseConnection :
    def __init__(self , db_name='user_data.csv'):
        """
        Inihialize the context manager with the dabase name.       
        """
        self.db_name= db_name
        self.conn= None 
    
    def __enter__(self):
        """
            Connect to the sqlite database and return the connection .
            this method is invoked when the context is entered using 'with'statement .
        """
        self.conn = sqlite3.conn(self.db_name)
        return self.conn
    
    def __exit__(self,exc_type,exc_type,traceback):
        """
        closes the database connection after the 'with' block is exited .
        It automatically gets called whether an execpetion occureed or not .
        """
        if self.conn:
            self.conn.close()
if __name__== '__main__':
    with DatabaseConnection('user_data.csv') as conn :
        cursor = conn.cursor()
        #execute a querry 
        cursor.execute("SELECT * FROM users ")
        results = cursor.fetchall()
        print(results)
