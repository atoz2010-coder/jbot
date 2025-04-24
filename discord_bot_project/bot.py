import datetime
import json
import os
import discord
import requests
from discord import app_commands
from discord.ext import commands
from discord.interactions import Interaction

# Load all cog modules dynamically
cog_modules = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        module_name = f'cogs.{filename[:-3]}'  # 'cogs' 폴더의 cog 파일들을 동적으로 로드
        cog_modules.append(module_name)

def load_config():
    """Loads the global configuration."""
    config_path = 'config/config.json'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(data):
    """Saves the global configuration."""
    config_path = 'config/config.json'
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

# Load global configuration
config = load_config()
token = config.get("token", "")
dashboard_url = config.get("dashboard_url", "")
prefix = config.get("prefix", "!")

# Setup bot intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True
intents.guilds = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=prefix, intents=intents)
        self.synced = False  # Ensure slash commands are synced only once

    async def setup_hook(self):
        if not self.synced:
            try:
                await self.tree.sync()
                self.synced = True
                print(f"✅ Slash commands synced with {len(self.tree.get_commands())} commands.")
            except discord.errors.HTTPException as e:
                print(f"❌ Failed to sync commands: {e}")

bot = MyBot()

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}! Bot is ready.')
    print(f"Current time: {datetime.datetime.now(datetime.UTC)} UTC")
    print('Loading cogs...')

    for module in cog_modules:
        try:
            await bot.load_extension(module)
            print(f'Loaded cog: {module}')
        except Exception as e:
            print(f"Failed to load cog {module}: {e}")

@app_commands.command(name="시세", description="실시간 암호화폐와 주식 정보를 제공합니다.")
async def fetch_prices(interaction: Interaction, asset_type: str, asset_name: str):
    try:
        await interaction.response.defer()
        if asset_type.lower() == "crypto":
            response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={asset_name.lower()}&vs_currencies=usd")
            if response.status_code == 200:
                data = response.json()
                price = data.get(asset_name.lower(), {}).get("usd")
                if price:
                    await interaction.followup.send(f"실시간 암호화폐 {asset_name} 가격: ${price}")
                else:
                    await interaction.followup.send(f"{asset_name} 암호화폐 정보를 찾을 수 없습니다.")
            else:
                await interaction.followup.send("암호화폐 가격을 가져오는 데 실패했습니다.")
        elif asset_type.lower() == "stock":
            response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={asset_name.upper()}&apikey=YOUR_STOCK_API_KEY")
            if response.status_code == 200:
                data = response.json()
                price = data.get("Global Quote", {}).get("05. price")
                if price:
                    await interaction.followup.send(f"실시간 주식 {asset_name} 가격: ${price}")
                else:
                    await interaction.followup.send(f"{asset_name} 주식 정보를 찾을 수 없습니다.")
            else:
                await interaction.followup.send("주식 가격을 가져오는 데 실패했습니다.")
        else:
            await interaction.followup.send("잘못된 자산 유형입니다. 'crypto' 또는 'stock'을 사용하세요.")
    except Exception as e:
        await interaction.followup.send("가격을 가져오는 동안 오류가 발생했습니다.")
        print(f"Error in fetch_prices command: {e}")

@app_commands.command(name="대시보드링크", description="서버 설정 대시보드 링크를 제공합니다.")
async def dashboard_link(interaction: Interaction):
    url = dashboard_url or "대시보드 URL이 구성되지 않았습니다."
    await interaction.response.send_message(f"서버 설정 대시보드는 아래 링크를 통해 액세스할 수 있습니다:\n{url}")

# Token 검증
if not token.strip():
    print("❌ Token is missing in the configuration. Please update the config file.")
else:
    bot.run(token.strip())
