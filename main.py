import os
import logging 
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self:
            return
        print(f'Message from {message.author}: {message.content}')
        await self.process_commands(message)

bot = MyBot(command_prefix='⛧', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('ping!')

bot.run(token, log_handler=handler, log_level=logging.DEBUG)

#Check