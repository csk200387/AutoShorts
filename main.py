import os
import discord
from dotenv import load_dotenv
from src.download import download
import time

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


# check video_nums file and video_queue
if not os.path.exists("src/video_nums"):
    with open("src/video_nums", "w") as f:
        f.write("1")

if not os.path.exists("src/video_queue"):
    with open("src/video_queue", "w") as f:
        f.write("")

@client.event
async def on_ready():
    # activity message
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="AutoShorts Ready"))
    await tree.sync()
    print("Bot is Ready.")


@tree.command(name="upload", description="다운로드 & 업로드")
async def upload_command(interaction: discord.Interaction, url:str):
    await interaction.response.defer()
    msg = await interaction.followup.send("다운로드 중...")
    videoid = download(url)


    await msg.edit(content=f"다운로드 완료. ID : {videoid}\n유튜브로 업로드중...")

    # Recording the number in the title
    with open("src/video_nums", "r") as f:
        partnum = int(f.read())
    with open("src/video_nums", "w") as f:
        f.write(str(partnum+1))

    os.system(f'python3 src/upload.py --file="{videoid}.webm" --title="Quick Dopamine Hits: Funny Memes, Part {partnum}" --description="#shorts #memes" --keywords="funny, memes, shorts" --category="22" --privacyStatus="public" --noauth_local_webserver')


    await msg.edit(content=f"꺼억~ 업로드 완료. 감사합니다.")
    os.remove(f"{videoid}.webm")


@tree.command(name="addqueue", description="대기열에 영상 저장")
async def queue_command(interaction: discord.Interaction, url:str):
    await interaction.response.defer()
    msg = await interaction.followup.send("큐에 추가중입니다..")

    with open("src/video_queue", "a") as f:
        f.write(url + "\n")

    await msg.edit(content="큐에 추가 완료.")


client.run(DISCORD_TOKEN)