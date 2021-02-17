# IsIt Bot

# Imports
import os
import discord
import datetime as dt
# Specific imports
from dotenv import load_dotenv
from discord.ext import commands


# Setting up the bot
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix='h-')
bot.remove_command('help')


# Variables
# Colors
valentines =0xdf6979
embed_color = valentines
timezone = 'Based on UTC +0 time'
github = 'https://github.com/msrogers2015/IsItBot'

holidays = {
    "new year" : [1,1],
    'valentines' : [2,14],
    'april fools' : [4,1],
    'cinco de mayo' : [5,5],
    'juneteenth' : [6,19],
    'independence' : [7,1],
    'halloween' : [10,31],
    'veterns' : [11,11],
    'christmas' : [12,25],
}

v_holidays = {
    # Format is Week, Day, Month
    'mlk' : [3,1,1],
    'president' : [3,1,2],
    'memorial' : [-1,1,5],
    'labor' : [1,1,9],
    'thanksgiving' : [4,4,11],
}

# Print that the bot is online
@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')
    await bot.change_presence(
       activity=discord.Activity(type=discord.ActivityType.watching,
       name=str(len(bot.guilds)) + " servers | h-help")
    )


# Update server count
async def on_guild_join():
    await bot.change_presence(
       activity=discord.Activity(type=discord.ActivityType.watching,
       name=str(len(bot.guilds)) + " servers | h-help")
    )
async def on_guild_remove():
    await bot.change_presence(
       activity=discord.Activity(type=discord.ActivityType.watching,
       name=str(len(bot.guilds)) + " servers | h-help")
    )


# Basic latency test
@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong!", description=f'{round(bot.latency*1000)}ms', color=embed_color)
    await ctx.send(embed=embed)


# Check if today is requested holiday
@bot.command(aliases=['is'])
async def _is(ctx, *, holiday):
    # If today month and day is the same as the saved value
    if holiday in holidays:
        # Creating date objects
        current = dt.datetime.utcnow()
        date = holidays[holiday]
        d = dt.datetime(current.year, date[0], date[1])
        # If date matches today
        if d.month and d.date == current.month and current.day:
            embed = discord.Embed(title=f'Is it {holiday.title()}?', description=f'Yes! Today is {holiday.capitalize()}. :smile: ', color=embed_color)
            embed.set_footer(text=timezone)
            embed.add_field(name=holiday.capitalize(), value=d)
            await ctx.send(embed=embed)
        # If date doesn't match today
        else:
            embed = discord.Embed(title=f'Is it {holiday.title()}?', description=f'Sorry, it is\'t {holiday.capitalize()} :cry:', color=embed_color)
            embed.set_footer(text=timezone)
            embed.add_field(name=holiday.capitalize(), value=d)
            await ctx.send(embed=embed)
    # If holiday isn't in the list
    if holiday not in holidays:
        embed = discord.Embed(title="Error 404: Holiday not found", description=f'Sorry, this holiday hasn\'t been added to the last. Try making a suggestion by opening an issue on the github repo <{github}>', color=embed_color)
        embed.set_footer(text=timezone)
        await ctx.send(embed=embed)


# Giving Wikipedia information for holidays
@bot.command()
async def wiki(ctx, *, holiday):
    if holiday in holidays:
        # Parsing
        uppercase = holiday.title()
        search = holiday.replace(' ',"_")
        await ctx.send(f'<https://en.wikipedia.org/wiki/{search}>')
    if holiday not in holidays:
        embed = discord.Embed(title="Error 404: Holiday not found", description=f'Sorry, this holiday hasn\'t been added to the last. Try making a suggestion by opening an issue on the github repo <{github}>', color=embed_color)
        embed.set_footer(text=timezone)
        await ctx.send(embed=embed)


# A list of currently accepted holidays
@bot.command()
async def dates(ctx):
    embed = discord.Embed(title='Holidays', description='A list of currently supported holidays', color=embed_color)
    for date in holidays:
        d = holidays[date]
        embed.add_field(name=date.title(), value=f'{d[0]}-{d[1]}' ,inline=True)
    return await ctx.send(embed=embed)


# Check time until a holiday
@bot.command()
async def when(ctx, *,holiday):
    if holiday in holidays:
        # Creating date objects
        current = dt.datetime.utcnow()
        date = holidays[holiday]
        d = dt.datetime(current.year, date[0], date[1])
        year_offset = 365
        t_delta = d - current
        # If date matches today
        if d.day and d.month == current.day and current.month:
            embed = discord.Embed(title=f'Today is {holiday.title()}!', description=f'Today is {holiday.capitalize()}. how are you going to celebrate?', color=embed_color)
            embed.set_footer(text=timezone)
            embed.add_field(name=holiday, value=d)
            await ctx.send(embed=embed)
        # If date has passed
        elif t_delta.total_seconds() < 0:
            h_passed = (d + dt.timedelta(days=year_offset)) - current
            result = str(h_passed)
            info, leftover = result.split('.')

            embed = discord.Embed(title=f'When is {holiday.title()}?', description=f'{holiday.capitalize()} is in {info}.', color=embed_color)
            embed.set_footer(text=timezone)
            await ctx.send(embed=embed)
        # If date is in the future
        else:
            result = str(t_delta)
            info, leftover = result.split('.')

            embed = discord.Embed(title=f'When is {holiday.title()}?', description=f'{holiday.capitalize()} is in {info}', color=embed_color)
            embed.set_footer(text=timezone)
            await ctx.send(embed=embed)
    # If holiday isn't in the list
    if holiday not in holidays:
        embed = discord.Embed(title="Error 404: Holiday not found", description=f'Sorry, this holiday hasn\'t been added to the last. Try making a suggestion by opening an issue on the github repo <{github}>', color=embed_color)
        embed.set_footer(text=timezone)
        await ctx.send(embed=embed)


@bot.command()
# Custom help command
async def help(ctx):
    embed = discord.Embed(title=f'Some useful commands!', color=embed_color)
    embed.set_footer(text=timezone)
    embed.add_field(name='h-ping', value='Standard latency testing. Nothing more to see here.', inline=False)
    embed.add_field(name='h-is', value='Check if today is a certain holiday.', inline=False)
    embed.add_field(name='h-when', value='Check how long until a given holiday.', inline=False)
    embed.add_field(name='wiki', value='Get more information about a given holiday.', inline=False)
    embed.add_field(name='h-dates', value='Get a list of currently accpeted holidays.', inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def support(ctx):
    embed = discord.Embed(title='Support Links', description='Support a local developer!', color=embed_color)
    embed.add_field(name='Discord', value='https://discord.com/invite/quailstudio', inline=False)
    embed.add_field(name='Fiverr', value='https://www.fiverr.com/users/quail_studio/seller_dashboard', inline=False)
    embed.add_field(name='Patreon', value='https://www.patreon.com/QuailWare', inline=False)
    embed.add_field(name='Github', value=github, inline=False)
    await ctx.send(embed=embed)

    
# Bot run loop
bot.run(TOKEN)
