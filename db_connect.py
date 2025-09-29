import mysql.connector

# Update these with your actual username and password
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "@Sank371322",  
    "database": "building_materials"
}

def create_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        print("Connected to database!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

if __name__ == "__main__":
    # Just for testing the connection
    connection = create_connection()
    if connection:
        connection.close()
