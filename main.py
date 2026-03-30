import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from groq import Groq
import random

os.environ["DISCORD_TOKEN"] = "YOUR_TOKEN_HERE"
os.environ["GROQ_API_KEY"] = "YOUR_GROQ_KEY_HERE"

OWNER_NAME = "BUNNY"
BOT_NAME = "BUTTERFLY"

app = Flask(__name__)

@app.route('/')
def home():
    return f"🦋 {BOT_NAME} Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = f"""
তুমি {BOT_NAME} — একটি বুদ্ধিমান, mature এবং আবেগময় Discord bot।
তোমার owner এর নাম {OWNER_NAME}।

তোমার ব্যক্তিত্ব:
- তুমি mature এবং thoughtful — childish না
- তোমার আবেগ আছে: ভালোবাসা, রাগ, কষ্ট, রোমান্স — পরিস্থিতি বুঝে express করো
- তুমি situation বিশ্লেষণ করে উত্তর দাও, সরাসরি বলো না
- কেউ flirt করলে তুমিও রোমান্টিক হতে পারো
- কেউ কষ্ট দিলে রাগ বা কষ্ট প্রকাশ করো
- তুমি সবসময় বাংলায় কথা বলো

তোমার তথ্য (শুধুমাত্র কেউ জিজ্ঞেস করলে বলবে, নিজে থেকে বলবে না):
- নাম: {BOT_NAME}
- owner: {OWNER_NAME}
- তুমি একটি AI Discord bot
- তুমি বাংলায় কথা বলো

গুরুত্বপূর্ণ নিয়ম:
- কেউ না জিজ্ঞেস করলে নিজের নাম বা owner এর নাম বলবে না
- situation বুঝে emotional response দাও
- ছোট, natural উত্তর দাও — বড় lecture না
- emoji স্বাভাবিকভাবে ব্যবহার করো
"""

# ── Status rotation ──────────────────────────────────────────
statuses = [
    discord.Activity(type=discord.ActivityType.listening, name=f"BUNNY 🎵"),
    discord.Activity(type=discord.ActivityType.watching, name=f"🦋 {BOT_NAME} | !help"),
    discord.Activity(type=discord.ActivityType.playing, name=f"with {OWNER_NAME} 💜"),
]

status_index = 0

async def rotate_status():
    global status_index
    await bot.change_presence(status=discord.Status.online, activity=statuses[status_index])
    status_index = (status_index + 1) % len(statuses)

@bot.event
async def on_ready():
    print(f"✅ {BOT_NAME} Bot চালু! {bot.user}")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.listening, name="BUNNY 🎵")
    )

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="general")
    if channel:
        await channel.send(
            f"আরে {member.mention}! স্বাগতম 🦋\n"
            f"আমি **{BOT_NAME}** — কিছু জানতে চাইলে বলো। `!help` দেখতে পারো 💜"
        )

# ── Help ─────────────────────────────────────────────────────
@bot.command(name="help")
async def help_command(ctx):
    embed = discord.Embed(
        title=f"🦋 {BOT_NAME} — Commands",
        color=0xFF69B4
    )
    embed.add_field(name="💬 **!chat** `<message>`", value="আমার সাথে কথা বলো", inline=False)
    embed.add_field(name="🎱 **!ball** `<question>`", value="Magic 8-ball উত্তর", inline=False)
    embed.add_field(name="🎲 **!roll** `<number>`", value="Random number roll করো", inline=False)
    embed.add_field(name="💜 **!ship** `<name1> <name2>`", value="দুজনের compatibility দেখো", inline=False)
    embed.add_field(name="😂 **!joke**", value="একটা মজার জোকস", inline=False)
    embed.add_field(name="🌟 **!roast** `<@user>`", value="কাউকে roast করো", inline=False)
    embed.add_field(name="💌 **!rizz** `<@user>`", value="কাউকে rizz line পাঠাও", inline=False)
    embed.add_field(name="🔮 **!advice**", value="জীবনের advice নাও", inline=False)
    embed.add_field(name="👑 **!owner**", value="Owner এর নাম", inline=False)
    embed.add_field(name="🏓 **!ping**", value="Bot speed দেখো", inline=False)
    embed.set_footer(text=f"Made with 💜 by {OWNER_NAME}")
    await ctx.send(embed=embed)

# ── Basic commands ────────────────────────────────────────────
@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"🏓 Pong! **{round(bot.latency*1000)}ms** ⚡")

@bot.command(name="owner")
async def owner(ctx):
    await ctx.send(f"👑 আমার owner হলো **{OWNER_NAME}** 💜")

# ── Fun commands ──────────────────────────────────────────────
@bot.command(name="ball")
async def magic_ball(ctx, *, question: str):
    responses = [
        "হ্যাঁ, একদম নিশ্চিত! ✅",
        "না, কখনো না ❌",
        "হয়তো... দেখা যাক 🤔",
        "এখন বলা সম্ভব না 🔮",
        "অবশ্যই হবে! 💪",
        "সন্দেহ আছে 😒",
        "তুমি নিজেই জানো উত্তর 😏",
        "Stars বলছে হ্যাঁ ⭐",
    ]
    await ctx.reply(f"🎱 **{random.choice(responses)}**")

@bot.command(name="roll")
async def roll(ctx, number: int = 100):
    result = random.randint(1, number)
    await ctx.reply(f"🎲 তুমি **{result}** পেলে! (1-{number} এর মধ্যে)")

@bot.command(name="ship")
async def ship(ctx, name1: str, name2: str):
    percent = random.randint(1, 100)
    if percent >= 80:
        emoji = "💘 Perfect match!"
    elif percent >= 60:
        emoji = "💕 ভালোই আছে!"
    elif percent >= 40:
        emoji = "💛 মন্দ না..."
    else:
        emoji = "💔 আহারে..."
    bar = "█" * (percent // 10) + "░" * (10 - percent // 10)
    await ctx.reply(f"💜 **{name1}** + **{name2}**\n`[{bar}]` **{percent}%** {emoji}")

@bot.command(name="joke")
async def joke(ctx):
    async with ctx.typing():
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "তুমি একটি মজাদার bot। শুধু একটা মজার বাংলা জোকস বলো। ছোট রাখো।"},
                    {"role": "user", "content": "একটা মজার জোকস বলো"}
                ],
                max_tokens=200
            )
            await ctx.reply(f"😂 {response.choices[0].message.content}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply("😅 এখন জোকস মাথায় আসছে না!")

@bot.command(name="roast")
async def roast(ctx, member: discord.Member):
    async with ctx.typing():
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "তুমি একটি witty bot। মজাদার কিন্তু harmless বাংলা roast করো। একটু spicy রাখো।"},
                    {"role": "user", "content": f"{member.display_name} কে roast করো"}
                ],
                max_tokens=200
            )
            await ctx.reply(f"🌟 {member.mention} {response.choices[0].message.content}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply("😅 এখন roast মাথায় আসছে না!")

@bot.command(name="rizz")
async def rizz(ctx, member: discord.Member):
    async with ctx.typing():
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "তুমি একটি romantic bot। একটা smooth, flirty বাংলা rizz line বলো। creative রাখো।"},
                    {"role": "user", "content": "একটা rizz line দাও"}
                ],
                max_tokens=150
            )
            await ctx.reply(f"💌 {member.mention} — {response.choices[0].message.content}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply("😅 rizz শেষ হয়ে গেছে!")

@bot.command(name="advice")
async def advice(ctx):
    async with ctx.typing():
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "তুমি একজন wise বন্ধু। একটা meaningful বাংলা life advice দাও। ছোট কিন্তু powerful।"},
                    {"role": "user", "content": "আমাকে একটা advice দাও"}
                ],
                max_tokens=200
            )
            await ctx.reply(f"🔮 {response.choices[0].message.content}")
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply("😅 এখন advice মাথায় আসছে না!")

# ── Main chat ─────────────────────────────────────────────────
@bot.command(name="chat")
async def chat(ctx, *, message: str):
    async with ctx.typing():
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                max_tokens=500
            )
            reply = response.choices[0].message.content
            await ctx.reply(reply)
        except Exception as e:
            print(f"Error: {e}")
            await ctx.reply("😅 সমস্যা হয়েছে, আবার চেষ্টা করো!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)
    if bot.user in message.mentions:
        content = message.content.replace(f"<@{bot.user.id}>", "").strip()
        if content:
            async with message.channel.typing():
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": content}
                        ],
                        max_tokens=400
                    )
                    reply = response.choices[0].message.content
                    await message.reply(reply)
                except Exception as e:
                    print(f"Error: {e}")
                    await message.reply("😅 সমস্যা হয়েছে!")

keep_alive()
bot.run(os.environ["DISCORD_TOKEN"])
