
from discord.ext import commands

class Faq(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

import discord
from discord.ext import commands
import json
import time

LOG_FILE_PATH = "logs/faq_logs.txt"


class FAQ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.faq_data = self.load_faq_data()

    def load_faq_data(self):
        try:
            with open("config/faq.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_faq_data(self):
        with open("config/faq.json", "w", encoding="utf-8") as f:
            json.dump(self.faq_data, f, ensure_ascii=False, indent=4)

    @commands.command(name="faq")
    async def faq(self, ctx, question: str):
        answer = self.faq_data.get(question.lower())
        if answer:
            await ctx.respond(f"**{question}**: {answer}")
        else:
            await ctx.respond(f"**{question}**에 대한 답변이 없습니다.")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} FAQ 요청: {question}\n")

    @commands.command(name="add_faq")
    @commands.has_permissions(administrator=True)
    async def add_faq(self, ctx, question: str, *, answer: str):
        self.faq_data[question.lower()] = answer
        self.save_faq_data()
        await ctx.respond(f"새 자주 묻는 질문 추가됨: **{question}** - {answer}")

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} FAQ 추가: {question} - {answer}\n")


async def setup(bot):
    await bot.add_cog(FAQ(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
