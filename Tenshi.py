#TenshiBot Slipstream version

#this version is still in early development and NOT ready to replace the main version

#todo
#server count display and posting
#dev id checking for some commands


##Parameters##

#token
tkn = open("test/token.txt", "r")
token = tkn.read()
tkn.close()

#booru URL, used for touhou images and safebooru command
booru = 'safebooru.org'

#booru rating
#options are: safe, questionable, explicit
#affects the safebooru command only
boorurating = 'safe'

#booru tag blacklist
#results which have these tags won't be shown in the touhou commands
#does not affect the safebooru command
boorublacklist = '-underwear+-sideboob+-pov_feet+-underboob+-upskirt+-sexually_suggestive+-ass+-bikini'

#append text to the start of booru url output
#change this if the bot is sending malformed booru urls
booruappend = 'http:'

#Discordbots.org API key
dbo_api = ''

#Variant
bot_variant = 'slipstream'

#Version
bot_version = '1.5'

#prefix
#Debug account has user ID 571094749537239042
#Normal account has user ID 252442396879486976
tb_prefix = ('<@571094749537239042> ')


#Booting text
print('Please wait warmly...')

import discord
import requests
import praw
import lxml
import random

from discord.ext import commands
from bs4 import BeautifulSoup


#bot = commands.Bot(command_prefix= '<@' + str(bot.user.id) + '> ')
#do not leave '' here
bot = commands.Bot(command_prefix= tb_prefix)
client = discord.client


#Prefix
#tb_prefix = ('<@' + client.user.id + '> ')

#bot will display this on startup when accepting commands

@bot.event
async def on_ready():
    print(' ')
    print('TenshiBot startup complete ')
    print(' ')
    print('User ID - ' + str(bot.user.id))
    print('Username - ' + bot.user.name)
    print('TenshiBot Ver - ' + bot_version)
    print('System Variant - ' + bot_variant)
    print(' ')
    print('servercount - ' + str(len(bot.guilds)))
    print(discord.version_info)


#other bot ignoring code 
@bot.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    await bot.process_commands(message)


    
@bot.command()
async def ping(ctx):
    await ctx.send('pong')


#now the fun part, getting these working...
#this works, just need to add the embeds    
@bot.command()
async def tenshi(ctx):
    char = 'hinanawi_tenshi'
    r = requests.get('http://' + booru + '/index.php?page=dapi&s=post&q=index&tags=solo+' + boorublacklist + '+' + char)
    if r.status_code == 200:
            soup = BeautifulSoup(r.text, "lxml")
            num = int(soup.find('posts')['count'])
            maxpage = int(round(num/100))
            page = random.randint(0, maxpage)
            t = soup.find('posts')
            p = t.find_all('post')
            if num == 0:
                msg = 'No posts found'
            else:
                if num < 100:
                    pic = p[random.randint(0,num-1)]
                elif page == maxpage:
                    pic = p[random.randint(0,num%100 - 1)]
                else:
                    pic = p[random.randint(0,99)]
                msg = pic['file_url']
            await ctx.send(booruappend + msg)
    else:
            msg = 'An error has occured'
            await ctx.send(msg)



#this has to be at the end of the code
#client.run(token)
bot.run(token, bot=True, reconnect=True)
