import subprocess
import time



command = "python3 -m createTimeSeries.py > log.txt"


while True:
    try:
        subprocess.run(command, shell=True)
    except:
        time.sleep(1500)
        