
import mysql.connector
from mysql.connector import pooling, Error

# Create a connection pool
connection_pool = None

def initialize_connection_pool():

    global connection_pool
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="grocery_pool",
            pool_size=5,  
            pool_reset_session=True,
            host='localhost',
            database='grocery_store',
            user='root',
            password='gaurav@sql'  
        )
        print("✓ Connection pool created successfully")
        return True
    except Error as e:
        print(f"✗ Error creating connection pool: {e}")
        return False

def get_sql_connection():

    global connection_pool
    
    try:
        if connection_pool is None:
            initialize_connection_pool()
        
        connection = connection_pool.get_connection()
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"✗ Error getting connection from pool: {e}")
        return None

def close_connection(connection):

    if connection and connection.is_connected():
        connection.close()  # Returns to pool, doesn't actually close
