#Import files for use
import os
import random
import discord
import datetime


#Import specific items from above files
from dotenv import load_dotenv
from discord.ext import commands

#Setting up bot token
load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='-', activity=discord.Activity(type=discord.ActivityType.watching,
       name=str(len(bot.guilds)) + " servers | -help"))
bot.remove_command('help')


# Get next year
y = datetime.datetime.now()

# Holidays
holidays = {
    'christmas' : datetime.datetime(y.year, 12, 25),
    'new year' : datetime.datetime(y.year, 1, 1),
    'valentines' : datetime.datetime(y.year, 2, 14),
    'aprilfools' : datetime.datetime(y.year, 4, 1),
    'cincodemayo' : datetime.datetime(y.year, 5, 5),
    'juneteenth' : datetime.datetime(y.year, 6, 19),
    'halloween' : datetime.datetime(y.year, 10, 31),
    'veterns' : datetime.datetime(y.year, 11, 11),
    'independence': datetime.datetime(y.year, 7, 4),
}

'''
# Holidays that change dates
easter
mothersday
fathersday
thanksgiving
springforward
fallback
memroial
winter
summer
laborday
blackfriday
cybermonday
'''

#Embed Color
embed_color = 0xff8200
timezone = "Based on Louisville, KY UTC-5"



#When the bot is online, print in terminal
@bot.event
async def on_ready():
   print(f'{bot.user.name} has connected to a server')


#Ping command to check for latency
@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'{round(bot.latency*1000)}ms', color=embed_color)
    embed.set_footer(text=timezone)
    await ctx.send(embed=embed)


@bot.command()
async def whenis(ctx, *,holiday):

    # Get the current year and check for leap year
    y = datetime.datetime.now()
    if y.year % 4 ==0:
        year_add = 366
    else:
        year_add = 365


    # Check if holiday has been listed
    if(holiday in holidays):
        time_diff = holidays[holiday] - y
        # If the holiday has already passed, add one year
        if time_diff.total_seconds() < 0:
            updated = (holidays[holiday]+ datetime.timedelta(days=year_add)) - y
            result = str(updated)
            info, leftover = result.split('.')

            embed = discord.Embed(title=f'When is {holiday.title()}?', description=f'{holiday.capitalize()} is in {info}.', color=embed_color)
            embed.set_footer(text=timezone)
            await ctx.send(embed=embed)
        # If holiday hasn't passed
        else:
            result = str(time_diff)
            info, leftover = result.split('.')

            embed = discord.Embed(title=f'When is {holiday.title()}?', description=f'{holiday.capitalize()} is in {info}', color=embed_color)
            embed.set_footer(text=timezone)
            await ctx.send(embed=embed)



@bot.command()
async def isit(ctx, *, holiday):
    if holidays[holiday].month and holidays[holiday].day == y.month and y.day:
        embed = discord.Embed(title=f'Is it {holiday.title()}?', description=f'Yes! Today is {holiday.capitalize()}. :smile: ', color=embed_color)
        embed.set_footer(text=timezone)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title=f'Is it {holiday.title()}?', description=f'Sorry, it is\'t {holiday.capitalize()} :cry:', color=embed_color)
        embed.set_footer(text=timezone)
        await ctx.send(embed=embed)


@bot.command()
async def wiki(ctx, *, holiday):
    if holiday in holidays:
        uppercase = holiday.title()
        search = holiday.replace(' ',"_")
        await ctx.send(f'<https://en.wikipedia.org/wiki/{search}>')
    if holiday not in holidays:
        await ctx.send('Sorry, I cant provide more information')


@bot.command()
async def dates(ctx):
    embed = discord.Embed(title='Holidays', description='A list of currently supported holidays', color=embed_color)
    for date in holidays:
        embed.add_field(name=date.title(), value=holidays[date].strftime("%b") + '-' + str(holidays[date].day) ,inline=False)
    return await ctx.send(embed=embed)



@bot.command()
async def help(ctx):
    embed = discord.Embed(title='IsItBot Help', description='Directions on how to use difference commands', color=embed_color, inline=False)
    embed.add_field(name='isit <holiday>', value='Tells you if the requested holiday is today.', inline=False)
    embed.add_field(name='whenis <holiday', value='Gives a time value for how long until given holiday.', inline=False)
    embed.add_field(name='wiki <holiday>', value='Returns a wiki link for more information on given holiday.', inline=False)
    embed.add_field(name='ping', value='Command to see if the bot is online.', inline=False)
    embed.add_field(name='dates', value='Returns a list of currently accepted holidays', inline=False)

    await ctx.send(embed=embed)
bot.run(TOKEN)