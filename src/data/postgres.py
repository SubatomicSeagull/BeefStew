import psycopg2
import os

# read data from the database
async def read(command: str, params: tuple = ()):
    try:
        connection = await get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(command, params)

            record = cursor.fetchall()

        connection.close()

    except (Exception, psycopg2.Error) as error:
        await log_error(error)
        return

    finally:
        connection.close()

    return record

# write data to the database
async def write(command: str, params: tuple = ()):
    try:
        connection = await get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(command, params)

        connection.commit()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        await print(error)
        return None

    finally:
        connection.close()

# log an error to the error_logs table
async def log_error(error_message: str):
    try:
        connection = await get_db_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO error_logs (error_message) VALUES (%s)",
                (error_message,)
            )

        connection.commit()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        connection.close()

    finally:
        connection.close()

# establish a connection to the database
async def get_db_connection():
    try:
        db_config = {
            "dbname": os.getenv("DBNAME"),
            "user": os.getenv("DBUSER"),
            "password": os.getenv("DBPASS"),
            "host": os.getenv("DBHOST"),
            "port": os.getenv("DBPORT")
        }

        connection = psycopg2.connect(**db_config)

        if connection is None:
            raise Exception("Failed to connect to the database.")

        return connection

    except (Exception, psycopg2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
        await log_error(error)