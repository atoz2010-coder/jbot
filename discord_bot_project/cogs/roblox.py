import discord
from discord.ext import commands
import time

LOG_FILE_PATH = "logs/roblox_logs.txt"


class Roblox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roblox_profile")
    async def roblox_profile(self, ctx, username: str):
        # 로블록스 프로필 정보를 가져오는 로직을 여기에 구현합니다.
        await ctx.respond(f"{ctx.author.mention} 요청하신 로블록스 프로필: {username}")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} 로블록스 프로필 요청: {username}\n")


async def setup(bot):
    await bot.add_cog(Roblox(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
