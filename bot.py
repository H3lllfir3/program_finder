import discord
import logging
import jdatetime

class DiscordClient:
    def __init__(self, token, channel_id, log_handler, log_level=logging.DEBUG):
        self.token = token
        self.channel_id = channel_id
        self.log_handler = log_handler
        self.log_level = log_level
        self.client = discord.Client(intents=discord.Intents.default())
        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(self.log_level)

    async def send_data_to_discord(self, lst, log_messages=None):
        self.logger.info('Sending data to discord...')
        await self.client.start(self.token)

        @self.client.event
        async def on_ready():
            self.logger.info('Bot is ready!')
            channel = self.client.get_channel(self.channel_id)
            time = jdatetime.datetime.now().strftime("%a, %d %b %Y %H:%M")
            if lst:
                await channel.send(f"***New program added at {time}***")
                for data in lst:
                    self.logger.info(f"Sending data to discord - {data}")
                    msg = f"""
                        ***Platform***: {data['platform']}
                        ***Name***: {data['program_name']}
                        ***Company***: {data['company_name']}
                        ***URL***: {data['program_url']}\n\n
                    """
                    await channel.send(msg)
            if log_messages:
                log_channel = self.client.get_channel(1083988375108866048)
                for msg in log_messages:
                    await log_channel.send(f"***{msg}***")

            if not lst:
                log_channel = self.client.get_channel(1083988375108866048)
                await log_channel.send(f"***No data found at {time}***")

            await self.client.close()

        await self.client.run(self.token)


token = 'your_discord_bot_token'
channel_id = 1077715462957310144
log_handler = logging.StreamHandler()
log_level = logging.DEBUG

client = DiscordClient(token, channel_id, log_handler, log_level)
lst = [{'platform': 'Windows', 'program_name': 'Notepad', 'company_name': 'Microsoft', 'program_url': 'https://notepad.com'}]
client.send_data_to_discord(lst)
