import psycopg2
import os
from psycopg2 import sql


async def connect_to_db():    
    try:
        connection = psycopg2.connect(
            dbname="beefstew",
            user="postgres",
            password=os.getenv("DBPASS"),
            host=os.getenv("DBHOST"),
            port="5432"
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return

async def read(command: str):
    try:
        connection = await connect_to_db()
        if connection == None:
            return
       
        with connection.cursor() as cursor: 
            cursor.execute(command)
            record = cursor.fetchall()
            
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return
    return record

async def write(command: str):
    try:
        connection = await connect_to_db()
        if connection == None:
            return
        
        with connection.cursor() as cursor:
            cursor.execute(command)
        
        connection.commit()
        connection.close()
        
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        return