import discord
from discord.ext import commands
import json
import time
import os

LOG_FILE_PATH = "logs/economy_logs.txt"


def load_user_data():
    file_path = 'config/economy.json'
    if not os.path.exists(file_path):
        # 파일이 없으면 기본 데이터 생성
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({}, f)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_data = load_user_data()

    def save_user_data(self):
        with open("config/economy.json", "w", encoding='utf-8') as f:
            json.dump(self.user_data, f, indent=4)

    def get_balance(self, user_id):
        return self.user_data.get(user_id, {"cash": 0, "bank": 0, "attendance_bonus": 0})

    @commands.command(name="나의 자산")
    async def balance(self, ctx):
        user_id = str(ctx.author.id)
        data = self.get_balance(user_id)

        embed = discord.Embed(title="💰 나의 재산 상태", color=discord.Color.green())
        embed.add_field(name="현금", value=f"{data['cash']} 원", inline=False)
        embed.add_field(name="은행 예금", value=f"{data['bank']} 원", inline=False)
        embed.add_field(name="출석 보상", value=f"{data['attendance_bonus']} 원", inline=False)

        await ctx.respond(embed=embed)

    @commands.command(name="입금")
    async def deposit(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        data = self.get_balance(user_id)

        if data["cash"] < amount:
            await ctx.respond("현금이 부족합니다.")
            return

        data["cash"] -= amount
        data["bank"] += amount
        self.user_data[user_id] = data
        self.save_user_data()

        await ctx.respond(f"{ctx.author.mention}님, {amount} 원를 은행에 입금했습니다.")
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} deposited {amount} points. Bank balance: {data['bank']}\n")

    @commands.command(name="출금")
    async def withdraw(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        data = self.get_balance(user_id)

        if data["bank"] < amount:
            await ctx.respond("잔액이 부족합니다.")
            return

        data["bank"] -= amount
        data["cash"] += amount
        self.user_data[user_id] = data
        self.save_user_data()

        await ctx.respond(f"{ctx.author.mention}님, {amount} 원를 은행에서 출금했습니다.")
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} withdrew {amount} points. Cash: {data['cash']}\n")

    @commands.command(name="출석체크")
    async def earn(self, ctx, amount: int):
        user_id = str(ctx.author.id)
        data = self.get_balance(user_id)

        data["cash"] += amount
        self.user_data[user_id] = data
        self.save_user_data()

        await ctx.respond(f"{ctx.author.mention}님, {amount} 원를 벌었습니다. 현재 현금: {data['cash']} 원")
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(f"[{time.ctime()}] {ctx.author} earned {amount} points. Cash: {data['cash']}\n")

    @commands.command(name="일일 보너스")
    async def attendance_bonus(self, ctx):
        user_id = str(ctx.author.id)
        data = self.get_balance(user_id)

        daily_bonus = 10000000
        data["attendance_bonus"] += daily_bonus
        data["cash"] += daily_bonus
        self.user_data[user_id] = data
        self.save_user_data()

        await ctx.respond(f"{ctx.author.mention}님, 오늘의 일일 보너스로 {daily_bonus} 원이 추가되었습니다. 현재 현금: {data['cash']} 원")
        with open(LOG_FILE_PATH, "a") as log_file:
            log_file.write(
                f"[{time.ctime()}] {ctx.author} received attendance bonus: {daily_bonus} points. Cash: {data['cash']}\n")


async def setup(bot):
    await bot.add_cog(Economy(bot))

# Example slash command
@commands.slash_command()
async def example_slash(ctx):
    await ctx.respond("This is a slash command!")
