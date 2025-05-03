import uuid
import sqlite3
from datetime import datetime

#connect the database 
conn = sqlite3.connect("database/app.db")
cursor = conn.cursor()

users = [
    {"email": "vidunithap@gmail.com", "full_name": "tesgt", "password": "test1234", "auth_provider" : "manual", "theme_preference" : "dark"}
]

for user in users:
    user_id = str(uuid.uuid4())
    join_date = datetime.now().isoformat()
    cursor.execute("""
INSERT INTO User (user_id, email, full_name, password, auth_provider, theme_preference, join_date) VALUES (?, ?, ?, ?, ?, ?, ?)
""", (user_id, user["email"], user["full_name"], user["password"], user["auth_provider"], user["theme_preference"], join_date))
    conn.commit()
    
print("done")


# guid = str(uuid.uuid4())

# print(guid)