import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import sql


async def read(command: str):
    try:
        load_dotenv()
    except Exception as e:
        print("Dotenv load failed, either dotenv is not installed or there is no .env file.")
    
    try:
        connection = psycopg2.connect(
            dbname="beefstew",
            user="postgres",
            password=os.getenv("DBPASS"),
            host=os.getenv("DBHOST"),
            port="5432"
        )
        
        cursor = connection.cursor()
       
        cursor.execute(command)
        record = cursor.fetchall()
        
        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return
    return record

async def write(command: str):
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
            host="192.168.1.114",
            port="5432"
        )
        
        cursor = connection.cursor()
        cursor.execute(command)
        
        connection.commit()
        
        cursor.close()
        connection.close()
        
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return
        