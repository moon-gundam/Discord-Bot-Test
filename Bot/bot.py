import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve API keys and bot token from environment variables
OMDB_API_KEY = os.getenv('OMDB_API_KEY')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CAT_API_KEY = os.getenv('CAT_API_KEY')  # Cat API key

intents = discord.Intents.default()
intents.members = True  # Enable member intent
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    embed = discord.Embed(title=f"{member.name}'s Profile", color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Username", value=member.name, inline=True)
    embed.add_field(name="Discriminator", value=member.discriminator, inline=True)
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(name="Status", value=str(member.status).title(), inline=True)
    embed.add_field(name="Top Role", value=member.top_role.name, inline=True)
    embed.add_field(name="Joined At", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def movie(ctx, *, title):
    """Search for a movie by title."""
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")
    data = response.json()

    if data['Response'] == 'True':
        embed = discord.Embed(title=data['Title'], description=data['Plot'], color=discord.Color.red())
        embed.set_thumbnail(url=data['Poster'])
        embed.add_field(name="Year", value=data['Year'], inline=True)
        embed.add_field(name="Rated", value=data['Rated'], inline=True)
        embed.add_field(name="Runtime", value=data['Runtime'], inline=True)
        embed.add_field(name="Genre", value=data['Genre'], inline=True)
        embed.add_field(name="Director", value=data['Director'], inline=True)
        embed.add_field(name="Writer", value=data['Writer'], inline=True)
        embed.add_field(name="Actors", value=data['Actors'], inline=True)
        embed.add_field(name="IMDB Rating", value=data['imdbRating'], inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Movie not found!")

@bot.command()
async def show(ctx, *, title):
    """Search for a TV show by title."""
    response = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}")
    data = response.json()

    if data['Response'] == 'True' and data['Type'] == 'series':
        embed = discord.Embed(title=data['Title'], description=data['Plot'], color=discord.Color.blue())
        embed.set_thumbnail(url=data['Poster'])
        embed.add_field(name="Year", value=data['Year'], inline=True)
        embed.add_field(name="Rated", value=data['Rated'], inline=True)
        embed.add_field(name="Runtime", value=data['Runtime'], inline=True)
        embed.add_field(name="Genre", value=data['Genre'], inline=True)
        embed.add_field(name="Director", value=data['Director'], inline=True)
        embed.add_field(name="Writer", value=data['Writer'], inline=True)
        embed.add_field(name="Actors", value=data['Actors'], inline=True)
        embed.add_field(name="IMDB Rating", value=data['imdbRating'], inline=True)
        await ctx.send(embed=embed)
    else:
        await ctx.send("TV show not found!")

@bot.command()
async def cat(ctx):
    """Generate a random image of a cat."""
    headers = {
        'x-api-key': CAT_API_KEY  # Add API key to headers
    }
    response = requests.get("https://api.thecatapi.com/v1/images/search", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data[0]['url']
        await ctx.send(image_url)
    else:
        await ctx.send("Sorry, I couldn't fetch a cat image at the moment.")

# Run the bot with the token from environment variables
bot.run(BOT_TOKEN)
