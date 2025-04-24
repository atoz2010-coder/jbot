import discord
from discord.ext import commands
import time

LOG_FILE_PATH = "logs/roles_logs.txt"


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="assign_role")
    @commands.has_permissions(manage_roles=True)
    async def assign_role(self, ctx, member: discord.Member, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            await member.add_roles(role)
            await ctx.respond(f"{member.mention}에게 역할 {role_name}을/를 부여했습니다.")

            with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
                log_file.write(f"[{time.ctime()}] {ctx.author} {member}에게 역할 부여: {role_name}\n")
        else:
            await ctx.respond(f"{role_name} 역할을 찾을 수 없습니다.")


async def setup(bot):
    await bot.add_cog(Roles(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
