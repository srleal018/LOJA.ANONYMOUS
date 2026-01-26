import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot online como {bot.user}")

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎟️ Abrir Ticket", style=discord.ButtonStyle.green)
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            overwrites={
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
        )

        await channel.send(
            f"🎫 Ticket de {user.mention}",
            view=FecharView()
        )

        await interaction.response.send_message(
            "✅ Ticket criado!",
            ephemeral=True
        )

class FecharView(discord.ui.View):
    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.red)
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.delete()

@bot.command()
async def ticket(ctx):
    await ctx.send(
        "Clique no botão para abrir um ticket:",
        view=TicketView()
    )

import os

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)

