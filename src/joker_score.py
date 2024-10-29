from data import db_connection

# keeps track of a users individual joke score
# joke score is added or taken away through either a /+2 /-2 command with the person they are scoring as an argument,
# or when someone replies to a message with +2 or -2,


#todo
# find a way to store each users individual score
# make it so that they cant adjust their own score
# make it so that they cant adjust beefstew's score
# sanitisation for slash command arguments, is the person they pinged a real user?
# add a way to see a users current score
# add a collection of phrases to say when the score is adjusted
# needs functionaliy to check the person who's message was replied to

#both the reply and slash command should invoke the same code

class Joker:
    def __init__(self, id, user_id, user_name, member_name, joke_score):
        self.id = id,
        self.user_id = user_id,
        self.user_name = user_name,
        self.member_name = member_name,
        self.joke_score = joke_score

def retrieve_joke_score(user_id):
    return int(db_connection.run_command(f"SELECT joke_score FROM user_joker_score WHERE user_id = '{user_id}';"))

def change_joke_score(user_id, value):
    raise NotImplementedError

def clear_joke_score(user_id):
    raise NotImplementedError


retrieve_joke_score(1283805971524747304)