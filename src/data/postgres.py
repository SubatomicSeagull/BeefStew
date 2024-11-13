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
        log_error(error)
        return

async def read(command: str):
    try:
        connection = await connect_to_db()
        if connection == None:
            return None
       
        with connection.cursor() as cursor: 
            cursor.execute(command)
            record = cursor.fetchall()
            
        connection.close()
        
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        log_error(error)
        return
    
    finally:
        connection.close()
        
    return record

async def write(command: str):
    try:
        connection = await connect_to_db()
        if connection == None:
            return None
        
        with connection.cursor() as cursor:
            cursor.execute(command)
        
        connection.commit()
        connection.close()
        
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)
        log_error(error)
        return None
    
    finally:
        connection.close()

async def log_error(error_message: str):
    try:
        connection = await connect_to_db()
        if connection is None:
            return

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO error_logs (error_message) VALUES (%s)",
                (error_message,)
            )

        connection.commit()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while logging error to PostgreSQL:", error)