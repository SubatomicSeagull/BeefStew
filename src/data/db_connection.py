import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import sql


def run_command(command: str):
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

        cursor.execute(command)
        record = cursor.fetchall()

        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
    return record
        

