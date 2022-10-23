from xml.dom.pulldom import START_ELEMENT
import discord
import subprocess
from discord.ext.commands import Bot 

client = Bot('techmc!')

def res_cmd(cmd):
  return subprocess.Popen(
      cmd, stdout=subprocess.PIPE,
      shell=True).communicate()[0]

@client.event
async def on_ready():
    print("Login successful!")

@client.command()
async def start(ctx):
    await ctx.send("サーバーを起動します。しばらくお待ちください。")
    start = "nohup java -Xms2G -jar Magma-1.12.2-9a3e486d.jar"
    subprocess.call(start.split())

@client.command()
async def stop(ctx):
    await ctx.send("サーバーを停止します。しばらくお待ちください。")
    stop = "pkill java"
    subprocess.call(stop.split())

@client.command()
async def restart(ctx):
    await ctx.send("サーバーを再起動します。しばらくお待ちください。")
    stop = "pkill java"
    start = "nohup java -Xms2G -jar Magma-1.12.2-9a3e486d.jar"
    subprocess.call(stop.split())
    subprocess.call(start.split())

@client.command()
async def install(ctx, type, URL):
    if type == "mod":
        wget = "wget -P ./mods " + URL
        subprocess.call(wget.split())
        await ctx.send("Modのインストールに成功しました。適用するには、/reload confirmで再読み込みしてください")
    elif type == "plugin":
        wget = "wget -P ./plugins " + URL
        subprocess.call(wget.split())
        await ctx.send("プラグインのインストールに成功しました。適用するには、/reload confirmで再読み込みしてください")
    elif type == "script":
        wget = "wget -P ./scripts " + URL
        subprocess.call(wget.split())
        await ctx.send("スクリプトのインストールに成功しました。適用するには、/reload confirmで再読み込みしてください")
    elif type == "config":
        wget = "wget -P ./config " + URL
        subprocess.call(wget.split())
        await ctx.send("Configのインストールに成功しました。適用するには、/reload confirmで再読み込みしてください")

@client.command()
async def delete(ctx, file):
    rm = "rm " + file
    subprocess.call(rm.split())
    await ctx.send("ファイルの削除に成功しました。")

@client.command()
async def ls(ctx, directory):
    ls = "ls " + directory
    result = res_cmd(ls)
    result = result.decode()
    await ctx.send(result)

client.run("MTAwMzM2NjcwMjgxOTU4MTk5Mg.GWCi3m.NdOe5TFGqzwXzdV-STKOEGFS8zDPkKSc7opPKI")