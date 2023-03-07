import requests
import logging


logging.basicConfig(filename='discord.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

def discord_bot(message):
    header = {
        'Authorization': 'Njg4NzY3ODgwMjA4MDU2MzUw.GbZfHS.qURB4mher8spxVCPoqxusU9lymIR0naO6gBgv0'
    }
    try:
        re = requests.post('https://discord.com/api/v9/channels/1077715462957310144/messages', 
                        data=message,
                        headers=header)
    except Exception as e:
        logging.info(f'Message can not be send the error is - {e}')

lst = [
    {'platform': 'Bugcrowd', 'program_name': 'hotdoc', 'company_name': 'easily book and manage all your appointments from one place.', 'program_url': 'https://bugcrowd.com/hotdoc1'},
    {'platform': 'Hackerone', 'program_name': 'Gog', 'company_name': 'Google', 'program_url': 'https://bugcrowd.com/'}
]

for data in lst:
    msg = f"""
    Platform: {data['platform']}
    Name: {data['program_name']}
    Company: {data['company_name']}
    Url: {data['program_url']}
    """
    discord_bot(msg)