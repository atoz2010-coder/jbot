import discord
from discord.ext import commands
import asyncio
import time

LOG_FILE_PATH = "logs/music_logs.txt"


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="play_music")
    async def play_music(self, ctx, url: str):
        # 음악을 플레이하는 로직을 여기에 구현합니다.
        await ctx.respond(f"{ctx.author.mention} 요청하신 음악을 재생 중입니다: {url}")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} 음악 재생: {url}\n")

    @commands.command(name="stop_music")
    async def stop_music(self, ctx):
        # 음악을 멈추는 로직을 여기에 구현합니다.
        await ctx.respond(f"{ctx.author.mention} 음악이 중지되었습니다.")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} 음악 중지\n")


async def setup(bot):
    await bot.add_cog(Music(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
