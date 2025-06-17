import discord
import os
from dotenv import load_dotenv

load_dotenv()
_TOKEN_ = os.getenv("TOKEN")

bot = discord.Bot()

@bot.slash_command(name="pat", description="Patting Nagi")
async def pat(ctx: discord.ApplicationContext):
    await ctx.respond("Meow~")

bot.run(_TOKEN_)
