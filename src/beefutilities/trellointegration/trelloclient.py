from main import trello_client # need to stop importing from main so much
import os
from dotenv import load_dotenv

# return the board object
async def get_trello_board(board_id):
    return trello_client.get_board(board_id)

# return the list object
async def get_trello_list(board, list_id):
    return board.get_list(list_id)

# find the board and the list and create a card
async def push_trello_card(name, desc, author):
    load_dotenv()
    board = await get_trello_board(os.getenv("BOARDID"))
    list = await get_trello_list(board, board.list_lists()[0].id)

    # formats the tile of the card
    suggested_title = (f"{author}: {name}")
    
    # pushes the card to the trello list under "User Suggestions"
    list.add_card(name=suggested_title, desc=desc)