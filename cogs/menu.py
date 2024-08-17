import json
import discord
from discord.ext import commands  #--- for slash commands
from discord import app_commands  #--- for slash commands
from discord.ui import Select, View
from logger_config import logger

# Load configuration from config.json
with open('config.json') as config_file:
    config = json.load(config_file)

@app_commands.guild_only()
class Menu(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Get list of commands.")
    async def help(self, interaction: discord.Interaction):
        try:
            supportButton = discord.ui.Button(label="Support Server", url=config['support_server_url'])

            select = Select(placeholder="Select a Category for a Specific Module", options=[
                discord.SelectOption(
                    label="Main Menu",
                    emoji="🏠",
                    description="Get to Main Menu"),
                discord.SelectOption(
                    label="Custom Sales Representative",
                    emoji="👋",
                    description="Get All Custom Sales Representative Commands")
            ])

            embed = discord.Embed(
                title=f"⚙  {config['bot_name']} Help Desk", color=int(config['bot_primary_color'], 16),
                description= 
                '''Click on the Dropdown to see each command within a Specific Category.

        **» List of Categories**
        ```👋 Customer Sales Representative
    ```
    Seeking further assistance? Join our Support Discord Server for prompt and reliable help from our expert team and friendly community.''')
            embed.set_thumbnail(url=config['bot_image'])
            embed.set_footer(text=config['embed_footer'], icon_url=config['bot_image'])

            async def my_callback(interaction):
                if select.values[0] == "Main Menu":
                    await interaction.response.edit_message(embed=embed, view=view)

                elif select.values[0] == "Custom Sales Representative":
                    await interaction.response.edit_message(embed=
                                            discord.Embed(title="👋 Custom Sales Representative Commands", color=int(config['bot_primary_color'], 16),
                                            description=
                                            '''**» List of Commands**
    <**/query**> : Ask a question based on the uploaded PDF content.
    <**/upload_file**> : Upload a PDF file to enable the bot to answer queries based on its content.''').set_footer(
                                                            text=config['embed_footer'], 
                                                            icon_url=config['bot_image']
                                                            ), view=view)
            select.callback = my_callback
            view = View(timeout= 300)
            view.add_item(select)
            view.add_item(supportButton)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            logger.error(f"Error in help command: {e}")


async def setup(bot):
    await bot.add_cog(Menu(bot))