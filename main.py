import logging
import random
import requests

from typing import List

import sys
sys.dont_write_bytecode = False


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


import django
from django.conf import settings
import jdatetime
from dotenv import load_dotenv
django.setup()


from db.models import Programs
from bot import DiscordWebhook
from hackerone import HackeroneScraper
from intigriti import Intigriti
from bugcrowd import Bugcrowd


logging.basicConfig(filename='debug.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)



handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    
    time = jdatetime.datetime.now().strftime("%a, %d %b %Y")
    logging.info(f'Program started at {time}')

    # Initialize requests to the platforms
    hackerone = HackeroneScraper(token='FbLO2BcOLeGeHZsd7KnlyJ0yk5JLxsoJKTFdAgEvnrw=',username='h3llfir3')
    intigriti = Intigriti()
    bugcrowd = Bugcrowd()

    # get the data from each plaform
    bugcrowd_lst = bugcrowd.get_programs()
    intigriti_lst = intigriti.get_programs()
    hackerone_lst = hackerone.get_programs()


    formatted_time = jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S")
    webhook = settings.DISCORD
    discord = DiscordWebhook(webhook)

    def send_message(lst):
        if lst:
            chunk_size = 14  # Number of URLs per message
            chunks = []
            if len(lst) > chunk_size:
                for i in range(0, len(lst), chunk_size):
                    chunk = lst[i : i + chunk_size]
                    chunks.append(chunk)
            else:
                chunks = lst

            print(chunks)
            for chunk in chunks:
                messages = "\n".join(f"\nURL: {url['program_url']}" for url in chunk)
                new_programs_message = f"New programs added at {formatted_time}:\n{messages}"
                msg = "```" + new_programs_message + "```"
                discord.send_message(msg)
    
    send_message(hackerone_lst)
    send_message(intigriti_lst)
    send_message(bugcrowd_lst)

    time = jdatetime.datetime.now().strftime("%a, %d %b %Y")
    logging.info(f'Program finished at {time}')

if __name__ == '__main__':
    main()
