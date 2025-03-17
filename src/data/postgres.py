import psycopg2
import os

async def connect_to_db():    
    try:
        # connect to the db with environment credentials
        connection = psycopg2.connect(
            dbname="bs_users_and_guilds",
            user=os.getenv("DBUSER"),
            password=os.getenv("DBPASS"),
            host=os.getenv("DBHOST"),
            port=os.getenv("DBPORT")
        )
        return connection
    
    except (Exception, psycopg2.Error) as error:
        return

async def read(command: str, params: tuple = ()):
    try:
        # connect to the db
        connection = await connect_to_db()
        if connection is None:
            return None

        # set the cursor and execute the given sql command
        with connection.cursor() as cursor: 
            cursor.execute(command, params)
            
            # return the result
            record = cursor.fetchall()
         
        # close the connection   
        connection.close()
        
    except (Exception, psycopg2.Error) as error:
        await log_error(error)
        return
    
    # make sure the connection is closed even in the event of an error
    finally:
        connection.close()
        
    return record

async def write(command: str, params: tuple = ()):
    try:
        # connect to the db
        connection = await connect_to_db()
        if connection is None:
            return None
        
        # set the cursor and execute the command
        with connection.cursor() as cursor:
            cursor.execute(command, params)
        
        # save the changes and close the conncection
        connection.commit()
        connection.close()
        
    except (Exception, psycopg2.Error) as error:
        await print(error)
        return None
    
    # close the connection even in the event of an error
    finally:
        connection.close()

async def log_error(error_message: str):
    try:
        # connect to the db
        connection = await connect_to_db()
        if connection is None:
            return

        # set the cursor and log the error (i dont think the error table is set up)
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO error_logs (error_message) VALUES (%s)",
                (error_message,)
            )

        # commit the changes and close the connection
        connection.commit()
        connection.close()
        
    # close the connection even in the event of an error
    except (Exception, psycopg2.Error) as error:
        connection.close()
        
    # close the connection even in the event of an error
    finally:
        connection.close()