import mysql.connector
from config import DB_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            print("✓ Successfully connected to database!")
            return True
        except mysql.connector.Error as err:
            print(f"✗ Connection failed: {err}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")
    
    def execute_query(self, query):
        """Execute a SELECT query and return results"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except mysql.connector.Error as err:
            print(f"✗ Query failed: {err}")
            return None

# Test connection
if __name__ == "__main__":
    db = DatabaseConnection()
    db.connect()
    db.disconnect()
