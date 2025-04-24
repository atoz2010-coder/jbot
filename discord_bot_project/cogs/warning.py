import discord
from discord.ext import commands
import time

LOG_FILE_PATH = "logs/warning_logs.txt"

class Warning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_warnings = {}

    @commands.command(name="warn")
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member, reason: str = "사유 없음"):
        # 경고 기능 구현
        warning_count = self.user_warnings.get(member.id, 0) + 1
        self.user_warnings[member.id] = warning_count

        if warning_count >= 8:
            await member.timeout(duration=3600)
            await ctx.respond(f"{member.mention}님이 1시간 동안 타임아웃 처리되었습니다. 이유: {reason}")
        else:
            await ctx.respond(f"{member.mention}님에게 경고가 부여되었습니다. 이유: {reason}")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} {member}에게 경고: {reason}\n")

async def setup(bot):
    await bot.add_cog(Warning(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
