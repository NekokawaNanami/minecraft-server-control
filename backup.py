import subprocess
import datetime

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