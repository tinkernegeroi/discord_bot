import discord
import logging
import requests
import sqlite3
import random
from discord.ext import commands
import json

con = sqlite3.connect("d_b_b.db")
cur = con.cursor()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

TOKEN = "OTY3MTE4MzY1OTc2MDY4MTY2.YmLpKg.l9K5RI70WwgIsEqnLnYNLH8ArvI"


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "привет" in message.content.lower():
            await message.channel.send("И тебе привет")
        if message.author == client.user:
            return

        if message.content.startswith('!help'):
            await message.channel.send('''Bot commands:
            !help - gets commands list
            !fh - finds hero on dota2.com
            !fa - finds account on dotabuff.com
            !chuck - send a random Chuck Norris joke
            !joke - send a random admin's joke
            !fox - send a random fox picture
            !quote - send a random quote
            ''')

        if message.content.startswith('!fh'):
            a = message.content.split()
            print(a)
            await message.channel.send(f'https://www.dota2.com/hero/{a[1]}')

        if message.content.startswith('!chuck'):
            response = requests.get('https://api.chucknorris.io/jokes/random')
            object = response.json()
            await message.channel.send(object["value"])

        if message.content.startswith('!fa'):
            a = message.content.split()
            if len(a) == 2:
                await message.channel.send(
                    f'https://ru.dotabuff.com/search?utf8=%E2%9C%93&q={a[1]}&commit=%D0%9F%D0%BE%D0%B8%D1%81%D0%BA')
            elif len(a) > 2:
                a.remove('!fa')
                b = '%20'.join(a)
                await message.channel.send(
                    f'https://ru.dotabuff.com/search?utf8=%E2%9C%93&q={b}&commit=%D0%9F%D0%BE%D0%B8%D1%81%D0%BA')

        if message.content.startswith('!joke'):
            s_id = random.randint(1, 14)
            result = cur.execute(f"""SELECT joke FROM jokes
            WHERE id = {s_id}""").fetchall()
            for i in result:
                a = i[0]
            await message.channel.send(a)

        if message.content.startswith('!quote'):
            response1 = requests.get(f'https://favqs.com/api/qotd')
            object1 = response1.json()
            await message.channel.send(f'''{object1["quote"]["body"]}. ©{object1["quote"]["author"]}''')

        if message.content.startswith('!fox'):
            response = requests.get('https://some-random-api.ml/img/fox')
            json_data = json.loads(response.text)
            embed = discord.Embed(color=0xff9900, title='Random Fox')
            embed.set_image(url=json_data['link'])
            await message.channel.send(embed=embed)


intents = discord.Intents.default()
intents.members = True
client = YLBotClient(intents=intents)
client.run(TOKEN)
