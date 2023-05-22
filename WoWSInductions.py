import PySimpleGUI as sg
from wowspy import Wows
# pyperclip is needed to copy the ID to the clipboard
import pyperclip
# this is simply config.py file that it's drawing the API key from so that I don't have to make that public
from config import APIKEY
# allows for caching of API lookups
from functools import lru_cache



# create an instance of the WoWS API with my API Key from the config file
my_api=Wows(APIKEY)

# just putting all the regions even though we only use NA and EU.
NA = my_api.region.NA
EU = my_api.region.EU
ASIA = my_api.region.AS
RU = my_api.region.RU 



# theme for the SimpleGUI windows
sg.theme('Default1')     

# Very basic window.
# Return values using
# automatic-numbered keys
layout = [
    [sg.Text('Please enter the IGN of the recruit you want to search for.')],
    [sg.Text('IGN', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
# title of the first window
window = sg.Window('WoWS IGN to Player ID', layout)

# properly handles closing the window upon submission or clicking "x".
while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    elif event == 'Submit':
        window.close()
    elif event == 'Cancel':
        window.close()

# the input is the player's IGN as a string
player_name = values[0]

@lru_cache(maxsize=None)
def get_player_id(region: str, player_name: str) -> int:
    """
    Given a player name, returns the account ID of the player in the specified region.

    :param region: str, the region of the player
    :param player_name: str, the name of the player
    :return: int, the account ID of the player
    """
    # Call the API to get the player's account ID
    player_id_response = my_api.players(region, player_name, fields='account_id', limit=1)

    # Extract the account ID from the response data
    player_id = player_id_response['data'][0]['account_id']

    return player_id




  
@lru_cache(maxsize=None)
def get_player_name(region: str, player_id: int) -> str:
    """
    Given a region and a player ID, this function retrieves the player's nickname and returns it as a string.

    Args:
        region (str): A string representing the region of the player.
        player_id (int): An integer representing the ID of the player.

    Returns:
        str: A string representing the player's nickname.
    """
    # Query the API for the player's nickname using their region and player ID
    data = my_api.player_personal_data(region, player_id, fields='nickname')

    # Extract the player's nickname from the response
    player_name = data['data'][str(player_id)]['nickname']

    # Return the player's nickname
    return player_name


# searches the API for the nickname, 
# returning the player ID & nickname 
# of the player that most closely matches the search query
player_id_response_na = my_api.players(
NA, player_name, fields='account_id', limit=1)
player_id_na = get_player_id(NA, player_name)
player_name_na = get_player_name(NA, player_id_na)

# searches the API for the nickname, 
# returning the player ID & nickname 
# of the player that most closely matches the search query
player_id_response_eu = my_api.players(
EU, player_name, fields='account_id', limit=1)
player_id_eu = get_player_id(EU, player_name)
player_name_eu = get_player_name(EU, player_id_eu)

#  setup a layout for the GUI, showing the player's name, id, and a button to copy the id to the clipboard.
layout = [  [sg.T(f'NA:    {player_name_na}:     {player_id_na}')], [sg.B('Copy NA ID to clipboard')],
            [sg.T(f'EU:    {player_name_eu}:     {player_id_eu}')], [sg.B('Copy EU ID to clipboard')],
            [sg.B('Close Window')]]  # Button to close window

# Create the Window
window = sg.Window('Output', layout).Finalize()
#window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    elif event == 'Copy NA ID to clipboard': # if the user clicks the button to copy the NA ID to the clipboard, it does just that
        pyperclip.copy(player_id_na)
    elif event == 'Copy EU ID to clipboard': # if the user clicks the button to copy the EU ID to the clipboard, it does just that
        pyperclip.copy(player_id_eu)
window.close()
