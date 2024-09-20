# Third-party imports
import asyncio
from discord.ext import commands
from discord.ext.commands import Context
from discord import Message

# Project-specific imports
from src.cogs.data.load_filters import load_filters, save_filters

# Logger
from src.configuration.debug import setup_logging
logger = setup_logging()

class FilterCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """
        Initializes the FilterCommands cog which contains commands for managing content filters.

        :param bot: The Discord bot instance.
        """
        self.bot = bot
        self.filters = load_filters()

    @commands.command()
    async def help(self, ctx: Context) -> None:
        """
        Custom help command for explaining how to use each filter-related command.

        :param ctx: The command context.
        """
        botprefix = ctx.prefix

        help_message = (
            "Help Command\n\n"
            "Here's how to use the available commands:\n"
            "`[]` = Optional | `<>` = Required\n\n"
            f"**{botprefix}filteradd <filter_word>** - Add a filter to the global filter list.\n"
            f"  > Example: `{botprefix}filteradd meow`\n"
            "  > Adds 'meow' to the list of filters being tracked.\n\n"
            f"**{botprefix}filterremove <filter_word>** - Remove a filter from the global filter list.\n"
            f"  > Example: `{botprefix}filterremove meow`\n"
            "  > Removes 'meow' from the list of filters being tracked.\n\n"
            f"**{botprefix}filterlists** - Lists all the current global filters.\n"
            f"  > Example: `{botprefix}filterlists`\n"
            "  > Shows all filters that are being tracked.\n\n"
            f"**{botprefix}clearfilters** - Clears all filters from the global list after confirmation.\n"
            f"  > Example: `{botprefix}clearfilters`\n"
            "  > Prompts a confirmation dialog to clear all filters."
        )

        await ctx.send(help_message)

    @commands.command(aliases=['addfilter'])
    async def filteradd(self, ctx: Context, *, filter_word: str) -> None:
        """
        Adds a new filter to the global filter list.

        :param ctx: The command context.
        :param filter_word: The word to add to the filter list.
        """
        filters = load_filters()  
        normalized_filter = filter_word.upper()

        if normalized_filter not in filters:
            filters.append(normalized_filter)
            save_filters(filters)

            await ctx.send(
                f"{ctx.author.mention}: Now listening to anything that includes '{normalized_filter}'.\n"
                f"Current total filters: {len(filters)}"
            )
        else:
            await ctx.send(
                f"{ctx.author.mention}: I am **already** listening to anything that includes '{normalized_filter}'."
            )

    @commands.command(aliases=['removefilter'])
    async def filterremove(self, ctx: Context, *, filter_word: str) -> None:
        """
        Removes a filter from the global filter list.

        :param ctx: The command context.
        :param filter_word: The word to remove from the filter list.
        """
        filters = load_filters()
        normalized_filter = filter_word.upper()

        if normalized_filter in filters:
            filters.remove(normalized_filter)
            save_filters(filters)

            await ctx.send(
                f"{ctx.author.mention}: Filter '{filter_word}' has been successfully removed from the list.\n"
                f"Current total filters: {len(filters)}"
            )
        else:
            await ctx.send(
                f"{ctx.author.mention}: Filter '{filter_word}' does not exist in the list."
            )

    @commands.command(aliases=['listfilters', 'listfilter', 'filterlist'])
    async def filterlists(self, ctx: Context) -> None:
        """
        Lists all currently active filters in the global filter list.

        :param ctx: The command context.
        """
        filters = load_filters()
        if filters:
            filters_list = '\n'.join([f"- {filter_word}" for filter_word in filters])

            await ctx.send(
                f"Here are the current filters being monitored:\n{filters_list}\n"
                f"Total Filters: {len(filters)}"
            )
        else:
            await ctx.send("No filters set.")

    @commands.command(aliases=['filtersclear'])
    async def clearfilters(self, ctx: Context) -> None:
        """
        Clears all filters from the global filter list after user confirmation.

        :param ctx: The command context.
        """
        filters = load_filters()

        if not filters:
            await ctx.send(f"{ctx.author.mention}: There are no filters to clear.")
            return

        await ctx.send(
            f"{ctx.author.mention}: Are you sure you want to clear `{len(filters)}` filters from the list? "
            "Reply with 'Yes' to confirm or 'No' to cancel."
        )

        def check(m: Message) -> bool:
            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no"]

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)

            if msg.content.lower() == "yes":
                amt = len(filters)
                filters.clear()
                save_filters(filters)

                await ctx.send(f"{ctx.author.mention}: Successfully cleared `{amt}` filters from the list.")
            else:
                await ctx.send(f"{ctx.author.mention}: Cancelled clearance of `{len(filters)}` filters.")
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention}: Timed out. No filters were cleared.")

async def setup(bot: commands.Bot) -> None:
    """
    Asynchronous function to set up the FilterCommands cog.

    :param bot: The Discord bot instance.
    """
    await bot.add_cog(FilterCommands(bot))