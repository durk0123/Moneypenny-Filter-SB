# Third-party imports
from discord.ext import commands

# Project-specific imports
from src.configuration.config import config
from src.utilities.console import clear_console, TerminalColors

# Logger
from src.configuration.debug import setup_logging
logger = setup_logging()

class Start(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """
        Initializes the Start cog, which handles events when the bot becomes ready.

        :param bot: The Discord bot instance.
        """
        self.bot = bot
        self.config = config

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """
        Event listener that is triggered when the bot is ready.

        This method performs the following actions:
        - Clears the console for a fresh log view.
        - Logs a message indicating the bot's connection to Discord.
        - Logs the command prefix set in the configuration.
        """
        clear_console()
        logger.info(f"{TerminalColors.GREEN}{self.bot.user}{TerminalColors.RESET} connected to {TerminalColors.BLUE}Discord{TerminalColors.RESET}")
        logger.info(f"Prefix: {self.config['prefix']}")

async def setup(bot: commands.Bot) -> None:
    """
    Asynchronous function to set up the Start cog.

    :param bot: The Discord bot instance.
    """
    await bot.add_cog(Start(bot))