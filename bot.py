import os
import logging

import jdatetime
import discord
# from dotenv import load_dotenv


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())




lst = [1,2,3,4,5,6,7,8,9,10]

@client.event
async def on_ready():
    channel = client.get_channel(1077715462957310144)
    
    time = jdatetime.datetime.now().strftime("%a, %d %b %Y")
    await channel.send(f"***New program added at {time} in {data['platform']}***")
    for data in lst:
        msg = f"""
            ***Platform***: {data['platform']}
            ***Name***: {data['program_name']}
            ***Company***: {data['company_name']}
            ***URL***: {data['program_url']}
        """
        await channel.send(msg)

    print('Bot is ready!')
    await client.close()



client.run(TOKEN, log_handler=handler, log_level=logging.DEBUG)

