import os
import json
import logging

from datetime import datetime
from logger_config import LoggerSetup, logger  # Import the logger

import discord
from discord.ext import commands
from discord.ui import View
from dotenv import load_dotenv, find_dotenv


# Load .env variables
load_dotenv(find_dotenv())
TOKEN = os.getenv('TOKEN')


# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)


intents = discord.Intents.default()
intents.message_content = True      # for hybrid commands
bot = commands.AutoShardedBot(command_prefix=config['prefix'], intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Logging in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=config['presence_activity']))

    extensions = [
        "menu",
        "customer_sales_representative"
    ]

    # Loading extensions
    for ext in extensions:
        try:
            await bot.load_extension(f"cogs.{ext}")
            logger.info(f"Loaded extension: {ext}")
        except commands.ExtensionError as e:
            logger.error(f"Failed to load extension {ext}: {e}")
    try:
        synced = await bot.tree.sync()
        logger.info(f"Synced {len(synced)} command(s)")
    except Exception as e:
        logger.error(f"Failed to sync commands: {e}")

    logger.success(f"Logged in as {bot.user}")

@bot.event
async def on_guild_join(guild):
    supportButton = discord.ui.Button(label="Support Server", url=config['support_server_url'])

    view = View(timeout=300)
    view.add_item(supportButton)

    # Fetching the owner/admin who invited the bot to greet them.
    admin_user = None
    try:
        async for entry in guild.audit_logs(action=discord.AuditLogAction.bot_add):
            admin_user = entry.user
            break
    except Exception as e:
        logger.error(f"Failed to fetch audit logs | {e}")
    
    if not admin_user:
        admin_user = guild.owner
    
    embed = discord.Embed(
        title="Thank You!", color=int(config['bot_primary_color'], 16),
        description=f"Thank you for adding {config['bot_name']} to **{guild.name}**. If you encounter any issues with the bot, please don't hesitate to join our [support server]({config['support_server_url']}) for more information."
    ).set_thumbnail(url=config['bot_image'])

    try:
        await admin_user.send(embed=embed, view=view)
    except Exception:
        pass


@bot.event
async def on_guild_remove(guild):
    supportButton = discord.ui.Button(label="Support Server", url=config['support_server_url'])
    view = View(timeout=300)
    view.add_item(supportButton)

    # Send a message to the guild owner when the bot is removed
    try:
        await guild.owner.send(embed=discord.Embed(
                title="Oh No!", color=int(config['bot_primary_color'], 16),
                description=f"I have been removed from **{guild.name}**. If you have encountered any issue with the bot, please report it in the [support server]({config['support_server_url']})."
            ).set_thumbnail(url=config['bot_image']),
            view=view)
    except Exception as e:
        logger.error(f"Failed to send message to the guild owner upon kicking | {e}")


if __name__ == '__main__':
    LoggerSetup(debug_enabled=True)
    log_file_name = f'{datetime.now().strftime("%d-%m-%Y")}-discord.log'
    log_dir = 'logs/discord_logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, log_file_name)
    
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)
    
    try:
        bot.run(TOKEN, log_handler=file_handler)
    except Exception as e:
        logger.error(f"Error with Discord bot TOKEN | {e}")
