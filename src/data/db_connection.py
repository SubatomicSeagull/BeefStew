import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import sql

class user:
    def __init__(self, id, user_id, user_name, member_name, joke_score):
        self.id = id,
        self.user_id = user_id,
        self.user_name = user_name,
        self.member_name = member_name,
        self.joke_score = joke_score

def connect_to_postgres():
    
    try:
        load_dotenv()
    except Exception as e:
        print("Dotenv load failed, either dotenv is not installed or there is no .env file.")
    
    
    try:
        connection = psycopg2.connect(
            dbname="beefstew",
            user="postgres",
            password=os.getenv("DBPASS"),
            #when public add host to .env
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor()

        print(connection.get_dsn_parameters(), "\n")

        cursor.execute("SELECT * FROM user_joke_score;")
        record = cursor.fetchall()
        print("You are connected to - ", record, "\n")

        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        
connect_to_postgres()