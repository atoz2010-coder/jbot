
from discord.ext import commands

class Server_status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

import discord
from discord.ext import commands
import time

LOG_FILE_PATH = "logs/server_status_logs.txt"


class ServerStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="서버 상태 알림")
    @commands.has_permissions(administrator=True)
    async def server_status(self, ctx, status_message: str):
        # 서버 상태 메시지를 업데이트하는 로직
        await ctx.respond(f"서버 상태 업데이트: {status_message}")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} 서버 상태 업데이트: {status_message}\n")


async def setup(bot):
    await bot.add_cog(ServerStatus(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
