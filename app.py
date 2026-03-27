import discord
from discord import ext
from discord.ext import commands


from dotenv import load_dotenv
import os


Intents = discord.Intents.default()
Intents.message_content = True

bot = commands.Bot(intents=Intents, command_prefix="!")

# loading cogs by loading every python file in the folder cogs


async def load_cogs():
    # getting the cogs folder
    for filename in os.listdir("./cogs"):

        # check if the file is a python file
        if filename.endswith(".py"):

            # trying to load a file in cogs
            try:

                # loading the file
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded cog: {filename}")

            # if the loading fails
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")  # print the error


@bot.event
async def on_ready():
    print(f"logged on as {bot.user}, latency: {bot.latency}")


async def main():

    # loading the .env file for token

    load_dotenv()
    # loading cogs

    await load_cogs()
    # get the loaded .env file token using os.getenv
    token = os.getenv("TOKEN")

    await bot.start(token)  # start the token with the


if __name__ == "__main__":

    import asyncio

    asyncio.run(main())
