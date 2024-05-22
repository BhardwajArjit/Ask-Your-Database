import sqlite3

def getDatabaseSchema(database_path):
    try:
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # Query to retrieve table schema
        cursor.execute("PRAGMA table_info(student)")

        # Fetch all rows
        schema_rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Extract table schema
        schema = {row[1]: row[2] for row in schema_rows}

        return schema

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
schema = getDatabaseSchema("student.db")
print("Database Schema:")
print(schema)
