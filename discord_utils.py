import discord
from discord.ext import commands, tasks

import requests

class DiscordClientHandler:
    def __init__(self, token):
        self.token = token
        self.bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_message(self, message):
        response = requests.post('https://d16c34dd6440.ngrok.io/discord', json={'text': message.content, 'user': message.author.display_name})
        message.channel.send(response['response'])