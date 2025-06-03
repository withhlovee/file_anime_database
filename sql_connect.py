import os
import mysql.connector as sql
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return sql.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def add_to_table(username, password):
    mycon = get_connection()
    cursor = mycon.cursor()
    query = "INSERT INTO people (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, password))
    mycon.commit()
    cursor.close()

def check_in_table(username, password):
    mycon = get_connection()
    cursor = mycon.cursor()
    query = "SELECT * FROM people WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    return bool(result)

def get_user_id(username):
    mycon = get_connection()
    cursor = mycon.cursor()
    cursor.execute("SELECT id FROM people WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None

def add_anime(user_id, name, season, episode):
    mycon = get_connection()
    cursor = mycon.cursor()
    query = "INSERT INTO anime_list (user_id, name, season, episode) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user_id, name, season, episode))
    mycon.commit()
    cursor.close()

def get_anime_list(user_id):
    mycon = get_connection()
    cursor = mycon.cursor()
    query = "SELECT name, season, episode FROM anime_list WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result
