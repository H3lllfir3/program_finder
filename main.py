import os
import logging
import requests
import jdatetime

import sys
sys.dont_write_bytecode = True

# Django specific settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import discord
import django
django.setup()


from db.models import Programs
from datahandler import Data



logging.basicConfig(filename='debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


TOKEN = os.getenv('DISCORD_TOKEN')


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
        r = requests.get(url, timeout=10)
        logging.info(f'Request send to - {url}')
        page += 1
        try:
            if not r.json():
                logging.warning(f"Data doesn't exist at - {url}")

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
    url = 'https://www.intigriti.com/_next/data/uV9iNviSBR6cDIRuoUTN7/en/programs.json'
    r = requests.get(url, timeout=10)
    logging.info(f'Request send to - {url}')
    try:
        programs = r.json()['pageProps']['programs']
        if not r.json():
            logging.warning(f"Data doesn't exist at - {url}")
    except:
        logging.error(f'Error while parsing data')

    # list of programs which should be send to the discord.
    lst = []
    # list of programs which are already in the database.
    programs_in_db = Programs.objects.filter(data__platform='Intigriti')
    list_of_programs_in_db = [program.data for program in programs_in_db]
    for i in range(len(programs)):
        try:
            company_handle = programs[i]['companyHandle'].lower()
            handle = programs[i]['handle'].lower()
            program_url = f'https://app.intigriti.com/programs/{company_handle}/{handle}/detail'
            data = Data(platform='Intigriti', program_name=handle, company_name=company_handle, program_url=program_url).dict()

            if not data in list_of_programs_in_db:
                Programs.objects.create(data=data)
                lst.append(data)

        except Exception as e:
            logging.error(f'Error while parsing data - {e}')
    return lst


def hackerone() -> list:
    """
    Get hackerone programs list and returns 
    Json object contains Company name and program URI.
    """
    programs = []
    page: int = 0
    while True:

        headers = {
            'Accept': 'application/json'
        }
        url = f'https://api.hackerone.com/v1/hackers/programs?page%5Bnumber%5D={page}'
        r = requests.get(
            url,
            auth=('h3llfir3', 'FbLO2BcOLeGeHZsd7KnlyJ0yk5JLxsoJKTFdAgEvnrw='),
            headers = headers
        )

        logging.info(f'Request sended to - {url}')
        page += 1
        try:
            if not r.json()['data']:
                logging.warning(f"Data doesn't exist at - {url}")
                break

            programs += r.json()['data']
        except:
            pass
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
    logging.info(f'Bugcrowd finished with {len(bugcrowd_lst)} results.')

    logging.info(f'Intigriti started at {time}')
    intigriti_lst = intigriti()
    logging.info(f'Intigiriti finished with {len(intigriti_lst)} results.')

    logging.info(f'Hackerone started at {time}')
    hackerone_lst = hackerone()
    logging.info(f'Hackerone finished with {len(hackerone_lst)} results.')

    # Flatting data to one list
    print('Data flattening...')
    lst = [j for i in (bugcrowd_lst, intigriti_lst, hackerone_lst) for j in i]

    client = discord.Client(intents=discord.Intents.default())

    print('Sending data to discord...')
    @client.event
    async def on_ready():
        channel = client.get_channel(1077715462957310144)
        if lst:
            time = jdatetime.datetime.now().strftime("%a, %d %b %Y")
            await channel.send(f"***New program added at {time}***")
            for data in lst:
                msg = f"""
                    ***Platform***: {data['platform']}
                    ***Name***: {data['program_name']}
                    ***Company***: {data['company_name']}
                    ***URL***: {data['program_url']}\n\n
                """
                await channel.send(msg)

        print('Bot is ready!')
        await client.close()



    client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

# if __name__ == '__main__':
main()