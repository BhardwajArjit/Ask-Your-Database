import sqlite3

connection = sqlite3.connect("student.db")

cursor = connection.cursor()

table_info = """
CREATE TABLE student(name VARCHAR(25), class VARCHAR(25), section VARCHAR(25), marks INT);
"""

cursor.execute(table_info)

cursor.execute("""INSERT INTO student VALUES ('Steve', 'Data Science', 'A', 100)""")
cursor.execute("""INSERT INTO student VALUES ('Taylor', 'Data Science', 'A', 95)""")
cursor.execute("""INSERT INTO student VALUES ('Al', 'Computer Vision', 'C', 92)""")
cursor.execute("""INSERT INTO student VALUES ('Robert', 'Machine Learning', 'B', 95)""")

print("The inserted records are: ")

data = cursor.execute("""SELECT * FROM STUDENT""")

for row in data:
    print(row)

connection.commit()
connection.close()
