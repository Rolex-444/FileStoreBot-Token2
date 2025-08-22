import subprocess
import time

while True:
    # Start your bot main file (adjust filename if different)
    process = subprocess.Popen(["python3", "main.py"])
    process.wait()
    print("Bot stopped unexpectedly. Restarting in 5 seconds...")
    time.sleep(5)
  
