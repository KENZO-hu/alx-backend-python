import sqlite3
 
 # create a class foor executing quries 
 class ExecuteQuerry :
    def __init__(self , querry , params=(), db_name='user_data.csv')
    """
    Intialize the context manager with the querry , parameters and the database name.
    """
    self.querry = querry 
    self.params = params
    self.db_name = db_name
    self.conn = None
    self.cursor = None
    self.results = None

    def __enter__(self):
        """
        Connects to the database , executes the query , and returns the results .
        """
        self.conn = sqlite3.conn(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.querry , self.params)
        self.results = self.cursor.fetchall()
        return self.results
    
    def __exit__(self,exc_type ,exc_type,traceback):
        """
        Closes the database connection .
        """
        if self.cursor :
            self.cursor.close()
        if self.conn : 
            self.conn.close()*
        return False 

# example usage 
if __name__ == '__main__':
    query = "SELECT * FROM users WHERE age > ?"
    params = (25 ,)
    

    with ExecuteQuerry(querry, params)as results :
        for row in results :
            print(row)
