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
        print(1)
        self.logger.info('Sending data to discord...')
        print(2)
        print(self.token)
        # await self.client.start(self.token)
        print(3)

        @self.client.event
        async def on_ready():
            print(4)
            self.logger.info('Bot is ready!')
            print(5)
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
            # if log_messages:
            #     log_channel = self.client.get_channel(1083988375108866048)
            #     for msg in log_messages:
            #         await log_channel.send(f"***{msg}***")

            if not lst:
                log_channel = self.client.get_channel(1083988375108866048)
                await log_channel.send(f"***No data found at {time}***")

            await self.client.close()
        print('im at the end.')
        await self.client.run(self.token)

