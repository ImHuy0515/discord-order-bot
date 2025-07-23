import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
OWNER_ID = os.getenv("OWNER_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")

if not TOKEN or not OWNER_ID or not CHANNEL_ID:
    raise ValueError("❌ Thiếu biến môi trường trong .env")

OWNER_ID = int(OWNER_ID)
CHANNEL_ID = int(CHANNEL_ID)

# Khởi tạo bot với các quyền cần thiết
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")
    try:
        owner = await bot.fetch_user(OWNER_ID)
        if owner:
            await owner.send("📬 Bot đã khởi động thành công!")
            print("✅ Đã gửi DM cho owner.")
    except Exception as e:
        print(f"❌ Lỗi khi gửi DM: {e}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.name == "g2g_notify":
        try:
            owner = await bot.fetch_user(OWNER_ID)
            if owner:
                if message.embeds:
                    # Nếu tin nhắn có embed (do webhook gửi), gửi lại từng cái
                    for embed in message.embeds:
                        clone = discord.Embed.from_dict(embed.to_dict())
                        await owner.send(embed=clone)
                    print("✅ Đã gửi embed đơn hàng cho owner.")
                else:
                    # Nếu không có embed → lọc text và gửi
                    lines = message.content.splitlines()
                    filtered_lines = [
                        line for line in lines
                        if not line.strip().startswith("@") and line.strip() != ""
                    ]
                    clean_text = "\n".join(filtered_lines)
                    if clean_text:
                        await owner.send(
                            f"Khang béo hiện lên và nói: CÓ LÀM THÌ MỚI CÓ ĂN, CHECK ĐƠN ĐÊ\n{clean_text}"
                        )
                        print("✅ Đã gửi đơn hàng dạng text cho owner.")
        except Exception as e:
            print(f"❌ Lỗi khi gửi DM: {e}")

    await bot.process_commands(message)


bot.run(TOKEN)
