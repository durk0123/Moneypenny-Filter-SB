# System imports
from datetime import datetime
from typing import Optional

# Third-party imports
import discord
from discord.ext import commands
import aiohttp  # Needed for sending webhook requests

# Project-specific imports
from src.configuration.config import config 
from src.cogs.data.load_filters import load_filters

# Logger
from src.configuration.debug import setup_logging
logger = setup_logging()

class MoneyPenny(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.webhook_url = config['webhook_url']

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """
        Listener for incoming messages. It processes messages and checks if they contain 
        specific filters. If a match is found, it sends a webhook notification.
        """
        # Skip the bot's own messages and command messages
        if message.author.id == self.bot.user.id or message.content.startswith('.'):
            return

        # Log to check if any message is detected (debugging)
        logger.info(f"Received message from: {message.author} (webhook_id: {message.webhook_id})")

        # Detect webhook messages by checking webhook_id or if author is a bot without a discriminator (webhook)
        if message.webhook_id or (message.author.bot and message.author.discriminator == "0000"):
            logger.info(f"Webhook or bot message detected: {message.content}")

            # Check if the message contains embeds
            for embed in message.embeds:
                if embed.author and embed.author.name == "Moneypenny":
                    filters = load_filters()  # Load the latest filters
                    
                    # Normalize filters to uppercase for case-insensitive matching
                    normalized_filters = [filter_word.upper() for filter_word in filters]

                    for filter_word in normalized_filters:
                        logger.debug(f"Checking filter '{filter_word}' in embed title(s)")

                        # Case-insensitive search for the filter word in the title
                        if embed.title and filter_word.lower() in embed.title.lower():
                            logger.info(f"Filter '{filter_word}' matched in embed title: {embed.title}")

                            # Find the start and end index of the filter word in the title (case-insensitive)
                            start_index = embed.title.lower().find(filter_word.lower())
                            end_index = start_index + len(filter_word)

                            # Bold the part of the title where the filter was found, preserving case
                            bolded_title = f"{embed.title[:start_index]}**{embed.title[start_index:end_index]}**{embed.title[end_index:]}"

                            # Initialize address field
                            address_value: Optional[str] = None

                            # Check for a field named "Address" or "Address:", case-insensitive
                            for field in embed.fields:
                                if field.name.lower() in ["address", "address:"]:
                                    address_value = field.value
                                    logger.info(f"Address found: {address_value}")
                                    break

                            # Prepare and send the alert with the clickable "Jump to Message" link
                            jump_url = message.jump_url
                            embed_alert = discord.Embed(
                                title=f"Filter **{filter_word.upper()}** found in message!",
                                description="**Details**: Filter matched in the title.",
                                color=0x7F868C,
                                timestamp=datetime.now()
                            )

                            embed_alert.add_field(
                                name="**Original Message Title**",
                                value=bolded_title if bolded_title else "No title",
                                inline=False
                            )

                            # Add the address field if it was found
                            if address_value:
                                embed_alert.add_field(
                                    name="**Address**",
                                    value=address_value,
                                    inline=False
                                )

                            embed_alert.add_field(
                                name="**Jump to Message**",
                                value=f"[Click here to view the message]({jump_url})",
                                inline=False
                            )

                            await self.send_webhook(embed_alert)
                            logger.info(f"Filter '{filter_word}' matched and alert sent.")
                            break
                        
        await self.bot.process_commands(message)

    async def send_webhook(self, embed: discord.Embed) -> None:
        """
        Sends a webhook notification with the embed if any filters are found in the message.
        """
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(self.webhook_url, session=session)

            # Get the bot's username and avatar
            bot_username = self.bot.user.display_name  # Self-bot's display name
            bot_avatar_url = self.bot.user.avatar.url  # Self-bot's avatar URL

            # Send the @everyone mention along with the embed
            await webhook.send(
                content="@everyone",
                embed=embed, 
                username=bot_username, 
                avatar_url=bot_avatar_url
            )

async def setup(bot: commands.Bot) -> None:
    """
    Setup function to add the MoneyPenny cog to the bot.
    """
    await bot.add_cog(MoneyPenny(bot))
