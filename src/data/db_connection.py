import psycopg2
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
        connection = psycopg2.connect(
            dbname="beefstew",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )

        cursor = connection.cursor()

        print(connection.get_dsn_parameters(), "\n")

        cursor.execute("SELECT * FROM user_joker_score;")
        record = cursor.fetchall()
        print("You are connected to - ", record, "\n")

        cursor.close()
        connection.close()

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        
connect_to_postgres()