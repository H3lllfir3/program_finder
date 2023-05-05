import logging
import random
import requests

from typing import List

import sys
sys.dont_write_bytecode = False


import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')


import django
import jdatetime
import discord
import asyncio
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



    # Merge lists
    lst = bugcrowd_lst + intigriti_lst + hackerone_lst
    

    # Send data to Discord
    # client = discord.Client(intents=discord.Intents.default())

    # logging.info('Sending data to discord...')
    # log_messages = None

    # @client.event
    # async def on_ready():

    #     logging.info('Bot is ready!')

    #     channel = client.get_channel(1077715462957310144)
    #     time = jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M")
    bot_data = DiscordWebhook('https://discord.com/api/webhooks/1104150221103042590/Fs3Uz2Otib2FhfT7u2QpOqrmE2U78cuREHHZ6HrAtbKweBYBj55J9x33ZAx5Bl9MPaO4')
    bot_logs = DiscordWebhook('https://discord.com/api/webhooks/1104151546620551179/-b59FL2OUOY1DA7e8AANKTRIlyh27lSnv05ChWF5QQB-3N6XzzI95cXQCtPy6dsUiyqx')
    if lst:
        for data in lst:
            logging.info(f"Sending data to discord - {data}")
            msg = f"""
                ***Platform***: {data['platform']}
                ***Name***: {data['program_name']}
                ***Company***: {data['company_name']}
                ***URL***: {data['program_url']}\n\n
            """
            bot_data.send_message(message_content)

    if log_messages:
        for msg in log_messages:
            bot_logs.send_message(f"***{msg}***")

    if not lst:
        bot_logs.send_message("No new programs found!")


if __name__ == '__main__':
    main()
