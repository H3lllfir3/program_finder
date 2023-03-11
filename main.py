import os
import logging
import random
import requests

import sys
sys.dont_write_bytecode = True


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import discord
import django
import jdatetime
from dotenv import load_dotenv

from db.models import Programs
from datahandler import Data



logging.basicConfig(filename='debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

django.setup()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

log_messages = []

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Mobile Safari/537.36',
]

def bugcrowd() -> list:
    """
    Get bugcrowd programs list and retuen 
    JSON object contains program url and ...
    program['program_url']
    """
    programs = []
    page: int = 0
    while True:
        url = f'https://bugcrowd.com/programs.json?sort[]=promoted-desc&vdp[]=false&page[]={page}'
        r = requests.get(url, timeout=10, headers={'User-Agent': random.choice(USER_AGENTS)})
        logging.info(f'Request send to - {url}')
        page += 1
        try:
            if not r.json():
                logging.warning(f"Data doesn't exist at - {url}")
                log_messages.append(f'The link you followed has expired. {url}')

            if not r.json()['programs']:
                logging.info(f'The last page of the programs is - {page}')
                break
            programs += r.json()['programs']
        except:
            pass
    # list of programs which should be send to the discord.
    lst = []
    # list of programs which are already in the database.
    programs_in_db = Programs.objects.filter(data__platform='Bugcrowd')
    list_of_programs_in_db = [program.data for program in programs_in_db]
    for program in programs:
        url = f'https://bugcrowd.com{program["program_url"]}'
        try:
            data = Data(platform='Bugcrowd', program_name=program['name'].lower(), company_name=program['tagline'].lower(), program_url=url).dict()
            if not data in list_of_programs_in_db:
                Programs.objects.create(data=data)
                lst.append(data)
        except Exception as e:
            logging.error(f'Error while parsing data - {e}')
    return lst


def intigriti() -> list:
    """
    Get intigriti programs list and returns 
    Json object contains Company name and program URI.
    """
    logging.info('Intigriti function runs.')
    url = "https://api.intigriti.com/core/researcher/program"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer 0855A112E633BD46EC3C04A206C67DCA673744694B693083E18F40C6CB366324-1",
        "User-Agent": random.choice(USER_AGENTS)
    }

    response = requests.get(url, headers=headers)
    logging.info(f'Request send to - {url}')
    try:
        programs_lst = response.json()
        if not programs_lst:
            logging.warning(f"Data doesn't exist at - {url}")
            log_messages.append(f"Data doesn't exist at - {url}")
        
        lst = []
        
        if programs_lst:
            # list of programs which are already in the database.
            programs_in_db = Programs.objects.filter(data__platform='Intigriti')
            list_of_programs_in_db = [program.data for program in programs_in_db]
            for program in programs_lst:
                try:
                    company_handle = program['companyHandle'].lower()
                    handle = program['handle'].lower()
                    program_url = f'https://app.intigriti.com/programs/{company_handle}/{handle}/detail'
                    data = Data(platform='Intigriti', program_name=handle, company_name=company_handle, program_url=program_url).dict()

                    if not data in list_of_programs_in_db:
                        Programs.objects.create(data=data)
                        lst.append(data)

                except Exception as e:
                    logging.error(f'Error while parsing data - {e}')
                    log_messages.append(f"The form of the data changed {url}")

            return lst
        
    except:
        logging.error(f'Error while intigriti functions runs')
    
            

def hackerone() -> list:
    """
    Get hackerone programs list and returns 
    Json object contains Company name and program URI.
    """
    programs = []
    page: int = 0
    while True:

        headers = {
            'Accept': 'application/json',
            'User-Agent': random.choice(USER_AGENTS)
        }
        url = f'https://api.hackerone.com/v1/hackers/programs?page%5Bnumber%5D={page}'
        r = requests.get(
            url,
            auth=('h3llfir3', 'FbLO2BcOLeGeHZsd7KnlyJ0yk5JLxsoJKTFdAgEvnrw='),
            headers = headers
        )

        logging.info(f'Request sended to - {url}')
        page += 1
        if not r.json()['data']:
            
            logging.warning(f"Data doesn't exist at - {url}")
            log_messages.append(f"Data doesn't exist at - {url}")
            break
        
        programs += r.json()['data']

    # list of programs which should be send to the discord.
    lst = []
    # get all objects from the database to check if the program is already in the database.
    programs_in_db = Programs.objects.filter(data__platform='Hackerone')
    list_of_programs_in_db = [program.data for program in programs_in_db]
    for program in programs:
        url = f"https://hackerone.com/{program['attributes']['handle'].lower()}"
        if program['attributes']['submission_state'] == 'open' and program['attributes']['state'] == 'public_mode':
            data = Data(platform='Hackerone', program_name=program['attributes']['handle'].lower(), company_name=program['attributes']['name'].lower(), program_url=url).dict()
            if not data in list_of_programs_in_db:
                Programs.objects.create(data=data)
                lst.append(data)
    return lst


def main():
    print('Program started.')
    time = jdatetime.datetime.now().strftime("%a, %d %b %Y")
    logging.info(f'Program started at {time}')

    logging.info(f'Bugcrowd started at {time}')
    bugcrowd_lst = bugcrowd()
    logging.info(f'Bugcrowd finished with results.')

    logging.info(f'Intigriti started at {time}')
    intigriti_lst = intigriti()
    logging.info(f'Intigiriti finished with results.')

    logging.info(f'Hackerone started at {time}')
    hackerone_lst = hackerone()
    logging.info(f'Hackerone finished with results.')
    
    lst = []
    if bugcrowd_lst is not None:
        lst = bugcrowd_lst 
    if intigriti_lst is not None:
        lst += intigriti_lst
    if hackerone_lst is not None:
        lst += hackerone_lst

    # Flatting data to one list
    print('Data flattening...')
    lst = [i for j in lst for i in j]

    client = discord.Client(intents=discord.Intents.default())

    print('Sending data to discord...')
    @client.event
    async def on_ready():

        print('Bot is ready!')

        channel = client.get_channel(1077715462957310144)
        time = jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M")

        if lst:
            await channel.send(f"***New program added at {time}***")
            for data in lst:
                msg = f"""
                    ***Platform***: {data['platform']}
                    ***Name***: {data['program_name']}
                    ***Company***: {data['company_name']}
                    ***URL***: {data['program_url']}\n\n
                """
                await channel.send(msg)
        if log_messages:
            channel = client.get_channel(1083988375108866048)
            for msg in log_messages:
                await channel.send(f"***{msg}***")

        channel = client.get_channel(1083988375108866048)
        await channel.send(f"***No data found at {time}***")

        await client.close()



    client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

if __name__ == '__main__':
    main()