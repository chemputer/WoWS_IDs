import PySimpleGUI as sg
from wowspy import Wows
import pyperclip
from config import APIKEY



# create an instance of the WoWS API with my API Key
my_api=Wows(APIKEY)

# just putting all the regions even though we only use NA and EU.
NA = my_api.region.NA
EU = my_api.region.EU
ASIA = my_api.region.AS
RU = my_api.region.RU 



# Add some color
# to the window
sg.theme('Default1')     

# Very basic window.
# Return values using
# automatic-numbered keys
layout = [
    [sg.Text('Please enter the IGN of the recruit you want to search for.')],
    [sg.Text('IGN', size =(15, 1)), sg.InputText()],
    [sg.Submit(), sg.Cancel()]
]
window = sg.Window('Simple data entry window', layout)
event, values = window.read()
window.close()
player_name = values[0]

player_id_response_na = my_api.players(
my_api.region.NA, player_name, fields='account_id', limit=1)
player_id_na = player_id_response_na['data'][0]['account_id']
na_data = my_api.player_personal_data(my_api.region.NA,player_id_na,fields='nickname')
player_name_na = na_data['data'][f'{player_id_na}']['nickname']
player_id_response_eu = my_api.players(
my_api.region.EU, player_name, fields='account_id', limit=1)
player_id_eu = player_id_response_eu['data'][0]['account_id']
eu_data = my_api.player_personal_data(my_api.region.EU,player_id_eu,fields='nickname')
player_name_eu = eu_data['data'][f'{player_id_eu}']['nickname']
#player_name_eu = my_api.player_personal_data(my_api.region.EU,player_id_eu,fields='nickname')

layout = [  [sg.Text(f'NA:    {player_name_na}:     {player_id_na}')], [sg.B('Copy NA ID to clipboard')],
            [sg.Text(f'EU:    {player_name_eu}:     {player_id_eu}')], [sg.B('Copy EU ID to clipboard')],
            [sg.Button('Close Window')]]  # identify the multiline via key option

# Create the Window
window = sg.Window('Output', layout).Finalize()
#window.Maximize()
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Close Window'): # if user closes window or clicks cancel
        break
    elif event == 'Copy NA ID to clipboard':
        pyperclip.copy(player_id_na)
    elif event == 'Copy EU ID to clipboard':
        pyperclip.copy(player_id_eu)
window.close()
