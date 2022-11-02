import discord
import subprocess
import datetime
import os
from dotenv import load_dotenv
from discord import app_commands
load_dotenv()

Token = os.getenv('Token')
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def res_cmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

@client.event
async def on_ready():
    print("Login successful!")
    await tree.sync()

@tree.command(name="start")
async def start(interaction: discord.Interaction):
    """サーバーを起動する"""
    if interaction.user.guild_permissions.mention_everyone:
        await interaction.response.send_message("\N{White Heavy Check Mark} **サーバーを起動しています**")
        start = "nohup java -Xms4G -jar paper-1.19.1-91.jar"
        subprocess.call(start.split())
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="stop")
async def stop(interaction: discord.Interaction):
    """サーバーを停止する"""
    if interaction.user.guild_permissions.mention_everyone:
        await interaction.response.send_message("\N{Octagonal Sign} **サーバーを停止します。**")
        stop = "pkill java"
        subprocess.call(stop.split())
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="restart")
async def restart(interaction: discord.Interaction):
    """サーバーを再起動する"""
    if interaction.user.guild_permissions.mention_everyone:
        await interaction.response.send_message("\N{White Heavy Check Mark} **サーバーを再起動しています**")
        stop = "pkill java"
        start = "nohup java -Xms4G -jar paper-1.19.1-91.jar"
        subprocess.call(stop.split())
        subprocess.call(start.split())
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="install")
@app_commands.describe(url='プラグインのダウンロードURL')
async def install(interaction: discord.Interaction, url: str):
    """プラグインをインストールする"""
    if interaction.user.guild_permissions.mention_everyone:
        wget = "wget -P ./plugins " + url
        subprocess.call(wget.split())
        await interaction.response.send_message("プラグインのインストールに成功しました。適用するには、/reload confirmで再読み込みしてください")
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="delete")
@app_commands.describe(file='削除するファイルのパス')
async def delete(interaction: discord.Interaction, file: str):
    """ファイルを削除する"""
    if interaction.user.guild_permissions.mention_everyone:
        rm = "rm " + file
        subprocess.call(rm.split())
        await interaction.response.send_message("ファイルの削除に成功しました。")
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="plugins")
async def plugins(interaction: discord.Interaction):
    """プラグインを一覧表示する"""
    if interaction.user.guild_permissions.mention_everyone:
        ls = "ls ./plugins"
        result = res_cmd(ls)
        result = result.decode()
        await interaction.response.send_message(f"```\n{result}\n```")
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="backup")
async def backup(interaction: discord.Interaction):
    """バックアップする"""
    await interaction.response.defer(thinking=True)
    if interaction.user.guild_permissions.mention_everyone:
        date = datetime.datetime.now()
        today = datetime.date.today()
        hour = date.hour
        minute = date.minute
        if (hour <= 9):
            hour = str(0) + str(hour)
        elif (minute <= 9):
            minute = str(0) + str(minute)
        date_result = str(today) + "." + str(hour) + ":" + str(minute)
        mkdir = "mkdir /home/user/backup/" + date_result
        cp_world = "cp -r /home/user/paper/world /home/user/backup/" + date_result + "/"
        cp_world_nether = "cp -r /home/user/paper/world_nether /home/user/backup/" + date_result + "/"
        cp_world_the_end = "cp -r /home/user/paper/world_the_end /home/user/backup/" + date_result + "/"
        subprocess.call(mkdir.split())
        subprocess.call(cp_world.split())
        subprocess.call(cp_world_nether.split())
        subprocess.call(cp_world_the_end.split())
        await interaction.followup.send("バックアップに成功しました。")
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.followup.send(embed=embed, ephemeral=True)

@tree.command(name="restore")
async def restore(interaction: discord.Interaction, file: str):
    """復元する"""
    await interaction.response.defer(thinking=True)
    if interaction.user.guild_permissions.mention_everyone:
        try:
            rm = "rm -rf /home/user/paper/world*"
            cp_world = f"cp -r /home/user/backup/{file}/world /home/user/paper/"
            cp_world_nether = f"cp -r /home/user/backup/{file}/world_nether /home/user/paper/"
            cp_world_the_end = f"cp -r /home/user/backup/{file}/world_the_end /home/user/paper/"
            subprocess.call(rm.split())
            subprocess.call(cp_world.split())
            subprocess.call(cp_world_nether.split())
            subprocess.call(cp_world_the_end.split())
            await interaction.followup.send(f"{file}の復元に成功しました。")
        except Exception:
            await interaction.followup.send("復元に失敗しました\nファイル名が正しいか確認してください", ephemeral=True)
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

@tree.command(name="backups")
async def backups(interaction: discord.Interaction):
    """バックアップされたファイル一覧を見る"""
    if interaction.user.guild_permissions.mention_everyone:
        ls = "ls ../backup"
        result = res_cmd(ls)
        result = result.decode()
        await interaction.response.send_message(f"```\n{result}\n```")
    else:
        embed = discord.Embed(title="権限がありません",description="この操作にはFriendsロールが必要です", color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

<<<<<<< HEAD
client.run("Token")
=======
client.run(Token)
>>>>>>> 80bbe5d (main)
