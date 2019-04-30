#touhou image cog test

#these have to be defined in here too
#booru URL, used for touhou images and safebooru command
booru = 'safebooru.org'

#NSFW booru URL, used for gelbooru command
booru_nsfw = 'gelbooru.com'

#booru rating
#options are: safe, questionable, explicit
#affects the safebooru command only
boorurating = 'safe'

#booru tag blacklist
#results which have these tags won't be shown in the touhou commands
#does not affect the safebooru command
boorublacklist = '-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini'

boorublacklist_nsfw = '-loli+-lolicon+-shota+-shotacon'

#append text to the start of booru url output
#change this if the bot is sending malformed booru urls
booruappend = 'http:'

import discord
import requests
import aiohttp
import praw
import lxml
import random
import asyncio

from discord.ext import commands
from bs4 import BeautifulSoup


class booruCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def safebooru(self, ctx, message):
        tag = ctx.message.content[len("<@571094749537239042> safebooru"):].strip()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=+' + boorublacklist + '+' + tag) as r:
                if r.status == 200:
                    soup = BeautifulSoup(await r.text(), "lxml")
                    num = int(soup.find('posts')['count'])
                    maxpage = int(round(num/100))
                    page = random.randint(0, maxpage)
                    t = soup.find('posts')
                    p = t.find_all('post')
                    source = ((soup.find('post'))['source'])
                    if num < 100:
                        pic = p[random.randint(0,num-1)]
                    elif page == maxpage:
                        pic = p[random.randint(0,num%100 - 1)]
                    else:
                        pic = p[random.randint(0,99)]
                    msg = pic['file_url']
                    em = discord.Embed(title='', description='Image Source: ' + source, colour=0x42D4F4)
                    #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                    em.set_author(name='Booru image')
                    em.set_image(url=booruappend + msg)
                    await ctx.send(embed=em)


#EXPERIMENTAL!
    @commands.command()
    async def gelbooru(self, ctx, message):
        if ctx.channel.is_nsfw():
            tag = ctx.message.content[len("<@571094749537239042> gelbooru"):].strip()
            async with aiohttp.ClientSession() as session:
                async with session.get('http://' + booru_nsfw + '/index.php?page=dapi&s=post&q=index&tags=+' + boorublacklist_nsfw + '+'  + tag) as r:
                    if r.status == 200:
                        soup = BeautifulSoup(await r.text(), "lxml")
                        num = int(soup.find('posts')['count'])
                        maxpage = int(round(num/100))
                        page = random.randint(0, maxpage)
                        t = soup.find('posts')
                        p = t.find_all('post')
                        source = ((soup.find('post'))['source'])
                        if num < 100:
                            pic = p[random.randint(0,num-1)]
                        elif page == maxpage:
                            pic = p[random.randint(0,num%100 - 1)]
                        else:
                            pic = p[random.randint(0,99)]
                        msg = pic['file_url']
                        em = discord.Embed(title='', description='Image Source: ' + source, colour=0x42D4F4)
                        #em.set_author(name='Character Image', icon_url=bot.user.avatar_url)
                        em.set_author(name='gelbooru image')
                        em.set_image(url=msg)
                        await ctx.send(embed=em)               
        else:
            await ctx.send('not nsfw channel')
					                    

def setup(bot):
    bot.add_cog(booruCog(bot))
