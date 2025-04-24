import discord
from discord.ext import commands
import random
import time

LOG_FILE_PATH = "logs/games_logs.txt"


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roll_dice")
    async def roll_dice(self, ctx):
        result = random.randint(1, 6)
        await ctx.respond(f"{ctx.author.mention} 주사위 결과: {result}")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} 주사위 굴림: {result}\n")

    @commands.command(name="flip_coin")
    async def flip_coin(self, ctx):
        result = random.choice(["앞면", "뒷면"])
        await ctx.respond(f"{ctx.author.mention} 동전 던지기 결과: {result}")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} 동전 던지기: {result}\n")


async def setup(bot):
    await bot.add_cog(Games(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
