# System imports
import asyncio
import aiohttp
import os
from typing import NoReturn, Optional

# Third-party imports
import discord
from discord.ext import commands

# Project-specific imports
from src.configuration.config import config
from src.configuration.debug import setup_logging

# Set up logging
logger = setup_logging()

# Initialize bot with the specified prefix and configurations
bot = commands.Bot(command_prefix=config['prefix'], self_bot=True, case_insensitive=True)
bot.remove_command('help')  # Removing default help command

# Placeholder for aiohttp session, using a type comment to avoid Pylance errors
bot.session = None  # type: Optional[aiohttp.ClientSession]

async def load_cogs() -> None:
    """
    Asynchronously loads all cog extensions from the 'src/cogs' directory.

    This function iterates over each Python file in the 'src/cogs' directory 
    and attempts to load it as an extension into the bot if the filename ends with '.py'.
    Logs successful cog loading or errors.
    """
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py'):
            cog_name = f'src.cogs.{filename[:-3]}'  # Strip '.py' to get cog name
            try:
                await bot.load_extension(cog_name)
                logger.info(f"Loaded cog: {cog_name}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_name}: {e}", exc_info=True)

async def main() -> NoReturn:
    """
    Main entry point for the bot.

    This function initializes the aiohttp session, loads the cogs, and starts the bot.
    """
    # Initialize aiohttp session for making asynchronous HTTP requests
    bot.session = aiohttp.ClientSession()

    # Load bot extensions (cogs)
    await load_cogs()

    # Start the bot using the token from the configuration
    await bot.start(config['token'])

@bot.event
async def on_shutdown() -> None:
    """
    Event handler that is called when the bot shuts down.

    This ensures that the aiohttp session is properly closed when the bot is shutting down.
    """
    if bot.session:
        await bot.session.close()
    logger.info("Closed aiohttp session.")

# Run the main function inside the asyncio event loop
asyncio.run(main())
